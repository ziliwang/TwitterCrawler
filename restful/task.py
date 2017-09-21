from flask_restful import Resource
from flask import request
import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from base import get_db, Task, IllegalArgumentsError, TaskIDnoExists, NoResultFound


class TaskAdd(Resource):
    """
    @api {post} /task/add Add Task
    @apiVersion 0.1.0
    @apiGroup Task
    @apiName Add Task to database
    @apiParam {String} type task type, 'USER' or 'SEARCH'
    @apiParam {String} args task arguments
    @apiParam {String} tittle task tittle
    @apiSuccessExample {json} Success-Response:
        {
            "message": "success",
            "status": 200
        }
    """
    def post(self):
        _type = request.form.get('type')
        _arg = request.form.get('args')
        tittle = request.form.get('tittle')
        if _type and _arg and tittle and _type in ['USER', 'SEARCH']:
            with get_db() as s:
                task = Task()
                task.ttype = _type
                task.tittle = tittle
                task.status = 'MONITOR'
                task.args = _arg
                s.add(task)
                s.commit()
            return {"message": "success", "status": 200}
        else:
            raise IllegalArgumentsError


class TaskList(Resource):
    """
    @api {get} /task/list List Task
    @apiVersion 0.1.0
    @apiGroup Task
    @apiName List task
    @apiSuccessExample {json} Success-Response:
        [
          {
            "id": 1,
            "tittle": "task A",
            "type": "USER",
            "status": "MONITOR",
            "args": "realDonaldTrump"
          },
          {
            "id": 2,
            "tittle": "task B",
            "type": "SEARCH",
            "status": "MONITOR",
            "args": "q=Donald Trump"
          }
        ]
    """
    def get(self):
        with get_db() as s:
            out = s.query(Task).all()
        tmp = []
        for i in out:
            tmp.append({
                'id': i.tid,
                'tittle': i.tittle,
                'type': i.ttype,
                'status': i.status,
                'args': i.args
            })
        return tmp


class TaskStatus(Resource):
    """
    @api {get} /task/status Get Task Status
    @apiVersion 0.1.0
    @apiGroup Task
    @apiName Task Status
    @apiParam {Integer} id task id
    @apiSuccessExample {json} Success-Response:
        "MONITOR"
    """
    def get(self):
        _id = request.args.get('id')
        if _id:
            try:
                with get_db() as s:
                    task = s.query(Task).filter(Task.tid == _id).one()
                    out = task.status
                    return out
            except NoResultFound:
                raise TaskIDnoExists
        else:
            raise IllegalArgumentsError


class TaskOpt(Resource):
    """
    @api {post} /task/opt Handle Task
    @apiVersion 0.1.0
    @apiGroup Task
    @apiName Handle Task
    @apiParam {Integer} id task id
    @apiParam {String} cmd operation on task, support "stop", "continue", "drop"
    @apiSuccessExample {json} Success-Response:
        {
            "message": "success",
            "status": 200
        }
    """
    def post(self):
        _id = request.form.get('id')
        cmd = request.form.get('cmd')
        if _id and cmd and cmd in ['stop', 'start', 'drop']:
            with get_db() as s:
                task = s.query(Task).filter(Task.tid == _id).one()
                if task:
                    if cmd == 'stop' and task.status != "STOP":
                        task.status = "STOP"
                        s.commit()
                    elif cmd == "start" and task.status != "MONITOR":
                        task.status = "MONITOR"
                        s.commit()
                    elif cmd == "drop":
                        s.delete(task)
                        s.commit()
                    else:
                        pass
                    return {"message": "success", "status": 200}
                else:
                    raise TaskIDnoExists
        else:
            raise IllegalArgumentsError
