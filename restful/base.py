from os import path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, exc
from sqlalchemy.orm.exc import NoResultFound
from contextlib import contextmanager
import sys

PACKAGE_ROOT = path.abspath(path.dirname(__file__))
sys.path.append(PACKAGE_ROOT + '../')

from db import CON, Task


@contextmanager
def get_db():
    # preprocess
    engine = create_engine(CON)
    DBSession = sessionmaker(bind=engine)
    sess = DBSession()
    # return connection
    yield sess
    # clean up
    sess.close()


class IllegalArgumentsError(Exception):
    pass


class TaskIDnoExists(Exception):
    pass
