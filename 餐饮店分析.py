# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import warnings
warnings.filterwarnings("ignore")

from bokeh.plotting import figure,show,output_file
from bokeh.models import ColumnDataSource

'''
(1)加载数据
'''

import os
os.chdir('/Users/wanmeng/Desktop/Python数据分析_项目资料/项目01城市餐饮店铺分析')
df1=pd.read_excel('上海餐饮数据.xlsx')

'''
(2)计算口味，客单价，性价比指标
'''
data1 = df1[['类别','口味','环境','服务','人均消费']]
data1.dropna(inplace = True)
data1 = data1[(data1['口味']>0) & (data1['人均消费']>0)]
data1['性价比'] = (data1['口味'] + data1['环境'] + data1['服务'])/data1['人均消费']
#数据清洗+性价比计算


def f1():
    fig,axes = plt.subplots(1,3,figsize = (10,4))
    data1.boxplot(column = ['口味'],ax = axes[0])
    data1.boxplot(column = ['人均消费'],ax = axes[1])
    data1.boxplot(column = ['性价比'],ax = axes[2])
#创建函数1:制作箱型图，查看异常值

def f2(data,col):
    q1 = data[col].quantile(q = 0.25)
    q3 = data[col].quantile(q = 0.75)
    iqr = q3 - q1
    t1 = q1 - 3*iqr
    t2 = q3 + 3*iqr
    return data[(data[col]>t1)&(data[col]<t2)][['类别',col]]
#创建函数2，清除异常值

data_kw = f2(data1,'口味')
data_rj = f2(data1,'人均消费')
data_xjb = f2(data1,'性价比')

def f3(data,col):
    col_name = col + '_norm'
    data_gp = data.groupby('类别').mean()
    data_gp[col_name] = (data_gp[col] - data_gp[col].min())/(data_gp[col].max()-data_gp[col].min())
    data_gp.sort_values(by = col_name, inplace = True, ascending = False)
    return data_gp
#创建函数3，标准化指标并排序

data_kw_score = f3(data_kw,'口味')
data_rj_score = f3(data_rj,'人均消费')
data_xjb_score = f3(data_xjb,'性价比')
#指标标准化得分

data_final_q1 = pd.merge(data_kw_score,data_rj_score,left_index = True,right_index = True)
data_final_q1 = pd.merge(data_final_q1,data_xjb_score,left_index = True,right_index = True)
#数据合并

'''
(3)绘制图表。辅助分析
'''
from bokeh.layouts import gridplot
from bokeh.models import HoverTool
from bokeh.models.annotations import BoxAnnotation

output_file('餐饮店分析图形.html')

data_final_q1['size'] = data_final_q1['口味_norm'] * 40
data_final_q1.index.name = 'type'
data_final_q1.columns = ['kw','kw_norm','price','price_norm','xjb','xjb_norm','size']
#将列名改为英文

source = ColumnDataSource(data_final_q1)
# 创建数据

hover = HoverTool(tooltips = [
                              ('餐饮类型','@type'),
                              ('人均消费','@price'),
                              ('性价比得分','@xjb_norm'),
                              ('口味得分','@kw_norm')
                              ])


result = figure(plot_width = 800,plot_height = 300,title = '餐饮类型得分',
                x_axis_label='人均消费',y_axis_label='性价比得分',
                tools = [hover,'box_select,reset,xwheel_zoom,pan,crosshair'])
result.circle(x = 'price',y = 'xjb_norm',source = source,
              line_color='black',line_dash = [6,4],fill_alpha=0.6,size = 'size')
price_mid = BoxAnnotation(left = 40,right = 80,fill_alpha = 0.1,fill_color = 'navy')
result.add_layout(price_mid)
#散点图

data_type = data_final_q1.index.tolist()

kw = figure(plot_width = 800,plot_height = 300,title = '口味得分',
                x_range= data_type,
                tools = [hover,'box_select,reset,xwheel_zoom,pan,crosshair'])
kw.vbar(x = 'type', top = 'kw_norm',source = source,
        width = 0.8, alpha = 0.7, color = 'red')
#柱状图1

price = figure(plot_width = 800,plot_height = 300,title = '人均消费得分',
                x_range = data_type,
                tools = [hover,'box_select,reset,xwheel_zoom,pan,crosshair'])
price.vbar(x = 'type', top = 'price_norm',source = source,
        width = 0.8, alpha = 0.7, color = 'green')
 #柱状图2
 
p = gridplot([[result],[kw],[price]])
 
show(p)
 
 





    
    


print("finished")
