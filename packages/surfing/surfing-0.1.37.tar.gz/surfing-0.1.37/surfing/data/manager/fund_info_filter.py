from typing import List
import pandas as pd

# 回测底层基金黑名单，筛掉没有办法处理的问题基金 2020-05-30
## #摘牌基金 发生大额申赎，导致净值剧烈波动， 用东财机构持有权重数据无法过滤
##'020035!0': 国泰上证5年期国债ETF联接A  '020036!0' 国泰上证5年期国债ETF联接C
BLACK_SHEEP = ['020035!0', '020036!0']

#基金基准发生改变  2020-06-22
##'320014!0':诺安沪深300指数增强   '050021!0':‘博时创业版ETF联接A 
BLACK_SHEEP.extend(['320014!0', '050021!0'])

#基金类别改变 2020-06-30
## ‘000512!0’: '国泰沪深300指数增强A'   曾用名 国泰结构转型
BLACK_SHEEP.extend(['000512!0'])

#基金类别改变 2020-07-14
## ‘001879!0’: '长城创业板指数增强A'   曾用名 长城创新动力灵活配置混合基金
BLACK_SHEEP.extend(['001879!0'])

#基金类别改变 2020-07-27
## ’519034!0' "海富通中证500增强" 曾用名 海富通中证低碳
BLACK_SHEEP.extend(['519034!0'])

# 发生净值突变的分级基金 属于放宽国债tag，加入信用债下的基金  2020-06-22
## 向上波动 '164210!1': 天弘同利分级, '164703!1': 汇添富互利分级 ,
## 向下波动 '000428!0' : 易方达聚盈分级
BLACK_SHEEP.extend(['164210!1','164703!1', '000428!0'])

# 没有办法筛选掉，早期终止 2020-06-30
## 000169!1 泰达宏利高票息A
## 000022!0 南方中债中期票据A
BLACK_SHEEP.extend(['000169!1','000022!0'])

EHR_PROBLEM_EKYWORDS = {
    'E': ['ETF', 'REITs', 'ESG', 'CES'],
    'H': ['H股', 'A-H50', '50AH', '中证AH'],
    'R': ['REITs'],
}

# 绝对收益基金关键字
ALPHA_FUND_KEY_WORD = ['对冲策略','阿尔法','绝对收益','对冲套利','量化收益']
ALPHA_PATTEN = '|'.join(ALPHA_FUND_KEY_WORD)

def filter_fund_info(fund_info: pd.DataFrame, index_list: List[str], is_normal_type: bool=False, is_mix_type: bool=False) -> pd.DataFrame:
    # 去掉基金份额 E类 H类 R类
    # E类 指定代销机构对基金
    # H类 基金场内上市份额
    # R类 对特定投资群体进行发售，特定群体指基本养老保险基金，企业年金计划筹集的资金等
    ehr_funds = []
    # 这里itertuples会比iterrows快1个数量级
    for r in fund_info[['desc_name', 'fund_id']].itertuples():
        for type_word, problem_words in EHR_PROBLEM_EKYWORDS.items():
            i = r.desc_name
            for problem_i in problem_words:
                i = i.replace(problem_i, '')
            if type_word in i:
                ehr_funds.append(r.fund_id)

    no_mmf_index = set(index_list) - set(['mmf'])
    fund_info = fund_info[
        (
            fund_info.index_id.isin(no_mmf_index)
            # 只选非分级基金
            & ((fund_info.structure_type == 0))
            # 去掉etf基金
            & (fund_info.is_etf != 1)
            # 只选择人民币支付的基金
            & (fund_info.currency == 'CNY')
            # 只选择开放式基金，去掉封闭式基金
            & (fund_info.is_open == 1)
            # 去掉基金份额类型是 E H R
            & (~fund_info.fund_id.isin(ehr_funds))
            # 去掉超短债类型的基金，国债tag下 13只
            & (~fund_info.desc_name.str.contains('超短债'))
            # 去掉短期融资债 10只
            & (~fund_info.desc_name.str.contains('短融')) 
            # 去掉双债型债券  双债多含可转债 共41只
            & (~fund_info.desc_name.str.contains('双债'))
            # 去掉短期纯债型基金
            & (fund_info.wind_class_2 != '短期纯债型基金')
            # 货币基金总共1000多只，fund indicator 计算压力大，当前人工用2020年5月的货币基金规模取了前50只作为 货币基金池
            | (fund_info.is_selected_mmf == 1)
            # 增加绝对收益型基金 17只
            | (fund_info.desc_name.str.contains(ALPHA_PATTEN))
        )
        & (~fund_info.fund_id.isin(BLACK_SHEEP))
    ].copy()
    
    if not is_normal_type:
        fund_info = fund_info[~(fund_info.wind_class_2 == '普通股票型基金')].copy()
    if not is_mix_type:
        fund_info = fund_info[~(fund_info.wind_class_2 == '偏股混合型基金')].copy()

    return fund_info

def fund_info_update(fund_info: pd.DataFrame):
    #增加绝对收益 到货币型基金 38只
    mmf_exp_fund_list = fund_info[fund_info.desc_name.str.contains(ALPHA_PATTEN)].index.tolist()
    fund_info.loc[mmf_exp_fund_list,'index_id'] = 'mmf'
    
    #国债类扩容
    fund_info.loc[fund_info.national_debt_extension == 1, 'index_id'] = 'national_debt'
            
    #增加港股基金 基准1含有恒生 共69只
    hsi_fund = []
    for r in fund_info.itertuples():
        if (r.benchmark_1) and ('恒生' in r.benchmark_1):
            hsi_fund.append(r.fund_id)
    fund_info.loc[fund_info.fund_id.isin(hsi_fund), 'index_id_new'] = 'hsi'

    #增加混合债型一级基金 到国债下，共271 （混合一级含股票， 股灾时mdd会扩大，还是考虑排除）
    #hybrid_class_1_funds = fund_info[fund_info['wind_class_2'] == '混合债券型一级基金'].fund_id.to_list()
    #fund_info.loc[fund_info.fund_id.isin(hybrid_class_1_funds), 'index_id_new'] = 'national_debt'
    fund_info.loc[:,'index_id'] = fund_info['index_id_new']

    return fund_info