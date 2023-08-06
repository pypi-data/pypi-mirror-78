import requests
from requests import HTTPError

from agent.certificates import logger
from agent.exceptions.agent_error import AgentError


class CertificateClient:
    def __init__(self, base_path, access_token):
        self.base_path = base_path
        self.access_token = access_token

    def send_csr(self, service_id, csr, cert_type):
        logger.info('Sending csr')
        csr_files = {'csr': ('service.csr', csr)}
        url = f'{self.base_path}/v1/certificates/{service_id}?type={cert_type}'

        try:
            resp = requests.post(url, files=csr_files, headers={'Authorization': f'Bearer {self.access_token}'})
            resp.raise_for_status()
        except HTTPError as error:
            logger.error(f'Error during certificate generation: {error}')
            raise AgentError(expression=url, message=error)
        return resp.text

    def get_ca_certs_chain(self):
        resp = requests.get(f'{self.base_path}/v1/certificates',
                            headers={'Authorization': f'Bearer {self.access_token}'})
        return resp.text
