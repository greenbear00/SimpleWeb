from common.lib.logger import web_logger_stream, web_logger_logstash, werkzeug

def logger_info(msg, flag=0):
    """
    flag = 0 -> all
    flag = 1 -> only logstash
    flag = 2 -> only stream
    :param msg:
    :param flag:
    :return:
    """
    if flag == 0:
        web_logger_logstash.info(msg)
        web_logger_stream.info(msg)
        werkzeug.info(msg)
    elif flag == 1:
        web_logger_logstash.info(msg)
    elif flag == 2:
        web_logger_stream.info(msg)
        werkzeug.info(msg)
    else:
        pass