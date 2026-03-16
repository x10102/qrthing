from flask import Blueprint, current_app, render_template, session, redirect, url_for, request, abort
from misc.auth_helpers import admin_only
import qrcode
import base64
from http import HTTPStatus

ApiController = Blueprint('ApiController', __name__)

@ApiController.route('/generate')
def generate_qr():
    data = request.args.get('d', None, str)
    ecc_level = request.args.get('e', None, int)
    version = request.args.get('v', None, int)
    border = request.args.get('b', 2, int)
    box_size = request.args.get('bs', 10, int)
    if not data or not version:
        abort(HTTPStatus.BAD_REQUEST)
    if not ecc_level:
        ecc_level = qrcode.ERROR_CORRECT_M
    qr = qrcode.QRCode(version=version, error_correction=ecc_level, box_size=box_size, border=border)
    qr.add_data(base64.urlsafe_b64decode(data))