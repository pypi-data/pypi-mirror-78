import numpy as np
import pandas as pd
from Util.MongoHelper import MongoHelper
from Core.Log import Log
from Util.JobHelper import *
from Util.EmailHelper import QaErrorEmailHelper
import inspect


class QaBase:

    def __init__(self, **kwargs):
        self.mongo_hook = kwargs.get('mongo_hook')
        self.log = kwargs.get('log', Log(self.__class__.__name__))
        self.qa_db = None
        self.run_result = {}
        self.qa_dfs = {}
        self.qa_name = None

    def conn_mongo(self, **kwargs):
        if self.mongo_hook:
            self.qa_db = self.mongo_hook.get_conn()['QaReport']
        else:
            self.qa_db = MongoHelper().connect(**kwargs)['QaReport']

        if debug():
            self.qa_name = self.__class__.__name__
            stack = inspect.stack()
            self.qa_report_file = os.path.join(os.path.dirname(get_stack_frame(stack)[1]), 'QaReports', '{}.html'.format(self.qa_name))
        else:
            self.qa_name = self.__module__ + self.__class__.__name__
            self.qa_report_file = os.path.join(os.path.expanduser('~'), 'QaReports', '{}.html'.format(self.qa_name))

        self.collection_qa = self.qa_db[self.qa_name]

    def get_history_qa_result(self, qa_type: str, record_count=10):
        qas = []
        for index, each in self.collection_qa.find({'qa_type': qa_type}):
            if index >= record_count:
                break
            each.pop('_id')
            each.pop('qa_type')
            qas.append(pd.DataFrame(each, index=[each.get('rundate')]))
        if not qas:
            return pd.DataFrame()
        if len(qas) == 1:  # std is nan if we have only one history record, duplicate it so that the std change to 0.0
            qas.append(qas[0].copy())
        qa_history = pd.concat(qas).sort_index(ascending=False).head(record_count)
        return qa_history

    def check_qa_result(self, qa_now: pd.Series, check_method: str = '3_sigema', **kwargs): # check qa result using 3 sigema princ
        qa_now.index = qa_now.index.astype(str) # convert all index to string, becasue mongo needs that
        if check_method == '3_sigema':
            self.check_qa_result_use_3_sigema(qa_now)
        else:
            raise ValueError('unknown check method', str(check_method))


    def check_qa_result_use_3_sigema(self, qa_now: pd.Series): # check qa result using 3 sigema princ
        qa_type = qa_now['qa_type']
        qa_history = self.get_history_qa_result(qa_type)
        if qa_history.empty:
            self.log.error("we haven't got any history records yet", qa_type)
            return

        # check field info
        diff1 = set(qa_now.index) - set(qa_history.columns)
        if len(diff1) != 1:
           self.log.error('we got new fields in this run', diff1)

        diff2 = set(qa_history.columns) - set(qa_now.index)
        if len(diff2) != 1:
            self.log.error('we lost fields in this run', diff2)

        # check data count info
        for col in qa_history:
            try:
                if col == 'rundate':
                    continue
                data_history = qa_history[col]
                std = data_history.std()
                mean = data_history.mean()
                if mean is np.nan:
                    self.log.info('Col %s in Nan' % col)
                    continue
                if col in qa_now.index:
                    data_this_run = qa_now[col]
                else:
                    self.log.error('''PAY ATTENTION !!!! We don't have column {} in this run'''.format(col))
                    continue

                if mean - 3 * std <= data_this_run <= mean + 3 * std:
                    pass
                else:
                    self.log.error(
                        "Column %s not qualified\n mean %s std %s data this run %s" % (
                            str(col), str(mean), str(std), str(data_this_run)))
                    self.log.error("increase/decrease ratio is %s" % str((data_this_run - mean) / mean))
            except Exception as e:
                self.log.error("failed to process col %s except: %s" % (str(col), str(e)))

    def save_qa_result(self, qa_result: pd.Series, rundate):
        qa_result['rundate'] = rundate
        qa_result.index = qa_result.index.astype(str) # convert all index to string, becasue mongo needs that
        qa_result_dict = qa_result.to_dict()
        self.collection_qa.insert_one(qa_result_dict)
        qa_type = qa_result['qa_type']
        self.report_qa(qa_type)

    @staticmethod
    def read_data_from_file(file) -> pd.DataFrame :
        '''
        user pandas to read data from file
        :param file:
        :return: pandas data frame
        '''
        if str(file).split('.')[-1] == 'csv':
            df = pd.read_csv(file)
        elif str(file).split('.')[-1] == 'parquet':
            df = pd.read_parquet(file)
        else:
            raise ValueError('Unknown file type', file)
        return df

    def read_data_from_mysql(self, **kwargs):
        pass

    def on_run(self, **kwargs):
        pass

    def run(self, **kwargs):
        self.before_run()
        self.run_result['run_result'] = self.on_run(**kwargs)
        self.after_run(**kwargs)
        return self.run_result

    def after_run(self, **kwargs):  # do something after run
        self.save_qa_report()
        dag = kwargs.get('dag')
        if dag:
            email = dag.default_args.get('email')
            if email:
                email_result = self.send_qa_error_email(email)
                self.run_result['email_result'] = email_result

    def report_qa(self, qa_type):
        from tabulate import tabulate
        df_report = self.get_history_qa_result(qa_type)
        report_msg_consle = tabulate(df_report, showindex=True, headers='keys', tablefmt='psql')
        print('\n' + '{}:'.format(qa_type) + '\n' + report_msg_consle)
        self.qa_dfs[qa_type] = df_report

    def before_run(self, **kwargs):  # do something before run
        self.conn_mongo(**kwargs)

    def send_qa_error_email(self, to):
        if debug():
            return
        if not self.log.error_list:
            self.log.info('nothing wrong happened')
            return
        error_html = pd.DataFrame(self.log.error_list).to_html()
        QaErrorEmailHelper(to=to, html_content=error_html, subject=self.qa_name + 'LogError').send_email()
        return to

    def send_qa_df_email(self, to):
        with open(self.qa_report_file, encoding='utf-8') as fh:
            qa_df_html = fh.read()
        QaErrorEmailHelper(to=to, html_content=qa_df_html, subject=self.qa_name + 'DataFrame').send_email()
        return to

    def save_qa_report(self):
        qa_htmls = []
        for qa_type, qa_df in self.qa_dfs.items():
            html = qa_df.reset_index(drop=True).style.bar().render()
            qa_htmls.append('<h2>{}: </h2>'.format(qa_type) + html)
        report_str = '\n'.join(qa_htmls)
        if not os.path.exists(os.path.dirname(self.qa_report_file)):
            os.makedirs(os.path.dirname(self.qa_report_file))
        with open(self.qa_report_file, 'w', encoding='utf-8') as fh:
            fh.write(report_str)

    def check_count_info(self, df: pd.DataFrame, fields=None, rundate=None, **kwargs):
        if not fields:
            fields = df.columns
        if not rundate:
            rundate = df['RunDate'].unique()[0]
        count_info = df[fields].count()
        count_info['qa_type'] = 'count_info'
        self.check_qa_result(count_info)
        self.save_qa_result(count_info, rundate)

    def check_null_info(self, df: pd.DataFrame, fields=None, rundate=None, **kwargs):
        if not fields:
            fields = df.columns
        if not rundate:
            rundate = df['RunDate'].unique()[0]
        null_count_info = df[fields].isna().sum()
        null_count_info['qa_type'] = 'null_count_info'
        self.check_qa_result(null_count_info)
        self.save_qa_result(null_count_info, rundate)

    def check_unique_count_info(self, df: pd.DataFrame, fields=None, rundate=None, **kwargs):
        if not fields:
            fields = df.columns
        if not rundate:
            rundate = df['RunDate'].unique()[0]
        unique_count_info = df[fields].nunique()
        unique_count_info['qa_type'] = 'unique_count_info'
        self.check_qa_result(unique_count_info)
        self.save_qa_result(unique_count_info, rundate)



if __name__ == '__main__':
    t = QaBase()
