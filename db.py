#!/usr/bin/env python3
import os
from sqlalchemy import *
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
import click
import json


Base = declarative_base()
SCHEMA = 'public'


class Task(Base):
    __tablename__ = "tbl_task"
    tid = Column(Integer, Sequence('task_id_seq'), primary_key=True)
    tittle = Column(VARCHAR(200), nullable=False)
    ttype = Column(VARCHAR(50), nullable=False)
    status = Column(VARCHAR(50), nullable=False)
    last = Column(BigInteger)
    args = Column(VARCHAR(200), nullable=False, unique=True)
    __table_args__ = (
        CheckConstraint("status IN ('ERROR', 'STOP', 'MONITOR')", name="status_constraint"),
        CheckConstraint("ttype IN ('USER', 'SEARCH')", name="type_constraint"),
        {'schema': SCHEMA}
    )

    def __init__(self):
        self.tid
        self.tittle
        self.ttype
        self.status
        self.last
        self.args

    def __str__(self):
        return "Task {}".format(self.tid)


class Account(Base):
    __tablename__ = "tbl_account"
    aid = Column(Integer, Sequence('account_id_seq'), primary_key=True)
    AK = Column(VARCHAR(30), nullable=False)
    AS = Column(VARCHAR(60), nullable=False)
    token = Column(VARCHAR(120))
    __table_args__ = ({'schema': SCHEMA})

    def __init__(self):
        self.aid
        self.AK
        self.AS
        self.token


def parse_conf():
    with open('configure.json') as f:
        d = json.load(f)
    con = '{}://{}:{}@{}/{}'.format(d['db_type'], d['db_role'], d['db_passwd'],
                                    d['db_host'], d['db_name'])
    return con


CON = parse_conf()


def init():
    engine = create_engine(CON)
    Base.metadata.create_all(engine)
    return engine, Base


def create_tables():
    engine, Base = init()
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


@click.command()
@click.option('--init', default=False, help='init database')
def main(init):
    if init:
        create_tables()


if __name__ == '__main__':
    main()
