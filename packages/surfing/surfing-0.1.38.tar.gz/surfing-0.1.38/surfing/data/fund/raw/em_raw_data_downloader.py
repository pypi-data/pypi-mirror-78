#!/usr/bin/env python
# coding: utf-8

import numpy as np
import pandas as pd
import rqdatac as rq
import pickle as pkl
from typing import List, Set, Tuple, Dict
from operator import itemgetter
from collections import defaultdict
from .EMQuantAPI_Python.python3.EmQuantAPI import *
import datetime
import json
import os
import csv
import traceback
from sqlalchemy import distinct
from sqlalchemy.orm import sessionmaker
from ...wrapper.mysql import RawDatabaseConnector
from ...view.raw_models import *
from ...api.basic import BasicDataApi
from ...api.raw import RawDataApi
from .raw_data_helper import RawDataHelper
from ....constant import SectorType, IndexPriceSource, CodeFeeMode, INDEX_PRICE_EXTRA_TRADE_DAYS


class EmRawDataDownloader:

    _MACROECONOMIC_MAP = {
        'EMM00166216': 'RA0000.IR',
        'EMM00166217': 'RA0001.IR',
        'EMM00166218': 'RA0002.IR',
        'EMM00166219': 'RA0003.IR',
        'EMM00166220': 'RA0004.IR',
        'EMM00166221': 'RA0005.IR',
        'EMM00166222': 'RA0006.IR',
        'EMM00166228': 'RA0007.IR',
    }
    _MACROECONOMIC_MAP_I = {v: k for k, v in _MACROECONOMIC_MAP.items()}

    def __init__(self, data_helper):
        self._data_helper = data_helper
        # ForceLogin
        # 取值0，当线上已存在该账户时，不强制登录
        # 取值1，当线上已存在该账户时，强制登录，将前一位在线用户踢下线
        options = 'ForceLogin=1'
        loginResult = c.start(options, mainCallBack=self._main_callback)
        if(loginResult.ErrorCode != 0):
            print('EM login failed')
            exit()

        self._quarter_update_dates = ['0331', '0630', '0930', '1231']
        self._semi_update_dates = ['0630', '1231']

    def __del__(self):
        c.stop()

    def _main_callback(self, quantdata):
        '''
        mainCallback 是主回调函数，可捕捉连接错误
        该函数只有一个为c.EmQuantData类型的参数quantdata
        :param quantdata: c.EmQuantData
        '''
        print(f'MainCallback: {quantdata}')

    def _get_date_list(self, start_date, end_date):
        start_datetime = datetime.datetime.strptime(start_date, '%Y%m%d')
        end_datetime = datetime.datetime.strptime(end_date, '%Y%m%d')
        date_list = []
        while start_datetime <= end_datetime:
            date_list.append(start_datetime.strftime('%Y%m%d'))
            start_datetime += datetime.timedelta(days=1)
        return date_list

    def em_fund_nav_history(self, nav_file_dir):
        try:
            index = 1
            for filename in os.listdir(nav_file_dir):
                if filename.endswith(".xls"):
                    print(f'{index}: {filename}')
                    index += 1
                    fund_nav = pd.concat(pd.read_excel(os.path.join(nav_file_dir, filename), sheet_name=None),
                                         ignore_index=True)
                    fund_nav = fund_nav.drop(['简称'], axis=1)
                    fund_nav = fund_nav.rename(columns={
                        '代码': 'CODES',
                        '时间': 'DATES',
                        '单位净值(元)': 'ORIGINALUNIT',
                        '累计净值(元)': 'ORIGINALNAVACCUM',
                        '复权净值(元)': 'ADJUSTEDNAV',
                        '万份基金单位收益(元)': 'UNITYIELD10K',
                        '7日年化收益率(%)': 'YIELDOF7DAYS'
                    })

                    fund_nav = fund_nav[(fund_nav['DATES'] != '--')
                                        & (~fund_nav['DATES'].isnull())]
                    fund_nav = fund_nav.replace('--', np.nan)
                    self._data_helper._upload_raw(fund_nav, EmFundNav.__table__.name)
                else:
                    continue
            return True
        except Exception as e:
            print(e)
            traceback.print_exc()
            return False

    def em_index_price_history(self, em_ids, start_date, end_date):
        em_id_str = ','.join(em_ids) if isinstance(em_ids, list) else em_ids
        df = c.csd(em_id_str, "VOLUME,CLOSE", start_date, end_date,
                   "period=1,adjustflag=1,curtype=1,order=1,market=0,Ispandas=1")
        if not isinstance(df, pd.DataFrame):
            if df.ErrorCode != 0:
                print(f'failed to get index price history: {df.ErrorMsg} (index_ids){em_ids}')
            return

        df = df.reset_index().rename(columns={
            'CODES': 'em_id',
            'DATES': 'datetime',
            'CLOSE': 'close',
            'OPEN': 'open',
            'HIGH':'high',
            'LOW':'low',
            'VOLUME':'volume'
        })
        df = df[df['close'].notna()]
        self._data_helper._upload_raw(df, EmIndexPrice.__table__.name)

    def em_fund_scale_history(self):
        with RawDatabaseConnector().managed_session() as db_session:
            try:
                dates = db_session.query(
                    distinct(EmFundNav.DATES)
                ).all()

                dates = [d for d, in dates]
                dates.sort()
                start_date = dates[0]
                for i in range(1, 100):
                    dates.insert(0, start_date - datetime.timedelta(days=i))

                for d in dates:
                    month_day = d.strftime('%m%d')
                    if month_day not in self._quarter_update_dates:
                        continue

                    print(d)

                    fund_ids = db_session.query(
                        distinct(EmFundNav.CODES)
                    ).filter(
                        EmFundNav.DATES >= d,
                        EmFundNav.DATES <= d + datetime.timedelta(days=100)
                    ).all()

                    fund_ids = [f for f, in fund_ids]
                    fund_id_str = ','.join(fund_ids)

                    df = c.css(fund_id_str, "FUNDSCALE",
                               f"EndDate={d},Ispandas=1").reset_index()
                    df['DATES'] = d

                    self._data_helper._upload_raw(df, EmFundScale.__table__.name)
            except Exception as e:
                print('Failed to get data <err_msg> {}'.format(e))
                return None

    def em_fund_holding_rate_history(self, end_date: str):
        fund_list_df = RawDataApi().get_em_fund_list(end_date, limit=1)
        if fund_list_df is None:
            print(f'failed to get fund list for fund status')
        else:
            fund_list = fund_list_df.all_live_fund_list.array[0].split(',')
            fund_list += fund_list_df.delisted_fund_list.array[0].split(',')
            y_list = [str(y) for y in range(2020, 2021, 1)]
            d_list = []
            for y in y_list:
                for d in self._semi_update_dates:
                    d_list.append(y + d)
            for d in d_list:
                data = c.css(fund_list, "HOLDPERSONALHOLDINGPCT,HOLDINSTIHOLDINGPCT,HOLDNUM", f"ReportDate={d},Ispandas=1")
                data = data[data.drop(columns='DATES').notna().any(axis=1)].reset_index()
                data['DATES'] = d
                self._data_helper._upload_raw(data, EmFundHoldingRate.__table__.name)
                print(f'finish {d}')

    def em_fund_nav(self, start_date, end_date, fund_id_list: Tuple[str] = ()):
        try:
            # TODO: 应该使用每一天当天的成分列表, 可能所有的sector都需要这样
            # Get all fund ids, 功能函数-板块成分
            # http://quantapi.eastmoney.com/Cmd/Sector?from=web
            start_date = datetime.datetime.strptime(start_date, '%Y%m%d') - datetime.timedelta(days=5)
            start_date = start_date.strftime('%Y%m%d')
            trade_date_df = RawDataApi().get_em_tradedates(start_date, end_date)
            if trade_date_df is None:
                print('failed to get em trade dates for em_fund_nav')
                return
            if not fund_id_list:
                fund_id_result = c.sector('507013', end_date)
                if fund_id_result.ErrorCode != 0:
                    print(f'Failed to get fund id list: {fund_id_result.ErrorMsg}')
                    return
                fund_id_list = fund_id_result.Codes
            fund_id_str = ','.join(fund_id_list)
            df_list: List[pd.DataFrame] = []
            for date in trade_date_df.TRADEDATES:
                # 基金 万份基金单位收益 7日年化收益率
                data1 = c.css(fund_id_str, "10KUNITYIELD,YIELDOF7DAYS", f"EndDate={date},Ispandas=1")
                if not isinstance(data1, pd.DataFrame):
                    if data1.ErrorCode != 0:
                        print(f'Failed to get fund nav data1: {data1.ErrorMsg}')
                    return
                # 基金 单位净值(原始披露) 累计单位净值(原始披露) 复权单位净值
                data2 = c.css(fund_id_str, "ORIGINALUNIT,ORIGINALNAVACCUM,NAVADJ", f"TradeDate={date},Ispandas=1")
                if not isinstance(data2, pd.DataFrame):
                    if data2.ErrorCode != 0:
                        print(f'Failed to get fund nava data2: {data2.ErrorMsg}')
                    return
                df = data2.drop(columns='DATES').join(data1.drop(columns='DATES'), how='outer')
                df = df[df[['ORIGINALUNIT', 'ORIGINALNAVACCUM', 'NAVADJ', '10KUNITYIELD', 'YIELDOF7DAYS']].notna().any(axis=1)]
                df = df.rename(columns={'10KUNITYIELD': 'UNITYIELD10K', 'NAVADJ': 'ADJUSTEDNAV'}).reset_index()
                df['DATES'] = pd.to_datetime(date).date().strftime('%Y-%m-%d')
                df_list.append(df)

            df_total = pd.concat(df_list)
            # 这里删掉之前几天的数据，然后再重刷一遍
            # TODO: 最好可以原子提交下边两步操作
            self.delete_em_fund_nav(start_date, end_date)
            self._data_helper._upload_raw(df_total, EmFundNav.__table__.name)
            return True
        except Exception as e:
            print(e)
            traceback.print_exc()
            return False

    def delete_em_fund_nav(self, start_date, end_date):
        try:
            RawDataApi().delete_em_fund_nav(start_date, end_date)
            return True
        except Exception as e:
            print(e)
            traceback.print_exc()
            return False

    def em_fund_status(self, end_date: str):
        try:
            fund_list = RawDataApi().get_em_fund_list(end_date, limit=1)
            if fund_list is None:
                print(f'failed to get fund list for fund status')
                return False
            fund_list = fund_list.all_live_fund_list.array[0]
            data1 = c.css(fund_list, 'FUNDSCALE', f'EndDate={end_date},Ispandas=1')
            if not isinstance(data1, pd.DataFrame):
                if data1.ErrorCode != 0:
                    print(f'failed to get fund status data1: {data1.ErrorMsg}')
                return False

            data2 = c.css(fund_list, 'PURCHSTATUS,REDEMSTATUS,LPLIMIT,OTCLPLIMIT,TRADESTATUS', f'TradeDate={end_date},Ispandas=1')
            if not isinstance(data2, pd.DataFrame):
                if data2.ErrorCode != 0:
                    print(f'failed to get fund status datta2: {data2.ErrorMsg}')
                return False

            df = data1.drop(columns='DATES').join(data2.drop(columns='DATES'), how='outer')
            df = df[df.notna().any(axis=1)]
            if df.empty:
                return True

            df = df.reset_index()
            df['DATES'] = end_date
            df = df.astype({'FUNDSCALE': 'float64', 'LPLIMIT': 'float64', 'OTCLPLIMIT': 'float64'})
            # 获取当前的fund status
            now_df = RawDataApi().get_em_fund_status(end_date=end_date)
            if now_df is not None:
                # 过滤出来新增基金status以及旧基金的status发生变化的情况
                df = df.merge(now_df.drop(columns=['_update_time']), how='left', on=['CODES', 'FUNDSCALE', 'LPLIMIT', 'OTCLPLIMIT', 'PURCHSTATUS', 'REDEMSTATUS', 'TRADESTATUS'], indicator=True, validate='one_to_many')
                df = df[df._merge == 'left_only'].drop(columns=['_merge', 'DATES_y']).rename(columns={'DATES_x': 'DATES'})
            self._data_helper._upload_raw(df, EmFundScale.__table__.name)
            return True
        except Exception as e:
            print(e)
            traceback.print_exc()
            return False

    def em_index_price(self, em_ids: Set[str], start_date, end_date):
        try:
            # 每次重刷15个交易日的数据
            data = c.getdate(start_date, -INDEX_PRICE_EXTRA_TRADE_DAYS)
            if data.ErrorCode != 0:
                print(f'[em_index_price] failed to get trade dates: {data.ErrorMsg} (start_date){start_date}')
                return False
            start_date = pd.to_datetime(data.Data[0]).strftime('%Y%m%d')

            # 不支持跨品种的index同时请求，所以需要拆出来分开去做
            df_list = []
            # 利率部分
            ir_index = []
            for one in ('LIGBP1M.IR', 'HIBOR3M.IR'):
                try:
                    em_ids.remove(one)
                except KeyError:
                    continue
                ir_index.append(one)
            if ir_index:
                data = c.csd(','.join(ir_index), "CLOSE", start_date, end_date, "period=1,adjustflag=1,curtype=1,order=1,market=CNSESH,Ispandas=1")
                if not isinstance(data, pd.DataFrame):
                    if data.ErrorCode != 0:
                        print(f'[em_index_price] failed to get index price: {data.ErrorMsg} (index_id){ir_index}')
                    return False
                df_list.append(data)

            # 期货部分
            future_index = []
            for one in ('AU9999.SGE', 'AU0.SHF'):
                try:
                    em_ids.remove(one)
                except KeyError:
                    continue
                future_index.append(one)
            if future_index:
                data = c.csd(','.join(future_index), "OPEN,HIGH,LOW,VOLUME,CLOSE", start_date, end_date, "period=1,adjustflag=1,curtype=1,order=1,market=CNSESH,Ispandas=1")
                if not isinstance(data, pd.DataFrame):
                    if data.ErrorCode != 0:
                        print(f'[em_index_price] failed to get index price: {data.ErrorMsg} (index_id){future_index}')
                    return False
                df_list.append(data)

            # 常规指数部分
            data = c.csd(','.join(em_ids), "OPEN,HIGH,LOW,VOLUME,CLOSE", start_date, end_date, "period=1,adjustflag=1,curtype=1,order=1,market=CNSESH,Ispandas=1")
            if not isinstance(data, pd.DataFrame):
                if data.ErrorCode != 0:
                    print(f'[em_index_price] failed to get index price: {data.ErrorMsg} (index_id){em_ids}')
                return False

            df = pd.concat(df_list + [data]).reset_index().rename(columns={
                'CODES': 'em_id',
                'DATES': 'datetime',
                'CLOSE': 'close',
                'OPEN': 'open',
                'HIGH':'high',
                'LOW':'low',
                'VOLUME':'volume'
            })
            df = df[df['close'].notna()]
            # TODO: 最好可以原子提交下边两步操作
            RawDataApi().delete_em_index_price(list(em_ids)+ir_index+future_index, start_date, end_date)
            self._data_helper._upload_raw(df, EmIndexPrice.__table__.name)
            return True
        except Exception as e:
            print(e)
            traceback.print_exc()
            return False

    def em_index_info(self, index_ids: List[str]):
        try:
            data = c.css(','.join(index_ids), 'SHORTNAME,NAME,PUBLISHDATE,MAKERNAME,INDEXPROFILE', 'Ispandas=1')
            if not isinstance(data, pd.DataFrame):
                if data.ErrorCode != 0:
                    print(f'failed to get index info: {data.ErrorMsg}')
                return False

            df = data.drop(columns='DATES').reset_index().rename(columns=lambda x: EmIndexInfo.__getattribute__(EmIndexInfo, x).name)
            # 统一设置一个默认值，之后可以按需手工修改
            df['price_source'] = IndexPriceSource.default.name
            # 更新到db
            self._data_helper._upload_raw(df, EmIndexInfo.__table__.name)
            return True
        except Exception as e:
            print(e)
            traceback.print_exc()
            return False

    def em_macroeconomic_price(self, start_date, end_date):
        try:
            index_info_df = RawDataApi().get_em_index_info()
            if index_info_df is None:
                print('failed to get index info for macroeconomic price')
                return False
            index_info_df = index_info_df[index_info_df.price_source == IndexPriceSource.macroeconomic]
            macroeconomic_list = [self._MACROECONOMIC_MAP_I[one] for one in index_info_df.em_id.to_list() if one in self._MACROECONOMIC_MAP_I]
            data = c.edb(','.join(macroeconomic_list), f'StartDate={start_date},EndDate={end_date},IsLatest=0,RowIndex=2,Ispandas=1')
            if not isinstance(data, pd.DataFrame):
                if data.ErrorCode != 0:
                    if data.ErrorCode == 10000009:
                        print(f'no macroeconomic price data during {start_date} and {end_date}')
                        return True
                    print(f'failed to get macroeconomic price: {data.ErrorMsg}')
                return False

            df = data.reset_index().rename(columns={
                'CODES': 'em_id',
                'DATES': 'datetime',
                'RESULT': 'close'
            })
            df = df[df.close.notna()]
            df['em_id'] = df['em_id'].map(self._MACROECONOMIC_MAP)
            # 更新到db
            self._data_helper._upload_raw(df, EmIndexPrice.__table__.name)
            return True
        except Exception as e:
            print(e)
            traceback.print_exc()
            return False

    def em_realtime_index(self, em_ids: Set[str], data_start_time, to_save):
        try:
            # 不支持跨品种的index同时请求，所以需要拆出来分开去做
            df_list = []

            # 利率部分
            ir_index = []
            for one in ('LIGBP1M.IR', 'HIBOR3M.IR'):
                try:
                    em_ids.remove(one)
                except KeyError:
                    continue
                ir_index.append(one)

            # 期货部分
            future_index = []
            for one in ('AU9999.SGE', 'AU0.SHF'):
                try:
                    em_ids.remove(one)
                except KeyError:
                    continue
                future_index.append(one)

            # 常规指数部分
            data = c.csqsnapshot(','.join(em_ids), 'Date,Time,Now', 'Ispandas=1')
            if not isinstance(data, pd.DataFrame):
                if data.ErrorCode != 0:
                    print(f'[em_index_price] failed to get index price: {data.ErrorMsg} (index_id){em_ids}')
                return None
            df_list.append(data)

            # # 每两次 csqsnapshot 请求之间必须大于 3000 ms
            # # 暂不实时更新利率指数（需要更新时取消注释）
            # time.sleep(3.1)
            # if ir_index:
            #     data = c.csqsnapshot(','.join(ir_index), 'Date,Time,Now', 'Ispandas=1')
            #     if not isinstance(data, pd.DataFrame):
            #         if data.ErrorCode != 0:
            #             print(f'[em_index_price] failed to get index price: {data.ErrorMsg} (index_id){ir_index}')
            #         return False
            #     df_list.append(data)

            # # 暂不实时更新期货指数（需要更新时取消注释）
            # time.sleep(3.1)
            # if future_index:
            #     data = c.csqsnapshot(','.join(future_index), 'Date,Time,Now', 'Ispandas=1')
            #     if not isinstance(data, pd.DataFrame):
            #         if data.ErrorCode != 0:
            #             print(f'[em_index_price] failed to get index price: {data.ErrorMsg} (index_id){future_index}')
            #         return False
            #     df_list.append(data)

            df = pd.concat(df_list)
            df = df[df['DATE'] != 0]
            df = df[df['TIME'] != 0]
            df['datetime'] = df.apply(
                lambda x: datetime.datetime.strptime(f'{x["DATE"]}{x["TIME"]}', '%Y%m%d%H%M%S'), 
                axis=1
            )
            if data_start_time:
                df = df[df['datetime'] > data_start_time]

            df = df.drop(columns=['DATES', 'DATE', 'TIME'])
            df = df.reset_index().rename(columns={
                'CODES': 'em_id',
                'NOW': 'price'
            })
            if to_save:
                try:
                    self._data_helper._upload_raw(df, EmRealtimeIndexPrice.__table__.name)
                except Exception as e:
                    print(e)
                    traceback.print_exc()
            
            return df

        except Exception as e:
            print(e)
            traceback.print_exc()
            return None

    # 从em客户端导出数据后读取并处理
    def em_stock_price_history(self, stock_price_file_dir: str):
        for index, filename in enumerate(os.listdir(stock_price_file_dir)):
            if not filename.endswith(".xls"):
                continue
            index += 1
            print(f'{index}: {filename}')
            stock_price = pd.concat(pd.read_excel(os.path.join(stock_price_file_dir, filename), sheet_name=None, na_values='--'),
                                    ignore_index=True)
            # 将列名字改为从API获取到数据时的列名字，便于后边统一处理
            stock_price = stock_price.drop(['简称'], axis=1).rename(columns={
                '代码': 'CODES',
                '时间': 'DATES',
                '开盘价(元)': 'OPEN',
                '收盘价(元)': 'CLOSE',
                '最高价(元)': 'HIGH',
                '最低价(元)': 'LOW',
                '前收盘价(元)': 'PRECLOSE',
                '均价(元)': 'AVERAGE',
                '成交量(股)': 'VOLUME',
                '成交金额(元)': 'AMOUNT',
                '换手率(%)': 'TURN',
                '交易状态': 'TRADESTATUS',
                '内盘成交量': 'BUYVOL',
                '外盘成交量': 'SELLVOL',
            })

            # 过滤掉个股未上市时的数据，以及日期为nan的行（表示整行为无效数据）
            stock_price = stock_price.loc[stock_price['TRADESTATUS'] != '未上市'].loc[~stock_price['DATES'].isna()].rename(columns=lambda x: EmStockPrice.__getattribute__(EmStockPrice, x).name)
            # 更新到db
            self._data_helper._upload_raw(stock_price, EmStockPrice.__table__.name)

    def em_stock_price(self, start_date: str, end_date: str, stock_list: Tuple[str] = ()):
        try:
            # 获取区间内所有交易日
            tradedates = c.tradedates(start_date, end_date, "period=1,order=1,market=CNSESH")
            if tradedates.ErrorCode != 0:
                print(f'[em_stock_price] failed to get trade dates: {tradedates.ErrorMsg}')
                return
            if len(tradedates.Data) == 0:
                print(f'[em_stock_price] no trade dates, return immediately (start_date){start_date} (end_date){end_date}')
                return

            if not stock_list:
                # 获取所有A股股票的ID, 功能函数-板块成分
                # http://quantapi.eastmoney.com/Cmd/Sector?from=web
                # 全部A股股票
                stock_id_result = c.sector('001004', end_date)
                if stock_id_result.ErrorCode != 0:
                    print(f'failed to get stock id list: {stock_id_result.ErrorMsg}')
                    return
                stock_list = stock_id_result.Codes

            df_list = []
            for date in tradedates.Data:
                # 获取个股股价信息
                temp_df = c.csd(stock_list,
                                'OPEN,CLOSE,HIGH,LOW,PRECLOSE,AVERAGE,VOLUME,AMOUNT,TURN,TRADESTATUS,TNUM,BUYVOL,SELLVOL',
                                date, date, 'period=1,adjustflag=1,curtype=1,order=1,market=0,Ispandas=1')
                if not isinstance(temp_df, pd.DataFrame) and temp_df.ErrorCode != 0:
                    print(f'failed to get stock price info: {temp_df.ErrorMsg} (date){date}')
                    return
                # 过滤掉个股未上市时的数据，以及日期为nan的行（表示整行为无效数据）
                df_list.append(temp_df.loc[temp_df['TRADESTATUS'] != '未上市'].loc[~temp_df['DATES'].isna()])

            df = pd.concat(df_list).reset_index().rename(columns=lambda x: EmStockPrice.__getattribute__(EmStockPrice, x).name)
            # 更新到db
            self._data_helper._upload_raw(df, EmStockPrice.__table__.name)
            return True
        except Exception as e:
            print(e)
            traceback.print_exc()
            return False

    # 从em客户端导出数据后读取并处理
    def em_stock_post_price_history(self, stock_post_price_file_dir: str):
        for index, filename in enumerate(os.listdir(stock_post_price_file_dir)):
            if not filename.endswith(".xls"):
                continue
            index += 1
            print(f'{index}: {filename}')
            stock_price = pd.concat(pd.read_excel(os.path.join(stock_post_price_file_dir, filename), sheet_name=None, na_values='--'),
                                    ignore_index=True)
            # 将列名字改为从API获取到数据时的列名字，便于后边统一处理
            stock_price = stock_price.drop(['简称'], axis=1).rename(columns={
                '代码': 'CODES',
                '时间': 'DATES',
                '开盘价(元)': 'OPEN',
                '收盘价(元)': 'CLOSE',
                '最高价(元)': 'HIGH',
                '最低价(元)': 'LOW',
                '前收盘价(元)': 'PRECLOSE',
                '均价(元)': 'AVERAGE',
                '成交量(股)': 'VOLUME',
                '成交金额(元)': 'AMOUNT',
                '交易状态': 'TRADESTATUS',
            })
            # 过滤掉个股未上市时的数据，以及日期为nan的行（表示整行为无效数据）
            stock_price = stock_price.loc[stock_price['TRADESTATUS'] != '未上市'].loc[~stock_price['DATES'].isna()].rename(columns=lambda x: EmStockPostPrice.__getattribute__(EmStockPostPrice, x).name)
            # 更新到db
            self._data_helper._upload_raw(stock_price, EmStockPostPrice.__table__.name)

    def em_stock_post_price(self, start_date: str, end_date: str, stock_list: Tuple[str] = ()):
        try:
            # 获取区间内所有交易日
            tradedates = c.tradedates(start_date, end_date, "period=1,order=1,market=CNSESH")
            if tradedates.ErrorCode != 0:
                print(f'[em_stock_post_price] failed to get trade dates: {tradedates.ErrorMsg}')
                return
            if len(tradedates.Data) == 0:
                print(f'[em_stock_post_price] no trade dates, return immediately (start_date){start_date} (end_date){end_date}')
                return

            if not stock_list:
                # 获取所有A股股票的ID, 功能函数-板块成分
                # http://quantapi.eastmoney.com/Cmd/Sector?from=web
                # 全部A股股票
                stock_id_result = c.sector('001004', end_date)
                if stock_id_result.ErrorCode != 0:
                    print(f'failed to get stock id list: {stock_id_result.ErrorMsg}')
                    return
                stock_list = stock_id_result.Codes

            df_list = []
            for date in tradedates.Data:
                # 获取个股股价信息
                temp_df = c.csd(stock_list,
                                'OPEN,CLOSE,HIGH,LOW,PRECLOSE,AVERAGE,VOLUME,AMOUNT,TRADESTATUS,TAFACTOR',
                                date, date, 'period=1,adjustflag=2,curtype=1,order=1,market=0,Ispandas=1')
                if not isinstance(temp_df, pd.DataFrame) and temp_df.ErrorCode != 0:
                    print(f'failed to get stock price info: {temp_df.ErrorMsg} (date){date}')
                    return
                # 过滤掉个股未上市时的数据，以及日期为nan的行（表示整行为无效数据）
                df_list.append(temp_df.loc[temp_df['TRADESTATUS'] != '未上市'].loc[~temp_df['DATES'].isna()])

            df = pd.concat(df_list).reset_index().rename(columns=lambda x: EmStockPostPrice.__getattribute__(EmStockPostPrice, x).name)
            # 更新到db
            self._data_helper._upload_raw(df, EmStockPostPrice.__table__.name)
            return True
        except Exception as e:
            print(e)
            traceback.print_exc()
            return False

    def em_stock_info(self, end_date: str):
        try:
            # 获取所有A股股票的ID, 功能函数-板块成分
            # http://quantapi.eastmoney.com/Cmd/Sector?from=web
            # 全部A股股票
            stock_id_result = c.sector('001004', end_date)
            if stock_id_result.ErrorCode != 0:
                print(f'failed to get stock id list: {stock_id_result.ErrorMsg}')
                return False

            # 去掉我们已经有的股票ID
            stock_info_df = RawDataApi().get_em_stock_info()
            new_stock_code = list(set(stock_id_result.Codes).difference(set(stock_info_df.stock_id.to_list())))
            if not new_stock_code:
                # 直接返回成功
                return True

            df_list: List[pd.DataFrame] = []
            # 获取无参数指标
            df_no_param = c.css(new_stock_code,
                                'NAME,LISTDATE,FINPURCHORNOT,FINSELLORNOT,STOHSTOCKCONNECTEDORNOT,SHENGUTONGTARGET,ENGNAME,COMPNAME,COMPNAMEENG',
                                'Ispandas=1')
            if not isinstance(df_no_param, pd.DataFrame):
                if df_no_param.ErrorCode != 0:
                    print(f'failed to get stock info(no param): {df_no_param.ErrorMsg}')
                return False
            # 将其中'是'/'否'的结果转换为True/False
            columns = ['FINPURCHORNOT', 'FINSELLORNOT', 'STOHSTOCKCONNECTEDORNOT', 'SHENGUTONGTARGET']
            df_no_param.loc[:, columns] = df_no_param.loc[:, columns].apply(lambda x: x.apply(lambda x: True if x == '是' else False))
            df_list.append(df_no_param)

            # 获取行业分类共有三级的指标
            df_lv4 = c.css(new_stock_code, "BLEMINDCODE,BLSWSINDCODE,SW2014CODE,EMINDCODE2016,CITICCODE2020", "ClassiFication=4,Ispandas=1")
            if not isinstance(df_lv4, pd.DataFrame):
                if df_lv4.ErrorCode != 0:
                    print(f'failed to get stock info(lv4): {df_lv4.ErrorMsg}')
                return False
            df_list.append(df_lv4)

            # 获取行业分类共有二级的指标
            df_lv3 = c.css(new_stock_code, "BLCSRCINDCODE,CSRCCODENEW", "ClassiFication=3,Ispandas=1")
            if not isinstance(df_lv3, pd.DataFrame):
                if df_lv3.ErrorCode != 0:
                    print(f'failed to get stock info(lv3): {df_lv3.ErrorMsg}')
                return False
            df_list.append(df_lv3)

            # 获取行业分类共有四级的指标
            df_lv5 = c.css(new_stock_code, "CSINDCODE2016,GICSCODE", "ClassiFication=5,Ispandas=1")
            if not isinstance(df_lv5, pd.DataFrame):
                if df_lv5.ErrorCode != 0:
                    print(f'failed to get stock info(lv5): {df_lv5.ErrorMsg}')
                return False
            df_list.append(df_lv5)

            if df_list:
                # 将每部分按列粘到一起
                df = pd.concat(df_list, axis=1)
                # 不需要存日期的列，去除索引并做列名转换
                df = df.drop(columns='DATES').reset_index().rename(columns=lambda x: EmStockInfo.__getattribute__(EmStockInfo, x).name)
                # 更新到db
                self._data_helper._upload_raw(df, EmStockInfo.__table__.name)
            return True
        except Exception as e:
            print(e)
            traceback.print_exc()
            return False

    def add_columns_to_fin_fac(self, end_date: str):
        # 获取所有A股股票的ID, 功能函数-板块成分
        # http://quantapi.eastmoney.com/Cmd/Sector?from=web
        # 全部A股股票
        stock_id_result = c.sector('001004', end_date)
        if stock_id_result.ErrorCode != 0:
            print(f'failed to get stock id list: {stock_id_result.ErrorMsg}')
            return

        # 获取主营收入构成(按产品)
        df = c.css(stock_id_result.Codes, "BALANCESTATEMENT_195", f'ReportDate={end_date},type=1,Ispandas=1')
        if not isinstance(df, pd.DataFrame) and df.ErrorCode != 0:
            print(f'failed to get stock financial factors: {df.ErrorMsg}')
            return

        count = 0
        Session = sessionmaker(RawDatabaseConnector().get_engine())
        db_session = Session()
        for row in db_session.query(EmStockFinFac):
            if row.DATES != datetime.datetime.strptime(end_date, '%Y%m%d').date():
                continue
            if row.CODES in df.index:
                row.BALANCESTATEMENT_195 = df.at[row.CODES, 'BALANCESTATEMENT_195']
                count += 1
        db_session.commit()
        db_session.close()
        print(f'append {count} value(s) to fin fac table')

    def em_stock_fin_fac(self, end_date: str):
        # 获取所有A股股票的ID, 功能函数-板块成分
        # http://quantapi.eastmoney.com/Cmd/Sector?from=web
        # 全部A股股票
        stock_id_result = c.sector('001004', end_date)
        if stock_id_result.ErrorCode != 0:
            print(f'failed to get stock id list: {stock_id_result.ErrorMsg}')
            return

        df_list: List[pd.DataFrame] = []
        # 获取无参数指标
        df_no_param = c.css(stock_id_result.Codes,
                            'EBIT,EBITDA,EXTRAORDINARY,LOWERDIANDNI,GROSSMARGIN,OPERATEINCOME,INVESTINCOME,EBITDRIVE,TOTALCAPITAL,WORKINGCAPITAL,\
                             NETWORKINGCAPITAL,TANGIBLEASSET,RETAINED,INTERESTLIBILITY,NETLIBILITY,EXINTERESTCL,EXINTERESTNCL,FCFF,FCFE,DA,FCFFDRIVE,\
                             PERFORMANCEEXPRESSPARENTNI,MBSALESCONS,GPMARGIN,NPMARGIN,EXPENSETOOR,INVTURNRATIO,ARTURNRATIO,ROEAVG,ROEWA,EPSBASIC,EPSDILUTED,\
                             BPS,MBREVENUE,MBCOST,BALANCESTATEMENT_25,BALANCESTATEMENT_46,BALANCESTATEMENT_93,BALANCESTATEMENT_103,BALANCESTATEMENT_141,BALANCESTATEMENT_195,\
                             BALANCESTATEMENT_140,INCOMESTATEMENT_9,INCOMESTATEMENT_48,INCOMESTATEMENT_60,INCOMESTATEMENT_61,INCOMESTATEMENT_83,INCOMESTATEMENT_85,INCOMESTATEMENT_127,\
                             INCOMESTATEMENT_14,CASHFLOWSTATEMENT_39,CASHFLOWSTATEMENT_59,CASHFLOWSTATEMENT_77,CASHFLOWSTATEMENT_82,CASHFLOWSTATEMENT_86',
                            f'ReportDate={end_date},type=1,Ispandas=1')
        if not isinstance(df_no_param, pd.DataFrame) and df_no_param.ErrorCode != 0:
            print(f'failed to get stock financial factors: {df_no_param.ErrorMsg}')
        else:
            df_list.append(df_no_param)

        # 获取主营收入构成(按产品)
        df_mb_sales_cons = c.css(stock_id_result.Codes, "MBSALESCONS", f'ReportDate={end_date},type=2,Ispandas=1')
        if not isinstance(df_mb_sales_cons, pd.DataFrame) and df_mb_sales_cons.ErrorCode != 0:
            print(f'failed to get stock financial factors: {df_mb_sales_cons.ErrorMsg}')
        else:
            df_list.append(df_mb_sales_cons.rename(columns={'MBSALESCONS': 'MBSALESCONS_P'}))

        # 获取归属于上市公司股东的扣除非经常性损益后的净利润(调整前)
        df_with_param_1 = c.css(stock_id_result.Codes, "DEDUCTEDINCOME", f'ReportDate={end_date},DataAdjustType=1,Ispandas=1')
        if not isinstance(df_with_param_1, pd.DataFrame) and df_with_param_1.ErrorCode != 0:
            print(f'failed to get stock financial factors: {df_with_param_1.ErrorMsg}')
        else:
            df_list.append(df_with_param_1.rename(columns={'DEDUCTEDINCOME': 'DEDUCTEDINCOME_BA'}))

        # 获取归属于上市公司股东的扣除非经常性损益后的净利润(调整后)
        df_with_param_2 = c.css(stock_id_result.Codes, "DEDUCTEDINCOME", f'ReportDate={end_date},DataAdjustType=2,Ispandas=1')
        if not isinstance(df_with_param_2, pd.DataFrame) and df_with_param_2.ErrorCode != 0:
            print(f'failed to get stock financial factors: {df_with_param_2.ErrorMsg}')
        else:
            df_list.append(df_with_param_2.rename(columns={'DEDUCTEDINCOME': 'DEDUCTEDINCOME_AA'}))

        # 获取TTM指标
        df_ttm = c.css(stock_id_result.Codes, 'GRTTMR,GCTTMR,ORTTMR,OCTTMR,EXPENSETTMR,GROSSMARGINTTMR,OPERATEEXPENSETTMR,ADMINEXPENSETTMR,FINAEXPENSETTMR,IMPAIRMENTTTMR,\
                       OPERATEINCOMETTMR,INVESTINCOMETTMR,OPTTMR,NONOPERATEPROFITTTMR,EBITTTMR,EBTTTMR,TAXTTMR,PNITTMR,KCFJCXSYJLRTTMR,\
                       NPTTMRP,FVVPALRP,IRTTMRP,IITTMFJVAJVRP,BTAATTMRP,SALESCASHINTTMR,CFOTTMR,CFITTMR,CFFTTMR,CFTTMR,CAPEXR',
                       f'ReportDate={end_date},Ispandas=1')
        if not isinstance(df_ttm, pd.DataFrame) and df_ttm.ErrorCode != 0:
            print(f'failed to get stock financial factors: {df_ttm.ErrorMsg}')
        else:
            df_list.append(df_ttm)

        if len(df_list) > 0:
            # 将每部分按列粘到一起
            df = pd.concat(df_list, axis=1)
            # 日期列修改为end_date
            df.loc[:, 'DATES'] = end_date
            df = df.reset_index().rename(columns=lambda x: EmStockFinFac.__getattribute__(EmStockFinFac, x).name)
            # 更新到db
            self._data_helper._upload_raw(df, EmStockFinFac.__table__.name)

    # 从em客户端导出数据后读取并处理
    def em_stock_daily_info_history(self, stock_daily_info_file_dir: str):
        for index, filename in enumerate(os.listdir(stock_daily_info_file_dir)):
            if not filename.endswith(".xls"):
                continue
            index += 1
            print(f'{index}: {filename}')
            stock_daily_info = pd.concat(pd.read_excel(os.path.join(stock_daily_info_file_dir, filename), sheet_name=None, na_values='--'),
                                         ignore_index=True)
            # 将列名字改为从API获取到数据时的列名字，便于后边统一处理
            stock_daily_info = stock_daily_info.drop(['简称'], axis=1).rename(columns={
                '代码': 'CODES',
                '时间': 'DATES',
                '总股本(股)': 'TOTALSHARE',
            })

            stock_daily_info = stock_daily_info.loc[~stock_daily_info['DATES'].isna()].rename(columns=lambda x: EmStockDailyInfo.__getattribute__(EmStockDailyInfo, x).name)

            # 更新到db
            self._data_helper._upload_raw(stock_daily_info, EmStockDailyInfo.__table__.name)

    def em_stock_daily_info(self, start_date: str, end_date: str, predict_year: int = 0):
        try:
            # 获取区间内所有交易日
            tradedates = c.tradedates(start_date, end_date, "period=1,order=1,market=CNSESH")
            if tradedates.ErrorCode != 0:
                print(f'[em_stock_daily_info] failed to get trade dates: {tradedates.ErrorMsg}')
                return
            if len(tradedates.Data) == 0:
                print(f'[em_stock_daily_info] no trade dates, return immediately (start_date){start_date} (end_date){end_date}')
                return

            # 获取所有A股股票的ID, 功能函数-板块成分
            # http://quantapi.eastmoney.com/Cmd/Sector?from=web
            # 全部A股股票
            stock_id_result = c.sector('001004', end_date)
            if stock_id_result.ErrorCode != 0:
                print(f'failed to get stock id list: {stock_id_result.ErrorMsg}')
                return

            if predict_year == 0:
                predict_year = datetime.datetime.strptime(end_date, '%Y%m%d').date().year

            df_list = []
            for date in tradedates.Data:
                temp_df = c.css(stock_id_result.Codes,
                                'TOTALSHARE,HOLDFROZENAMTACCUMRATIO,PETTMDEDUCTED,PBLYRN,PSTTM,AHOLDER,ESTPEG',
                                f'EndDate={date},TradeDate={date},PREDICTYEAR={predict_year},Ispandas=1')
                if not isinstance(temp_df, pd.DataFrame) and temp_df.ErrorCode != 0:
                    print(f'failed to get stock daily info: {temp_df.ErrorMsg} (date){date}')
                    return
                # 日期列修改为end_date
                temp_df.loc[:, 'DATES'] = date
                df_list.append(temp_df)

            df = pd.concat(df_list).reset_index().rename(columns=lambda x: EmStockDailyInfo.__getattribute__(EmStockDailyInfo, x).name)
            # 更新到db
            self._data_helper._upload_raw(df, EmStockDailyInfo.__table__.name)
            return True
        except Exception as e:
            print(e)
            traceback.print_exc()
            return False

    def em_stock_refinancing(self, start_date: str, end_date: str):
        try:
            data = c.ctr("AdditionPlanInfo",
                         "SECURITYCODE,APPROVENOTICEDATE,PLANNOTICEDDATE,NEWPROGRESS,SUMFINA_T,ATTACHNAME,ADDPURPOSE",
                        f"DateType=2,StartDate={start_date},EndDate={end_date},Process=0")
            if data.ErrorCode != 0:
                print(f'failed to get stock refinancing info: {data.ErrorMsg}')
                return False

            infos: List[List] = []
            for v in data.Data.values():
                # if v[3] in ('董事会批准', '董事会修改', '董事会终止', '股东大会批准', '股东大会修改'):
                #    continue
                infos.append(v)
            df = pd.DataFrame(infos, columns=['SECURITYCODE', 'APPROVENOTICEDATE', 'PLANNOTICEDDATE',
                                              'NEWPROGRESS', 'SUMFINA_T', 'ATTACHNAME', 'ADDPURPOSE'])
            self._data_helper._upload_raw(df.rename(columns=lambda x: EmStockRefinancing.__getattribute__(EmStockRefinancing, x).name), EmStockRefinancing.__table__.name)
            return True
        except Exception as e:
            print(e)
            traceback.print_exc()
            return False

    def em_stock_estimate_fac(self, start_date: str, end_date: str, predict_year: int = 0):
        try:
            # 获取区间内所有交易日
            df = RawDataApi().get_em_tradedates(start_date, end_date)
            if df is None or df.shape[0] == 0:
                print(f'[em_stock_estimate_fac] no trade dates, return immediately (start_date){start_date} (end_date){end_date}')
                return False

            # 获取所有A股股票的ID, 功能函数-板块成分
            # http://quantapi.eastmoney.com/Cmd/Sector?from=web
            # 全部A股股票
            stock_id_result = c.sector('001004', end_date)
            if stock_id_result.ErrorCode != 0:
                print(f'failed to get stock id list: {stock_id_result.ErrorMsg}')
                return False

            if predict_year == 0:
                predict_year = datetime.datetime.strptime(end_date, '%Y%m%d').date().year + 1

            df_list = []
            for date in df.TRADEDATES:
                temp_df = c.css(stock_id_result.Codes,
                                'ESTGR,ESTNI',
                                f'EndDate={date},PREDICTYEAR={predict_year},Ispandas=1')
                if not isinstance(temp_df, pd.DataFrame):
                    if temp_df.ErrorCode != 0:
                        print(f'failed to get stock daily info: {temp_df.ErrorMsg} (date){date}')
                    return False
                # 日期列修改为end_date
                temp_df.loc[:, 'DATES'] = date
                df_list.append(temp_df)

            df = pd.concat(df_list).reset_index().rename(columns=lambda x: EmStockEstimateFac.__getattribute__(EmStockEstimateFac, x).name)
            df = df[df.notna().all(axis=1)]
            df['predict_year'] = predict_year
            # 更新到db
            self._data_helper._upload_raw(df, EmStockEstimateFac.__table__.name)
            return True
        except Exception as e:
            print(e)
            traceback.print_exc()
            return False

    def em_index_val_history(self, start_date: str, end_date: str, index_list: List[str]):
        # 获取区间内所有交易日
        trade_day_df = RawDataApi().get_em_tradedates(start_date, end_date)
        if trade_day_df is None or trade_day_df.shape[0] == 0:
            print(f'[em_index_val_history] no trade dates, return immediately (start_date){start_date} (end_date){end_date}')
            return

        df_list: List[pd.DataFrame] = []
        # 一天一天地获取
        for date in trade_day_df.TRADEDATES:
            data = c.csd(index_list,
                        "PETTM,PBMRQ,PSTTM,PCFTTM,ROE,EPSTTM,DIVIDENDYIELD",
                        date, date,
                        "DelType=1,period=1,adjustflag=1,curtype=1,order=1,market=0,Ispandas=1")
            if not isinstance(data, pd.DataFrame):
                if data.ErrorCode != 0:
                    print(f'failed to get index val info: {data.ErrorMsg} (date){date}')
                break

            _y = pd.to_datetime(date).date().year + 1
            another_data = c.css(index_list, "ESTPEG", f"TradeDate={date},PREDICTYEAR={_y},Ispandas=1")
            if not isinstance(another_data, pd.DataFrame):
                if another_data.ErrorCode != 0:
                    print(f'failed to get index val info part 2: {another_data.ErrorMsg} (date){date}')
                break
            df_list.append(data.join(another_data.drop(columns='DATES'), how='outer'))
            print(f'{date} done')

        if df_list:
            if len(df_list) == 1:
                df = df_list[0]
            else:
                df = pd.concat(df_list)
            df = df[df.drop(columns=['DATES']).notna().any(axis=1)]
            df = df.reset_index().rename(columns={'DIVIDENDYIELD': 'DIVIDENDRATETTM'}).rename(columns=lambda x: EmIndexVal.__getattribute__(EmIndexVal, x).name)
            self._data_helper._upload_raw(df, EmIndexVal.__table__.name)

    def em_index_val(self, start_date: str, end_date: str):
        try:
            # 获取区间内所有交易日
            trade_day_df = RawDataApi().get_em_tradedates(start_date, end_date)
            if trade_day_df is None or trade_day_df.shape[0] == 0:
                print(f'[em_index_val] no trade dates, return immediately (start_date){start_date} (end_date){end_date}')
                return False

            # 获取basic table中index_info信息
            index_info_df = BasicDataApi().get_index_info()
            if index_info_df is None:
                print(f'[em_index_val] get index info failed')
                return False
            em_indexes = index_info_df[index_info_df.tag_method.isin(['PE百分位', 'PB百分位', 'PS百分位'])].em_id
            # 过滤掉几个特殊指数
            em_indexes = em_indexes[em_indexes.notna() & ~em_indexes.isin(['LIGBP1M.IR', 'HIBOR3M.IR', 'AU9999.SGE', 'AU0.SHF'])]
            index_list = em_indexes.to_list()
            if not index_list:
                print(f'[em_index_val] empty index list, return immediately')
                return False

            df_list: List[pd.DataFrame] = []
            # 一天一天地获取
            for date in trade_day_df.TRADEDATES:
                data = c.csd(index_list,
                           "PETTM,PBMRQ,PSTTM,PCFTTM,ROE,EPSTTM",
                           date, date,
                           "DelType=1,period=1,adjustflag=1,curtype=1,order=1,market=0,Ispandas=1")
                if not isinstance(data, pd.DataFrame):
                    if data.ErrorCode != 0:
                        print(f'failed to get index val info: {data.ErrorMsg} (date){date}')
                    break

                # Caution!! 股息率补历史的话需要使用csd中的DIVIDENDYIELD，这里的DIVIDENDRATETTM只能用作每日更新
                _y = pd.to_datetime(date).date().year + 1
                another_data = c.css(index_list, "DIVIDENDRATETTM,ESTPEG", f"TradeDate={date},PREDICTYEAR={_y},Ispandas=1")
                if not isinstance(another_data, pd.DataFrame):
                    if another_data.ErrorCode != 0:
                        print(f'failed to get index val info part 2: {another_data.ErrorMsg} (date){date}')
                    break
                # 这里除以100与股息率历史数据保持单位一致
                another_data['DIVIDENDRATETTM'] /= 100
                df_list.append(data.join(another_data.drop(columns='DATES'), how='outer'))

            if df_list:
                if len(df_list) == 1:
                    df = df_list[0]
                else:
                    df = pd.concat(df_list)
                df = df[df.drop(columns='DATES').notna().any(axis=1)]
                df = df.reset_index().rename(columns=lambda x: EmIndexVal.__getattribute__(EmIndexVal, x).name)
                self._data_helper._upload_raw(df, EmIndexVal.__table__.name)
                return True
            else:
                return False
        except Exception as e:
            print(e)
            traceback.print_exc()
            return False

    def em_tradedates(self, start_date, end_date, is_automatic_update=True):
        try:
            if is_automatic_update:
                # 如果是每日自动更新，我们需要去存T+1日的数据，这里保险起见多取30天的
                end_date_dt: datetime.datetime = datetime.datetime.strptime(end_date, '%Y%m%d')
                extra_end_date = (end_date_dt + datetime.timedelta(days=30)).strftime('%Y%m%d')
            else:
                extra_end_date = end_date
            # 这里确保返回结果按日期升序排序
            tradedates_result = c.tradedates(start_date, extra_end_date, "period=1,order=1,market=CNSESH")
            if tradedates_result.ErrorCode != 0:
                print(f'Failed to get tradedates: {tradedates_result.ErrorMsg}')
                return False

            tradedates = tradedates_result.Data
            if is_automatic_update:
                # 如果是每日自动更新，看一下返回的第一个日期是否是start_date，如果不是，表明今天不是交易日
                start_date_dt: datetime.datetime = pd.to_datetime(start_date, infer_datetime_format=True)
                if start_date_dt != pd.to_datetime(tradedates[0], infer_datetime_format=True):
                    print(f'today {start_date} is not a trading day')
                    return False

            df = pd.DataFrame(tradedates, columns=['TRADEDATES'])
            if is_automatic_update:
                # 如果是每日自动更新，向DB中insert T+1日的日期
                df = df.iloc[[1], :]
            self._data_helper._upload_raw(df, EmTradeDates.__table__.name)
            return True
        except Exception as e:
            print(e)
            traceback.print_exc()
            return False

    def em_index_component(self, start_date: str, end_date: str):
        try:
            index_info = BasicDataApi().get_index_info()

            date_list = self._get_date_list(start_date, end_date)
            s_list: List[pd.Series] = []
            for row in index_info[~index_info['em_plate_id'].isna()].loc[:, ['index_id', 'em_id', 'em_plate_id']].itertuples(index=False):
                for date in date_list:
                    stock_id_result = c.sector(row.em_plate_id, date)
                    if stock_id_result.ErrorCode != 0:
                        # print(f'failed to get stock id list: {stock_id_result.ErrorMsg}')
                        continue

                    stock_id_list: List[str] = []
                    for i in range(0, len(stock_id_result.Data), 2):
                        stock_id_list.append(stock_id_result.Data[i])
                    if len(stock_id_list) != 0:
                        s_list.append(pd.Series(row._asdict()).append(pd.Series({'datetime': date, 'stock_list': ','.join(stock_id_list)})))

            # 更新到db
            self._data_helper._upload_raw(pd.DataFrame(s_list), EmIndexComponent.__table__.name)
            return True
        except Exception as e:
            print(e)
            traceback.print_exc()
            return

    @staticmethod
    def _lambda_func_index_component_1(x: pd.Series):
        value: List[Dict[str, str]] = json.loads(x)
        new_value = []
        for one in value:
            one = (*one.keys(), float(*one.values()))
            new_value.append(one)
        new_value.sort(key=itemgetter(1), reverse=True)
        return json.dumps(new_value)

    @staticmethod
    def _lambda_func_index_component_2(em_id_map: Dict[str, str], x: pd.Series):
        try:
            return em_id_map[x]
        except KeyError:
            return x

    @staticmethod
    def _lambda_func_index_component_3(x: pd.Series):
        value: List[Dict[str, str]] = json.loads(x)
        new_value = []
        for one in value:
            one = [*one.keys(), float(*one.values())]
            if one[0][0] in ('0', '3'):
                one[0] += '.SZ'
            elif one[0][0] in ('6'):
                one[0] += '.SH'
            new_value.append(one)
        new_value.sort(key=itemgetter(1), reverse=True)
        return json.dumps(new_value)

    @staticmethod
    def _lambda_func_index_component_4(x: pd.Series):
        if pd.isnull(x):
            return x
        return json.dumps([one + '.OF' for one in x.array])

    def cs_index_component(self, date: str):
        try:
            em_id_list = BasicDataApi().get_index_info().em_id.to_list()

            # 中证指数爬下来的部分
            columns_list = ['id', 'name', 'num', 'id_cat', 'sector', 'top10', 'related_funds']
            df_list: List[pd.DataFrame] = []
            for cat in ('industry', 'topic', 'strat', 'cap'):
                raw_df = pd.read_excel(f'./data/Index/{cat}_data.xlsx', na_values='--')
                df_list.append(raw_df[columns_list])

            df = pd.concat(df_list)
            df['id'] = df['id'].transform(lambda x: EmRawDataDownloader._lambda_func_index_component_2({em_id.split('.')[0]: em_id for em_id in em_id_list if em_id is not None}, x))
            df['id_cat'] = df['id_cat'].map({'行业': SectorType.industry.name, '主题': SectorType.topic.name, '策略': SectorType.strategy.name, '规模': SectorType.scale.name})
            df['sector'] = df['sector'].transform(EmRawDataDownloader._lambda_func_index_component_1)
            df['top10'] = df['top10'].transform(EmRawDataDownloader._lambda_func_index_component_3)
            df = df.rename(columns={'id': 'index_id'})
            # Choice中指数的全部成分及权重
            # 该表主要提供指定日期的指数成分股代码及权重等信息
            choice_data = defaultdict(list)
            for em_id in df['index_id'].to_list():
                data = c.ctr("INDEXCOMPOSITION","SECUCODE,NAME,WEIGHT",f"IndexCode={em_id},EndDate={date}")
                if data.ErrorCode != 0:
                    print(f'[cs_index_component] (em_id){em_id} (err_msg){data.ErrorMsg}')
                    continue
                for constituent in data.Data.values():
                    choice_data[em_id].append((constituent[0], round(constituent[2] * 100, 2)))
                choice_data[em_id].sort(key=itemgetter(1), reverse=True)
                choice_data[em_id] = json.dumps(choice_data[em_id])

            df['datetime'] = date
            df = df.set_index('index_id').assign(all_constitu=pd.Series(choice_data))
            # 更新到db
            self._data_helper._upload_raw(df.drop(columns='name').reset_index(), CSIndexComponent.__table__.name)
            return True
        except Exception as e:
            print(e)
            traceback.print_exc()
            return

    def em_fund_list(self, start_date: str, end_date: str):
        try:
            # 这两个成分只能取到最新的，所以直接用end_date即可，没必要遍历
            # 获取所有基金列表（不包含未成立、已到期）
            fund_list_result = c.sector('507013', end_date)
            if fund_list_result.ErrorCode != 0:
                print(f'failed to get live fund list: {fund_list_result.ErrorMsg}')
                return
            # 获取已摘牌基金列表
            delisted_fund_list_result = c.sector('507022', end_date)
            if delisted_fund_list_result.ErrorCode != 0:
                print(f'failed to get delisted fund list: {delisted_fund_list_result.ErrorMsg}')
                return

            df = pd.DataFrame({'datetime': [end_date], 'all_live_fund_list': [','.join(fund_list_result.Codes)],
                               'delisted_fund_list': [','.join(delisted_fund_list_result.Codes)]})
            # 更新到db
            self._data_helper._upload_raw(df, EmFundList.__table__.name)
            return True
        except Exception as e:
            print(e)
            traceback.print_exc()
            return

    def _em_get_all_fund_list(self, date: str):
        # 获取全部基金
        all_fund = c.sector('507013', date)
        if all_fund.ErrorCode != 0:
            print(f'failed to get all fund list: {all_fund.ErrorMsg}')
            return

        # 获取全部基金列表（含未成立、已到期）
        all_fund_extra_full = c.sector('507010', date)
        if all_fund_extra_full.ErrorCode != 0:
            print(f'failed to get all fund list: {all_fund_extra_full.ErrorMsg}')
            return

        # 获取全部基金列表（含未成立）
        all_fund_extra = c.sector('507009', date)
        if all_fund_extra.ErrorCode != 0:
            print(f'failed to get all fund list: {all_fund_extra.ErrorMsg}')
            return

        # 不应该保存未成立基金的数据，这里我们需要(全部 + (含未成立、已到期 - 含未成立))
        all_fund_list = set(all_fund.Codes)
        all_fund_extra_full_list = set(all_fund_extra_full.Codes)
        all_fund_extra_list = set(all_fund_extra.Codes)
        all_fund_list.update(all_fund_extra_full_list.difference(all_fund_extra_list))
        return all_fund_list

    def em_fund_info_history(self, date: str):
        fund_list = self._em_get_all_fund_list(date)
        if fund_list is None:
            return

        # 更新wind_fund_info中没有的数据
        wind_df = RawDataApi().get_wind_fund_info()
        self.em_fund_info(fund_list.difference(wind_df.wind_id))

    def em_fund_info(self, fund_id_list: Set[str]):
        if not fund_id_list:
            return True
        try:
            # 过滤掉非.OF结尾的基金
            fund_id_list = [one for one in fund_id_list if one.split('.')[1] == 'OF']
            if not fund_id_list:
                return True
            data = c.css(','.join(fund_id_list), 'NAME,FNAME,FUNDTYPE,FOUNDDATE,MATURITYDATE,FIRSTINVESTTYPE,SECONDINVESTTYPE,TRADECUR,STRUCFUNDORNOT,GFCODEM,PREDFUNDMANAGER,MGRCOMP,CUSTODIANBANK,FOREIGNCUSTODIAN', 'Ispandas=1')
            if not isinstance(data, pd.DataFrame):
                if data.ErrorCode != 0:
                    print(f'failed to get fund info: {data.ErrorMsg}')
                return False

            data['FUNDTYPE'] = data['FUNDTYPE'].map(lambda x: True if x == '契约型开放式' else False)
            data['STRUCFUNDORNOT'] = data['STRUCFUNDORNOT'].map(lambda x: True if x == '是' else False)
            df = data.drop(columns='DATES').reset_index().rename(columns=lambda x: EmFundInfo.__getattribute__(EmFundInfo, x).name)
            # 更新到db，先删再添，确保数据不会冲突，且有一个更新的机会
            # TODO: 最好原子提交下边两个操作
            RawDataApi().delete_em_fund_info(df.em_id.to_list())
            self._data_helper._upload_raw(df, EmFundInfo.__table__.name)
            return True
        except Exception as e:
            print(e)
            traceback.print_exc()
            return False

    def em_fund_fee_history(self, date: str):
        fund_list = self._em_get_all_fund_list(date)
        if fund_list is None:
            return
        self.em_fund_fee(all_fund_list)

    @staticmethod
    def _lambda_fund_fee_1(x):
        if x.CODEFEEMODE.array[0] == CodeFeeMode.none:
            fee_type = 1
        else:
            fee_type = x.CODEFEEMODE.array[0].value
        data = c.css(','.join(x.index.to_list()), 'MANAGFEERATIO,CUSTODIANFEERATIO,PURCHFEERATIO,REDEMFEERATIO,SERVICEFEERATIO,SUBSCRFEERATIO', f'FeeType={fee_type},Ispandas=1')
        if not isinstance(data, pd.DataFrame):
            if data.ErrorCode != 0:
                print(f'failed to get fund code fee: {data.ErrorMsg}')
            return
        return data

    def em_fund_fee(self, fund_id_list: Set[str]):
        if not fund_id_list:
            return True
        try:
            data = c.css(','.join(fund_id_list), 'CODEFEEMODE', 'Ispandas=1')
            if not isinstance(data, pd.DataFrame):
                if data.ErrorCode != 0:
                    print(f'failed to get fund code fee mode: {data.ErrorMsg}')
                return False
            # 这里没有判断css的返回值
            data['CODEFEEMODE'] = data['CODEFEEMODE'].map({'前端': CodeFeeMode.a_type, '后端': CodeFeeMode.b_type, None: CodeFeeMode.none})
            data = data.groupby(by='CODEFEEMODE', sort=False).apply(EmRawDataDownloader._lambda_fund_fee_1).reset_index()
            data['CODEFEEMODE'] = data['CODEFEEMODE'].transform(lambda x: x.name)
            df = data.drop(columns='DATES').rename(columns=lambda x: EmFundFee.__getattribute__(EmFundFee, x).name)
            # 更新到db，先删再添，确保数据不会冲突，且有一个更新的机会
            # TODO: 最好原子提交下边两个操作
            RawDataApi().delete_em_fund_fee(df.em_id.to_list())
            self._data_helper._upload_raw(df, EmFundFee.__table__.name)
            return True
        except Exception as e:
            print(e)
            traceback.print_exc()
            return False

    def em_fund_benchmark_history(self, start_date: str, end_date: str):
        # 获取所有基金列表（含未成立、已到期）
        fund_list_result = c.sector('507010', end_date)
        if fund_list_result.ErrorCode != 0:
            print(f'failed to get all fund list: {fund_list_result.ErrorMsg}')
            return

        df = RawDataApi().get_em_tradedates(start_date, end_date)
        for row in df.itertuples(index=False):
            if self.em_fund_benchmark(row.TRADEDATES, fund_list_result.Codes):
                print(f'[em_fund_benchmark_history] {row.TRADEDATES} done')
            else:
                print(f'[em_fund_benchmark_history] {row.TRADEDATES} failed')
                break

    def em_fund_benchmark(self, end_date: str, fund_list):
        try:
            data = c.css(fund_list, 'BENCHMARK', f'EndDate={end_date},Ispandas=1')
            if not isinstance(data, pd.DataFrame):
                if data.ErrorCode != 0:
                    print(f'failed to get fund benchmark: {data.ErrorMsg}')
                return False
            data = data[data.notna().all(axis=1)]
            if data.empty:
                return True

            df = data.reset_index().rename(columns=lambda x: EmFundBenchmark.__getattribute__(EmFundBenchmark, x).name)
            df['datetime'] = end_date
            df['benchmark'] = df.benchmark.str.rstrip()
            # 获取当前的benchmark
            now_df = RawDataApi().get_em_fund_benchmark(end_date)
            if now_df is not None:
                # 过滤出来新增基金benchmark以及旧基金的benchmark发生变化的情况
                df = df.merge(now_df.drop(columns=['_update_time']), how='left', on=['em_id', 'benchmark'], indicator=True, validate='one_to_one')
                df = df[df._merge == 'left_only'].drop(columns=['_merge', 'datetime_y']).rename(columns={'datetime_x': 'datetime'})
            # 更新到db
            self._data_helper._upload_raw(df, EmFundBenchmark.__table__.name)
            return True
        except Exception as e:
            print(e)
            traceback.print_exc()
            return False

    def em_fund_rate(self, end_date: str):
        try:
            fund_list = c.sector('507013', end_date)
            fund_list = fund_list.Codes
            df=c.css(fund_list,"MKTCOMPRE3YRAT,MORNSTAR3YRAT,MORNSTAR5YRAT,MERCHANTS3YRAT,TXCOMRATRAT,SHSTOCKSTAR3YCOMRAT,SHSTOCKSTAR3YSTOCKRAT,SHSTOCKSTAR3YTIMERAT,SHSTOCKSTAR3YSHARPERAT,SHSTOCKSTAR5YCOMRATRAT,SHSTOCKSTAR5YSTOCKRAT,SHSTOCKSTAR5YTIMERAT,SHSTOCKSTAR5YSHARPRAT,JAJXCOMRAT,JAJXEARNINGPOWERRAT,JAJXACHIEVESTABILITYRAT,JAJXANTIRISKRAT,JAJXSTOCKSELECTIONRAT,JAJXTIMESELECTIONRAT,JAJXBENCHMARKTRACKINGRAT,JAJXEXCESSEARNINGSRAT,JAJXTOTALFEERAT",
                f"EndDate={end_date},Ispandas=1")
            df['DATES'] = datetime.datetime.strptime(end_date,'%Y%m%d').date()
            df = df.reset_index()
            self._data_helper._upload_raw(df, EMFundRate.__table__.name)
            return True
        except Exception as e:
            print(e)
            traceback.print_exc()
            return False

    def em_fund_asset(self, end_date: str):
        fund_list_df = RawDataApi().get_em_fund_list(end_date, limit=1)
        if fund_list_df is None:
            print(f'failed to get fund list for fund status')
            return False
        fund_list: List[str] = fund_list_df.all_live_fund_list.array[0].split(',')
        fund_list += fund_list_df.delisted_fund_list.array[0].split(',')

        start_year = 2010
        end_year = 2014
        res: List[pd.DataFrame] = []
        for year in range(start_year, end_year+1):
            for date in self._quarter_update_dates:
                dt = str(year) + date
                print(f'doing {dt}')
                data = c.css(fund_list, "PRTSTOCKTONAV,PRTBONDTONAV,PRTCASHTONAV,PRTOTHERTONAV,MMFFIRSTREPOTONAV,MMFAVGPTM", f"ReportDate={dt},Ispandas=1")
                data['DATES'] = dt
                res.append(data)
                print(f'{dt} done')
        df = pd.concat(res).reset_index()
        df = df[df.drop(columns=['CODES', 'DATES']).notna().any(axis=1)]
        self._data_helper._upload_raw(df, EMFundHoldAsset.__table__.name)

    def em_fund_industry(self, end_date: str):
        fund_list_df = RawDataApi().get_em_fund_list(end_date, limit=1)
        if fund_list_df is None:
            print(f'failed to get fund list for fund status')
            return False
        fund_list: List[str] = fund_list_df.all_live_fund_list.array[0].split(',')
        fund_list += fund_list_df.delisted_fund_list.array[0].split(',')

        res = []
        start_year = 2015
        end_year = 2019
        rank_list = [1, 2, 3]
        for year in range(start_year, end_year+1):
            for date in self._quarter_update_dates:
                dt = str(year) + date
                print(f'doing {dt}')
                _res = []
                for rank in rank_list:
                    data = c.css(fund_list, "PRTKEYINDNAME,PRTKEYINDTOASSET", f"ReportDate={dt},Rank={rank},IndustryCode=A,NewOldType=1,Ispandas=1")
                    data = data.rename(columns={'PRTKEYINDNAME':f'rank{rank}_indname','PRTKEYINDTOASSET':f'rank{rank}_indweight'})
                    data = data.drop(columns='DATES')
                    _res.append(data)
                df = pd.concat(_res, axis=1)
                df['DATES'] = dt
                res.append(df)
                print(f'{dt} done')
        df = pd.concat(res).reset_index()
        df = df[df.drop(columns=['CODES', 'DATES']).notna().any(axis=1)]
        self._data_helper._upload_raw(df, EMFundHoldIndustry.__table__.name)

    def em_fund_stock_history(self, fund_stock_path: str, report_date: str):
        df: pd.DataFrame = pd.read_excel(fund_stock_path, na_values='——')
        df = df[df['证券名称'].notna()]
        df = df.drop(columns='证券名称')

        columns_name = ['CODES'] + ['rank'+str(i+1)+'_stock'+suffix for suffix in ('', '_code', 'val', 'weight') for i in range(10)]
        assert len(columns_name) == df.shape[1], 'len of columns name should be equal with columns number of df'
        df = df.set_axis(columns_name, axis=1)
        df['DATES'] = report_date
        em._data_helper._upload_raw(df, EMFundHoldStock.__table__.name)

    def em_fund_stock(self):
        all_fund = c.sector('507013', '20200719').Codes
        dt_list = ['20191231','20200331','20200630']
        res = []
        rank_list = [i for i in range(1,11,1)]
        for dt in dt_list:
            _res = [] 
            for rank in rank_list:
                data=c.css(all_fund,"PRTKEYSTOCKNAME,PRTKEYSTOCKCODE,PRTKEYSTOCKVALUE,PRTKEYSTOCKTONAV",f"ReportDate={dt},Rank={rank},Ispandas=1")
                data = data.rename(columns={'PRTKEYSTOCKNAME': f'rank{rank}_stock',
                                            'PRTKEYSTOCKCODE': f'rank{rank}_stock_code',
                                            'PRTKEYSTOCKVALUE': f'rank{rank}_stockval',
                                            'PRTKEYSTOCKTONAV': f'rank{rank}_stockweight',
                                            })
                data = data.drop('DATES',axis=1)
                _res.append(data)
                print(f'[em_fund_stock] {dt} rank {rank} done')
            df = pd.concat(_res,axis=1)
            df['DATES'] = dt
            res.append(df)
        df = pd.concat(res).reset_index()
        self._data_helper._upload_raw(df, 'em_fund_stock')

    def em_fund_bond_history(self, fund_bond_path: str, report_date: str):
        df: pd.DataFrame = pd.read_excel(fund_bond_path, na_values='——')
        df = df[fund_bond['证券名称'].notna()]
        df = df.drop(columns='证券名称')

        columns_name = ['CODES'] + ['rank'+str(i+1)+'_bond'+suffix for suffix in ('', '_code', 'val', 'weight') for i in range(10)]
        assert len(columns_name) == df.shape[1], 'len of columns name should be equal with columns number of df'
        df = df.set_axis(columns_name, axis=1)
        df['DATES'] = report_date
        em._data_helper._upload_raw(df, EMFundHoldBond.__table__.name)

    def em_mng_info_history(self,path):
        col_dic = {'基金经理':'mng_name', 
            '代码': 'code', 
            '名称':'desc_name', 
            '在管基金规模(亿元)':'fund_size', 
            '任职日期':'start_date',
            '任职天数':'work_days', 
            '任职以来回报(%)':'his_ret',
            '任职以来年化回报(%)':'his_annual_ret', 
            '业绩比较基准':'benchmark', 
            '基金类型':'fund_type', 
            '管理公司':'company_name', 
            '共同任职经理':'coworkers', 
            '基金经理年限':'mng_work_year', 
            '任职基金数':'worked_funds_num',
            '任职基金公司数':'worked_funds_num', 
            '任职基金几何总回报(%)':'fund_total_geo_ret', 
            '几何平均年化收益率(%)':'geo_annual_ret', 
            '算术平均年化收益率(%)':'cal_annual_ret', 
            '性别':'gender', 
            '出生年份':'birth_year',
            '年龄':'age',
            '学历':'education', 
            '国籍':'nationality', 
            '简历':'resume', 
            '最早任职基金经理日期':'start_mng_date'}
        df = pd.read_excel(path, header=1).dropna(axis=0)
        df = df.rename(columns = col_dic)
        df = df.replace('——',np.NaN)
        em._data_helper._upload_raw(df,EMMngInfo.__table__.name)

    def em_fund_mng_change_history(self, path):
        col_dic = {
            '代码':'code', 
            '名称':'desc_name', 
            '现任基金经理':'mng_now', 
            '现任经理最新任职日期':'mng_now_start_date', 
            '最早任职基金经理':'mng_begin', 
            '最早任职基金经理日期':'mng_begin_date',
            '现任基金经理年限':'mng_now_work_year', 
            '同类型基金现任基金经理年限均值':'same_type_fund_work_year', 
            '已离任基金经理':'resign_mngs', 
            '历任基金经理人数':'total_mng_num', 
            '历任基金经理人均任职年限':'total_mng_avg_work_year',
            '投资类型':'fund_type',
            '管理公司':'company', 
            '监管辖区':'region'
        }
        df = pd.read_excel(path, header=0).dropna(axis=0)
        df = df.rename(columns = col_dic)
        df = df.replace('——',np.NaN)
        df = df.drop_duplicates('code') # 发现有重复的数据 比如 codes = 000063.OF
        em._data_helper._upload_raw(df,EMFundMngChange.__table__.name)

    def em_fund_comp_mng_change_history(self, path):
        col_dic = {
            '基金公司':'company',
            '基金经理数':'total_mng_num',
            '基金经理平均年限':'mng_avg_year',
            '基金经理最大年限':'mng_max_year',
            '团队稳定性':'team_stability',
            '新聘基金经理数':'new_mng_num',
            '离职基金经理数':'resign_mng_num',
            '基金经理变动率(%)':'mng_turnover_rate',
            '1年以内':'exp_less_than_1',
            '1-2年':'exp_1_to_2',
            '2-3年':'exp_2_to_3',
            '3-4年':'exp_3_to_4',
            '4年以上':'exp_more_than_4',
        }
        df = pd.read_excel(path, header=1).dropna(axis=0)
        df = df.rename(columns = col_dic)
        df = df.replace('——',np.NaN)
        em._data_helper._upload_raw(df,EMFundCompMngChange.__table__.name)

    def em_fund_com_core_mng_history(self, path):
        col_dic = {
            '基金代码':'code',
            '基金名称':'desc_name',
            '本基金离职基金经理人数':'fund_resign_mng_num',
            '所属基金公司':'company',
            '基金公司基金经理数':'com_mng_num',
            '基金公司离职基金经理数':'com_resign_mng_num',
            '基金公司基金经理离职率(%)':'com_resign_mng_rate',
            '基金公司核心人员人数':'com_core_mng_num',
            '基金公司核心人员离职人数':'com_core_mng_resign_num',
            '基金公司核心人员离职率(%)':'com_core_mng_resign_rate',
            '投资类型':'fund_type',
            '监管区域':'region'
        }
        df = pd.read_excel(path, header=1).dropna(axis=0)
        df = df.rename(columns = col_dic)
        df = df.replace('——',np.NaN)
        df = df.drop_duplicates('code') # 发现有重复的数据 比如 codes = 000424.OF
        em._data_helper._upload_raw(df,EMFundCompCoreMng.__table__.name)

    def em_fund_bond(self):
        all_fund = c.sector('507013', '20200719').Codes
        fund_list = all_fund
        dt_list = ['20191231','20200331','20200630']
        res = []
        rank_list = [i for i in range(1,11,1)]
        for dt in dt_list:
            print(f'doing {dt}')
            _res = [] 
            for rank in rank_list:
                data=c.css(fund_list,"PRTKEYBONDNAME,PRTKEYBONDCODE,PRTKEYBONDVALUE,PRTKEYBONDTONAV",f"ReportDate={dt},Rank={rank},Ispandas=1")
                data = data.rename(columns={'PRTKEYBONDNAME':f'rank{rank}_bond','PRTKEYBONDCODE':f'rank{rank}_bond_code','PRTKEYBONDVALUE':f'rank{rank}_bondval','PRTKEYBONDTONAV':f'rank{rank}_bondweight'})
                data = data.drop('DATES',axis=1)
                _res.append(data)
            df = pd.concat(_res,axis=1)
            df['DATES'] = dt
            res.append(df)
            print(f'{dt} done')
        df = pd.concat(res).reset_index()
        em._data_helper._upload_raw(df, EMFundHoldBond.__table__.name)

    def download_all(self, start_date, end_date):
        failed_tasks = []
        # If em_tradedates fails, there is no trading day between start_date and end_date
        # Stop and return
        if not self.em_tradedates(start_date, end_date):
            failed_tasks.append('em_tradedates')
            return failed_tasks

        # could only update the end_date's data
        if not self.em_fund_status(end_date):
            failed_tasks.append('em_fund_status')

        if not self.em_fund_nav(start_date, end_date):
            failed_tasks.append('em_fund_nav')

        index_info_df = BasicDataApi().get_index_info()
        if index_info_df is None:
            failed_tasks.append('retrieve data for em_index_price')
        else:
            index_info_df = index_info_df[index_info_df.price_source == IndexPriceSource.default]
            index_ids = set(index_info_df.em_id.to_list())
            index_ids.discard(None)
            if not self.em_index_price(index_ids, start_date, end_date):
                failed_tasks.append('em_index_price')

        if not self.em_stock_info(end_date):
            failed_tasks.append('em_stock_info')

        if not self.em_stock_price(start_date, end_date):
            failed_tasks.append('em_stock_price')

        if not self.em_stock_post_price(start_date, end_date):
            failed_tasks.append('em_stock_post_price')

        if not self.em_index_val(start_date, end_date):
            failed_tasks.append('em_index_val')

        if not self.em_stock_daily_info(start_date, end_date):
            failed_tasks.append('em_stock_daily_info')

        if not self.em_index_component(start_date, end_date):
            failed_tasks.append('em_index_component')

        if not self.em_fund_list(start_date, end_date):
            failed_tasks.append('em_fund_list')
        else:
            new_fund_list, _ = RawDataHelper.get_new_and_delisted_fund_list(end_date)
            if new_fund_list is None:
                failed_tasks.append('get new_fund_list')
            else:
                if not self.em_fund_info(new_fund_list):
                    failed_tasks.append('em_fund_info')
                if not self.em_fund_fee(new_fund_list):
                    failed_tasks.append('em_fund_fee')
                # if not self.em_fund_benchmark(end_date, new_fund_list):
                #     failed_task.append('em_fund_benchmark')

        if not self.em_macroeconomic_price(start_date, end_date):
            failed_tasks.append('em_macroeconomic_price')

        if not self.em_fund_rate(end_date):
            failed_tasks.append('em_fund_rate')

        return failed_tasks


