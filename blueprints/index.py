from flask import Blueprint, current_app, render_template

IndexController = Blueprint('IndexController', __name__)

@IndexController.route('/')
def app_index():
    return render_template('index.j2')