from flask import Flask, make_response, request
from flask_restful import Api
from logging.handlers import RotatingFileHandler
import logging
import json
from os import path
from restful.server import Opt as ServerOpt, status as ServerStatus
from restful.task import TaskAdd, TaskList, TaskOpt, TaskStatus


class ContextualFilter(logging.Filter):
    def filter(self, log_record):
        """ Provide some extra variables to give our logs some
            better info """
        log_record.url = request.path
        # Try to get the IP address of the user through reverse proxy
        log_record.ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        return True


"""error handle"""
errors = {
    'IllegalArgumentsError': {
        'message': "illegal arguments",
        'status': 601,
    },
    'TaskIDnoExists': {
        'message': "task id not exists",
        'status': 602,
    },
}


app = Flask(__name__)
"""log handler"""
handler = RotatingFileHandler(path.join(path.abspath(path.dirname(__file__)),
                                        'run/APP.log'),
                              maxBytes=3 * 1024 * 1024,
                              backupCount=4)
handler.setLevel(logging.INFO)
formator = logging.Formatter('%(asctime)s - %(url)s - %(ip)s - %(message)s')
handler.addFilter(ContextualFilter())
handler.setFormatter(formator)
app.logger.addHandler(handler)
app.logger.setLevel(logging.INFO)
api = Api(app, errors=errors)

"""response"""


@api.representation('application/json')
def output_json(data, code, headers=None):
    """Makes a Flask response with a JSON encoded body"""
    resp = make_response(json.dumps(data), code)
    resp.headers['Content-Type'] = 'application/json; charset=utf-8'
    resp.headers['Server'] = 'CEIEC-NLP v0.1.1'
    resp.headers.extend(headers or {})
    return resp


api.add_resource(ServerStatus, '/server/status')
api.add_resource(ServerOpt, '/server/opt')
api.add_resource(TaskList, '/task/list')
api.add_resource(TaskStatus, '/task/status')
api.add_resource(TaskAdd, '/task/add')
api.add_resource(TaskOpt, '/task/opt')


if __name__ == "__main__":
    # app.debug = True
    app.run(host='0.0.0.0', port=5000)
