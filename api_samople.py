import time
import requests
from common.config import WEB_CONFIG
import os


class TestCheckInCheckOut:
    sid = '9cea2a86-27ec-4428-a308-491ed0f0071a'
    rq_session = requests.Session()
    rq_session.headers = {
        'sid': sid
    }

    def send_checkin(self):
        data = {
            'coord': '21.076491378255305, 105.6985938529995'
        }
        rq = self.rq_session.post(url='%s/api/attendance/checkin' % WEB_CONFIG['RUN_DOMAIN'], json=data)
        print(rq.content)

    def send_checkout(self):
        data = {
            'coord': '21.076491378255305, 105.6985938529995'
        }
        rq = self.rq_session.post(url='%s/api/attendance/checkout' % WEB_CONFIG['RUN_DOMAIN'], json=data)
        print(rq.content)

    def today_status(self):
        rq = self.rq_session.get(url='%s/api/attendance/today-status' % WEB_CONFIG['RUN_DOMAIN'])
        print(rq.content)


if __name__ == '__main__':
    # TestCheckInCheckOut().send_checkin()
    # time.sleep(3)
    # TestCheckInCheckOut().send_checkout()
    TestCheckInCheckOut().today_status()
