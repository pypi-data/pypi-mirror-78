
import time
from typing import Union

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler

from collections import defaultdict
from ...wrapper.mysql import DerivedDatabaseConnector


def normalize(a: Union[pd.DataFrame, pd.Series]) -> np.ndarray:
    return StandardScaler().fit_transform(a)


def score_rescale(a: pd.DataFrame) -> np.ndarray:
    return MinMaxScaler().fit_transform(a) * 100


class DerivedDataHelper:
    def __init__(self):
        self._updated_count = defaultdict(int)
        self._timer = time.monotonic()

    def _upload_derived(self, df, table_name):
        print(table_name)
        # print(df)
        df.to_sql(table_name, DerivedDatabaseConnector().get_engine(), index=False, if_exists='append')

        now: float = time.monotonic()
        print(f'{table_name} costs {now - self._timer}s')
        self._timer = now
        self._updated_count[table_name] += df.shape[0]
