import shlex
import subprocess

from agent.config.properties import INSTALL_DIR, REXSIO_USER
from agent.constants import UNINSTALL_SCRIPT_FILE
from agent.exceptions.agent_error import AgentError
from agent.scheduler.scheduled_tasks_manager import ScheduledTaskManager


def uninstall():
    ScheduledTaskManager.get_instance().stop_executing()
    uninstall_script_path = f'{INSTALL_DIR}/{UNINSTALL_SCRIPT_FILE}'
    try:
        subprocess.call(shlex.split(f'sudo {uninstall_script_path} {INSTALL_DIR} {REXSIO_USER}'))
    except subprocess.CalledProcessError as err:
        raise AgentError(expression=uninstall_script_path, message=err.output)
