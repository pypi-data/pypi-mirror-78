from agent.commands.utils import prepare_message_to_send
from agent.constants import SERVICE_DETAILS
from agent.websocket.client import AgentWebSocketClient


def send_service_details(body):
    details_message = prepare_message_to_send(message_type=SERVICE_DETAILS, body=body)
    client = AgentWebSocketClient.get_instance()
    client.safe_message_send(details_message)
