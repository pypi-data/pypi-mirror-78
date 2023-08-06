import os

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

INSTALL_DIR = os.getenv('INSTALL_DIR')
BASE_SERVICES_PATH = f'{INSTALL_DIR}/services'
ACCESS_TOKEN_PATH = f'{INSTALL_DIR}/agent/access.token'
REXSIO_HOST = os.getenv('REXSIO_HOST') or 'api-dev.rexs.io'
REXSIO_WS_HOST = os.getenv('REXSIO_WS_HOST') or 'ws-service.rexsio.dev.dac.systems'
REXSIO_USER = os.getenv('REXSIO_USER')
