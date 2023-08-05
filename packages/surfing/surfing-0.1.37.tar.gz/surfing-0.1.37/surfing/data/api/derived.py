
from typing import Tuple

import math
import pandas as pd
import pickle as pkl
from ..wrapper.mysql import DerivedDatabaseConnector
from ..view.derived_models import *


class DerivedDataApi(object):
    def get_fund_indicator(self, fund_list):
        with DerivedDatabaseConnector().managed_session() as quant_session:
            try:
                query = quant_session.query(
                        FundIndicator.fund_id,
                        FundIndicator.datetime,
                        FundIndicator.alpha,
                        FundIndicator.beta,
                        FundIndicator.fee_rate,
                        FundIndicator.track_err,
                    ).filter(
                        FundIndicator.fund_id.in_(fund_list),
                    )
                tag_df = pd.read_sql(query.statement, query.session.bind)
                return tag_df

            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {FundIndicator.__tablename__}')

    def get_fund_indicator_by_date(self, fund_list, date):
        with DerivedDatabaseConnector().managed_session() as quant_session:
            try:
                query = quant_session.query(
                    FundIndicator
                ).filter(
                    FundIndicator.datetime == date,
                    FundIndicator.fund_id.in_(fund_list),
                )
                tag_df = pd.read_sql(query.statement, query.session.bind)
                return tag_df

            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {FundIndicator.__tablename__}')

    def get_fund_indicator_monthly(self, start_date, end_date, fund_list, columns: Tuple[str] = ()):
        with DerivedDatabaseConnector().managed_session() as quant_session:
            try:
                query = quant_session.query(
                    FundIndicatorMonthly.fund_id,
                    FundIndicatorMonthly.datetime,
                )
                if columns:
                    query = query.add_columns(*columns)
                query = query.filter(
                    FundIndicatorMonthly.fund_id.in_(fund_list),
                    FundIndicatorMonthly.datetime >= start_date,
                    FundIndicatorMonthly.datetime <= end_date
                )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {FundIndicatorMonthly.__tablename__}')

    def get_fund_indicator_group(self, start_date: str, end_date: str):
        with DerivedDatabaseConnector().managed_session() as quant_session:
            try:
                query = quant_session.query(
                    FundIndicatorGroup
                )
                query = query.filter(
                    FundIndicatorGroup.datetime >= start_date,
                    FundIndicatorGroup.datetime <= end_date
                )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {FundIndicatorGroup.__tablename__}')

    def get_fund_score(self):
        with DerivedDatabaseConnector().managed_session() as quant_session:
            try:
                query = quant_session.query(
                        FundScore,
                    )
                tag_df = pd.read_sql(query.statement, query.session.bind)
                return tag_df

            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {FundScore.__tablename__}')

    def get_fund_score_extended_by_id(self, fund_id):
        with DerivedDatabaseConnector().managed_session() as quant_session:
            try:
                query = quant_session.query(
                    FundScoreExtended,
                ).filter(
                    FundScoreExtended.fund_id == fund_id,
                )

                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {FundScoreExtended.__tablename__}')
                return pd.DataFrame([])

    def get_fund_score_extended(self, start_date: str, end_date: str, fund_list: Tuple[str] = (), columns: Tuple[str] = ()):
        with DerivedDatabaseConnector().managed_session() as quant_session:
            try:
                if columns:
                    query = quant_session.query(
                        FundScoreExtended.fund_id,
                        FundScoreExtended.datetime,
                    )
                    query = query.add_columns(*columns)
                else:
                    query = quant_session.query(
                        FundScoreExtended,
                    )
                if fund_list:
                    query = query.filter(
                        FundScoreExtended.fund_id.in_(fund_list)
                    )
                query = query.filter(
                    FundScoreExtended.datetime >= start_date,
                    FundScoreExtended.datetime <= end_date,
                )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {FundScoreExtended.__tablename__}')

    def get_fund_score_extended_for_ranks(self, start_date: str, end_date: str, fund_list: Tuple[str] = ()):
        return self.get_fund_score_extended(start_date, end_date, fund_list=fund_list, columns=['wind_class_1', 'return_score', 'robust_score', 'timing_score', 'return_rank', 'robust_rank', 'timing_rank'])

    def get_index_valuation_develop(self, index_ids, start_date, end_date):
        with DerivedDatabaseConnector().managed_session() as mn_session:
            try:
                query = mn_session.query(
                    IndexValuationLongTerm
                ).filter(
                    IndexValuationLongTerm.index_id.in_(index_ids),
                    IndexValuationLongTerm.datetime >= start_date,
                    IndexValuationLongTerm.datetime <= end_date,
                ).order_by(IndexValuationLongTerm.datetime.asc())
                df = pd.read_sql(query.statement, query.session.bind)
                return df
            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {IndexValuationLongTerm.__tablename__}')
                return pd.DataFrame([])

    def get_index_valuation_develop_without_date(self, index_ids):
        with DerivedDatabaseConnector().managed_session() as mn_session:
            try:
                query = mn_session.query(
                    IndexValuationLongTerm
                ).filter(
                    IndexValuationLongTerm.index_id.in_(index_ids),
                ).order_by(IndexValuationLongTerm.datetime.asc())
                df = pd.read_sql(query.statement, query.session.bind)
                return df
            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {IndexValuationLongTerm.__tablename__}')
                return pd.DataFrame([])

    def get_asset_allocation_info(self, version:int=2):
        with DerivedDatabaseConnector().managed_session() as mn_session:
            try:
                query = mn_session.query(
                    AssetAllocationInfo
                ).filter(
                    AssetAllocationInfo.version == version
                ).order_by(AssetAllocationInfo.allocation_id)
                df = pd.read_sql(query.statement, query.session.bind)
                return df
            except Exception as e:
                print(f'Failed to get data <err_msg> {e} from {AssetAllocationInfo.__tablename__}')
                return pd.DataFrame([])

    def get_style_factor_return(self, start_date: str, end_date: str, index_list: Tuple[str] = ()):
        with DerivedDatabaseConnector().managed_session() as session:
            try:
                query = session.query(
                    StyleAnalysisFactorReturn
                )
                if index_list:
                    query = query.filter(StyleAnalysisFactorReturn.universe_index.in_(index_list))
                query = query.filter(
                    StyleAnalysisFactorReturn.datetime >= start_date,
                    StyleAnalysisFactorReturn.datetime <= end_date,
                )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'Failed to get_style_factor_return {e} from {StyleAnalysisFactorReturn.__tablename__}')
                return

    def get_barra_cne5_factor_return(self, start_date: str, end_date: str):
        with DerivedDatabaseConnector().managed_session() as session:
            try:
                query = session.query(
                    BarraCNE5FactorReturn
                ).filter(
                    BarraCNE5FactorReturn.datetime >= start_date,
                    BarraCNE5FactorReturn.datetime <= end_date,
                )
                return pd.read_sql(query.statement, query.session.bind)
            except Exception as e:
                print(f'Failed to get_style_factor_return {e} from {StyleAnalysisFactorReturn.__tablename__}')
                return

    def get_allocation_distribution(self, version:str=1):
        with DerivedDatabaseConnector().managed_session() as session:
            try:
                query = session.query(
                    AllocationDistribution
                ).filter(
                    AllocationDistribution.version == version
                )
                df = pd.read_sql(query.statement, query.session.bind)
                return df
            except Exception as e:
                print(f'Failed to get_style_factor_return {e} from {AllocationDistribution.__tablename__}')
                return

