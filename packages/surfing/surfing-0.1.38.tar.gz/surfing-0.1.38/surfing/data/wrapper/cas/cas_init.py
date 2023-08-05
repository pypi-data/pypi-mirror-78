from .cas_connection import CassandraConnector
from ...view.cas.fund_estimated_nav import FundEstimatedNav
from ...view.cas.realtime_index_price import RealtimeIndexPrice
from ...view.cas.realtime_index_price_snapshot import RealtimeIndexPriceSnapshot
from cassandra.cqlengine.management import sync_table, drop_table

CassandraConnector().get_conn()

def sync_cas_table():
    sync_table(FundEstimatedNav)
    sync_table(RealtimeIndexPrice)
    sync_table(RealtimeIndexPriceSnapshot)

def drop_cas_table():
    drop_table(FundEstimatedNav)
    drop_table(RealtimeIndexPrice)
    drop_table(RealtimeIndexPriceSnapshot)


if __name__ == '__main__':
    sync_cas_table()
    # drop_cas_table()
