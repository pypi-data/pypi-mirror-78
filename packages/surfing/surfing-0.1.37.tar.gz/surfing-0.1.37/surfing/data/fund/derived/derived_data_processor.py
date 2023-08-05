
import datetime
from typing import List

import pandas as pd

from .fund_score_processor import FundScoreProcessor
from .fund_indicator_processor import FundIndicatorProcessor
# from .derived_index_val import IndexValProcess
from .derived_index_val_long_term import IndexValProcessLongTerm
from .style_analysis_processor import StyleAnalysisProcessor
from .derived_data_helper import DerivedDataHelper
from .fund_indicator_processor_weekly import FundIndicatorProcessorWeekly
from .fund_indicator_processor_monthly import FundIndicatorProcessorMonthly
from .derived_indicators_processor_group import FundIndicatorProcessorGroup
from .derived_index_ret_vol import IndexIndicatorProcessor
from .derived_fund_aic import AIPProcess
# from .derived_fund_score_extended import FundScoreExtendedProcess
from .derived_fund_score_group import FundScoreGroupProcess
from .barra_cne5_factor_processor import BarraCNE5FactorProcessor
from .style_reg_processer import StyleBoxReg
from ...api.basic import BasicDataApi


class DerivedDataProcessor:
    def __init__(self):
        self._data_helper = DerivedDataHelper()
        self.fund_indicator_processor = FundIndicatorProcessor(self._data_helper)
        self.fund_indicator_processor_weekly = FundIndicatorProcessorWeekly(self._data_helper)
        self.fund_indicator_processor_monthly = FundIndicatorProcessorMonthly(self._data_helper)
        self.fund_indicator_processor_group = FundIndicatorProcessorGroup(self._data_helper)
        self.fund_score_processor = FundScoreProcessor(self._data_helper)
        # self.index_val_processor = IndexValProcess(self._data_helper)
        self.index_val_processor_long_term = IndexValProcessLongTerm(self._data_helper)
        self.index_indicator = IndexIndicatorProcessor(self._data_helper)
        self.fund_aip = AIPProcess(self._data_helper)
        # 这版基金评分先不用了，这里先注释掉
        # self._derived_fund_score_extended = FundScoreExtendedProcess(self._data_helper)
        self._derived_fund_score_group = FundScoreGroupProcess(self._data_helper)
        self._barra_cne5_factor_processor = BarraCNE5FactorProcessor(self._data_helper)
        self._style_regression_processor = StyleBoxReg(self._data_helper)
        self.style_analysis_processors: List[StyleAnalysisProcessor] = []
        # 暂时只算这三个universe
        for universe in ('hs300', 'csi800', 'all'):
            sap = StyleAnalysisProcessor(self._data_helper, universe)
            self.style_analysis_processors.append(sap)

    def process_all(self, start_date, end_date):
        failed_tasks = []
        failed_tasks.extend(self.fund_indicator_processor.process(start_date, end_date))
        failed_tasks.extend(self.fund_score_processor.process(start_date, end_date))
        # failed_tasks.extend(self.index_val_processor.process(start_date, end_date))
        failed_tasks.extend(self.index_val_processor_long_term.process(start_date, end_date))
        failed_tasks.extend(self.index_indicator.process(end_date))
        failed_tasks.extend(self.fund_aip.process(start_date, end_date))
        failed_tasks.extend(self._barra_cne5_factor_processor.process(start_date, end_date))
        failed_tasks.extend(self._style_regression_processor.process(start_date, end_date))
        for sap in self.style_analysis_processors:
            failed_tasks.extend(sap.process(start_date, end_date))

        # 获取下一个交易日
        api = BasicDataApi()
        trading_day_df = api.get_trading_day_list(start_date=end_date)
        if trading_day_df.shape[0] <= 1:
            print(f'get trading days start with {end_date} failed')
            failed_tasks.append('get_trading_day for weekly/monthly indicator')
        else:
            next_trading_day = trading_day_df.iloc[1, :].datetime
            print(f'got next trading day {next_trading_day}')
            end_date_dt = pd.to_datetime(end_date, infer_datetime_format=True).date()
            next_trading_dt = pd.to_datetime(next_trading_day, infer_datetime_format=True).date()
            if end_date_dt.weekday() < next_trading_dt.weekday() and next_trading_dt < end_date_dt + datetime.timedelta(weeks=1):
                # 表明本周后边还有交易日，今天不需要更新
                print(f'weekly indicator only update on the last day of week, not today {end_date_dt}')
            else:
                failed_tasks.extend(self.fund_indicator_processor_weekly.process(start_date, end_date, end_date_dt))
                failed_tasks.extend(self.fund_indicator_processor_group.process(start_date, end_date, end_date_dt))
                # failed_tasks.extend(self._derived_fund_score_extended.process(start_date, end_date, end_date_dt))
                failed_tasks.extend(self._derived_fund_score_group.process(start_date, end_date, end_date_dt))

            if end_date_dt.year == next_trading_dt.year and end_date_dt.month == next_trading_dt.month:
                # 表明本月后边还有交易日，今天不需要更新
                print(f'monthly indicator only update on the last day of month, not today {end_date_dt}')
            else:
                failed_tasks.extend(self.fund_indicator_processor_monthly.process(start_date, end_date, end_date_dt))
        return failed_tasks

    def get_updated_count(self):
        return self._data_helper._updated_count


if __name__ == '__main__':
    ddp = DerivedDataProcessor()
    start_date = '20200820'
    end_date = '20200820'
    ddp.process_all(start_date, end_date)
    # ddp.fund_indicator_processor.process(start_date, end_date)
    # ddp.fund_score_processor.process(start_date, end_date)
    # import pandas as pd
    # date_list = pd.date_range(end='2010-05-31', periods=65, freq='M').sort_values(ascending=False).to_pydatetime()
    # for date in date_list:
    #     date = date.strftime('%Y%m%d')
    #     ddp.fund_indicator_processor_monthly.process(date, date)
