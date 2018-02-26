import time
from multiprocessing import Process
from api import app
from getter import Getter
from tester import Tester
from db import RedisClient
from setting import *

class Scheduler():
    def scheduler_tester(self, cycle = TESTER_CYCLE):
        tester = Tester()
        while True:
            print('测试器开始运行')
            tester.run()
            time.sleep(cycle)

    def scheduler_getter(self, cycle = GETTER_CYCLE):
        getter = Getter()
        while True:
            print('生产器开始运行')
            getter.run()
            time.sleep(cycle)

    def scheduler_api(self):
        app.run(API_HOST, API_PORT)

    def run(self):
        print('代理池开始运行')

        if TESTER_ENABLED:
            tester_process = Process(target=self.scheduler_tester)
            tester_process.start()

        if API_ENABLED:
            api_process = Process(target=self.scheduler_api)
            api_process.start()

        if GETTER_ENABLED:
            getter_process = Process(target=self.scheduler_getter)
            getter_process.start()






if __name__ == '__main__':
    s = Scheduler()
    s.run()