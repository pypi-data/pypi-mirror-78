import subprocess

from agent.commands import logger
from agent.commands.utils import get_docker_compose_path, get_field_from_body, docker_compose_restart
from agent.constants import SERVICE_RESTARTING, SERVICE_DOWN, SERVICE_UP
from agent.services.status_sender import send_status


def restart_service(body):
    service_id = get_field_from_body('nodeServiceId', body)
    logger.info(f'Restarting {service_id} service')
    _restart_service(service_id)


def restart_services(service_id_list):
    for service_id in service_id_list:
        logger.info(f'Service {service_id} is DOWN, restarting')
        _restart_service(service_id)


def _restart_service(service_id):
    send_status(service_id, SERVICE_RESTARTING)
    docker_compose_path = get_docker_compose_path(service_id)
    try:
        docker_compose_restart(docker_compose_path)
        send_status(service_id, SERVICE_UP)
    except subprocess.CalledProcessError:
        send_status(service_id, SERVICE_DOWN)
