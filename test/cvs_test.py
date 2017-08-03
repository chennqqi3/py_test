
# coding: utf-8

# In[ ]:

import pandas as pd
import numpy as np
import json
import datetime
import time
import random


def build_zf():
    fields='secID,tradeDate,closePrice,preClosePrice'
    df_stkchose = pd.read_csv('stk_choose.txt')
    df_stkchose['stkcd']=df_stkchose['stkcd'].apply(lambda xx: str(int(xx)+1000000)[1:])
    df_stkchose['stkcd']=df_stkchose['stkcd'].apply(lambda xx:  xx + ('.XSHG' if xx[0]=='6' else ".XSHE"))
    df_stkchose['zhangfu']=np.NAN
    df_stkchose['bid_week']= df_stkchose['bid_day'].apply(lambda xx: datetime.date(int(xx[:4]), int(xx[5:7]), int(xx[8:10])).isocalendar()[1] )
    for ii in df_stkchose.index:
        secID = df_stkchose.loc[ii]['stkcd']
        trDate = df_stkchose.loc[ii]['bid_day']
        df_factor=get_price([secID], datetime.datetime.today()-datetime.timedelta(days=60),end_date= datetime.datetime.today(),fields=['ClosingPx','OpeningPx'])
        df_factor['closePrice']=df_factor['ClosingPx']
        df_factor_b1 = df_factor.shift(1)
        df_factor['preClosePrice'] = df_factor_b1['closePrice']
        df_factor['zhangfu'] = df_factor['closePrice']/ df_factor['preClosePrice']*100-100
        if df_factor.empty:continue
        df_stkchose.at[ii,'zhangfu'] = df_factor.loc[trDate]['zhangfu']

    #     print(df_stkchose)

    df_stkchose.index = df_stkchose['bid_day']
    df_stkchose.sort_index(inplace=True)
    df_stkchose['rank']=np.NAN
    for bid_day in np.unique(df_stkchose.index):
        df_day = df_stkchose.loc[bid_day]
        df_day['rank'] =df_stkchose.loc[bid_day]['zhangfu'].rank()
        df_stkchose.loc[bid_day] =df_day
    #         print (df_day)

    df_stkchose= df_stkchose.fillna(0)
    print (df_stkchose)

    df_srt= df_stkchose.groupby(['user','bid_week']).aggregate(np.sum)
    df_srt['bid_week'] = df_srt.index.get_level_values(1)
    #     print (df_srt)
    print (df_srt.sort_values(by=['bid_week','rank'],ascending=False))
    print (df_srt.sort_values(by=['bid_week','rank'],ascending=False)[0])


build_zf()

