import logging
import logstash
from flask import request, has_request_context

'''
#################################################################################
                    SET LOG FORMAT
#################################################################################
'''
# 예) 2021-06-10 02:04:04,803 - web_stream - INFO - session = no
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

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
# 예)
# formatter = RequestFormatter(
#     '%(asctime)s - %(name)s - %(remote_addr)s - %(method)s - %(user_agent)s - requested %(url)s - %(levelname)s in %(module)s - %(message)s'
# )
formatter = RequestFormatter(
    '%(asctime)s - %(name)s - %(remote_addr)s - %(method)s - %(paltform)s - requested %(url)s - %(levelname)s in %(module)s - %(message)s'
)
'''
#################################################################################
                    Werkzeug LOGGER SETTING
#################################################################################
'''
werkzeug = logging.getLogger('werkzeug')
# werkzeug.disabled = True

handler = logging.handlers.RotatingFileHandler("/tmp/logs/flask.log", maxBytes=1024*1024)
werkzeug.setLevel(logging.DEBUG)
handler.setFormatter(formatter)
werkzeug.addHandler(handler)
# web_logger_logstash.disabled = True

'''
#################################################################################
                    MAIN LOGGER SETTING
#################################################################################
'''
web_logger_logstash = logging.getLogger('web_logger')
web_logger_logstash.setLevel(logging.DEBUG)
stash = logstash.TCPLogstashHandler('logstash',5001,version=1)
stash.setFormatter(formatter)
web_logger_logstash.addHandler(stash)
# web_logger_logstash.disabled = True

'''
#################################################################################
                    Stream LOGGER SETTING
#################################################################################
'''
web_logger_stream = logging.getLogger('web_stream')
web_logger_stream.setLevel(logging.DEBUG)
stream = logging.StreamHandler()
stream.setFormatter(formatter)
web_logger_stream.addHandler(stream)
# web_logger_stream.disabled = True