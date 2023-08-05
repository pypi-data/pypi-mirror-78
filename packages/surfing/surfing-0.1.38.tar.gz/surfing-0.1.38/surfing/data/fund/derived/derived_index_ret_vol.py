import pandas as pd
import numpy as np
import datetime
import json
import traceback
from ...wrapper.mysql import BasicDatabaseConnector, DerivedDatabaseConnector
from ...api.basic import *
from ...view.derived_models import *


class IndexIndicatorProcessor(object):
    w1 = 5
    m1 = 20
    m3 = 60
    m6 = 121
    y1 = 242
    y3 = 242*2
    y5 = 242*5
    y10 = 242*10

    def __init__(self, data_helper):
        self._data_helper = data_helper

    def history_init(self):
        with BasicDatabaseConnector().managed_session() as db_session:
            query = db_session.query(IndexPrice).filter(IndexPrice.datetime >= datetime.date(2010,1,1))
            self.index_price = pd.read_sql(query.statement, query.session.bind)
            self.index_price = self.index_price.pivot_table(index='datetime', columns='index_id', values='close').fillna(method='ffill').fillna(method='bfill')
            self.date_list = self.index_price.index

    def init(self, end_date:str='20200715'):
        self.end_date = datetime.datetime.strptime(end_date,'%Y%m%d').date()
        with BasicDatabaseConnector().managed_session() as db_session:
            query = db_session.query(IndexPrice).filter(IndexPrice.datetime <= self.end_date,
                                                        IndexPrice.datetime >= datetime.date(2005,1,1))
            self.index_price = pd.read_sql(query.statement, query.session.bind)
            self.index_price_ret = self.index_price.pivot_table(index='datetime', columns='index_id', values='close').fillna(method='ffill').fillna(method='bfill')
            self.index_price_vol_part = self.index_price.pivot_table(index='datetime', columns='index_id', values='close')
            query = db_session.query(TradingDayList)
            trade_day_df = pd.read_sql(query.statement, query.session.bind).drop(columns='_update_time')
            begin_d = self.index_price_vol_part.index[0]
            end_d = self.index_price_vol_part.index[-1]
            trade_day_list = trade_day_df.datetime
            trade_day_index = trade_day_list[(trade_day_list>=begin_d) & (trade_day_list<=end_d)]
            self.index_price_vol_part = self.index_price_vol_part.reindex(trade_day_index).pct_change(1)
            self.date_list = self.index_price_ret.index

    def _get_begin_of_year(self, dt):
        _dt = datetime.date(dt.year,1,1)
        return self.date_list[self.date_list >= _dt][0]

    def _get_begin_of_season(self, dt):
        _m = int((dt.month-1) / 3) * 3 + 1
        _dt = datetime.date(dt.year, _m, 1)
        return self.date_list[self.date_list >= _dt][0]

    def _term_ret(self, df):
        return df.iloc[-1] / df.iloc[0] - 1

    def _term_vol(self, df):
        return df.std(ddof=1)

    def _this_y_ret(self, x):
        dt2 = x.name
        dt1 = self._get_begin_of_year(dt2)
        return self._term_ret(self.index_price.loc[dt1:dt2])

    def _this_s_ret(self, x):
        dt2 = x.name
        dt1 = self._get_begin_of_season(dt2)
        return self._term_ret(self.index_price.loc[dt1:dt2])

    def _cumulative_ret(self, x):
        dt = x.name
        return self._term_ret(self.index_price.loc[:dt])

    def _this_y_vol(self, x):
        dt2 = x.name
        dt1 = self._get_begin_of_year(dt2)
        return self._term_vol(self.index_price.loc[dt1:dt2])

    def _this_s_vol(self, x):
        dt2 = x.name
        dt1 = self._get_begin_of_season(dt2)
        return self._term_vol(self.index_price.loc[dt1:dt2])

    def _cumulative_vol(self, x):
        dt = x.name
        return self._term_vol(self.index_price.loc[:dt])

    def _ret_history(self):
        self.ret_res = {}
        self.ret_res['w1_ret'] = self.index_price.pct_change(self.w1)
        self.ret_res['m1_ret'] = self.index_price.pct_change(self.m1)
        self.ret_res['m3_ret'] = self.index_price.pct_change(self.m3)
        self.ret_res['m6_ret'] = self.index_price.pct_change(self.m6)
        self.ret_res['y1_ret'] = self.index_price.pct_change(self.y1)
        self.ret_res['y3_ret'] = self.index_price.pct_change(self.y3)
        self.ret_res['y5_ret'] = self.index_price.pct_change(self.y5)
        self.ret_res['y10_ret'] = self.index_price.pct_change(self.y10)
        self.ret_res['this_s_ret'] = self.index_price.apply(self._this_s_ret, axis=1)
        self.ret_res['this_y_ret'] = self.index_price.apply(self._this_y_ret, axis=1)
        self.ret_res['cumulative_ret'] = self.index_price.apply(self._cumulative_ret, axis=1)

    def _process_result(self, result):
        _res = []
        for k, df in result.items():
            _res.append(pd.DataFrame(df.stack()).rename(columns={0:k}))
        self.result = pd.concat(_res,axis=1,sort=False).reset_index()

    def process_ret_history(self):
        self._ret_history()
        self._process_result(self.ret_res)
        df = self.result[self.result.datetime > datetime.date(2018,1,1)]
        df = df.replace(np.Inf,None).replace(-np.Inf,None)
        df = df.drop_duplicates(subset=['index_id','datetime'])
        self._data_helper._upload_derived(df, IndexReturn.__table__.name)

    def _vol_history(self):
        self.ret_vol = {}
        self.ret_vol['w1_vol'] = self.index_price.rolling(self.w1).std(ddof=1)
        self.ret_vol['m1_vol'] = self.index_price.rolling(self.m1).std(ddof=1)
        self.ret_vol['m3_vol'] = self.index_price.rolling(self.m3).std(ddof=1)
        self.ret_vol['m6_vol'] = self.index_price.rolling(self.m6).std(ddof=1)
        self.ret_vol['y1_vol'] = self.index_price.rolling(self.y1).std(ddof=1)
        self.ret_vol['y3_vol'] = self.index_price.rolling(self.y3).std(ddof=1)
        self.ret_vol['y5_vol'] = self.index_price.rolling(self.y5).std(ddof=1)
        self.ret_vol['y10_vol'] = self.index_price.rolling(self.y10).std(ddof=1)
        self.ret_vol['this_s_vol'] = self.index_price.apply(self._this_s_vol, axis=1)
        self.ret_vol['this_y_vol'] = self.index_price.apply(self._this_y_vol, axis=1)
        self.ret_vol['cumulative_vol'] = self.index_price.apply(self._cumulative_vol, axis=1)

    def process_vol_history(self):
        self._vol_history()
        self._process_result(self.ret_vol)
        df = self.result[self.result.datetime > datetime.date(2018,1,1)]
        df = df.replace(np.Inf,None).replace(-np.Inf,None)
        df = df.drop_duplicates(subset=['index_id','datetime'])
        self._data_helper._upload_derived(df, IndexVolatility.__table__.name)

    def _process_update_result(self, result):
        res = []
        for k, s in result.items():
            s.name = k
            res.append(pd.DataFrame(s).rename(columns={0:k}))
        result = pd.concat(res, sort=False, axis=1).reset_index()
        result['datetime'] = self.end_date
        return result

    def _update_ret(self):
        y_date = self._get_begin_of_year(self.end_date)
        s_date = self._get_begin_of_season(self.end_date)
        self.ret_res = {}
        self.ret_res['w1_ret'] = self.index_price_ret.tail(self.w1+1).pct_change(self.w1).iloc[-1]
        self.ret_res['m1_ret'] = self.index_price_ret.tail(self.m1+1).pct_change(self.m1).iloc[-1]
        self.ret_res['m3_ret'] = self.index_price_ret.tail(self.m3+1).pct_change(self.m3).iloc[-1]
        self.ret_res['m6_ret'] = self.index_price_ret.tail(self.m6+1).pct_change(self.m6).iloc[-1]
        self.ret_res['y1_ret'] = self.index_price_ret.tail(self.y1+1).pct_change(self.y1).iloc[-1]
        self.ret_res['y3_ret'] = self.index_price_ret.tail(self.y3+1).pct_change(self.y3).iloc[-1]
        self.ret_res['y5_ret'] = self.index_price_ret.tail(self.y5+1).pct_change(self.y5).iloc[-1]
        self.ret_res['y10_ret'] = self.index_price_ret.tail(self.y10+1).pct_change(self.y10).iloc[-1]
        self.ret_res['this_s_ret'] = self._term_ret(self.index_price_ret.loc[s_date:])
        self.ret_res['this_y_ret'] = self._term_ret(self.index_price_ret.loc[y_date:])
        self.ret_res['cumulative_ret'] = self._term_ret(self.index_price_ret)
        result_ret = self._process_update_result(self.ret_res)
        result_ret = result_ret.replace(np.Inf,None).replace(-np.Inf,None).drop_duplicates(subset=['index_id','datetime'])
        return result_ret

    def _update_vol(self):
        y_date = self._get_begin_of_year(self.end_date)
        s_date = self._get_begin_of_season(self.end_date)
        self.vol_res = {}
        self.vol_res['w1_vol'] = self.index_price_vol_part.tail(self.w1).std(ddof=1)
        self.vol_res['m1_vol'] = self.index_price_vol_part.tail(self.m1).std(ddof=1)
        self.vol_res['m3_vol'] = self.index_price_vol_part.tail(self.m3).std(ddof=1)
        self.vol_res['m6_vol'] = self.index_price_vol_part.tail(self.m6).std(ddof=1)
        self.vol_res['y1_vol'] = self.index_price_vol_part.tail(self.y1).std(ddof=1)
        self.vol_res['y3_vol'] = self.index_price_vol_part.tail(self.y3).std(ddof=1)
        self.vol_res['y5_vol'] = self.index_price_vol_part.tail(self.y5).std(ddof=1)
        self.vol_res['y10_vol'] = self.index_price_vol_part.tail(self.y10).std(ddof=1)
        self.vol_res['this_s_vol'] = self._term_vol(self.index_price_vol_part.loc[s_date:])
        self.vol_res['this_y_vol'] = self._term_vol(self.index_price_vol_part.loc[y_date:])
        self.vol_res['cumulative_vol'] = self._term_vol(self.index_price_vol_part)
        result_vol = self._process_update_result(self.vol_res)
        result_vol = result_vol.replace(np.Inf,None).replace(-np.Inf,None).drop_duplicates(subset=['index_id','datetime'])
        return result_vol

    def process(self, end_date):
        failed_tasks = []
        try:
            #一次load
            self.init(end_date=end_date)
            result_ret = self._update_ret()
            self._data_helper._upload_derived(result_ret, IndexReturn.__table__.name)

        except Exception as e:
            print(e)
            traceback.print_exc()
            failed_tasks.append('index_return')

        try:
            result_vol = self._update_vol()
            self._data_helper._upload_derived(result_vol, IndexVolatility.__table__.name)
        except Exception as e:
            print(e)
            traceback.print_exc()
            failed_tasks.append('index_volatility')
        return failed_tasks


if __name__ == '__main__':
    from .derived_data_helper import DerivedDataHelper
    from ...api.basic import BasicDataApi

    trading_days = BasicDataApi().get_trading_day_list('20200713', '20200821')
    iip = IndexIndicatorProcessor(DerivedDataHelper())
    for date in trading_days.datetime:
        date = date.strftime('%Y%m%d')
        print(f'deal with {date}')
        if iip.process(date):
            break
