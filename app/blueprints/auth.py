from flask import Blueprint, render_template, flash, redirect, url_for
from misc.forms import LoginForm
from flask_login import login_user, logout_user, login_required
from flask_babel import _
from bcrypt import checkpw
from db import User

AuthController = Blueprint('AuthController', __name__)

@AuthController.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_and_flash():
        user = User.get_or_none(User.username == login_form.username.data)
        if not user or not checkpw(login_form.password.data.encode(), user.password):
            flash(_('Incorrect username or password'))
            return redirect(url_for('AuthController.login'))
        login_user(user)
        flash(_('You are now logged in'))
        return redirect(url_for('IndexController.app_index'))
    return render_template('auth/login.j2', form=login_form)
    
@AuthController.route('/logout')
def logout():
    logout_user()
    flash(_('Logged out'))
    return redirect(url_for('IndexController.app_index'))