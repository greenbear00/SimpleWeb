# from flask_restful import Resource
# class app_route(Resource):
#
#     def get(self):
#         return {'hello': "world"}

from flask import Blueprint, render_template, session, request, flash
hello_bp = Blueprint('hello', __name__, url_prefix='/')
# import logging
# log = logging.getLogger("app")
# @hello_bp.route("/")
# def index():
#     log.info(f"session = {str(session)}")
#     log.info("call render_template(index.html)")
#     return render_template('index.html')

from common.log import logger_info
@hello_bp.route("/")
def index():
    if session:
        id = session['loggin_id']
    else:
        id = None
    logger_info(f"session = {id if session else 'None'}")
    # if session:
    #     flash("wrong password!!")
    # else:
    #     logger_info("call render_template(index.html)")
    return render_template('index.html')

@hello_bp.route("/test")
def index_test():
    return {"id": "test"}