if __name__ == '__main__':
    em = EmRawDataDownloader(RawDataHelper())
    # em.em_tradedates('20000101', '20091231')
    # em.em_index_val('20200428', '20200428')
    # em.em_fund_nav('20200415', '20200427')
    # em.em_index_price_history('H00140.SH', '20050101', '20200419')
    # em.em_fund_scale_history()
    # em.em_stock_fin_fac('20161231')
    # em.em_stock_info('20200424')
    # em.em_stock_price('20041231', '20041231')
    # em.em_stock_post_price('20041231', '20041231')
    # em.em_stock_daily_info('20041231', '20041231')
    # em.em_stock_price_history('./')
    # em.em_stock_post_price_history('./')
    # em.em_stock_daily_info_history('./')
    # em.em_stock_refinancing('20170101', '20181231')
    # em.add_columns_to_fin_fac('20190930')
    # em.em_fund_status('20200513')
    # em.em_index_component('20200528', '20200529')
    # em.em_fund_list('20200702', '20200702')
    # em.em_fund_info_history('20200707')
    # em.em_fund_benchmark_history('20130320', '20131231')
    # em.em_index_info(['399972.SZ'])
    # em.em_fund_info({'165807.SZ'})
    # em.em_stock_estimate_fac('20200101', '20200709', 2020)
    # em.cs_index_component('20200713')
    # em.em_macroeconomic_price('20200714', '20200714')
    # em.em_fund_fee_history('20200715')
    # em.em_fund_asset('20200819')
    # em.em_fund_holding_rate_history('20200819')
