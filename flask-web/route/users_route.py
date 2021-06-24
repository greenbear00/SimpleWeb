
from flask import Blueprint, render_template, session
from service.users_service import login, signup, logout
users_bp = Blueprint('users', __name__, url_prefix='/')

users_bp.route('/login', methods=['GET', 'POST']) (login)
users_bp.route('/signup', methods=['GET', 'POST']) (signup)
users_bp.route('/logout', methods=['GET', 'POST']) (logout)