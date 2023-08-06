import shutil

from agent.commands.utils import get_field_from_body, get_base_service_path, docker_compose_down
from agent.constants import DOCKER_COMPOSE_FILE
from agent.scheduler.scheduled_tasks_manager import ScheduledTaskManager


def delete_service(body):
    service_id = get_field_from_body('nodeServiceId', body)
    service_path = get_base_service_path(service_id)
    docker_compose_file = f'{service_path}/{DOCKER_COMPOSE_FILE}'

    tasks_manager = ScheduledTaskManager.get_instance()
    tasks_manager.stop_executing()
    docker_compose_down(docker_compose_file)
    shutil.rmtree(service_path, ignore_errors=True)
    tasks_manager.start_executing()
