import socket

import psutil

from agent.commands import logger
from agent.commands.utils import prepare_message_to_send
from agent.constants import NODE_METRICS
from agent.exceptions.agent_error import AgentError


def read_metrics():
    ip_address = _get_network_interface_controller_ip_address()
    metrics_body = dict(ip=ip_address)
    return prepare_message_to_send(message_type=NODE_METRICS, body=metrics_body)


def _get_network_interface_controller_ip_address():
    network_interfaces = psutil.net_if_addrs()
    try:
        ethernet_interface = _find_ethernet_interface(network_interfaces)
        snic_addresses = network_interfaces.get(ethernet_interface)
        snic = _find_af_inet_snic(snic_addresses)
        return snic.address
    except AgentError as err:
        logger.error(f'IP address not found. {err}')


def _find_ethernet_interface(network_interfaces):
    interfaces = network_interfaces.keys()
    try:
        return next(interface for interface in interfaces if interface.startswith('e'))
    except StopIteration as err:
        raise AgentError(expression=interfaces, message=err)


def _find_af_inet_snic(snic_addresses):
    try:
        return next(snic for snic in snic_addresses if snic.family == socket.AF_INET)
    except StopIteration as err:
        raise AgentError(expression=snic_addresses, message=err)
