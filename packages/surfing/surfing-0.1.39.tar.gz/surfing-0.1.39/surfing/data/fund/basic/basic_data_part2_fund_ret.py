import pandas as pd
import numpy as np
import datetime
import traceback
from ...api.raw import RawDataApi
from ...api.basic import BasicDataApi
from .basic_data_part1 import BasicDataPart1
from ...view.basic_models import *
from ...wrapper.mysql import BasicDatabaseConnector
from .basic_data_helper import BasicDataHelper

class BasicFundRet(BasicDataPart1):
    # inport end date , none std,
    W_1 = 5
    M_1 = 20
    M_3 = 60
    M_6 = 121
    Y_1 = 242
    Y_3 = Y_1 * 3
    Y_5 = Y_1 * 5
    SMALL_NUMBER = 1e-8
    RISK_FEE_RATE = 0.025

    def __init__(self, data_helper: BasicDataHelper):
        self._data_helper = data_helper
        self.raw_api = RawDataApi()
        self.basic_api = BasicDataApi()
        BasicDataPart1.__init__(self, self._data_helper)

    def init(self, start_date, end_date):
        with BasicDatabaseConnector().managed_session() as quant_session:
            query = quant_session.query(TradingDayList)
            trading_days = pd.read_sql(query.statement, query.session.bind).drop(columns='_update_time')

        self.start_date = start_date if isinstance(start_date, datetime.date) else datetime.datetime.strptime(start_date,'%Y%m%d').date()
        self.end_date = end_date if isinstance(end_date, datetime.date) else datetime.datetime.strptime(end_date,'%Y%m%d').date()
        dts = trading_days.datetime
        dts = dts[(dts >= self.start_date) & (dts <= self.end_date)]
        self.fund_list = self._fund_info_df.fund_id.tolist()
        self.fund_nav = self.basic_api.get_fund_nav_with_date(self.start_date, self.end_date, self.fund_list)
        # 直接使用basic的最新fund scale
        self.fund_scale = self.basic_api.get_fund_size()
        self.index_list = list(set(self._fund_info_df.index_id))
        self._fund_to_enddate_dict = self._fund_info_df[['fund_id', 'end_date']].set_index('fund_id').to_dict()['end_date']
        self.fund_nav = self.fund_nav.pivot_table(index='datetime', columns='fund_id', values='adjusted_net_value').reindex(dts).fillna(method='ffill')
        self.fund_nav_fill = self.fund_nav.fillna(method='bfill').copy()
        # 超过基金终止日的基金净值赋空
        for fund_id in self.fund_nav.columns:
            fund_end_date = self._fund_to_enddate_dict[fund_id]
            if self.end_date > fund_end_date:
                self.fund_nav.loc[fund_end_date:,fund_id] = np.nan
        self.fund_scale['datetime'] = self.fund_nav.index.array[-1]
        self.fund_scale = self.fund_scale.pivot_table(index='datetime', columns='fund_id', values='latest_size').iloc[0, :]
        # 基金天数
        _get_days = lambda x : pd.Series(x).count()
        self.days = self.fund_nav.count() - 1
        self.begin_day_of_year = datetime.date(self.end_date.year,1,1)
        self.begin_day_of_year = self.fund_nav.index[self.fund_nav.index > self.begin_day_of_year][0]

    def get_annual_ret(self):
        '''
        累计年化收益
        exp(log(p[-1] / p[0]) / (trade_days / 242)) - 1
        '''
        self.log_total_ret = np.log(self.total_ret)
        ret_yearly = self.days / self.Y_1
        return np.exp(self.log_total_ret / ret_yearly) - 1

    def get_annual_vol(self):
        '''
        累计年化波动率
        (p.shift(1) / p).std(ddof=1) * np.sqrt((days - 1) / year)
        '''
        diff = self.fund_nav.shift(1) / self.fund_nav
        std = diff.std(ddof=1)
        std_yearly = np.sqrt((self.days - 1) / (self.days / self.Y_1))
        return std * std_yearly

    def get_mdd(self):
        '''
        累计最大回撤
        1 - (p / p.cummax()).min()
        '''
        return 1 - (self.fund_nav / self.fund_nav.cummax()).min()

    def calculate_one_date(self):
        self.w1_ret = self.fund_nav_fill.tail(self.W_1+1).pct_change(self.W_1).tail(1).T.rename(columns={self.fund_nav.index[-1]:'w1_ret'})
        self.m1_ret = self.fund_nav_fill.tail(self.M_1+1).pct_change(self.M_1).tail(1).T.rename(columns={self.fund_nav.index[-1]:'m1_ret'})
        self.m3_ret = self.fund_nav_fill.tail(self.M_3+1).pct_change(self.M_3).tail(1).T.rename(columns={self.fund_nav.index[-1]:'m3_ret'})
        self.m6_ret = self.fund_nav_fill.tail(self.M_6+1).pct_change(self.M_6).tail(1).T.rename(columns={self.fund_nav.index[-1]:'m6_ret'})
        self.y1_ret = self.fund_nav_fill.tail(self.Y_1+1).pct_change(self.Y_1).tail(1).T.rename(columns={self.fund_nav.index[-1]:'y1_ret'})
        self.y3_ret = self.fund_nav_fill.tail(self.Y_3+1).pct_change(self.Y_3).tail(1).T.rename(columns={self.fund_nav.index[-1]:'y3_ret'})
        self.y5_ret = self.fund_nav_fill.tail(self.Y_5+1).pct_change(self.Y_5).tail(1).T.rename(columns={self.fund_nav.index[-1]:'y5_ret'})

        self.total_ret = self.fund_nav_fill.iloc[-1] / self.fund_nav_fill.iloc[0]
        self.to_date_ret = self.total_ret - 1
        self.annual_ret = self.get_annual_ret()
        self.annual_vol = self.get_annual_vol()
        self.vol = self.fund_nav.pct_change(1).std(ddof=1)
        self.sharpe_ratio = (self.annual_ret  - self.RISK_FEE_RATE) / self.annual_vol
        self.mdd = self.get_mdd()
        self.recent_y_ret = self.fund_nav_fill.iloc[-1] / self.fund_nav_fill.loc[self.begin_day_of_year:].fillna(method = 'bfill').iloc[0] - 1

        data_list = [self.w1_ret, self.m1_ret, self.m3_ret, self.m6_ret, self.y1_ret, self.y3_ret, self.y5_ret, self.to_date_ret, self.fund_scale, self.annual_ret, self.sharpe_ratio, self.mdd, self.recent_y_ret, self.vol]
        fac_list = ['w1_ret', 'm1_ret', 'm3_ret', 'm6_ret', 'y1_ret', 'y3_ret', 'y5_ret', 'to_date_ret', 'avg_size', 'annual_ret', 'sharpe_ratio', 'mdd', 'recent_y_ret', 'vol']
        self.res = []
        for name, data in zip(fac_list, data_list):
            df = pd.DataFrame(data).rename(columns = {0:name,self.fund_nav.index[-1]:'avg_size'})
            self.res.append(df)
        self.result = pd.concat(self.res, axis=1, sort=True).reset_index().rename(columns={'index':'fund_id'})
        self.result['datetime'] = self.fund_nav.index[-1]
        self.result['info_ratio'] = None  # TODO
        self.result = self.result.replace({np.inf: None, -np.inf: None})
        self.result = self.result[self.result.drop(columns=['fund_id', 'datetime']).notna().any(axis=1)]

    def process_all(self, end_date):
        failed_tasks = []
        try:
            default_begin_date = '20050101'#算累计指标用较久对起始日
            self.init(default_begin_date, end_date)
            self.calculate_one_date()
            self._data_helper._upload_basic(self.result, FundRet.__table__.name)
        except Exception as e:
            print(e)
            traceback.print_exc()
            failed_tasks.append('fund_score')

        return failed_tasks
