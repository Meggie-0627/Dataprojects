#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  1 16:31:56 2020

@author: wanmeng
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import warnings
warnings.filterwarnings("ignore")

from bokeh.plotting import figure,show,output_file
from bokeh.models import ColumnDataSource

'''
(1)导入数据
'''

import os
os.chdir('/Users/wanmeng/Desktop/Python数据分析_项目资料/项目02电商打折分析')
#工作路径

df = pd.read_excel('双十一淘宝美妆数据.xlsx')
df.fillna(0,inplace = True)
df.index = df['update_time']
df['date'] = df.index.day
#记载数据，提取销售日期


'''
(2)双十一当天在售的商品占比情况
'''
data1 = df[['id','title','店名','date']]
#筛选数据

d1 = data1[['id','date']].groupby(by = 'id').agg(['min','max'])['date']
#统计不同商品的销售开始，结束时间

id_11 = data1[data1['date'] == 11]['id']
d2 = pd.DataFrame({'id':id_11,'双十一当天是否售卖':True})
#双十一当天售卖商品的id

id_data = pd.merge(d1,d2,left_index = True,right_on = 'id',how = 'left')
id_data.fillna(False,inplace = True)
#合并数据

m = len(d1)
m_11 = len(id_11)
m_pre = m_11/m
print('双十一当天参加活动的商品为%i个，占比为%.2f%%'%(m_11,m_pre*100))

'''
(3)商品销售节奏分类
'''

id_data['type'] = '待分类'
id_data['type'][(id_data['min']<11)&(id_data['max']>11)] = 'A'
id_data['type'][(id_data['min']<11)&(id_data['max']==11)] = 'B'
id_data['type'][(id_data['min']==11)&(id_data['max']>11)] = 'c'
id_data['type'][(id_data['min']==11)&(id_data['max']==11)] = 'D'
id_data['type'][id_data['双十一当天是否售卖']==False] = 'F'
id_data['type'][id_data['max']<11] = 'E'
id_data['type'][id_data['min']>11] = 'G'
#销售节凑分类

result1 = id_data['type'].value_counts()
result1 = result1.loc[result1.index.intersection(['A','B','C','D','E','F','G'])]
#计算不同类别的商品数量

from bokeh.palettes import brewer
colori = brewer['YlGn'][7]
plt.axis('equal')
plt.pie(result1,labels = result1.index,autopct = '%.2f%%',colors = colori,
        startangle = 90,radius = 1.5,counterclock = False)


print('finished')