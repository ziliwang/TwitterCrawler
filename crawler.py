import time
import base64
import os
import json
from db import Account, Task
from restful.base import get_db
import requests
import logging
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# disable InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def log_conf(_log_file):
    logging.basicConfig(
        level=logging.INFO,
        format='%(levelname)s %(asctime)s %(funcName)s %(message)s',
        filename=_log_file,
        filemode='a')
    console = logging.StreamHandler()
    console.setLevel(logging.NOTSET)
    formatter = logging.Formatter(
        '%(levelname)s %(asctime)s %(funcName)s %(message)s')
    console.setFormatter(formatter)
    logger = logging.getLogger('')
    logger.addHandler(console)
    return logger


class Token():
    """授权"""
    def __init__(self, AK, AS, token=None, proxy=None, logger):
        self.AK = AK
        self.AS = AS
        tmp = AK + ':' + AS
        self.base64 = base64.b64encode(tmp.encode()).decode('utf-8')
        self.availbale = True
        self.reset = False
        self.token = token
        self.proxy = proxy
        self.logger = logger
        if not self.token:
            self.auth()

    def auth(self):
        try:
            resp = requests.post(
                'https://api.twitter.com/oauth2/token?grant_type=client_credentials',
                headers={'Authorization': 'Basic ' + self.base64,
                         'accept-encoding': 'json'},
                proxies=self.proxy)
            self.token = resp.json()['access_token']
            self.logger.info('Auth success {} {}'.format(self.AK, self.AS))
        except BaseException as e:
            self.logger.error('Auth failed {} {}'.format(self.AK, self.AS))
            raise ValueError('Auth failed')

    def update(self):
        if self.reset:
            if time.time() < self.reset:
                self.availbale = False
                return
        self.availbale = True
        self.logger.info('update success {} {}'.format(self.AK, self.AS))


class TokenSched():
    """授权调度"""
    def __init__(self, proxy, logger):
        self.token_ls = []
        self.logger = logger
        with get_db() as s:
            all_record = s.query(Account).all()
            self.logger.info('Total {}'.format(len(all_record)))
            for i in all_record:
                tmp = Token(i.AK, i.AS, i.token, proxy=proxy)
                if not i.token:
                    i.token = tmp.token
                self.token_ls.append(tmp)
            s.commit()
        self.current_index = None

    def get(self, reset=None):
        if self.current_index is None:
            self.current_index = 0
            self.logger.info('Init Token, Index: {}'.format(self.current_index))
            return self.token_ls[self.current_index].token
        else:
            if reset:
                self.token_ls[self.current_index].reset = reset
                self.logger.info('Limited, Index: {}'.format(self.current_index))
                if self.current_index == len(self.token_ls) - 1:
                    self.current_index = 0
                else:
                    self.current_index += 1
                # check
                self.logger.info('BlockCheck, Index: {}'.format(self.current_index))
                while True:
                    self.token_ls[self.current_index].update()
                    if self.token_ls[self.current_index].availbale:
                        self.logger.info('BlockCheck: passed, Index: {}'.format(
                            self.current_index))
                        return self.token_ls[self.current_index].token
                    else:
                        self.logger.info('BlockCheck:failed, Index: {}'.format(
                            self.current_index))
                        time.sleep(60)
            else:
                self.token_ls[self.current_index].token


class GetSearch():
    """单个任务实例"""
    headers = {'accept-encoding': 'gzip'}
    url = 'https://api.twitter.com/1.1/search/tweets.json'

    def __init__(self, tokensched, proxy, logger):
        self.tokensched = tokensched
        self.proxy = proxy
        self.logger = logger
        self.headers['Authorization'] = 'Bearer ' + self.tokensched.get()

    def get(self, args):
        """下载单任务文件"""
        self.logger.info('start {}'.format(json.dumps(args)))
        args = dict(tuple(i.split('=')) for i in args.split('&'))
        args['count'] = 200
        args['tweet_mode'] = 'extended'
        _next = None
        dls = []
        while True:
            if not _next:
                retry = 0
                try:
                    resp = requests.get(
                        self.url,
                        params=args,
                        headers=self.headers,
                        proxies=self.proxy,
                        verify=False)
                except requests.exceptions.SSLError as e:
                    self.logger.warn('1stRequest retry')
                    retry += 1
                    if retry > 3:
                        raise ValueError('max time')
                except BaseException as e:
                    self.logger.error('1stRequest: {}'.format(str(e)))
                    raise ValueError('unkown error')
            else:
                retry = 0
                while True:
                    try:
                        resp = requests.get(
                            self.url + _next,
                            headers=self.headers,
                            proxies=self.proxy,
                            verify=False)
                        break
                    except requests.exceptions.SSLError as e:
                        self.logger.warn('Request retry')
                        retry += 1
                        if retry > 3:
                            raise ValueError('max time')
                    except BaseException as e:
                        self.logger.error('Request {}'.format(str(e)))
                        raise ValueError('unkown error')
            resp.close()
            try:
                if int(resp.headers['x-rate-limit-remaining']) == 0:
                    self.logger.info('token limited')
                    self.headers['Authorization'] = 'Bearer ' + \
                        self.tokensched.get(int(resp.headers['x-rate-limit-reset']))
            except KeyError as e:
                self.logger.info("IllegalHeaders")
                if set(['next_results', 'status']).issubset(resp.json().keys()):
                    self.logger.info("IllegalHeaders, Legal Response: record")
                else:
                    self.logger.info(
                        "IllegalHeaders, Illegal Response {}".format(
                            json.dumps(resp.headers.keys())))
                    break
            dls += resp.json()['statuses']
            if 'next_results' in resp.json()['search_metadata']:
                _next = resp.json()['search_metadata']['next_results']
            else:
                max_id = resp.json()['search_metadata']['max_id']
                break
        return dls, max_id


def main():
    with open('conf.json') as f:
        conf = json.load(f)
    proxy = conf['proxy']
    # check log file
    if not os.path.exists(os.path.dirname(conf['log_file'])):
        os.makedirs(conf['log_file'])
    # check output
    if not os.path.exists(conf['store_dir']):
        os.makedirs(conf['store_dir'])
    logger = log_conf(conf['log_file'])
    tokensched = TokenSched(proxy=proxy, logger=logger)
    fecthor = GetSearch(tokensched=tokensched, proxy=proxy, logger=logger)
    out_dir = os.path.join(conf['store_dir'],
                           time.strftime('%Y%m%d-%H:%M', time.localtime()))
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    with get_db() as s:
        tasks = s.query(Task).filter(Task.status == 'MONITOR').all()
        logger.info('{} Tasks'.format(len(tasks)))
        for t in tasks:
            logger.info('start task {}'.format(t.tid))
            if t.ttype == 'SEARCH':
                args = t.args + '&{}'.format(t.last) if t.last else t.args
            else:
                args = 'q=from:{}&max_id={}'.format(t.args, t.last) if t.last else 'q=from:{}'.format(t.args)
            d, max_id = fecthor.get(args)
            t.last = int(max_id)
            logger.info('write task {}'.format(t.tid))
            with open(os.path.join(out_dir, str(t.tid)), 'w') as f:
                json.dump(d, f)
        s.commit()
    logger.info('Finished, clean_up and quite')


if __name__ == '__main__':
    main()
