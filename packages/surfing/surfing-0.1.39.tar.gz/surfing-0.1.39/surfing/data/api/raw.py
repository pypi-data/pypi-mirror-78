from typing import List, Tuple, Union
import pandas as pd
from ..wrapper.mysql import RawDatabaseConnector
from ..view.raw_models import *
from sqlalchemy.sql import func


class RawDataApi:
    def get_raw_cm_index_price_df(self, start_date, end_date):
        with RawDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    CmIndexPrice
                ).filter(
                    CmIndexPrice.datetime >= start_date,
                    CmIndexPrice.datetime <= end_date
                )
                df = pd.read_sql(query.statement, query.session.bind)
                return df

            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {CmIndexPrice.__tablename__}')

    def get_cxindex_index_price_df(self, start_date, end_date):
        with RawDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    CxindexIndexPrice
                ).filter(
                    CxindexIndexPrice.datetime >= start_date,
                    CxindexIndexPrice.datetime <= end_date
                )
                df = pd.read_sql(query.statement, query.session.bind)
                return df

            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {CxindexIndexPrice.__tablename__}')

    def get_yahoo_index_price_df(self, start_date, end_date):
        with RawDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    YahooIndexPrice
                ).filter(
                    YahooIndexPrice.datetime >= start_date,
                    YahooIndexPrice.datetime <= end_date
                )
                df = pd.read_sql(query.statement, query.session.bind)
                return df

            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {YahooIndexPrice.__tablename__}')

    def get_rq_index_price_df(self, start_date, end_date):
        with RawDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    RqIndexPrice
                ).filter(
                    RqIndexPrice.datetime >= start_date,
                    RqIndexPrice.datetime <= end_date
                )
                df = pd.read_sql(query.statement, query.session.bind)
                return df

            except Exception as e:
                print('Failed to get data <err_msg> {}'.format(e))

    def get_wind_fund_info(self, funds: Tuple[str] = ()):
        with RawDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    WindFundInfo
                )
                if funds:
                    query = query.filter(
                        WindFundInfo.wind_id.in_(funds),
                    )
                df = pd.read_sql(query.statement, query.session.bind)
                return df

            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {WindFundInfo.__tablename__}')

    def get_fund_fee(self):
        with RawDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    FundFee
                )
                df = pd.read_sql(query.statement, query.session.bind)
                return df

            except Exception as e:
                print('Failed to get data <err_msg> {}'.format(e))

    def get_fund_rating(self):
        with RawDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    FundRating
                )
                df = pd.read_sql(query.statement, query.session.bind)
                return df

            except Exception as e:
                print('Failed to get data <err_msg> {}'.format(e))

    def get_stock_fin_fac(self, stock_id_list, start_date):
        with RawDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    RqStockFinFac
                ).filter(
                    RqStockFinFac.stock_id.in_(stock_id_list),
                    RqStockFinFac.datetime >= start_date,
                )
                df = pd.read_sql(query.statement, query.session.bind)
                return df

            except Exception as e:
                print('Failed to get data <err_msg> {}'.format(e))

    def get_rq_stock_valuation(self, stock_id_list, start_date):
        with RawDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    RqStockValuation.datetime,
                    RqStockValuation.stock_id,
                    RqStockValuation.pb_ratio_lf,
                    RqStockValuation.pe_ratio_ttm,
                    RqStockValuation.peg_ratio_ttm,
                    RqStockValuation.dividend_yield_ttm,
                ).filter(
                    RqStockValuation.stock_id.in_(stock_id_list),
                    RqStockValuation.datetime >= start_date,

                )
                df = pd.read_sql(query.statement, query.session.bind)
                return df

            except Exception as e:
                print('Failed to get data <err_msg> {}'.format(e))

    def get_rq_index_weight(self, index_id_list, start_date: str, end_date: str = ''):
        with RawDatabaseConnector().managed_session() as quant_session:
            try:
                query = quant_session.query(
                        RqIndexWeight.index_id,
                        RqIndexWeight.datetime,
                        RqIndexWeight.stock_list,
                        RqIndexWeight.weight_list,
                    ).filter(
                        RqIndexWeight.index_id.in_(index_id_list),
                        RqIndexWeight.datetime >= start_date,
                    )
                if end_date:
                    query = query.filter(
                        RqIndexWeight.datetime <= end_date,
                    )
                df = pd.read_sql(query.statement, query.session.bind)
                return df

            except Exception as e:
                print('Failed to get data <err_msg> {}'.format(e))

    def get_index_val_pct(self):
        with RawDatabaseConnector().managed_session() as quant_session:
            try:
                query = quant_session.query(
                        IndexValPct
                    )
                df = pd.read_sql(query.statement, query.session.bind)
                return df

            except Exception as e:
                print('Failed to get data <err_msg> {}'.format(e))

    def get_rq_fund_indicator(self, start_date, end_date):
        with RawDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    RqFundIndicator
                ).filter(
                    RqFundIndicator.datetime >= start_date,
                    RqFundIndicator.datetime <= end_date
                )
                df = pd.read_sql(query.statement, query.session.bind)
                return df
            except Exception as e:
                print('Failed to get data <err_msg> {}'.format(e))
                return None

    def get_rq_trading_day_list(self, start_date, end_date):
        with RawDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    TradingDayList
                ).filter(
                    TradingDayList.datetime >= start_date,
                    TradingDayList.datetime <= end_date
                )
                df = pd.read_sql(query.statement, query.session.bind)
                return df
            except Exception as e:
                print('Failed to get data <err_msg> {}'.format(e))
                return None

    def get_em_tradedates(self, start_date='', end_date=''):
        with RawDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    EmTradeDates
                )
                if start_date:
                    query = query.filter(
                        EmTradeDates.TRADEDATES >= start_date,
                    )
                if end_date:
                    query = query.filter(
                        EmTradeDates.TRADEDATES <= end_date,
                    )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {EmTradeDates.__tablename__}')
                return None

    def get_stock_info(self):
        with RawDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    StockInfo
                )
                df = pd.read_sql(query.statement, query.session.bind)
                return df
            except Exception as e:
                print('Failed to get data <err_msg> {}'.format(e))
                return None

    def get_rq_fund_nav(self, start_date, end_date):
        with RawDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    RqFundNav
                ).filter(
                    RqFundNav.datetime >= start_date,
                    RqFundNav.datetime <= end_date
                )
                df = pd.read_sql(query.statement, query.session.bind)
                return df
            except Exception as e:
                print('Failed to get data <err_msg> {}'.format(e))
                return None

    def get_em_fund_nav(self, start_date: str = '', end_date: str = '', fund_ids: Tuple[str] = (), columns: Tuple[str] = ()):
        with RawDatabaseConnector().managed_session() as db_session:
            try:
                if not columns:
                    query = db_session.query(
                        EmFundNav
                    )
                else:
                    query = db_session.query(
                        EmFundNav.CODES,
                        EmFundNav.DATES,
                    ).add_columns(*columns)
                if fund_ids:
                    query = query.filter(
                        EmFundNav.CODES.in_(fund_ids),
                    )
                if start_date:
                    query = query.filter(
                        EmFundNav.DATES >= start_date,
                    )
                if end_date:
                    query = query.filter(
                        EmFundNav.DATES <= end_date,
                    )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {EmFundNav.__tablename__}')
                return None

    def delete_em_fund_nav(self, start_date, end_date):
        with RawDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    EmFundNav
                ).filter(
                    EmFundNav.DATES >= start_date,
                    EmFundNav.DATES <= end_date
                ).delete(synchronize_session=False)
                db_session.commit()
                return True
            except Exception as e:
                print(f'Failed to delete data <err_msg> {e} from {EmFundNav.__tablename__}')
                return None

    def get_rq_fund_size(self):
        with RawDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    RqFundSize
                )
                df = pd.read_sql(query.statement, query.session.bind)
                return df
            except Exception as e:
                print('Failed to get data <err_msg> {}'.format(e))
                return None

    def get_rq_stock_price(self, start_date, end_date):
        with RawDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    RqStockPrice
                ).filter(
                    RqStockPrice.datetime >= start_date,
                    RqStockPrice.datetime <= end_date
                )
                df = pd.read_sql(query.statement, query.session.bind)
                return df
            except Exception as e:
                print('Failed to get data <err_msg> {}'.format(e))
                return None

    def get_rq_stock_post_price(self, start_date, end_date):
        with RawDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    RqStockPostPrice
                ).filter(
                    RqStockPostPrice.datetime >= start_date,
                    RqStockPostPrice.datetime <= end_date
                )
                df = pd.read_sql(query.statement, query.session.bind)
                return df
            except Exception as e:
                print('Failed to get data <err_msg> {}'.format(e))
                return None

    def get_rq_stock_minute(self, dt=None):
        with RawDatabaseConnector().managed_session() as db_session:
            try:
                if not dt:
                    dt = db_session.query(
                        func.max(RqStockMinute.datetime)
                    ).one_or_none()
                if dt:
                    dt = dt[0]
                query = db_session.query(
                    RqStockMinute
                ).filter(
                    RqStockMinute.datetime == dt
                )
                df = pd.read_sql(query.statement, query.session.bind)
                return df
            except Exception as e:
                print('Failed to get data <err_msg> {}'.format(e))
                return None

    def get_em_index_price(self, start_date, end_date, index_id_list: Tuple = ()):
        with RawDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    EmIndexPrice
                )
                if index_id_list:
                    query = query.filter(
                        EmIndexPrice.em_id.in_(index_id_list),
                    )
                query = query.filter(
                    EmIndexPrice.datetime >= start_date,
                    EmIndexPrice.datetime <= end_date,
                )
                df = pd.read_sql(query.statement, query.session.bind)
                return df
            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {EmIndexPrice.__tablename__}')
                return None

    def delete_em_index_price(self, index_id_list, start_date, end_date):
        with RawDatabaseConnector().managed_session() as db_session:
            try:
                db_session.query(
                    EmIndexPrice
                ).filter(
                    EmIndexPrice.em_id.in_(index_id_list),
                    EmIndexPrice.datetime >= start_date,
                    EmIndexPrice.datetime <= end_date,
                ).delete(synchronize_session=False)
                db_session.commit()
                return True
            except Exception as e:
                print(f'Failed to delete data <err_msg> {e} from {EmIndexPrice.__tablename__}')
                return None

    def get_em_index_val(self, start_date, end_date, index_id_list: Tuple[str] = ()):
        with RawDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    EmIndexVal
                )
                if index_id_list:
                    query = query.filter(
                        EmIndexVal.CODES.in_(index_id_list),
                    )
                query = query.filter(
                    EmIndexVal.DATES >= start_date,
                    EmIndexVal.DATES <= end_date,
                )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {EmIndexVal.__tablename__}')
                return None

    def get_em_fund_scale(self, start_date: str = '', end_date: str = ''):
        with RawDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    EmFundScale.CODES,
                    EmFundScale.DATES,
                    EmFundScale.FUNDSCALE,
                )
                if start_date:
                    query = query.filter(
                        EmFundScale.DATES >= start_date,
                    )
                if end_date:
                    query = query.filter(
                        EmFundScale.DATES <= end_date,
                    )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'Failed to get scale data <err_msg> {e} from {EmFundScale.__tablename__}')
                return None

    def get_em_fund_status(self, end_date: str = ''):
        with RawDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    EmFundScale
                )
                if end_date:
                    query = query.filter(
                        EmFundScale.DATES <= end_date,
                    )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {EmFundScale.__tablename__}')
                return None

    def get_em_stock_price(self, start_date: str, end_date: str, stock_list: Tuple[str] = (), columns: Tuple[str] = ()):
        with RawDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    EmStockPrice.CODES,
                    EmStockPrice.DATES,
                )
                if columns:
                    query = query.add_columns(*columns)
                if stock_list:
                    query = query.filter(
                        EmStockPrice.CODES.in_(stock_list)
                    )
                query = query.filter(
                    EmStockPrice.DATES >= start_date,
                    EmStockPrice.DATES <= end_date,
                )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {EmStockPrice.__tablename__}')
                return None

    def get_em_stock_post_price(self, start_date: str, end_date: str, stock_list: Tuple[str] = (), columns: Tuple[str] = ()):
        with RawDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    EmStockPostPrice.CODES,
                    EmStockPostPrice.DATES,
                )
                if columns:
                    query = query.add_columns(*columns)
                if stock_list:
                    query = query.filter(
                        EmStockPostPrice.CODES.in_(stock_list)
                    )
                query = query.filter(
                    EmStockPostPrice.DATES >= start_date,
                    EmStockPostPrice.DATES <= end_date,
                )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {EmStockPostPrice.__tablename__}')
                return None

    def get_em_stock_info(self, stock_list: Tuple[str] = ()):
        with RawDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    EmStockInfo
                )
                if stock_list:
                    query = query.filter(
                        EmStockInfo.CODES.in_(stock_list)
                    )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {EmStockInfo.__tablename__}')
                return None

    def get_em_daily_info(self, start_date: str, end_date: str, stock_list: Tuple[str] = (), columns: Tuple[str] = ()):
        with RawDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    EmStockDailyInfo.CODES,
                    EmStockDailyInfo.DATES,
                )
                if columns:
                    query = query.add_columns(*columns)
                if stock_list:
                    query = query.filter(
                        EmStockDailyInfo.CODES.in_(stock_list)
                    )
                query = query.filter(
                    EmStockDailyInfo.DATES >= start_date,
                    EmStockDailyInfo.DATES <= end_date,
                )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {EmStockDailyInfo.__tablename__}')
                return None

    def get_em_stock_fin_fac(self, *, stock_list: Tuple[str] = (), date_list: Tuple[str] = (), start_date: str = '', end_date: str = ''):
        with RawDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    EmStockFinFac
                )
                if stock_list:
                    query = query.filter(
                        EmStockFinFac.CODES.in_(stock_list)
                    )
                if date_list:
                    query = query.filter(
                        EmStockFinFac.DATES.in_(date_list)
                    )
                else:
                    if start_date:
                        query = query.filter(
                            EmStockFinFac.DATES >= start_date,
                        )
                    if end_date:
                        query = query.filter(
                            EmStockFinFac.DATES <= end_date,
                        )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {EmStockFinFac.__tablename__}')
                return None

    def get_em_stock_estimate_fac(self, predict_year: int, start_date: str = '', end_date: str = ''):
        with RawDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    EmStockEstimateFac
                )
                if start_date:
                    query = query.filter(
                        EmStockEstimateFac.DATES >= start_date,
                    )
                if end_date:
                    query = query.filter(
                        EmStockEstimateFac.DATES <= end_date,
                    )
                query = query.filter(
                    EmStockEstimateFac.predict_year == predict_year,
                )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {EmStockEstimateFac.__tablename__}')
                return None

    def get_em_index_info(self, index_list: Union[Tuple[str], List[str]] = ()):
        with RawDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    EmIndexInfo
                )
                if index_list:
                    query = query.filter(
                        EmIndexInfo.CODES.in_(index_list)
                    )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {EmIndexInfo.__tablename__}')
                return None

    def get_em_index_component(self, start_date: str, end_date: str, index_list: Tuple[str] = ()):
        with RawDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    EmIndexComponent
                )
                if index_list:
                    query = query.filter(
                        EmIndexComponent.index_id.in_(index_list)
                    )
                query = query.filter(
                    EmIndexComponent.datetime >= start_date,
                    EmIndexComponent.datetime <= end_date,
                )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {EmIndexComponent.__tablename__}')
                return None

    def get_cs_index_component(self, index_list: Tuple[str] = ()):
        with RawDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    CSIndexComponent
                )
                if index_list:
                    query = query.filter(
                        CSIndexComponent.index_id.in_(index_list)
                    )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {CSIndexComponent.__tablename__}')
                return None

    def get_em_fund_holding_rate(self, start_date: str):
        with RawDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    EmFundHoldingRate
                ).filter(
                    EmFundHoldingRate.DATES >= start_date,
                )
                df = pd.read_sql(query.statement, query.session.bind)
                return df
            except Exception as e:
                print('Failed to get data <err_msg> {}'.format(e))
                return None

    def get_em_fund_list(self, date: str, limit = -1):
        with RawDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    EmFundList.datetime,
                    EmFundList.all_live_fund_list,
                    EmFundList.delisted_fund_list,
                ).filter(
                    EmFundList.datetime <= date,
                )
                if limit != -1:
                    query = query.order_by(EmFundList.datetime.desc()).limit(limit)
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {EmFundList.__tablename__}')
                return None

    def delete_em_fund_info(self, funds: List[str]):
        with RawDatabaseConnector().managed_session() as db_session:
            query = db_session.query(
                EmFundInfo
            ).filter(
                EmFundInfo.CODES.in_(funds),
            ).delete(synchronize_session=False)
            db_session.commit()

    def get_em_fund_info(self, funds: List[str] = []):
        with RawDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    EmFundInfo
                )
                if funds:
                    query = query.filter(
                        EmFundInfo.CODES.in_(funds),
                    )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {EmFundInfo.__tablename__}')
                return None

    def delete_em_fund_fee(self, funds: List[str]):
        with RawDatabaseConnector().managed_session() as db_session:
            query = db_session.query(
                EmFundFee
            ).filter(
                EmFundFee.CODES.in_(funds),
            ).delete(synchronize_session=False)
            db_session.commit()

    def get_em_fund_fee(self, funds: List[str]):
        with RawDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    EmFundFee
                ).filter(
                    EmFundFee.CODES.in_(funds),
                )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {EmFundFee.__tablename__}')
                return None

    def get_em_fund_benchmark(self, end_date: str):
        with RawDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    EmFundBenchmark
                ).filter(
                    EmFundBenchmark.DATES <= end_date,
                )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {EmFundBenchmark.__tablename__}')
                return None

    def get_wind_holder_structure(self, start_date: str, wind_fund_list:list):
        with RawDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    WindFundHolderStructure
                ).filter(
                    WindFundHolderStructure.END_DT >= start_date,
                    WindFundHolderStructure.S_INFO_WINDCODE.in_(wind_fund_list),
                )
                df = pd.read_sql(query.statement, query.session.bind)
                return df
            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {WindFundHolderStructure.__tablename__}')
                return None

    def get_wind_fund_stock_portfolio(self, start_date: str, end_date: str, wind_fund_list: List[str]):
        with RawDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    WindFundStockPortfolio
                ).filter(
                    WindFundStockPortfolio.F_PRT_ENDDATE >= start_date,
                    WindFundStockPortfolio.F_PRT_ENDDATE <= end_date,
                    WindFundStockPortfolio.S_INFO_WINDCODE.in_(wind_fund_list),
                )
                df = pd.read_sql(query.statement, query.session.bind)
                return df
            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {WindFundStockPortfolio.__tablename__}')
                return None

    def get_wind_fund_bond_portfolio(self, start_date: str, end_date: str, wind_fund_list: Tuple[str] = ()):
        with RawDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    WindFundBondPortfolio
                ).filter(
                    WindFundBondPortfolio.F_PRT_ENDDATE >= start_date,
                    WindFundBondPortfolio.F_PRT_ENDDATE <= end_date,
                )
                if wind_fund_list:
                    query = query.filter(
                        WindFundBondPortfolio.S_INFO_WINDCODE.in_(wind_fund_list),
                    )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {WindFundBondPortfolio.__tablename__}')

    def get_wind_fund_nav(self, start_date: str, wind_fund_list:list):
        with RawDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    WindFundNav
                ).filter(
                    WindFundNav.PRICE_DATE >= start_date,
                    WindFundNav.F_INFO_WINDCODE.in_(wind_fund_list),
                )
                df = pd.read_sql(query.statement, query.session.bind)
                return df
            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {WindFundNav.__tablename__}')
                return None

    def get_wind_manager_info(self, wind_fund_list: List[str] = '', columns: Tuple[str] = ()):
        with RawDatabaseConnector().managed_session() as db_session:
            try:
                if not columns:
                    query = db_session.query(
                        WindFundManager
                    )
                else:
                    query = db_session.query(
                        WindFundManager.F_INFO_FUNDMANAGER_ID,
                        WindFundManager.F_INFO_WINDCODE,
                    ).add_columns(*columns)
                if wind_fund_list:
                    query = query.filter(
                        WindFundManager.F_INFO_WINDCODE.in_(wind_fund_list),
                    )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {WindFundManager.__tablename__}')
                return None

    def get_wind_indus_portfolio(self, start_date: str, wind_fund_list:list):
        with RawDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    WindIndPortfolio
                ).filter(
                    WindIndPortfolio.F_PRT_ENDDATE >= start_date,
                    WindIndPortfolio.S_INFO_WINDCODE.in_(wind_fund_list),
                )
                df = pd.read_sql(query.statement, query.session.bind)
                return df
            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {WindIndPortfolio.__tablename__}')
                return None

    def get_em_fund_rate(self, datetime: str):
        with RawDatabaseConnector().managed_session() as raw_session:
            try:
                query = raw_session.query(
                    EMFundRate
                ).filter(
                    EMFundRate.DATES == datetime,
                )
                df = pd.read_sql(query.statement, query.session.bind)
                return df
            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {EMFundRate.__tablename__}')
                return None

    def get_em_fund_hold_asset(self, start_date: str = '', end_date: str = '', fund_ids: Tuple[str] = ()):
        with RawDatabaseConnector().managed_session() as raw_session:
            try:
                query = raw_session.query(EMFundHoldAsset)
                if fund_ids:
                    query = query.filter(
                        EMFundHoldAsset.CODES.in_(fund_ids),
                    )
                if start_date:
                    query = query.filter(
                        EMFundHoldAsset.DATES >= start_date,
                    )
                if end_date:
                    query = query.filter(
                        EMFundHoldAsset.DATES <= end_date,
                    )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {EMFundHoldAsset.__tablename__}')
                return None

    def get_em_fund_hold_industry(self, end_date: str = '', fund_ids: Tuple[str] = ()):
        with RawDatabaseConnector().managed_session() as raw_session:
            try:
                query = raw_session.query(EMFundHoldIndustry)
                if fund_ids:
                    query = query.filter(
                        EMFundHoldIndustry.CODES.in_(fund_ids),
                    )
                if end_date:
                    query = query.filter(
                        EMFundHoldIndustry.DATES <= end_date,
                    )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {EMFundHoldIndustry.__tablename__}')
                return None

    def get_em_fund_hold_stock(self, end_date: str = '', fund_ids: Tuple[str] = ()):
        with RawDatabaseConnector().managed_session() as raw_session:
            try:
                query = raw_session.query(EMFundHoldStock)
                if fund_ids:
                    query = query.filter(
                        EMFundHoldStock.CODES.in_(fund_ids),
                    )
                if end_date:
                    query = query.filter(
                        EMFundHoldStock.DATES <= end_date
                    )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {EMFundHoldStock.__tablename__}')
                return None

    def get_em_fund_hold_bond(self, end_date: str = '', fund_ids: Tuple[str] = ()):
        with RawDatabaseConnector().managed_session() as raw_session:
            try:
                query = raw_session.query(EMFundHoldBond)
                if fund_ids:
                    query = query.filter(
                        EMFundHoldBond.CODES.in_(fund_ids),
                    )
                if end_date:
                    query = query.filter(
                        EMFundHoldBond.DATES <= end_date
                    )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print('Failed to get data <err_msg> {}'.format(e))
                return None

    def get_em_mng_info(self, fund_ids: Tuple[str] = ()):
        with RawDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    EMMngInfo
                )
                if fund_ids:
                    query = query.filter(
                        EMMngInfo.code.in_(fund_ids),
                    )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print('Failed to get data <err_msg> {}'.format(e))

    def get_em_fund_mng_change(self, fund_ids: Tuple[str] = ()):
        with RawDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    EMFundMngChange
                )
                if fund_ids:
                    query = query.filter(
                        EMFundMngChange.code.in_(fund_ids),
                    )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print('Failed to get data <err_msg> {}'.format(e))

    def get_fund_com_mng_change(self):
        with RawDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    EMFundCompMngChange
                )
                df = pd.read_sql(query.statement, query.session.bind)
                return df

            except Exception as e:
                print('Failed to get data <err_msg> {}'.format(e))

    def get_em_fund_com_core_mng(self, fund_ids: Tuple[str] = ()):
        with RawDatabaseConnector().managed_session() as db_session:
            try:
                query = db_session.query(
                    EMFundCompCoreMng
                )
                if fund_ids:
                    query = query.filter(
                        EMFundCompCoreMng.code.in_(fund_ids),
                    )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print('Failed to get data <err_msg> {}'.format(e))

    def get_em_stock_dividend(self, end_date: str = ''):
        with RawDatabaseConnector().managed_session() as raw_session:
            try:
                query = raw_session.query(EmStockDividend)
                if end_date:
                    query = query.filter(
                        EmStockDividend.DATES <= end_date
                    )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {EmStockDividend.__tablename__}')

    def get_em_bond_info(self):
        with RawDatabaseConnector().managed_session() as raw_session:
            try:
                query = raw_session.query(EmBondInfo)
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {EmBondInfo.__tablename__}')

    def get_em_bond_rating(self, end_date: str = ''):
        with RawDatabaseConnector().managed_session() as raw_session:
            try:
                query = raw_session.query(EmBondRating)
                if end_date:
                    query = query.filter(
                        EmBondRating.DATES <= end_date
                    )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {EmBondRating.__tablename__}')
