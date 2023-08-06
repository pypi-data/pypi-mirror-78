from collections import namedtuple

from agent.config.properties import ACCESS_TOKEN_PATH
from agent.config.properties import REXSIO_WS_HOST

command = namedtuple('command', ['type', 'body'])


def resolve_ws_endpoint():
    access_token = get_access_token()
    return f'wss://{REXSIO_WS_HOST}/ws?access_token={access_token}'


def get_access_token():
    with open(ACCESS_TOKEN_PATH, 'r') as f:
        token = f.read()
    return token.strip()
