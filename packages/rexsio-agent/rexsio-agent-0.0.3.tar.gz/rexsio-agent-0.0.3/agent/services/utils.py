import os

from agent.config.properties import BASE_SERVICES_PATH


def get_services_id_list():
    try:
        return os.listdir(BASE_SERVICES_PATH)
    except FileNotFoundError:
        return []
