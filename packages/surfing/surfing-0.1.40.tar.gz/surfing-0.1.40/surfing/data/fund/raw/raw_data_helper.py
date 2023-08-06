
import time
from typing import Tuple, Set

from collections import defaultdict
from ...wrapper.mysql import RawDatabaseConnector


class RawDataHelper(object):
    def __init__(self):
        self._updated_count = defaultdict(int)
        self._timer: float = time.monotonic()

    def _upload_raw(self, df, table_name, to_truncate=False):
        print(table_name)
        # print(df)
        if to_truncate:
            with RawDatabaseConnector().managed_session() as mn_session:
                try:
                    mn_session.execute(f'TRUNCATE TABLE {table_name}')
                    mn_session.commit()
                except Exception as e:
                    print(f'Failed to truncate table {table_name} <err_msg> {e}')

        df = df.drop(columns='_update_time', errors='ignore')
        df.to_sql(table_name, RawDatabaseConnector().get_engine(), index=False, if_exists='append')

        now: float = time.monotonic()
        print(f'{table_name} costs {now - self._timer}s')
        self._timer = now
        self._updated_count[table_name] += df.shape[0]

    @staticmethod
    def get_new_and_delisted_fund_list(date: str) -> Tuple[Set[str], Set[str]]:
        import pandas as pd
        from ...api.raw import RawDataApi

        fund_list = RawDataApi().get_em_fund_list(date, limit=2)
        if fund_list.shape[0] < 2:
            print(f"Failed to get two days' fund list, (date){date} (len){fund_list.shape[0]}")
            return (None, None)

        lastest_list: pd.Series = fund_list.iloc[0, :]
        last_list: pd.Series = fund_list.iloc[1, :]
        print(f"got two days' fund list, (latest){lastest_list.datetime} (prev){last_list.datetime}")
        return (set(lastest_list.all_live_fund_list.split(',')).difference(set(last_list.all_live_fund_list.split(','))),
                set(lastest_list.delisted_fund_list.split(',')).difference(set(last_list.delisted_fund_list.split(','))))
