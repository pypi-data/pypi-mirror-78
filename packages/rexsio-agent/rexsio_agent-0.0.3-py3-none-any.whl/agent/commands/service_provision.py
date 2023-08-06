import os
from collections import namedtuple
from urllib.error import HTTPError

import requests

from agent.certificates.certificate_client import CertificateClient
from agent.certificates.certificate_config_generator import CertificateConfigGenerator
from agent.commands import logger
from agent.commands.smart_card_reader import find_smart_card_reader_address
from agent.commands.utils import save_config, get_field_from_body, docker_compose_up, \
    get_docker_compose_path
from agent.config.properties import BASE_SERVICES_PATH
from agent.config.properties import REXSIO_HOST
from agent.exceptions.agent_error import AgentError
from agent.uds.service_uds_observers_manager import ServiceUdsObserversManager
from agent.websocket.utils import get_access_token


def provision_service(body):
    service = _get_service_data_from_json(body)
    save_config(service_id=service.id, config=service.config)
    _generate_service_certificate(service.id)
    docker_compose_file_path = _download_docker_compose(compose_url=service.compose_url, service_id=service.id)
    _set_smart_card_reader_address_if_needed(service_type=service.type, config=service.config)
    ServiceUdsObserversManager.get_instance().add_new_observer(service.id)
    docker_compose_up(docker_compose_file_path)
    logger.info(f'Service {service.type}/{service.id} is running')


def _get_service_data_from_json(body):
    service = namedtuple('service', ['type', 'id', 'config', 'compose_url', 'version'])
    service.type = get_field_from_body('serviceType', body)
    service.id = get_field_from_body('nodeServiceId', body)
    service.config = get_field_from_body('config', body)
    service.compose_url = get_field_from_body('dockerComposeUrl', body)
    service.version = get_field_from_body('version', body)
    return service


def _generate_service_certificate(service_id):
    token = get_access_token()
    rexsio_path = f'https://{REXSIO_HOST}'
    client = CertificateClient(base_path=rexsio_path, access_token=token)
    generator = CertificateConfigGenerator(service_configs_path=BASE_SERVICES_PATH,
                                           cert_client=client)
    generator.generate_cert_config(service_id)


def _download_docker_compose(compose_url, service_id):
    file_path = get_docker_compose_path(service_id)
    try:
        _get_docker_compose_file(url=compose_url, filename=file_path)
    except HTTPError as error:
        logger.error(f'Docker compose file download failed: {file_path}, url: {compose_url}')
        raise AgentError(expression=compose_url, message=error)
    logger.info(f'Docker compose file downloaded: {file_path}')
    return file_path


def _get_docker_compose_file(url, filename):
    r = requests.get(url)
    r.raise_for_status()
    with open(filename, 'wb') as file:
        file.write(r.content)


def _set_smart_card_reader_address_if_needed(service_type, config):
    if _is_card_reader_needed(service_type, config):
        _set_smart_card_reader_address()


def _set_smart_card_reader_address():
    address = find_smart_card_reader_address()
    os.environ['REXSIO_SMART_CARD_READER_ADDRESS'] = address
    logger.info(f'Smart card reader address added: {address}')


def _is_card_reader_needed(service_type, config):
    return _is_service_notary(service_type) and _is_not_using_private_key(config)


def _is_service_notary(service_type):
    return 'notary' in service_type.lower()


def _is_not_using_private_key(config):
    is_private_key = get_field_from_body('usePrivateKey', config)
    return not is_private_key
