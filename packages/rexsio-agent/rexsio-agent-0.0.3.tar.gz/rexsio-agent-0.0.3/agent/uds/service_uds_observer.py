import os
import socket

from agent.uds import logger


class ServiceUdsObserver:

    def __init__(self, service_id, uds_socket_file_path, on_message_handler):
        self.service_id = service_id
        self.uds_socket_file_path = uds_socket_file_path
        self._remove_socket_file_if_exists()
        self.on_message_handler = on_message_handler

    def _remove_socket_file_if_exists(self):
        try:
            os.remove(self.uds_socket_file_path)
        except OSError:
            if os.path.exists(self.uds_socket_file_path):
                raise

    def start_observing(self):
        logger.info(f'Observing UDS socket {self.uds_socket_file_path}')
        sock = self._get_socket()
        while True:
            try:
                self._observe_service(sock)
            except socket.timeout:
                pass

    def _get_socket(self):
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.bind(self.uds_socket_file_path)
        sock.listen()
        return sock

    def _observe_service(self, sock):
        logger.debug('Waiting for UDS connection')
        connection, client_address = sock.accept()
        logger.debug(f'UDS connection established for {connection.getsockname()} file')

        try:
            self._receive_message(connection)
        finally:
            connection.close()

    def _receive_message(self, connection):
        payload = bytearray()

        while True:
            chunk = connection.recv(1024)

            if not chunk:
                break
            payload.extend(chunk)

        if payload and self.on_message_handler:
            logger.debug(f'Received payload: {payload}')
            self.on_message_handler(self.service_id, payload)
