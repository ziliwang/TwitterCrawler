#!/usr/bin/env python3
import time
import os
import sched
import click
import crawler
import signal
import schedule
import re


def job():
    print('启动定时执行')
    crawler.main()


def main():
    root = os.path.abspath(os.path.dirname(__file__))
    run = os.path.join(root, 'run')  # pid 文件
    if not os.path.exists(run):
        os.makedirs(run)
    # check  pid file crawler.pid
    pidf = os.path.join(run, 'crawler.pid')
    if os.path.exists(pidf):
        with open(pidf) as f:
            tmp = f.read()
            if re.match(r'\d+', tmp):
                try:
                    os.kill(int(tmp), signal.SIGTERM)
                except ProcessLookupError as e:
                    pass
    pid = os.getpid()
    with open(pidf, 'w') as f:
        f.write(str(pid))
    # circle schedule
    schedule.every().hour.do(crawler.main)
    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == '__main__':
    main()
