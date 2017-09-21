import requests
import unittest
import time

baseurl = 'http://192.168.19.126:5000/'


class twitterAPItest(unittest.TestCase):
    testid = None

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testT0_set_up(self):
        lsresp = requests.get(baseurl + 'task/list')
        for i in lsresp.json():
            if 'test' == i['tittle']:
                resp = requests.post(baseurl + 'task/opt',
                                     data={'id': i['id'], 'cmd': 'drop'})
                self.assertEqual(resp.json()['message'], 'success')
                break
        lsresp = requests.get(baseurl + 'task/list')
        self.assertNotIn('test', [i['tittle'] for i in lsresp.json()])

    def testT1_stop_server(self):
        api = 'server/opt'
        resp = requests.post(baseurl + api, data={'cmd': 'stop'})
        self.assertEqual(resp.json()['message'], 'success')
        resp = requests.get(baseurl + 'server/status')
        self.assertEqual(resp.json(), 'stoped')

    def testT2_start_server(self):
        api = 'server/opt'
        resp = requests.post(baseurl + api, data={'cmd': 'start'})
        self.assertEqual(resp.json()['message'], 'success')
        time.sleep(3)
        resp = requests.get(baseurl + 'server/status')
        self.assertEqual(resp.json(), 'running')

    def testT3_add_task(self):
        api = 'task/add'
        resp = requests.post(baseurl + api,
                             data={'type': 'USER',
                                   'tittle': 'test',
                                   'args': 'CNN'})
        self.assertEqual(resp.json()['message'], 'success')
        lsresp = requests.get(baseurl + 'task/list')
        self.assertIn('test', [i['tittle'] for i in lsresp.json()])

    def testT4_stop_task(self):
        lsresp = requests.get(baseurl + 'task/list')
        for i in lsresp.json():
            if i['tittle'] == 'test':
                testid = i['id']
        api = 'task/opt'
        resp = requests.post(baseurl + api,
                             data={'id': testid, 'cmd': 'stop'})
        self.assertEqual(resp.json()['message'], 'success')
        st = requests.get(baseurl + 'task/status', params={'id': testid})
        self.assertEqual(st.json(), 'STOP')

    def testT5_start_task(self):
        lsresp = requests.get(baseurl + 'task/list')
        for i in lsresp.json():
            if i['tittle'] == 'test':
                testid = i['id']
        api = 'task/opt'
        resp = requests.post(baseurl + api,
                             data={'id': testid, 'cmd': 'start'})
        self.assertEqual(resp.json()['message'], 'success')
        time.sleep(1)
        st = requests.get(baseurl + 'task/status', params={'id': testid})
        self.assertEqual(st.json(), 'MONITOR')

    def testT6_drop_task(self):
        lsresp = requests.get(baseurl + 'task/list')
        for i in lsresp.json():
            if i['tittle'] == 'test':
                testid = i['id']
        api = 'task/opt'
        resp = requests.post(baseurl + api,
                             data={'id': testid, 'cmd': 'drop'})
        self.assertEqual(resp.json()['message'], 'success')
        time.sleep(1)
        st = requests.get(baseurl + 'task/status', params={'id': testid})
        self.assertEqual(st.json()['message'], 'task id not exists')


if __name__ == '__main__':
    unittest.main(failfast=True)
