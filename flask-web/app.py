from flask import Flask, request, has_request_context

from flask_restful import Api

from route import hello_route, users_route
from flask.logging import default_handler

import logging, logstash
from logging.handlers import RotatingFileHandler

class RequestFormatter(logging.Formatter):
    def format(self, record):
        if has_request_context():
            record.url = request.url
            record.remote_addr = request.remote_addr
            record.method = request.method

            record.user_agent = request.user_agent.string
            platforms = ["macos", "windows"]
            record.paltform = "OS" if [x for x in platforms if request.user_agent.platform.lower() in x ] else "Mobile"
        else:
            record.url = None
            record.remote_addr = None

        return super().format(record)


def create_app():
    app = Flask("app")

    app.register_blueprint(hello_route.hello_bp)
    app.register_blueprint(users_route.users_bp)

    from common.database import Base, engine
    from sqlalchemy_utils import database_exists, create_database
    from model.users import Users
    print(f"already created {engine.url} database" if database_exists(engine.url) else f"create {engine.url} database")
    if not database_exists(engine.url):
        create_database(engine.url)
    Base.metadata.create_all(bind=engine)

    return app


app = create_app()
# api = Api(app)
# api.add_resource(app_route, '/')
# app.register_blueprint(hello_route)

app.secret_key = b'greenbear'
app.debug = True



# # log관련 참조 : https://jangseongwoo.github.io/logging/flask_logging/
# #               https://dev.to/rhymes/logging-flask-requests-with-colors-and-structure--7g1
# # formatter = logging.Formatter(
# #         '{request.remote_addr} %(asctime)s [%(levelname)s] - %(filename)s:%(funcName)s - line:%(lineno)d - %(message)s')
# formatter = RequestFormatter(
#     '[%(asctime)s] %(remote_addr)s [%(method)s] [%(user_agent)s] [%(paltform)s] requested %(url)s %(levelname)s in %(module)s: %(message)s'
# )

# # Append logstashLogger
# logstash_logger = logstash.TCPLogstashHandler('logstash', 5001, version=1)
# logstash_logger.setLevel(logging.DEBUG)
# # logstash_logger.setFormatter(logging.Formatter('\n[%(levelname)s|%(name)s|%(filename)s:%(lineno)s] %(asctime)s > %(message)s'))
# app.logger.addHandler(logstash_logger)

# # Append FileHandler
# handler = RotatingFileHandler("/tmp/logs/app.log", maxBytes=10000000, backupCount=5)
# handler.setLevel(logging.DEBUG)
# handler.setFormatter(formatter)
# app.logger.addHandler(handler)

# # Append defaultHandler
# default_handler.setFormatter(formatter)
# app.logger.addHandler(default_handler)
# # app.logger.info("start..")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
