from flask_restful import Resource
from flask import request
import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from base import PACKAGE_ROOT, IllegalArgumentsError
import re
import signal
import subprocess


class status(Resource):
    """
    @api {get} /server/status Get Crawler scheduler status
    @apiVersion 0.1.0
    @apiGroup server
    @apiName Crawler scheduler status
    @apiSuccessExample {json} Success-Response:
        "runing"
    """
    def get(self):
        pidf = os.path.join(PACKAGE_ROOT, '../run/crawler.pid')
        if os.path.exists(pidf):
            with open(pidf) as f:
                pid = f.read()
            if re.match(r'\d+$', pid):
                if os.path.exists('/proc/{}/'.format(pid)):
                    return "running"
        return "stoped"


class Opt(Resource):
    """
    @api {post} /server/opt server level operation
    @apiVersion 0.1.0
    @apiGroup server
    @apiName server operation
    @apiParam {String} cmd operation command, 'start' or 'stop', command equal status, no operating.
    @apiSuccessExample {json} Success-Response:
        {
            "message": "success",
            "status": 200
        }
    """
    def post(self):
        cmd = request.form.get('cmd')
        if cmd and cmd in ['start', 'stop']:
            pidf = os.path.join(PACKAGE_ROOT, '../run/crawler.pid')
            if os.path.exists(pidf):
                with open(pidf) as f:
                    pid = f.read()
                if re.match(r'\d+$', pid):
                    if os.path.exists('/proc/{}/'.format(pid)):
                        if cmd == 'stop':
                            os.kill(int(pid), signal.SIGTERM)
                            os.remove(pidf)
                        else:
                            pass
                        return {"message": "success", "status": 200}
            if cmd == "start":
                subprocess.Popen(["python3", os.path.join(
                                PACKAGE_ROOT, '../crawler_scheduler.py')])
                return {"message": "success", "status": 200}
            else:
                pass
            return {"message": "success", "status": 200}
        else:
            raise IllegalArgumentsError
