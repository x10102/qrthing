from flask import Blueprint, current_app, render_template, session, redirect, url_for
from misc.auth_helpers import admin_only

IndexController = Blueprint('IndexController', __name__)

@IndexController.route('/')
def app_index():
    return render_template('index.j2')

# Localization test route
@IndexController.route('/switch_lang')
def switch_lang():
    if 'language' not in session:
        session['language'] = 'cs'
        return redirect(url_for("IndexController.app_index"))
    if session['language'] == 'cs':
        session['language'] = 'en'
        return redirect(url_for("IndexController.app_index"))
    if session['language'] == 'en':
        session['language'] = 'cs'
    return redirect(url_for("IndexController.app_index"))