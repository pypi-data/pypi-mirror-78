import datetime
import os
import pandas as pd
from .Log import Log
from .HttpManager import HttpManager
from .Proxy import Proxy
from .DaoBase import DaoBase
from Util.DumperHelper import DumperHelper
from Util.JobHelper import debug
from Util.EmailHelper import BotErrorEmailHelper
from Util.DateTimeHelper import now
import time


class JobBase:

    def __init__(self, *args, **kwargs):
        self.init_proxy()

        self.run_date = kwargs.get('run_date', datetime.datetime.now())
        self.log = Log(self.__class__.__name__)
        kwargs['rundate'] = self.run_date
        kwargs['log'] = self.log

        self.dumper = DumperHelper(**kwargs)
        self.dumper_error = DumperHelper(category='error', **kwargs)
        self._dao = DaoBase(**kwargs)

        self.maxHourlyPageView = 600
        self.job_id = kwargs.get('job_id')
        self.run_id = kwargs.get('run_id')

        self._proxy_instance = Proxy()
        self.func = None
        self.run_result = {}

    def init_http_manager(self, timeout=30, default_header=False):

        manager = HttpManager(proxy=self._proxy_instance
                              , default_header=default_header
                              , log=self.log
                              , timeout=timeout
                              , max_hourly_page_view=self.maxHourlyPageView
        )

        return manager

    def download_page(self
                      , url: str
                      , manager: HttpManager
                      , max_retry: int = 10
                      , post_data: str = None
                      , validate_str_list: list = None
                      ):
        retry = 0
        page = ''
        while retry < max_retry:
            retry += 1
            # When retry big then 1, need be write log
            if retry > 3:
                self.log.info('retry', str(retry))
                time.sleep(retry)

            resp = manager.download_page(url, post_data=post_data)
            if resp is None:
                continue
            page = resp.text

            for each in validate_str_list:
                if page and each in page:
                    return page

        if retry == max_retry:
            self.log.error('retry all failed', url)

        return page

    def debug(self):
        return debug()

    def on_run(self, **kwargs):
        pass

    def run(self, **kwargs):
        self.before_run()

        if kwargs.get('func_name'):
            func_name = kwargs.get('func_name')
            exec('self.func=self.{}'.format(func_name))
            self.func()
            if not kwargs.get('file'):
                kwargs['file'] = '{}_{}.csv'.format(func_name, now().date())
        else:
            if not kwargs.get('file'):
                kwargs['file'] = '{}_{}.csv'.format(self.__class__.__name__.lower(), now().date())
            self.run_result['run_result'] = self.on_run(**kwargs)

        self.after_run(**kwargs)
        return self.run_result

    def after_run(self, **kwargs):  # do something after run
        dag = kwargs.get('dag')
        if dag:
            email = dag.default_args.get('email')
            if email:
                email_result = self.send_bot_error_email(email)
                self.run_result['email_result'] = email_result

        if kwargs.get('file'):
            file = kwargs.get('file')
            files = [file] if isinstance(file, str) else file  # file list
            if len(files) != len(self._dao.meta_datas):
                raise ValueError('file names does not match with meta datas')
            for i in range(len(self._dao.meta_datas)):
                self._dao.meta_datas[i]['file'] = files[i]
                self._dao.meta_datas[i]['project_name'] = self.__module__.lower()
            self.run_result['export_result'] = self._dao.export_data()

    def before_run(self, **kwargs): # do something before run
        pass

    @property
    def proxy(self):
        return self._proxy_instance.proxy_pool

    @proxy.setter
    def proxy(self, value):
        self._proxy_instance.proxy_pool = value

    def init_proxy(self):
        self.LOCALHOST = '127.0.0.1:8888'
        self.NONE_PROXY = ''
        self.PROXY_SQUID_US_3 = os.getenv('PROXY_SQUID_US_3', '')
        self.LOCAL_PROXY_P4 = os.getenv('LOCAL_PROXY_P4', '')
        self.LOCAL_PROXY_P5 = os.getenv('LOCAL_PROXY_P5', '')

    def send_bot_error_email(self, to):
        if debug():
            return
        if not self.log.error_list:
            self.log.info('nothing wrong happened')
            return
        html_content = pd.DataFrame(self.log.error_list).to_html()
        BotErrorEmailHelper(to=to, html_content=html_content, subject=self.__module__).send_email()
        return to
