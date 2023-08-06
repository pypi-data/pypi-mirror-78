from agent.commands import logger
from agent.commands.service_delete import delete_service
from agent.commands.service_details import send_service_details
from agent.commands.service_provision import provision_service
from agent.commands.service_restart import restart_service
from agent.commands.uninstall import uninstall
from agent.constants import PROVISION_SERVICE, DELETE_SERVICE, SERVICE_DETAILS, DELETE_NODE, RESTART_SERVICE
from agent.exceptions.agent_error import AgentError


def dispatch_command(command, body):
    _validate_command(command)

    if not body:
        return commands_dispatcher[command]()

    _validate_body(body)
    return commands_dispatcher[command](body)


def _validate_command(command):
    if command in commands_dispatcher.keys():
        logger.info(f'Recognized command: {command}!')
    else:
        raise AgentError(command, f'Invalid command!')


def _validate_body(body):
    if isinstance(body, dict):
        logger.info(f'{body} is a dict!')
    else:
        raise AgentError(body, f'Body is not a dict!')


commands_dispatcher = {
    PROVISION_SERVICE: provision_service,
    DELETE_SERVICE: delete_service,
    SERVICE_DETAILS: send_service_details,
    DELETE_NODE: uninstall,
    RESTART_SERVICE: restart_service
}
