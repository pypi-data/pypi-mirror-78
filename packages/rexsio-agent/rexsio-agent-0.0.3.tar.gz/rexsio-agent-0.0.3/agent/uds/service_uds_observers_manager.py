from pathlib import Path

from twisted.internet import reactor

from agent.commands.utils import get_base_service_path
from agent.constants import UDS_FOLDER, UDS_SERVICE_FILE_NAME
from agent.services.utils import get_services_id_list
from agent.uds.service_uds_observer import ServiceUdsObserver


def _get_socket_folder_path(service_id):
    return f'{get_base_service_path(service_id)}/{UDS_FOLDER}'


class ServiceUdsObserversManager:
    _instance = None

    @staticmethod
    def init(on_message_handler):
        ServiceUdsObserversManager._instance = ServiceUdsObserversManager(on_message_handler)

    @staticmethod
    def get_instance():
        return ServiceUdsObserversManager._instance

    def __init__(self, on_message_handler):
        self.is_observing = False
        self.observers = {}
        self.on_message_handler = on_message_handler

        service_ids = get_services_id_list()
        for service_id in service_ids:
            self.add_new_observer(service_id)

    def start_observing(self):
        if self.is_observing:
            return

        for observer in self.observers.values():
            reactor.callInThread(observer.start_observing)
        self.is_observing = True

    def add_new_observer(self, service_id):
        observer = self._get_observer(service_id)
        self.observers[service_id] = observer
        if self.is_observing:
            reactor.callInThread(observer.start_observing)

    def _get_observer(self, service_id):
        socket_path = _get_socket_folder_path(service_id)
        Path(socket_path).mkdir(parents=True, exist_ok=True)
        return ServiceUdsObserver(service_id=service_id,
                                  uds_socket_file_path=f'{socket_path}/{UDS_SERVICE_FILE_NAME}',
                                  on_message_handler=self.on_message_handler)
