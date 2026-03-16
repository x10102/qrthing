import waitress
import json
import secrets
import logging
from logging import info, warning, error
import bcrypt
from os import getcwd
from os.path import exists, join

from misc.typing_hacks import _l

from flask import Flask, request, session
from db import database, User, UserRole, DynamicCode

from blueprints.index import IndexController
from extensions import login_manager, babel

app = Flask(__name__)
cfg_file = 'config.json'

LOGGER_FORMAT_STR = '[%(asctime)s][%(module)s] %(levelname)s: %(message)s'

def get_locale():
    if 'language' in session:
        return session['language']
    return request.accept_languages.best_match(app.config['LANGUAGES'])

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
        "DEBUG": False,
        "LANGUAGES": ['en', 'cs']
        }

def init_db():
    database.connect()
    database.create_tables([User, UserRole, DynamicCode])
    role_user = UserRole.insert(id=1, name="user").on_conflict_ignore().execute()
    role_admin = UserRole.insert(id=2, name="administrator").on_conflict_ignore().execute()

def register_blueprints():
    app.register_blueprint(IndexController)

# Sounds cooler than just 'admin' imo
def create_administrator(username: str = 'sysop', password: str = 'mikumiku'):
    admin_role = UserRole.get_by_id(2)
    if len(list(admin_role.users)) == 0:
        hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        new_admin = User.create(username=username, password=hashed_pw, role=admin_role)
        info(f"New admin created with ID {new_admin.id}")

def init_app():
    cfg_path = join(getcwd(), cfg_file)
    if not exists(cfg_path):
        new_config = open(cfg_file, 'w')
        json.dump(make_default_config(), new_config, indent=4)
        new_config.close()
    app.config.from_file(cfg_file, json.load)
    register_blueprints()
    create_administrator()
    # Set up login manager
    login_manager.session_protection = "basic"
    login_manager.login_message = _l('Log in to access this page')
    login_manager.user_loader(lambda uid: User.get_or_none(uid))
    login_manager.init_app(app)
    babel.init_app(app, locale_selector=get_locale)

if __name__ == '__main__':
    init_logger()
    init_db()
    init_app()
    if app.config['DEBUG']:
        logging.getLogger().setLevel(logging.DEBUG)
        app.run('0.0.0.0', 8080, True)
    else:
        waitress.serve(app, listen='0.0.0.0:8080', threads=16)