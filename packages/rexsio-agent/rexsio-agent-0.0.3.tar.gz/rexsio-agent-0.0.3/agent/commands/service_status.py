import docker

from agent.commands.utils import prepare_message_to_send
from agent.constants import SERVICE_DOWN, SERVICE_UP, SERVICES_STATUS
from agent.services.utils import get_services_id_list


def check_service_statuses():
    service_id_list = get_services_id_list()
    client = docker.from_env()
    service_status_list = _get_services_status_list(service_id_list, client.containers)
    services_to_restart = _get_services_id_to_restart(service_status_list)
    service_status_body = {"statuses":service_status_list}
    service_status_message = prepare_message_to_send(message_type=SERVICES_STATUS, body=service_status_body)
    return service_status_message, services_to_restart


def _get_services_status_list(id_list, containers):
    statuses_list = [_get_service_status(containers, service_id) for service_id in id_list]
    services_statuses = [dict(serviceId=service_id, status=status) for service_id, status in
                         list(zip(id_list, statuses_list))]
    return _remove_services_with_none_status(services_statuses)


def _remove_services_with_none_status(services_statuses):
    services_without_none_status = []
    for service in services_statuses:
        if service['status'] is not None:
            services_without_none_status.append(service)
    return services_without_none_status


def _get_service_status(containers, service_id):
    service_filter = service_id.lower()
    service_containers = containers.list(all=True, filters=dict(name=service_filter))
    if not service_containers:
        service_containers = containers.list(all=True, filters=dict(name=service_filter.replace('-', '')))
    if not service_containers:
        return None
    service_containers_status = [container.status for container in service_containers]
    return SERVICE_UP if _are_all_containers_running(service_containers_status) else SERVICE_DOWN


def _are_all_containers_running(service_containers_status):
    return all(container_status == 'running' for container_status in service_containers_status)


def _get_services_id_to_restart(service_status_list):
    return [service['serviceId'] for service in service_status_list if service['status'] == SERVICE_DOWN]
