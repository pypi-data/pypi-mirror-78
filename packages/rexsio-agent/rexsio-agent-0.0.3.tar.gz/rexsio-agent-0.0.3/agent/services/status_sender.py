from agent.commands.utils import prepare_message_to_send
from agent.constants import SERVICES_STATUS
from agent.scheduler import logger
from agent.websocket.client import AgentWebSocketClient


def send_statuses(statuses):
    AgentWebSocketClient.get_instance().safe_message_send(statuses)
    logger.info(f'Service statuses sent: {statuses}')


def send_status(service_id, status):
    service_status_list = {"statuses":[{"serviceId": service_id, "status": status}]}
    service_status_message = prepare_message_to_send(message_type=SERVICES_STATUS, body=service_status_list)
    send_statuses(service_status_message)
