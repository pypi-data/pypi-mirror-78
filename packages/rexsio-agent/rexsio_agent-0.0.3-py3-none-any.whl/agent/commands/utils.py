import json
import os
import shlex
import subprocess
from pathlib import Path

from agent.commands import logger
from agent.config.properties import BASE_SERVICES_PATH
from agent.constants import DOCKER_COMPOSE_FILE
from agent.exceptions.agent_error import AgentError


def get_base_service_path(service_id):
    return f'{BASE_SERVICES_PATH}/{service_id}'


def get_docker_compose_path(service_id):
    return f'{get_base_service_path(service_id)}/{DOCKER_COMPOSE_FILE}'


def get_field_from_body(key, body):
    try:
        return body[key]
    except KeyError as e:
        logger.error(f'{body} does not contain any {key}!')
        raise AgentError(body, e)


def prepare_message_to_send(message_type, body):
    message = dict(messageType=message_type, body=body)
    return json.dumps(message).encode('utf-8')


def save_config(config, service_id):
    config_directory = _create_config_path_for_service(service_id)
    file_path = f'{config_directory}/config.json'
    _save_data_to_file(config, file_path)
    logger.info(f'Config updated: {file_path}')


def _save_data_to_file(data, file_path):
    with open(file_path, 'w') as f:
        json.dump(data, f)


def _create_config_path_for_service(service_id):
    service_base_path = get_base_service_path(service_id)
    config_path = f'{service_base_path}/config'
    _create_config_path_if_needed(config_path)
    return config_path


def _create_config_path_if_needed(config_path):
    if not os.path.isdir(config_path):
        logger.info(f'Directory {config_path} does not exist, creating one')
        try:
            Path(config_path).mkdir(parents=True, exist_ok=True)
        except PermissionError as e:
            logger.error(f'User has no permission to this path: {config_path}')
            raise AgentError(config_path, e)


def docker_compose_up(path):
    try:
        subprocess.call(shlex.split(f'docker-compose -f {path} up -d'))
    except subprocess.CalledProcessError as err:
        raise AgentError(expression=path, message=err.output)


def docker_compose_down(path):
    try:
        subprocess.call(shlex.split(f'docker-compose -f {path} down'))
    except subprocess.CalledProcessError as err:
        raise AgentError(expression=path, message=err.output)


def docker_compose_restart(path):
    try:
        subprocess.call(shlex.split(f'docker-compose -f {path} restart'))
    except subprocess.CalledProcessError as exc:
        logger.error(f'Failed to restart docker-compose {path}', exc)
        docker_compose_up(path)
