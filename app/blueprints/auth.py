from flask import Blueprint, render_template

AuthController = Blueprint('AuthController', __name__)

@AuthController.route('/login')
def login():
    return render_template('auth/login.j2')
    