import pandas as pd
import traceback
from sqlalchemy import distinct
from ...wrapper.mysql import DerivedDatabaseConnector, BasicDatabaseConnector, ViewDatabaseConnector
from ...view.view_models import IndexDailyCollection
from ...view.basic_models import IndexInfo, IndexPrice, IndexComponent
from ...view.derived_models import IndexValuationLongTerm, IndexReturn, IndexVolatility

class IndexDailyCollectionProcessor(object):
    def get_index_volatility(self):
        with DerivedDatabaseConnector().managed_session() as mn_session:
            try:
                latest_time = mn_session.query(IndexVolatility).order_by(IndexVolatility.datetime.desc()).limit(1).one_or_none()
                latest_time = latest_time.datetime
                print(latest_time)
                query = mn_session.query(
                    IndexVolatility.index_id,
                    IndexVolatility.datetime,
                    IndexVolatility.w1_vol,
                    IndexVolatility.m1_vol,
                    IndexVolatility.m3_vol,
                    IndexVolatility.m6_vol,
                    IndexVolatility.y1_vol,
                    IndexVolatility.y3_vol,
                    IndexVolatility.y5_vol,
                    IndexVolatility.y10_vol,
                    IndexVolatility.this_y_vol,
                    IndexVolatility.cumulative_vol,
                ).filter(IndexVolatility.datetime==latest_time)
                df = pd.read_sql(query.statement, query.session.bind)
                df = df.rename(columns={'datetime': 'vol_datetime'})
                df = df.set_index('index_id')
                return df
            except Exception as e:
                print('Failed get_index_volatility <err_msg> {}'.format(e))

    # TODO: Use basic.index_valuation_develop table
    def get_index_valuation(self):
        with DerivedDatabaseConnector().managed_session() as mn_session:
            try:
                latest_time = mn_session.query(IndexValuationLongTerm).order_by(IndexValuationLongTerm.datetime.desc()).limit(1).one_or_none()
                latest_time = latest_time.datetime
                print(latest_time)
                query = mn_session.query(
                    IndexValuationLongTerm.index_id,
                    IndexValuationLongTerm.pb_mrq,
                    IndexValuationLongTerm.pe_ttm,
                    IndexValuationLongTerm.peg_ttm,
                    IndexValuationLongTerm.roe,
                    IndexValuationLongTerm.dy,
                    IndexValuationLongTerm.pe_pct,
                    IndexValuationLongTerm.pb_pct,
                    IndexValuationLongTerm.ps_pct,
                    IndexValuationLongTerm.val_score,
                    IndexValuationLongTerm.datetime,
                    IndexValuationLongTerm.est_peg,
                ).filter(IndexValuationLongTerm.datetime==latest_time)
                df = pd.read_sql(query.statement, query.session.bind)
                df = df.set_index('index_id')
                return df

            except Exception as e:
                print('Failed get_index_valuation <err_msg> {}'.format(e))

    def get_index_return(self):
        with DerivedDatabaseConnector().managed_session() as mn_session:
            try:
                latest_time = mn_session.query(IndexReturn).order_by(IndexReturn.datetime.desc()).limit(1).one_or_none()
                latest_time = latest_time.datetime
                print(latest_time)
                query = mn_session.query(
                    IndexReturn.index_id,
                    IndexReturn.datetime,
                    IndexReturn.w1_ret,
                    IndexReturn.m1_ret,
                    IndexReturn.m3_ret,
                    IndexReturn.m6_ret,
                    IndexReturn.y1_ret,
                    IndexReturn.y3_ret,
                    IndexReturn.y5_ret,
                    IndexReturn.y10_ret,
                    IndexReturn.this_y_ret,
                    IndexReturn.cumulative_ret,
                ).filter(IndexReturn.datetime==latest_time)
                df = pd.read_sql(query.statement, query.session.bind)
                df = df.rename(columns={'datetime': 'ret_datetime'})
                df = df.set_index('index_id')
                return df

            except Exception as e:
                print('Failed get_index_return<err_msg> {}'.format(e))

    def get_index_info(self):
        with BasicDatabaseConnector().managed_session() as mn_session:
            try:
                query = mn_session.query(
                    IndexInfo.index_id,
                    IndexInfo.em_id,
                    IndexInfo.industry_tag,
                    IndexInfo.tag_method,
                    IndexInfo.desc_name,
                )
                df = pd.read_sql(query.statement, query.session.bind)
                df = df.set_index('index_id')
                return df

            except Exception as e:
                print('Failed get_index_info<err_msg> {}'.format(e))

    def get_index_component(self):
        with BasicDatabaseConnector().managed_session() as mn_session:
            try:
                query = mn_session.query(
                    IndexComponent.index_id,
                    IndexComponent.id_cat,
                )
                df = pd.read_sql(query.statement, query.session.bind)
                df['id_cat'] = df['id_cat'].apply(lambda x: x.name)
                df = df.set_index('index_id')
                return df

            except Exception as e:
                print('Failed get_index_info<err_msg> {}'.format(e))

    def get_index_price(self):
        with BasicDatabaseConnector().managed_session() as mn_session:
            try:
                latest_time = mn_session.query(IndexPrice).order_by(IndexPrice.datetime.desc()).limit(1).one_or_none()
                latest_time = latest_time.datetime
                print(latest_time)
                query = mn_session.query(
                    IndexPrice.index_id,
                    IndexPrice.datetime,
                    IndexPrice.volume,
                    IndexPrice.low,
                    IndexPrice.close,
                    IndexPrice.high,
                    IndexPrice.open,
                    IndexPrice.ret,
                    IndexPrice.total_turnover
                ).filter(IndexPrice.datetime==latest_time)
                df = pd.read_sql(query.statement, query.session.bind)
                df = df.rename(columns={'datetime': 'price_datetime'})
                df = df.set_index('index_id')
                return df

            except Exception as e:
                print('Failed get_index_price<err_msg> {}'.format(e))

    def get_index_yesterday_price(self):
        with BasicDatabaseConnector().managed_session() as mn_session:
            try:
                yest_time = mn_session.query(
                    distinct(IndexPrice.datetime)
                ).order_by(
                    IndexPrice.datetime.desc()
                ).offset(1).limit(1).one_or_none()
                yest_time = yest_time[0]
                print(yest_time)
                query = mn_session.query(
                    IndexPrice.index_id,
                    IndexPrice.close,
                ).filter(IndexPrice.datetime==yest_time)
                df = pd.read_sql(query.statement, query.session.bind)
                df = df.rename(columns={
                    'close': 'yest_close',
                })
                df = df.set_index('index_id')
                return df

            except Exception as e:
                print('Failed get_index_price<err_msg> {}'.format(e))

    def append_data(self, table_name, data_append_directly_data_df):
        if not data_append_directly_data_df.empty:
            with ViewDatabaseConnector().managed_session() as mn_session:
                try:
                    mn_session.execute(f'TRUNCATE TABLE {table_name}')
                    mn_session.commit()
                except Exception as e:
                    print(f'Failed to truncate table {table_name} <err_msg> {e}')
            data_append_directly_data_df.to_sql(table_name, ViewDatabaseConnector().get_engine(), index = False, if_exists = 'append')
            print('新数据已插入')
        else:
            print('没有需要插入的新数据')

    def collection_daily_index(self):
        try:
            print('1、 load data...')
            info = self.get_index_info()
            vol = self.get_index_volatility().reindex(info.index)
            ret = self.get_index_return().reindex(info.index)
            val = self.get_index_valuation().reindex(info.index)
            price = self.get_index_price().reindex(info.index)
            yest_price = self.get_index_yesterday_price().reindex(info.index)
            component = self.get_index_component().reindex(info.index)

            print('2、 concat data...')
            df = pd.concat([info, vol, ret, val, price, yest_price, component], axis=1, sort=False)
            df.index.name = 'index_id'
            df = df.reset_index()

            print('3、 special option...')

            df['order_book_id'] = df['em_id'].apply(lambda x: x.split('.')[0] if (x and x != 'not_available') else None)
            df = df.drop(['em_id'], axis=1)
            df['industry_tag'] = df['industry_tag'].apply(lambda x: x if x != 'not_available' else None)

            self.append_data(IndexDailyCollection.__tablename__, df)

            print(df)
            return True
        except Exception as e:
            print(e)
            traceback.print_exc()
            return False

    def process(self):
        failed_tasks = []
        if not self.collection_daily_index():
            failed_tasks.append('collection_daily_index')
        return failed_tasks


if __name__ == '__main__':
    IndexDailyCollectionProcessor().collection_daily_index()
