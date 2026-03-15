import waitress
import json
import secrets
import logging
from os import getcwd
from os.path import exists, join

from flask import Flask
from db import database, User

from blueprints.index import IndexController

app = Flask(__name__)
cfg_file = 'config.json'

LOGGER_FORMAT_STR = '[%(asctime)s][%(module)s] %(levelname)s: %(message)s'

def init_logger() -> None:
    """
    Sets up logging
    """
    logging.getLogger().handlers.clear()
    logging.basicConfig(filename='qrthing.log', filemode='a', format=LOGGER_FORMAT_STR, encoding='utf-8')
    logging.getLogger().setLevel(logging.INFO)
    handler_st = logging.StreamHandler()
    handler_st.setFormatter(logging.Formatter(LOGGER_FORMAT_STR))
    logging.getLogger().addHandler(handler_st)

def make_default_config() -> dict:
    """
    Returns a default config object
    """
    secret_key = secrets.token_urlsafe(24)
    return {
        "SECRET_KEY": secret_key,
        "DEBUG": False
        }

def init_db():
    database.connect()
    database.create_tables([User])

def register_blueprints():
    app.register_blueprint(IndexController)

def init_app():
    cfg_path = join(getcwd(), cfg_file)
    if not exists(cfg_path):
        new_config = open(cfg_file, 'w')
        json.dump(make_default_config(), new_config, indent=4)
        new_config.close()
    app.config.from_file(cfg_file, json.load)
    register_blueprints()

if __name__ == '__main__':
    init_logger()
    init_db()
    init_app()
    if app.config['DEBUG']:
        logging.getLogger().setLevel(logging.DEBUG)
        app.run('0.0.0.0', 8080, True)
    else:
        waitress.serve(app, listen='0.0.0.0:8080', threads=16)