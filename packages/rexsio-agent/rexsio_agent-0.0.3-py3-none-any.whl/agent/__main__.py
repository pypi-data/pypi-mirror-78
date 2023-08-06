from autobahn.twisted.websocket import connectWS
from twisted.internet import reactor

from agent.communication.message_processor import convert_message_to_json, process_json_message
from agent.logger import setup_logger
from agent.uds.service_uds_observers_manager import ServiceUdsObserversManager
from agent.websocket.client import AgentWebSocketFactory

logger = setup_logger()


def main():
    logger.info('Launching Agent...')
    connectWS(AgentWebSocketFactory.get_instance())
    ServiceUdsObserversManager.init(handle_uds_messages)
    ServiceUdsObserversManager.get_instance().start_observing()
    reactor.run()


def handle_uds_messages(service_id, payload):
    json_message = convert_message_to_json(payload.decode("utf8"))
    json_message['body']['nodeServiceId'] = service_id
    process_json_message(json_message)


if __name__ == '__main__':
    main()
