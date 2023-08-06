from pathlib import Path

from OpenSSL import crypto
from OpenSSL.crypto import PKey, TYPE_RSA, X509Req, FILETYPE_PEM, PKCS12

from agent.certificates import logger

CERT_BEGIN_PREFIX = '-----BEGIN CERTIFICATE-----'
CERT_END_PREFIX = '-----END CERTIFICATE-----'

KNOWN_PASSWORD = 'known-password'


def parse_ca_certs_chain(ca_certs_chain):
    ca_certs = ca_certs_chain.split(f'{CERT_END_PREFIX}\n{CERT_BEGIN_PREFIX}')
    return list(map(convert_to_certificate, ca_certs))


def convert_to_certificate(ca_cert):
    if not ca_cert.startswith(CERT_BEGIN_PREFIX):
        ca_cert = CERT_BEGIN_PREFIX + ca_cert
    if not ca_cert.endswith(CERT_END_PREFIX):
        ca_cert = ca_cert + CERT_END_PREFIX

    return crypto.load_certificate(FILETYPE_PEM, ca_cert)


class CertificateConfigGenerator:
    def __init__(self, service_configs_path, cert_client):
        self.service_configs_path = service_configs_path
        self.cert_client = cert_client
        self.ca_certs_chain = self.cert_client.get_ca_certs_chain()
        self.ca_certs = parse_ca_certs_chain(self.ca_certs_chain)
        self.key = PKey()
        self.key.generate_key(TYPE_RSA, 2048)

    def generate_cert_config(self, service_id):
        self._generate_cert_config_for_type(service_id, 'SERVER')
        self._generate_cert_config_for_type(service_id, 'CLIENT')

    def _generate_cert_config_for_type(self, service_id, cert_type):
        self.cert_type = cert_type
        Path(self._service_config_path(service_id)).mkdir(parents=True, exist_ok=True)
        self._save_private_key(service_id)
        self._save_ca_certs_chain(service_id)
        cert = self._generate_cert(service_id)
        self._generate_p12_cert(cert, service_id)

    def _save_ca_certs_chain(self, service_id):
        certs_chain_path = self._ca_certs_chain_path(service_id)
        logger.info(f'Saving certificates chain: {certs_chain_path}')
        with open(certs_chain_path, 'w') as cert_file:
            cert_file.write(self.ca_certs_chain)

        self._generate_truststore(service_id)

    def _save_private_key(self, service_id):
        private_key_path = self._private_key_path(service_id)
        logger.info(f'Saving private key: {private_key_path}')

        with open(private_key_path, 'wb') as private_key_file:
            private_key_file.write(crypto.dump_privatekey(FILETYPE_PEM, self.key))

    def _generate_cert(self, service_id):
        csr = self._generate_csr(service_id)

        cert = self.cert_client.send_csr(service_id=service_id, csr=csr, cert_type=self.cert_type)

        cert_path = self._service_cert_path(service_id)
        logger.info(f'Saving service certificate: {cert_path}')
        with open(cert_path, 'w') as cert_file:
            cert_file.write(cert)

        return crypto.load_certificate(FILETYPE_PEM, cert)

    def _generate_csr(self, service_id):
        logger.info('Generating csr')

        csr = X509Req()
        csr.get_subject().C = 'PL'
        csr.get_subject().ST = 'Poland'
        csr.get_subject().O = 'REXS.IO'
        csr.get_subject().CN = f'{self.cert_type}-{service_id}'

        csr.set_pubkey(self.key)
        csr.sign(self.key, 'sha256')

        return crypto.dump_certificate_request(FILETYPE_PEM, csr)

    def _generate_p12_cert(self, cert, service_id):
        p12_cert_path = self._p12_cert_path(service_id)
        logger.info(f'Generating p12 certificate: {p12_cert_path}')

        pkcs12_cert = PKCS12()
        pkcs12_cert.set_certificate(cert)
        pkcs12_cert.set_ca_certificates(self.ca_certs)
        pkcs12_cert.set_privatekey(self.key)

        with open(p12_cert_path, 'wb') as pkcs12_cert_file:
            pkcs12_cert_file.write(pkcs12_cert.export(KNOWN_PASSWORD))

    def _generate_truststore(self, service_id):
        truststore_path = self._truststore_path(service_id)
        logger.info(f'Generating truststore: {truststore_path}')

        truststore = PKCS12()
        truststore.set_certificate(self.ca_certs[0])
        truststore.set_friendlyname(b'rexsio')

        with open(truststore_path, 'wb') as truststore_file:
            truststore_file.write(truststore.export(KNOWN_PASSWORD))

    def _private_key_path(self, service_id):
        return self._service_config_file_path(service_id, 'service-private.key')

    def _service_cert_path(self, service_id):
        return self._service_config_file_path(service_id, 'service.crt')

    def _ca_certs_chain_path(self, service_id):
        return self._service_config_file_path(service_id, 'ca-certificates.chain')

    def _truststore_path(self, service_id):
        return self._service_config_file_path(service_id, 'truststore.p12')

    def _p12_cert_path(self, service_id):
        return self._service_config_file_path(service_id, 'service.p12')

    def _service_config_file_path(self, service_id, file_name):
        return f'{self._service_config_path(service_id)}/{file_name}'

    def _service_config_path(self, service_id):
        return f'{self.service_configs_path}/{service_id}/config/{self.cert_type.lower()}'
