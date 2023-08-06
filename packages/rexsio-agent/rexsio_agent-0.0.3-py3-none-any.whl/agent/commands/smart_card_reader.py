import re
import shlex
import subprocess

from agent.constants import FILTER_SMART_CARD_COMMANDS, LIST_USB_DEVICES
from agent.exceptions.agent_error import AgentError

address_re = re.compile("Bus\s+(?P<bus>\d+)\s+Device\s+(?P<device>\d+).+ID\s.+$", re.I)


def find_smart_card_reader_address():
    raw_reader_address = _get_reader_usb_details()
    return _parse_reader_address(raw_reader_address)


def _get_reader_usb_details():
    input_process = _open_subprocess_pipe(command=LIST_USB_DEVICES)
    for command in FILTER_SMART_CARD_COMMANDS:
        current_process = _open_subprocess_pipe(command=command,
                                                stdin=input_process.stdout)
        input_process.stdout.close()
        input_process = current_process
    filtered_devices, error = input_process.communicate()
    if error is not None:
        raise AgentError(expression=filtered_devices, message=error)
    return filtered_devices


def _open_subprocess_pipe(command, **kwargs):
    return subprocess.Popen(args=shlex.split(command),
                            stdout=subprocess.PIPE,
                            universal_newlines=True,
                            **kwargs)


def _parse_reader_address(raw_data):
    data_lines = raw_data.split('\n')
    address_line = _get_line_with_the_usb_address(data_lines)
    bus_and_device = address_re.match(address_line).groupdict()
    return _build_usb_address(bus_and_device)


def _get_line_with_the_usb_address(data_lines):
    return next(data_line for data_line in data_lines if 'Bus' and 'Device' in data_line)


def _build_usb_address(bus_and_device):
    bus = bus_and_device.pop('bus')
    device = bus_and_device.pop('device')
    return f"/dev/bus/usb/{bus}/{device}"
