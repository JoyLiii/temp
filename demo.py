# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 15:07:55 2020

@author: 2007043
"""

## 主要呈現的程式
## target life爬取資料時間較久

from flask import Flask, render_template, request

## 引入所需的py檔
from scheduling import *
from monte_carlo import *
from ACO import *
from PSO import *
from tabu_search import *
from GA import *
from database import *

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import base64
from machine_plot import *
from TLdata import *


app = Flask(__name__)


PEP1 = ['GL-SPT','RS','GL-IEX','CD01', 'GL-WMA','CD01']
PEP2 = ['AS-CVD','THK_SiNx','AS-IEX','CD01','AS-RIE','CD01']   #02的產品
#PEP2 = ['AS-CVD','THK_SiNx','AS-IEX','CD01','AS-IEX','CD01']    #01的產品
PEP3 = ['SL-SPT','RS','SL-IEX','CD01','SL-WMA','CD01']
PEP4 = ['PX1-SPT','RS','PX1-IEX','CD01','PX1-WTO','CD01']
PEP5 = ['PV-CVD','THK_PV','TH-IEX','CD01','TH-RIE','CD01']
PEP6 = ['PX2-SPT','RS','PX2-IEX','CD01','PX2-WTO','CD01']

## machine呈現的顏色
c1 = (250, 235, 215)
c2 = (176, 224, 230)
c3 = (255, 192, 203)

@app.route('/')
def login():
     ## 輸入資料
     return render_template('index.html')


@app.route('/input', methods=['POST'])
def result():

    if request.method == 'POST':
        
        ## 讀入使用者所需的資料
        product = request.values['product']
        date = request.values['last_time']
        end_date = request.values['end_time']
        
        tabu = request.values['tabu']
        
        ## target life的臨界值
        threshold = request.values['threshold']
        threshold = int(threshold)
        
        ## 是否需要TF資料
        TF = request.values['choose']
        
        ## target life的資料限制
        if TF == 'No':
            SL_TF_frame, SL_TF_tabu = [] , []
            GL_TF_frame, GL_TF_tabu = [], []
        else:
            SL_TF_frame, SL_TF_tabu = get_TF_tabu(PEP1[0], threshold)
            GL_TF_frame, GL_TF_tabu = get_TF_tabu(PEP3[0], threshold)
        
        # PEP1
        thin1 = dataprocessing(date, end_date, PEP1[0], product, PEP1[1], tabu, SL_TF_tabu, GL_TF_tabu)
        photo1 = dataprocessing(date, end_date, PEP1[2], product , PEP1[3], tabu, SL_TF_tabu, GL_TF_tabu)
        etch1 = dataprocessing(date, end_date, PEP1[4], product , PEP1[5], tabu, SL_TF_tabu, GL_TF_tabu)
        
        # PEP2
        thin2 = dataprocessing(date, end_date, PEP2[0], product, PEP2[1], tabu, SL_TF_tabu, GL_TF_tabu)
        photo2 = dataprocessing(date, end_date, PEP2[2], product , PEP2[3], tabu, SL_TF_tabu, GL_TF_tabu)
        etch2 = dataprocessing(date, end_date, PEP2[4], product , PEP2[5], tabu, SL_TF_tabu, GL_TF_tabu)
        
        # PEP3
        thin3 = dataprocessing(date, end_date, PEP3[0], product, PEP3[1], tabu, SL_TF_tabu, GL_TF_tabu)
        photo3 = dataprocessing(date, end_date, PEP3[2], product , PEP3[3], tabu, SL_TF_tabu, GL_TF_tabu)
        etch3 = dataprocessing(date, end_date, PEP3[4], product , PEP3[5], tabu, SL_TF_tabu, GL_TF_tabu)
        
        # PEP4
        thin4 = dataprocessing(date, end_date, PEP4[0], product, PEP4[1], tabu, SL_TF_tabu, GL_TF_tabu)
        photo4 = dataprocessing(date, end_date, PEP4[2], product , PEP4[3], tabu, SL_TF_tabu, GL_TF_tabu)
        etch4 = dataprocessing(date, end_date, PEP4[4], product , PEP4[5], tabu, SL_TF_tabu, GL_TF_tabu)
        
        # PEP5
        thin5 = dataprocessing(date, end_date, PEP5[0], product, PEP5[1], tabu, SL_TF_tabu, GL_TF_tabu)
        photo5 = dataprocessing(date, end_date, PEP5[2], product , PEP5[3], tabu, SL_TF_tabu, GL_TF_tabu)
        etch5 = dataprocessing(date, end_date, PEP5[4], product , PEP5[5], tabu, SL_TF_tabu, GL_TF_tabu)
        
        # PEP6
        thin6 = dataprocessing(date, end_date, PEP6[0], product, PEP6[1], tabu, SL_TF_tabu, GL_TF_tabu)
        photo6 = dataprocessing(date, end_date, PEP6[2], product , PEP6[3], tabu, SL_TF_tabu, GL_TF_tabu)
        etch6 = dataprocessing(date, end_date, PEP6[4], product , PEP6[5], tabu, SL_TF_tabu, GL_TF_tabu)

    
        start = ['start']
        P1M1 = list(thin1.index)
        P1M2 = list(photo1.index)
        P1M3 = list(etch1.index)
        
        P2M1 = list(thin2.index)
        P2M2 = list(photo2.index)
        P2M3 = list(etch2.index)
        
        P3M1 = list(thin3.index)
        P3M2 = list(photo3.index)
        P3M3 = list(etch3.index)
        
        P4M1 = list(thin4.index)
        P4M2 = list(photo4.index)
        P4M3 = list(etch4.index)
        
        P5M1 = list(thin5.index)
        P5M2 = list(photo5.index)
        P5M3 = list(etch5.index)
        
        P6M1 = list(thin6.index)
        P6M2 = list(photo6.index)
        P6M3 = list(etch6.index)
        
        w1 = float(request.values['w1'])
        w2 = float(request.values['w2'])
        w3 = float(request.values['w3'])
        w4 = float(request.values['w4'])
        w5 = float(request.values['w5'])
        w6 = float(request.values['w6'])
        w7 = float(request.values['w7'])
        w8 = float(request.values['w8'])
        w9 = float(request.values['w9'])
        
        
        machine_list1, best_machine_1, best_ca_value_1, best_u_value_1, best_DD_value_1, worst_machine_1, worst_ca_value_1, worst_u_value_1, worst_DD_value_1 = scheduling_main(thin1, photo1, etch1, w1, w2, w3, w4, w5, w6, w7, w8, w9)
        machine_list2, best_machine_2, best_ca_value_2, best_u_value_2, best_DD_value_2, worst_machine_2, worst_ca_value_2, worst_u_value_2, worst_DD_value_2 = scheduling_main(thin2, photo2, etch2, w1, w2, w3, w4, w5, w6, w7, w8, w9)
        machine_list3, best_machine_3, best_ca_value_3, best_u_value_3, best_DD_value_3, worst_machine_3, worst_ca_value_3, worst_u_value_3, worst_DD_value_3 = scheduling_main(thin3, photo3, etch3, w1, w2, w3, w4, w5, w6, w7, w8, w9)
        machine_list4, best_machine_4, best_ca_value_4, best_u_value_4, best_DD_value_4, worst_machine_4, worst_ca_value_4, worst_u_value_4, worst_DD_value_4 = scheduling_main(thin4, photo4, etch4, w1, w2, w3, w4, w5, w6, w7, w8, w9)
        machine_list5, best_machine_5, best_ca_value_5, best_u_value_5, best_DD_value_5, worst_machine_5, worst_ca_value_5, worst_u_value_5, worst_DD_value_5 = scheduling_main(thin5, photo5, etch5, w1, w2, w3, w4, w5, w6, w7, w8, w9)
        machine_list6, best_machine_6, best_ca_value_6, best_u_value_6, best_DD_value_6, worst_machine_6, worst_ca_value_6, worst_u_value_6, worst_DD_value_6 = scheduling_main(thin6, photo6, etch6, w1, w2, w3, w4, w5, w6, w7, w8, w9)
        select_1, MC_Ca_value_1, MC_u_value_1, MC_DD_value_1 = MC_main(thin1, photo1, etch1, w1, w2, w3, w4, w5, w6, w7, w8, w9)
        select_2, MC_Ca_value_2, MC_u_value_2, MC_DD_value_2 = MC_main(thin2, photo2, etch2, w1, w2, w3, w4, w5, w6, w7, w8, w9)
        select_3, MC_Ca_value_3, MC_u_value_3, MC_DD_value_3 = MC_main(thin3, photo3, etch3, w1, w2, w3, w4, w5, w6, w7, w8, w9)
        select_4, MC_Ca_value_4, MC_u_value_4, MC_DD_value_4 = MC_main(thin4, photo4, etch4, w1, w2, w3, w4, w5, w6, w7, w8, w9)
        select_5, MC_Ca_value_5, MC_u_value_5, MC_DD_value_5 = MC_main(thin5, photo5, etch5, w1, w2, w3, w4, w5, w6, w7, w8, w9)
        select_6, MC_Ca_value_6, MC_u_value_6, MC_DD_value_6 = MC_main(thin6, photo6, etch6, w1, w2, w3, w4, w5, w6, w7, w8, w9)
        path, M_path_1, minn1_1, minn2_1, minn3_1 = ACO_main(thin1, photo1, etch1, w1, w2, w3, w4, w5, w6, w7, w8, w9)
        path, M_path_2, minn1_2, minn2_2, minn3_2 = ACO_main(thin2, photo2, etch2, w1, w2, w3, w4, w5, w6, w7, w8, w9)
        path, M_path_3, minn1_3, minn2_3, minn3_3 = ACO_main(thin3, photo3, etch3, w1, w2, w3, w4, w5, w6, w7, w8, w9)
        path, M_path_4, minn1_4, minn2_4, minn3_4 = ACO_main(thin4, photo4, etch4, w1, w2, w3, w4, w5, w6, w7, w8, w9)
        path, M_path_5, minn1_5, minn2_5, minn3_5 = ACO_main(thin5, photo5, etch5, w1, w2, w3, w4, w5, w6, w7, w8, w9)
        path, M_path_6, minn1_6, minn2_6, minn3_6 = ACO_main(thin6, photo6, etch6, w1, w2, w3, w4, w5, w6, w7, w8, w9)
        GA_machine_list_1, GA_ca_1, GA_u_1, GA_DD_1 = GA_main(thin1, photo1, etch1, w1, w2, w3, w4, w5, w6, w7, w8, w9)
        GA_machine_list_2, GA_ca_2, GA_u_2, GA_DD_2 = GA_main(thin2, photo2, etch2, w1, w2, w3, w4, w5, w6, w7, w8, w9)
        GA_machine_list_3, GA_ca_3, GA_u_3, GA_DD_3 = GA_main(thin3, photo3, etch3, w1, w2, w3, w4, w5, w6, w7, w8, w9)
        GA_machine_list_4, GA_ca_4, GA_u_4, GA_DD_4 = GA_main(thin4, photo4, etch4, w1, w2, w3, w4, w5, w6, w7, w8, w9)
        GA_machine_list_5, GA_ca_5, GA_u_5, GA_DD_5 = GA_main(thin5, photo5, etch5, w1, w2, w3, w4, w5, w6, w7, w8, w9)
        GA_machine_list_6, GA_ca_6, GA_u_6, GA_DD_6 = GA_main(thin6, photo6, etch6, w1, w2, w3, w4, w5, w6, w7, w8, w9)
        gbest_machine_1, PSO_Ca_value_1, PSO_u_value_1, PSO_DD_value_1 = PSO_main(thin1, photo1, etch1, w1, w2, w3, w4, w5, w6, w7, w8, w9)
        gbest_machine_2, PSO_Ca_value_2, PSO_u_value_2, PSO_DD_value_2 = PSO_main(thin2, photo2, etch2, w1, w2, w3, w4, w5, w6, w7, w8, w9)
        gbest_machine_3, PSO_Ca_value_3, PSO_u_value_3, PSO_DD_value_3 = PSO_main(thin3, photo3, etch3, w1, w2, w3, w4, w5, w6, w7, w8, w9)
        gbest_machine_4, PSO_Ca_value_4, PSO_u_value_4, PSO_DD_value_4 = PSO_main(thin4, photo4, etch4, w1, w2, w3, w4, w5, w6, w7, w8, w9)
        gbest_machine_5, PSO_Ca_value_5, PSO_u_value_5, PSO_DD_value_5 = PSO_main(thin5, photo5, etch5, w1, w2, w3, w4, w5, w6, w7, w8, w9)
        gbest_machine_6, PSO_Ca_value_6, PSO_u_value_6, PSO_DD_value_6 = PSO_main(thin6, photo6, etch6, w1, w2, w3, w4, w5, w6, w7, w8, w9)
        TS_machine_list_1, TS_ca_1 ,TS_u_1, TS_DD_1 = TS_main(thin1, photo1, etch1, w1, w2, w3, w4, w5, w6, w7, w8, w9)
        TS_machine_list_2, TS_ca_2 ,TS_u_2, TS_DD_2 = TS_main(thin2, photo2, etch2, w1, w2, w3, w4, w5, w6, w7, w8, w9)
        TS_machine_list_3, TS_ca_3 ,TS_u_3, TS_DD_3 = TS_main(thin3, photo3, etch3, w1, w2, w3, w4, w5, w6, w7, w8, w9)
        TS_machine_list_4, TS_ca_4 ,TS_u_4, TS_DD_4 = TS_main(thin4, photo4, etch4, w1, w2, w3, w4, w5, w6, w7, w8, w9)
        TS_machine_list_5, TS_ca_5 ,TS_u_5, TS_DD_5 = TS_main(thin5, photo5, etch5, w1, w2, w3, w4, w5, w6, w7, w8, w9)
        TS_machine_list_6, TS_ca_6 ,TS_u_6, TS_DD_6 = TS_main(thin6, photo6, etch6, w1, w2, w3, w4, w5, w6, w7, w8, w9)
        
        ## machine的呈現 共3*6*7
        for j in range(1,7):
            for i in range(len(best_machine_1)):
                if (i == 1):
                    if str(eval('best_machine_'+ str(j))[0]) == 'No_machine' :
#                    if len(eval('P'+ str(j) + 'M1')) == 0 or len(eval('P'+ str(j) + 'M2')) == 0 or len(eval('P'+ str(j) + 'M3')) == 0:
                        img = make_pie([1,1,1],str(eval('best_machine_'+ str(j))[0]),[c1,c2,c3],
                                       ['Ca mean:\n'+'0',
                                        'DD:\n'+'0', 
                                        'U mean:\n'+'0'])
                    else:
                        img = make_pie([1,1,1],str(eval('best_machine_'+ str(j))[0]),[c1,c2,c3],
                                       ['Ca mean:\n'+ str(round((eval('thin'+str(j)).loc[eval('best_machine_'+ str(j))[0]].Ca_mean),4)),
                                        'DD:\n'+ str(round((eval('thin'+str(j)).loc[eval('best_machine_'+ str(j))[0]].DD),4)), 
                                        'U mean:\n'+ str(round((eval('thin'+str(j)).loc[eval('best_machine_'+ str(j))[0]].u_mean),4))])
                    if(j == 1):
                        scheduling_P1M1_plot_url= base64.b64encode(img.getvalue()).decode()
                    if(j == 2):
                        scheduling_P2M1_plot_url= base64.b64encode(img.getvalue()).decode()
                    if(j == 3):
                        scheduling_P3M1_plot_url= base64.b64encode(img.getvalue()).decode()
                    if(j == 4):
                        scheduling_P4M1_plot_url= base64.b64encode(img.getvalue()).decode()
                    if(j == 5):
                        scheduling_P5M1_plot_url= base64.b64encode(img.getvalue()).decode()
                    if(j == 6):
                        scheduling_P6M1_plot_url= base64.b64encode(img.getvalue()).decode()   
                if(i == 2):
                    if str(eval('best_machine_'+ str(j))[1]) == 'No_machine' :
#                    if len(eval('P'+ str(j) + 'M1')) == 0 or len(eval('P'+ str(j) + 'M2')) == 0 or len(eval('P'+ str(j) + 'M3')) == 0:
                        img = make_pie([1,1,1],str(eval('best_machine_'+ str(j))[1]),[c1,c2,c3],
                                       ['Ca mean:\n'+'0',
                                        'DD:\n'+'0', 
                                        'U mean:\n'+'0'])
                    else:
                        img = make_pie([1,1,1],str(eval('best_machine_'+ str(j))[1]),[c1,c2,c3],
                                       ['Ca mean:\n'+ str(round((eval('photo'+str(j)).loc[eval('best_machine_'+ str(j))[1]].Ca_mean),4)), 
                                        'DD:\n'+ str(round((eval('photo'+str(j)).loc[eval('best_machine_'+ str(j))[1]].DD),4)), 
                                        'U mean:\n'+ str(round((eval('photo'+str(j)).loc[eval('best_machine_'+ str(j))[1]].u_mean),4))])   
                    if(j == 1):
                        scheduling_P1M2_plot_url= base64.b64encode(img.getvalue()).decode()
                    if(j == 2):
                        scheduling_P2M2_plot_url= base64.b64encode(img.getvalue()).decode()
                    if(j == 3):
                        scheduling_P3M2_plot_url= base64.b64encode(img.getvalue()).decode()
                    if(j == 4):
                        scheduling_P4M2_plot_url= base64.b64encode(img.getvalue()).decode()
                    if(j == 5):
                        scheduling_P5M2_plot_url= base64.b64encode(img.getvalue()).decode()
                    if(j == 6):
                        scheduling_P6M2_plot_url= base64.b64encode(img.getvalue()).decode()
                        
                else:
                    if str(eval('best_machine_'+ str(j))[2]) == 'No_machine' :
#                    if len(eval('P'+ str(j) + 'M1')) == 0 or len(eval('P'+ str(j) + 'M2')) == 0 or len(eval('P'+ str(j) + 'M3')) == 0:
                        img = make_pie([1,1,1],str(eval('best_machine_'+ str(j))[2]),[c1,c2,c3],
                                       ['Ca mean:\n'+'0',
                                        'DD:\n'+'0', 
                                        'U mean:\n'+'0'])
                    else:
                        img = make_pie([1,1,1],str(eval('best_machine_'+ str(j))[2]),[c1,c2,c3],
                                       ['Ca mean:\n'+ str(round((eval('etch'+str(j)).loc[eval('best_machine_'+ str(j))[2]].Ca_mean),4)), 
                                        'DD:\n'+ str(round((eval('etch'+str(j)).loc[eval('best_machine_'+ str(j))[2]].DD),4)), 
                                        'U mean:\n'+ str(round((eval('etch'+str(j)).loc[eval('best_machine_'+ str(j))[2]].u_mean),4))])
                    if(j == 1):
                        scheduling_P1M3_plot_url= base64.b64encode(img.getvalue()).decode()
                    if(j == 2):
                        scheduling_P2M3_plot_url= base64.b64encode(img.getvalue()).decode()
                    if(j == 3):
                        scheduling_P3M3_plot_url= base64.b64encode(img.getvalue()).decode()
                    if(j == 4):
                        scheduling_P4M3_plot_url= base64.b64encode(img.getvalue()).decode()
                    if(j == 5):
                        scheduling_P5M3_plot_url= base64.b64encode(img.getvalue()).decode()
                    if(j == 6):
                        scheduling_P6M3_plot_url= base64.b64encode(img.getvalue()).decode()
        
        for j in range(1,7):
            for i in range(len(M_path_1)):
                if (i == 1):
                    if str(eval('M_path_'+ str(j))[0]) == 'No_machine' :
#                    if len(eval('P'+ str(j) + 'M1')) == 0 or len(eval('P'+ str(j) + 'M2')) == 0 or len(eval('P'+ str(j) + 'M3')) == 0:
                        img = make_pie([1,1,1],str(eval('M_path_'+ str(j))[0]),[c1,c2,c3],
                                       ['Ca mean:\n'+'0',
                                        'DD:\n'+'0', 
                                        'U mean:\n'+'0'])
                    else:
                        img = make_pie([1,1,1],str(eval('M_path_'+ str(j))[0]),[c1,c2,c3],
                                       ['Ca mean:\n'+ str(round((eval('thin'+str(j)).loc[eval('M_path_'+ str(j))[0]].Ca_mean),4)), 
                                        'DD:\n'+ str(round((eval('thin'+str(j)).loc[eval('M_path_'+ str(j))[0]].DD),4)), 
                                        'U mean:\n'+ str(round((eval('thin'+str(j)).loc[eval('M_path_'+ str(j))[0]].u_mean),4))])
                    if(j == 1):
                        ACO_P1M1_plot_url= base64.b64encode(img.getvalue()).decode()
                    if(j == 2):
                        ACO_P2M1_plot_url= base64.b64encode(img.getvalue()).decode()
                    if(j == 3):
                        ACO_P3M1_plot_url= base64.b64encode(img.getvalue()).decode()
                    if(j == 4):
                        ACO_P4M1_plot_url= base64.b64encode(img.getvalue()).decode()
                    if(j == 5):
                        ACO_P5M1_plot_url= base64.b64encode(img.getvalue()).decode()
                    if(j == 6):
                        ACO_P6M1_plot_url= base64.b64encode(img.getvalue()).decode()
                elif(i == 2):
                    if str(eval('M_path_'+ str(j))[1]) == 'No_machine' :
#                    if len(eval('P'+ str(j) + 'M1')) == 0 or len(eval('P'+ str(j) + 'M2')) == 0 or len(eval('P'+ str(j) + 'M3')) == 0:
                        img = make_pie([1,1,1],str(eval('M_path_'+ str(j))[1]),[c1,c2,c3],
                                       ['Ca mean:\n'+'0',
                                        'DD:\n'+'0', 
                                        'U mean:\n'+'0'])
                    else:
                        img = make_pie([1,1,1],str(eval('M_path_'+ str(j))[1]),[c1,c2,c3],
                                       ['Ca mean:\n'+ str(round((eval('photo'+str(j)).loc[eval('M_path_'+ str(j))[1]].Ca_mean),4)), 
                                        'DD:\n'+ str(round((eval('photo'+str(j)).loc[eval('M_path_'+ str(j))[1]].DD),4)), 
                                        'U mean:\n'+ str(round((eval('photo'+str(j)).loc[eval('M_path_'+ str(j))[1]].u_mean),4))])

                    if(j == 1):
                        ACO_P1M2_plot_url= base64.b64encode(img.getvalue()).decode()
                    if(j == 2):
                        ACO_P2M2_plot_url= base64.b64encode(img.getvalue()).decode()
                    if(j == 3):
                        ACO_P3M2_plot_url= base64.b64encode(img.getvalue()).decode()
                    if(j == 4):
                        ACO_P4M2_plot_url= base64.b64encode(img.getvalue()).decode()
                    if(j == 5):
                        ACO_P5M2_plot_url= base64.b64encode(img.getvalue()).decode()
                    if(j == 6):
                        ACO_P6M2_plot_url= base64.b64encode(img.getvalue()).decode()
                else:
                    if str(eval('M_path_'+ str(j))[2]) == 'No_machine' :
#                    if len(eval('P'+ str(j) + 'M1')) == 0 or len(eval('P'+ str(j) + 'M2')) == 0 or len(eval('P'+ str(j) + 'M3')) == 0:
                        img = make_pie([1,1,1],str(eval('M_path_'+ str(j))[2]),[c1,c2,c3],
                                       ['Ca mean:\n'+'0',
                                        'DD:\n'+'0', 
                                        'U mean:\n'+'0'])
                    else:
                        img = make_pie([1,1,1],str(eval('M_path_'+ str(j))[2]),[c1,c2,c3],
                                       ['Ca mean:\n'+ str(round((eval('etch'+str(j)).loc[eval('M_path_'+ str(j))[2]].Ca_mean),4)), 
                                        'DD:\n'+ str(round((eval('etch'+str(j)).loc[eval('M_path_'+ str(j))[2]].DD),4)),
                                        'U mean:\n'+ str(round((eval('etch'+str(j)).loc[eval('M_path_'+ str(j))[2]].u_mean),4))])

                    if(j == 1):
                        ACO_P1M3_plot_url= base64.b64encode(img.getvalue()).decode()
                    if(j == 2):
                        ACO_P2M3_plot_url= base64.b64encode(img.getvalue()).decode()
                    if(j == 3):
                        ACO_P3M3_plot_url= base64.b64encode(img.getvalue()).decode()
                    if(j == 4):
                        ACO_P4M3_plot_url= base64.b64encode(img.getvalue()).decode()
                    if(j == 5):
                        ACO_P5M3_plot_url= base64.b64encode(img.getvalue()).decode()
                    if(j == 6):
                        ACO_P6M3_plot_url= base64.b64encode(img.getvalue()).decode()
        for j in range(1,7):
            for i in range(len(gbest_machine_1)):
                if (i == 1):
                    if str(eval('gbest_machine_'+ str(j))[0]) == 'No_machine' :
                        img = make_pie([1,1,1],str(eval('gbest_machine_'+ str(j))[0]),[c1,c2,c3],
                                       ['Ca mean:\n'+'0',
                                        'DD:\n'+'0', 
                                        'U mean:\n'+'0'])
                    else:
                        img = make_pie([1,1,1],str(eval('gbest_machine_'+ str(j))[0]),[c1,c2,c3],
                                       ['Ca mean:\n'+ str(round((eval('thin'+str(j)).loc[eval('gbest_machine_'+ str(j))[0]].Ca_mean),4)), 
                                        'DD :\n'+ str(round((eval('thin'+str(j)).loc[eval('gbest_machine_'+ str(j))[0]].DD),4)), 
                                        'U mean:\n'+ str(round((eval('thin'+str(j)).loc[eval('gbest_machine_'+ str(j))[0]].u_mean),4))])
                    
                    
                    if(j == 1):
                        PSO_P1M1_plot_url= base64.b64encode(img.getvalue()).decode()
                    if(j == 2):
                        PSO_P2M1_plot_url= base64.b64encode(img.getvalue()).decode()
                    if(j == 3):
                        PSO_P3M1_plot_url= base64.b64encode(img.getvalue()).decode()
                    if(j == 4):
                        PSO_P4M1_plot_url= base64.b64encode(img.getvalue()).decode()
                    if(j == 5):
                        PSO_P5M1_plot_url= base64.b64encode(img.getvalue()).decode()
                    if(j == 6):
                        PSO_P6M1_plot_url= base64.b64encode(img.getvalue()).decode()
                        
                elif(i == 2):
                    if str(eval('gbest_machine_'+ str(j))[1]) == 'No_machine' :                        
                        img = make_pie([1,1,1],str(eval('gbest_machine_'+ str(j))[1]),[c1,c2,c3],
                                       ['Ca mean:\n'+'0',
                                        'DD:\n'+'0', 
                                        'U mean:\n'+'0'])
                    else:
                        img = make_pie([1,1,1],str(eval('gbest_machine_'+ str(j))[1]),[c1,c2,c3],
                                       ['Ca mean:\n'+ str(round((eval('photo'+str(j)).loc[eval('gbest_machine_'+ str(j))[1]].Ca_mean),4)), 
                                        'DD:\n'+ str(round((eval('photo'+str(j)).loc[eval('gbest_machine_'+ str(j))[1]].DD),4)), 
                                        'U mean:\n'+ str(round((eval('photo'+str(j)).loc[eval('gbest_machine_'+ str(j))[1]].u_mean),4))])
                    
        
                    if(j == 1):
                        PSO_P1M2_plot_url= base64.b64encode(img.getvalue()).decode()
                    if(j == 2):
                        PSO_P2M2_plot_url= base64.b64encode(img.getvalue()).decode()
                    if(j == 3):
                        PSO_P3M2_plot_url= base64.b64encode(img.getvalue()).decode()
                    if(j == 4):
                        PSO_P4M2_plot_url= base64.b64encode(img.getvalue()).decode()
                    if(j == 5):
                        PSO_P5M2_plot_url= base64.b64encode(img.getvalue()).decode()
                    if(j == 6):
                        PSO_P6M2_plot_url= base64.b64encode(img.getvalue()).decode()
                        
                else:
                    
                    if str(eval('M_path_'+ str(j))[2]) == 'No_machine' :                        
                        img = make_pie([1,1,1],str(eval('M_path_'+ str(j))[2]),[c1,c2,c3],
                                       ['Ca mean:\n'+'0',
                                        'DD:\n'+'0', 
                                        'U mean:\n'+'0'])
                    else:
                        img = make_pie([1,1,1],str(eval('M_path_'+ str(j))[2]),[c1,c2,c3],
                                       ['Ca mean:\n'+ str(round((eval('etch'+str(j)).loc[eval('gbest_machine_'+ str(j))[2]].Ca_mean),4)),
                                        'DD:\n'+ str(round((eval('etch'+str(j)).loc[eval('gbest_machine_'+ str(j))[2]].DD),4)), 
                                        'U mean:\n'+ str(round((eval('etch'+str(j)).loc[eval('gbest_machine_'+ str(j))[2]].u_mean),4))])
                    if(j == 1):
                        PSO_P1M3_plot_url= base64.b64encode(img.getvalue()).decode()
                    if(j == 2):
                        PSO_P2M3_plot_url= base64.b64encode(img.getvalue()).decode()
                    if(j == 3):
                        PSO_P3M3_plot_url= base64.b64encode(img.getvalue()).decode()
                    if(j == 4):
                        PSO_P4M3_plot_url= base64.b64encode(img.getvalue()).decode()
                    if(j == 5):
                        PSO_P5M3_plot_url= base64.b64encode(img.getvalue()).decode()
                    if(j == 6):
                        PSO_P6M3_plot_url= base64.b64encode(img.getvalue()).decode()
        for j in range(1,7):
            for i in range(len(GA_machine_list_1)):
                if (i == 1):
                    if str(eval('GA_machine_list_'+ str(j))[0]) == 'No_machine' :
                        img = make_pie([1,1,1],str(eval('GA_machine_list_'+ str(j))[0]),[c1,c2,c3],
                                       ['Ca mean:\n'+'0',
                                        'DD:\n'+'0', 
                                        'U mean:\n'+'0'])
                    else:
                        img = make_pie([1,1,1],str(eval('GA_machine_list_'+ str(j))[0]),[c1,c2,c3],
                                       ['Ca mean:\n'+ str(round((eval('thin'+str(j)).loc[eval('GA_machine_list_'+ str(j))[0]].Ca_mean),4)),
                                        'DD:\n'+ str(round((eval('thin'+str(j)).loc[eval('GA_machine_list_'+ str(j))[0]].DD),4)), 
                                        'U mean:\n'+ str(round((eval('thin'+str(j)).loc[eval('GA_machine_list_'+ str(j))[0]].u_mean),4))])
                    

                    if(j == 1):
                        GA_P1M1_plot_url= base64.b64encode(img.getvalue()).decode()
                    if(j == 2):
                        GA_P2M1_plot_url= base64.b64encode(img.getvalue()).decode()
                    if(j == 3):
                        GA_P3M1_plot_url= base64.b64encode(img.getvalue()).decode()
                    if(j == 4):
                        GA_P4M1_plot_url= base64.b64encode(img.getvalue()).decode()
                    if(j == 5):
                        GA_P5M1_plot_url= base64.b64encode(img.getvalue()).decode()
                    if(j == 6):
                        GA_P6M1_plot_url= base64.b64encode(img.getvalue()).decode()
                        
                    
                elif(i == 2):
                    if str(eval('GA_machine_list_'+ str(j))[1]) == 'No_machine' :
                        img = make_pie([1,1,1],str(eval('GA_machine_list_'+ str(j))[1]),[c1,c2,c3],
                                       ['Ca mean:\n'+'0',
                                        'DD:\n'+'0', 
                                        'U mean:\n'+'0'])
                    else:
                        img = make_pie([1,1,1],str(eval('GA_machine_list_'+ str(j))[1]),[c1,c2,c3],
                                       ['Ca mean:\n'+ str(round((eval('photo'+str(j)).loc[eval('GA_machine_list_'+ str(j))[1]].Ca_mean),4)),
                                        'DD:\n'+ str(round((eval('photo'+str(j)).loc[eval('GA_machine_list_'+ str(j))[1]].DD),4)), 
                                        'U mean:\n'+ str(round((eval('photo'+str(j)).loc[eval('GA_machine_list_'+ str(j))[1]].u_mean),4))])                      

                    if(j == 1):
                        GA_P1M2_plot_url= base64.b64encode(img.getvalue()).decode()
                    if(j == 2):
                        GA_P2M2_plot_url= base64.b64encode(img.getvalue()).decode()
                    if(j == 3):
                        GA_P3M2_plot_url= base64.b64encode(img.getvalue()).decode()
                    if(j == 4):
                        GA_P4M2_plot_url= base64.b64encode(img.getvalue()).decode()
                    if(j == 5):
                        GA_P5M2_plot_url= base64.b64encode(img.getvalue()).decode()
                    if(j == 6):
                        GA_P6M2_plot_url= base64.b64encode(img.getvalue()).decode()
                        
                else:
                    if str(eval('GA_machine_list_'+ str(j))[2]) == 'No_machine' :
                        img = make_pie([1,1,1],str(eval('GA_machine_list_'+ str(j))[2]),[c1,c2,c3],
                                       ['Ca mean:\n'+'0',
                                        'DD:\n'+'0', 
                                        'U mean:\n'+'0'])
                    else:
                        img = make_pie([1,1,1],str(eval('GA_machine_list_'+ str(j))[2]),[c1,c2,c3],
                                       ['Ca mean:\n'+ str(round((eval('etch'+str(j)).loc[eval('GA_machine_list_'+ str(j))[2]].Ca_mean),4)), 
                                        'DD:\n'+ str(round((eval('etch'+str(j)).loc[eval('GA_machine_list_'+ str(j))[2]].DD),4)), 
                                        'U mean:\n'+ str(round((eval('etch'+str(j)).loc[eval('GA_machine_list_'+ str(j))[2]].u_mean),4))])                        

                    if(j == 1):
                        GA_P1M3_plot_url= base64.b64encode(img.getvalue()).decode()
                    if(j == 2):
                        GA_P2M3_plot_url= base64.b64encode(img.getvalue()).decode()
                    if(j == 3):
                        GA_P3M3_plot_url= base64.b64encode(img.getvalue()).decode()
                    if(j == 4):
                        GA_P4M3_plot_url= base64.b64encode(img.getvalue()).decode()
                    if(j == 5):
                        GA_P5M3_plot_url= base64.b64encode(img.getvalue()).decode()
                    if(j == 6):
                        GA_P6M3_plot_url= base64.b64encode(img.getvalue()).decode()
                            
        for j in range(1,7):
            for i in range(len(TS_machine_list_1)):
                if (i == 1):
                    if str(eval('TS_machine_list_'+ str(j))[0]) == 'No_machine' :
                        img = make_pie([1,1,1],str(eval('TS_machine_list_'+ str(j))[0]),[c1,c2,c3],
                                       ['Ca mean:\n'+'0',
                                        'DD:\n'+'0', 
                                        'U mean:\n'+'0'])
                    else:
                        img = make_pie([1,1,1],str(eval('TS_machine_list_'+ str(j))[0]),[c1,c2,c3],
                                       ['Ca mean:\n'+ str(round((eval('thin'+str(j)).loc[eval('TS_machine_list_'+ str(j))[0]].Ca_mean),4)), 
                                        'DD:\n'+ str(round((eval('thin'+str(j)).loc[eval('TS_machine_list_'+ str(j))[0]].DD),4)), 
                                        'U mean:\n'+ str(round((eval('thin'+str(j)).loc[eval('TS_machine_list_'+ str(j))[0]].u_mean),4))])


                    if(j == 1):
                        TS_P1M1_plot_url= base64.b64encode(img.getvalue()).decode()
                    if(j == 2):
                        TS_P2M1_plot_url= base64.b64encode(img.getvalue()).decode()
                    if(j == 3):
                        TS_P3M1_plot_url= base64.b64encode(img.getvalue()).decode()
                    if(j == 4):
                        TS_P4M1_plot_url= base64.b64encode(img.getvalue()).decode()
                    if(j == 5):
                        TS_P5M1_plot_url= base64.b64encode(img.getvalue()).decode()
                    if(j == 6):
                        TS_P6M1_plot_url= base64.b64encode(img.getvalue()).decode()
                elif(i == 2):
                    if str(eval('TS_machine_list_'+ str(j))[1]) == 'No_machine' :
                        img = make_pie([1,1,1],str(eval('TS_machine_list_'+ str(j))[1]),[c1,c2,c3],
                                       ['Ca mean:\n'+'0',
                                        'DD:\n'+'0', 
                                        'U mean:\n'+'0'])
                    else:
                        img = make_pie([1,1,1],str(eval('TS_machine_list_'+ str(j))[1]),[c1,c2,c3],
                                       ['Ca mean:\n'+ str(round((eval('photo'+str(j)).loc[eval('TS_machine_list_'+ str(j))[1]].Ca_mean),4)), 
                                        'DD:\n'+ str(round((eval('photo'+str(j)).loc[eval('TS_machine_list_'+ str(j))[1]].DD),4)), 
                                        'U mean:\n'+ str(round((eval('photo'+str(j)).loc[eval('TS_machine_list_'+ str(j))[1]].u_mean),4))])
    

                    if(j == 1):
                        TS_P1M2_plot_url= base64.b64encode(img.getvalue()).decode()
                    if(j == 2):
                        TS_P2M2_plot_url= base64.b64encode(img.getvalue()).decode()
                    if(j == 3):
                        TS_P3M2_plot_url= base64.b64encode(img.getvalue()).decode()
                    if(j == 4):
                        TS_P4M2_plot_url= base64.b64encode(img.getvalue()).decode()
                    if(j == 5):
                        TS_P5M2_plot_url= base64.b64encode(img.getvalue()).decode()
                    if(j == 6):
                        TS_P6M2_plot_url= base64.b64encode(img.getvalue()).decode()
                else:
                    if str(eval('TS_machine_list_'+ str(j))[2]) == 'No_machine' :
                        img = make_pie([1,1,1],str(eval('TS_machine_list_'+ str(j))[2]),[c1,c2,c3],
                                       ['Ca mean:\n'+'0',
                                        'DD:\n'+'0', 
                                        'U mean:\n'+'0'])
                    else:
                        img = make_pie([1,1,1],str(eval('TS_machine_list_'+ str(j))[2]),[c1,c2,c3],
                                       ['Ca mean:\n'+ str(round((eval('etch'+str(j)).loc[eval('TS_machine_list_'+ str(j))[2]].Ca_mean),4)), 
                                        'DD:\n'+ str(round((eval('etch'+str(j)).loc[eval('TS_machine_list_'+ str(j))[2]].DD),4)), 
                                        'U mean:\n'+ str(round((eval('etch'+str(j)).loc[eval('TS_machine_list_'+ str(j))[2]].u_mean),4))])

                    if(j == 1):
                        TS_P1M3_plot_url= base64.b64encode(img.getvalue()).decode()
                    if(j == 2):
                        TS_P2M3_plot_url= base64.b64encode(img.getvalue()).decode()
                    if(j == 3):
                        TS_P3M3_plot_url= base64.b64encode(img.getvalue()).decode()
                    if(j == 4):
                        TS_P4M3_plot_url= base64.b64encode(img.getvalue()).decode()
                    if(j == 5):
                        TS_P5M3_plot_url= base64.b64encode(img.getvalue()).decode()
                    if(j == 6):
                        TS_P6M3_plot_url= base64.b64encode(img.getvalue()).decode()
                            
                            
        for j in range(1,7):
            for i in range(len(select_1)):
                if (i == 1):
                    if str(eval('select_'+ str(j))[0]) == 'No_machine' :
                        img = make_pie([1,1,1],str(eval('select_'+ str(j))[0]),[c1,c2,c3],
                                       ['Ca mean:\n'+'0',
                                        'DD:\n'+'0', 
                                        'U mean:\n'+'0'])
                    else:
                        img = make_pie([1,1,1],str(eval('select_'+ str(j))[0]),[c1,c2,c3],
                                       ['Ca mean:\n'+ str(round((eval('thin'+str(j)).loc[eval('select_'+ str(j))[0]].Ca_mean),4)), 
                                        'DD:\n'+ str(round((eval('thin'+str(j)).loc[eval('select_'+ str(j))[0]].DD),4)), 
                                        'U mean:\n'+ str(round((eval('thin'+str(j)).loc[eval('select_'+ str(j))[0]].u_mean),4))])

                    if(j == 1):
                        MC_P1M1_plot_url= base64.b64encode(img.getvalue()).decode()
                    if(j == 2):
                        MC_P2M1_plot_url= base64.b64encode(img.getvalue()).decode()
                    if(j == 3):
                        MC_P3M1_plot_url= base64.b64encode(img.getvalue()).decode()
                    if(j == 4):
                        MC_P4M1_plot_url= base64.b64encode(img.getvalue()).decode()
                    if(j == 5):
                        MC_P5M1_plot_url= base64.b64encode(img.getvalue()).decode()
                    if(j == 6):
                        MC_P6M1_plot_url= base64.b64encode(img.getvalue()).decode()
                elif(i == 2):
                    if str(eval('select_'+ str(j))[1]) == 'No_machine' :
                        img = make_pie([1,1,1],str(eval('select_'+ str(j))[1]),[c1,c2,c3],
                                       ['Ca mean:\n'+'0',
                                        'DD:\n'+'0', 
                                        'U mean:\n'+'0'])
                    else:
                        img = make_pie([1,1,1],str(eval('select_'+ str(j))[1]),[c1,c2,c3],
                                       ['Ca mean:\n'+ str(round((eval('photo'+str(j)).loc[eval('select_'+ str(j))[1]].Ca_mean),4)), 
                                        'DD:\n'+ str(round((eval('photo'+str(j)).loc[eval('select_'+ str(j))[1]].DD),4)),
                                        'U mean:\n'+ str(round((eval('photo'+str(j)).loc[eval('select_'+ str(j))[1]].u_mean),4))])

                    if(j == 1):
                        MC_P1M2_plot_url= base64.b64encode(img.getvalue()).decode()
                    if(j == 2):
                        MC_P2M2_plot_url= base64.b64encode(img.getvalue()).decode()
                    if(j == 3):
                        MC_P3M2_plot_url= base64.b64encode(img.getvalue()).decode()
                    if(j == 4):
                        MC_P4M2_plot_url= base64.b64encode(img.getvalue()).decode()
                    if(j == 5):
                        MC_P5M2_plot_url= base64.b64encode(img.getvalue()).decode()
                    if(j == 6):
                        MC_P6M2_plot_url= base64.b64encode(img.getvalue()).decode()
                else:
                    if str(eval('select_'+ str(j))[2]) == 'No_machine' :
                        img = make_pie([1,1,1],str(eval('select_'+ str(j))[2]),[c1,c2,c3],
                                       ['Ca mean:\n'+'0',
                                        'DD:\n'+'0', 
                                        'U mean:\n'+'0'])
                    else:
                        img = make_pie([1,1,1],str(eval('select_'+ str(j))[2]),[c1,c2,c3],
                                       ['Ca mean:\n'+ str(round((eval('etch'+str(j)).loc[eval('select_'+ str(j))[2]].Ca_mean),4)),
                                        'DD:\n'+ str(round((eval('etch'+str(j)).loc[eval('select_'+ str(j))[2]].DD),4)), 
                                        'U mean:\n'+ str(round((eval('etch'+str(j)).loc[eval('select_'+ str(j))[2]].u_mean),4))])                    

                    if(j == 1):
                        MC_P1M3_plot_url= base64.b64encode(img.getvalue()).decode()
                    if(j == 2):
                        MC_P2M3_plot_url= base64.b64encode(img.getvalue()).decode()
                    if(j == 3):
                        MC_P3M3_plot_url= base64.b64encode(img.getvalue()).decode()
                    if(j == 4):
                        MC_P4M3_plot_url= base64.b64encode(img.getvalue()).decode()
                    if(j == 5):
                        MC_P5M3_plot_url= base64.b64encode(img.getvalue()).decode()
                    if(j == 6):
                        MC_P6M3_plot_url= base64.b64encode(img.getvalue()).decode()
        
        
        for j in range(1,7):
            for i in range(len(worst_machine_1)):
                if (i == 1):
                    if str(eval('worst_machine_'+ str(j))[0]) == 'No_machine' :
                        img = make_pie([1,1,1],str(eval('worst_machine_'+ str(j))[0]),[c1,c2,c3],
                                       ['Ca mean:\n'+'0',
                                        'DD:\n'+'0', 
                                        'U mean:\n'+'0'])
                    else:
                        img = make_pie([1,1,1],str(eval('worst_machine_'+ str(j))[0]),[c1,c2,c3],
                                       ['Ca mean:\n'+ str(round((eval('thin'+str(j)).loc[eval('worst_machine_'+ str(j))[0]].Ca_mean),4)),
                                        'DD:\n'+ str(round((eval('thin'+str(j)).loc[eval('worst_machine_'+ str(j))[0]].DD),4)), 
                                        'U mean:\n'+ str(round((eval('thin'+str(j)).loc[eval('worst_machine_'+ str(j))[0]].u_mean),4))])

                    if(j == 1):
                        bad_P1M1_plot_url= base64.b64encode(img.getvalue()).decode()
                    if(j == 2):
                        bad_P2M1_plot_url= base64.b64encode(img.getvalue()).decode()
                    if(j == 3):
                        bad_P3M1_plot_url= base64.b64encode(img.getvalue()).decode()
                    if(j == 4):
                        bad_P4M1_plot_url= base64.b64encode(img.getvalue()).decode()
                    if(j == 5):
                        bad_P5M1_plot_url= base64.b64encode(img.getvalue()).decode()
                    if(j == 6):
                        bad_P6M1_plot_url= base64.b64encode(img.getvalue()).decode()
                elif(i == 2):
                    if str(eval('worst_machine_'+ str(j))[1]) == 'No_machine' :
                        img = make_pie([1,1,1],str(eval('worst_machine_'+ str(j))[1]),[c1,c2,c3],
                                       ['Ca mean:\n'+'0',
                                        'DD:\n'+'0', 
                                        'U mean:\n'+'0'])
                    else:
                        img = make_pie([1,1,1],str(eval('worst_machine_'+ str(j))[1]),[c1,c2,c3],
                                       ['Ca mean:\n'+ str(round((eval('photo'+str(j)).loc[eval('worst_machine_'+ str(j))[1]].Ca_mean),4)),
                                        'DD:\n'+ str(round((eval('photo'+str(j)).loc[eval('worst_machine_'+ str(j))[1]].DD),4)), 
                                        'U mean:\n'+ str(round((eval('photo'+str(j)).loc[eval('worst_machine_'+ str(j))[1]].u_mean),4))])

                    if(j == 1):
                        bad_P1M2_plot_url= base64.b64encode(img.getvalue()).decode()
                    if(j == 2):
                        bad_P2M2_plot_url= base64.b64encode(img.getvalue()).decode()
                    if(j == 3):
                        bad_P3M2_plot_url= base64.b64encode(img.getvalue()).decode()
                    if(j == 4):
                        bad_P4M2_plot_url= base64.b64encode(img.getvalue()).decode()
                    if(j == 5):
                        bad_P5M2_plot_url= base64.b64encode(img.getvalue()).decode()
                    if(j == 6):
                        bad_P6M2_plot_url= base64.b64encode(img.getvalue()).decode()
                        
                else:
                    
                    if str(eval('worst_machine_'+ str(j))[2]) == 'No_machine' :
                        img = make_pie([1,1,1],str(eval('worst_machine_'+ str(j))[2]),[c1,c2,c3],
                                       ['Ca mean:\n'+'0',
                                        'DD:\n'+'0', 
                                        'U mean:\n'+'0'])
                    else:
                        img = make_pie([1,1,1],str(eval('worst_machine_'+ str(j))[2]),[c1,c2,c3],
                                       ['Ca mean:\n'+ str(round((eval('etch'+str(j)).loc[eval('worst_machine_'+ str(j))[2]].Ca_mean),4)), 
                                        'DD:\n'+ str(round((eval('etch'+str(j)).loc[eval('worst_machine_'+ str(j))[2]].DD),4)),
                                        'U mean:\n'+ str(round((eval('etch'+str(j)).loc[eval('worst_machine_'+ str(j))[2]].u_mean),4))])
                    if(j == 1):
                        bad_P1M3_plot_url= base64.b64encode(img.getvalue()).decode()
                    if(j == 2):
                        bad_P2M3_plot_url= base64.b64encode(img.getvalue()).decode()
                    if(j == 3):
                        bad_P3M3_plot_url= base64.b64encode(img.getvalue()).decode()
                    if(j == 4):
                        bad_P4M3_plot_url= base64.b64encode(img.getvalue()).decode()
                    if(j == 5):
                        bad_P5M3_plot_url= base64.b64encode(img.getvalue()).decode()
                    if(j == 6):
                        bad_P6M3_plot_url= base64.b64encode(img.getvalue()).decode()
    
        
        ## 回傳到呈現的頁面
        return render_template('final.html', product = product,
                               P1_machine1 = P1M1, P1_machine2 = P1M2, P1_machine3 = P1M3,
                               P2_machine1 = P2M1, P2_machine2 = P2M2, P2_machine3 = P2M3,
                               P3_machine1 = P3M1, P3_machine2 = P3M2, P3_machine3 = P3M3,
                               P4_machine1 = P4M1, P4_machine2 = P4M2, P4_machine3 = P4M3,
                               P5_machine1 = P5M1, P5_machine2 = P5M2, P5_machine3 = P5M3,
                               P6_machine1 = P6M1, P6_machine2 = P6M2, P6_machine3 = P6M3,
                               scheduling_machine_list_1= best_machine_1, scheduling_ca_1 = best_ca_value_1, scheduling_u_1 = best_u_value_1, scheduling_DD_1 = best_DD_value_1, scheduling_worst_machine_list_1 = worst_machine_1, scheduling_worst_ca_1 = worst_ca_value_1, scheduling_worst_u_1 = worst_u_value_1, scheduling_worst_DD_1 = worst_DD_value_1, 
                               scheduling_machine_list_2= best_machine_2, scheduling_ca_2 = best_ca_value_2, scheduling_u_2 = best_u_value_2, scheduling_DD_2 = best_DD_value_2, scheduling_worst_machine_list_2 = worst_machine_2, scheduling_worst_ca_2 = worst_ca_value_2, scheduling_worst_u_2 = worst_u_value_2, scheduling_worst_DD_2 = worst_DD_value_2,
                               scheduling_machine_list_3= best_machine_3, scheduling_ca_3 = best_ca_value_3, scheduling_u_3 = best_u_value_3, scheduling_DD_3 = best_DD_value_3, scheduling_worst_machine_list_3 = worst_machine_3, scheduling_worst_ca_3 = worst_ca_value_3, scheduling_worst_u_3 = worst_u_value_3, scheduling_worst_DD_3 = worst_DD_value_3,
                               scheduling_machine_list_4= best_machine_4, scheduling_ca_4 = best_ca_value_4, scheduling_u_4 = best_u_value_4, scheduling_DD_4 = best_DD_value_4, scheduling_worst_machine_list_4 = worst_machine_4, scheduling_worst_ca_4 = worst_ca_value_4, scheduling_worst_u_4 = worst_u_value_4, scheduling_worst_DD_4 = worst_DD_value_4,
                               scheduling_machine_list_5= best_machine_5, scheduling_ca_5 = best_ca_value_5, scheduling_u_5 = best_u_value_5, scheduling_DD_5 = best_DD_value_5, scheduling_worst_machine_list_5 = worst_machine_5, scheduling_worst_ca_5 = worst_ca_value_5, scheduling_worst_u_5 = worst_u_value_5, scheduling_worst_DD_5 = worst_DD_value_5,
                               scheduling_machine_list_6= best_machine_6, scheduling_ca_6 = best_ca_value_6, scheduling_u_6 = best_u_value_6, scheduling_DD_6 = best_DD_value_6, scheduling_worst_machine_list_6 = worst_machine_6, scheduling_worst_ca_6 = worst_ca_value_6, scheduling_worst_u_6 = worst_u_value_6, scheduling_worst_DD_6 = worst_DD_value_6,
                               MC_machine_list_1= select_1, MC_ca_1= MC_Ca_value_1, MC_u_1= MC_u_value_1, MC_DD_1= MC_DD_value_1,
                               MC_machine_list_2= select_2, MC_ca_2= MC_Ca_value_2, MC_u_2= MC_u_value_2, MC_DD_2= MC_DD_value_2,
                               MC_machine_list_3= select_3, MC_ca_3= MC_Ca_value_3, MC_u_3= MC_u_value_3, MC_DD_3= MC_DD_value_3,
                               MC_machine_list_4= select_4, MC_ca_4= MC_Ca_value_4, MC_u_4= MC_u_value_4, MC_DD_4= MC_DD_value_4,
                               MC_machine_list_5= select_5, MC_ca_5= MC_Ca_value_5, MC_u_5= MC_u_value_5, MC_DD_5= MC_DD_value_5,
                               MC_machine_list_6= select_6, MC_ca_6= MC_Ca_value_6, MC_u_6= MC_u_value_6, MC_DD_6= MC_DD_value_6,
                               ACO_machine_list_1= M_path_1, ACO_ca_1= minn1_1, ACO_u_1= minn2_1, ACO_DD_1= minn3_1,
                               ACO_machine_list_2= M_path_2, ACO_ca_2= minn1_2, ACO_u_2= minn2_2, ACO_DD_2= minn3_2,
                               ACO_machine_list_3= M_path_3, ACO_ca_3= minn1_3, ACO_u_3= minn2_3, ACO_DD_3= minn3_3,
                               ACO_machine_list_4= M_path_4, ACO_ca_4= minn1_4, ACO_u_4= minn2_4, ACO_DD_4= minn3_4,
                               ACO_machine_list_5= M_path_5, ACO_ca_5= minn1_5, ACO_u_5= minn2_5, ACO_DD_5= minn3_5,
                               ACO_machine_list_6= M_path_6, ACO_ca_6= minn1_6, ACO_u_6= minn2_6, ACO_DD_6= minn3_6,
                               GA_machine_list_1= GA_machine_list_1, GA_ca_1= GA_ca_1, GA_u_1 = GA_u_1, GA_DD_1 = GA_DD_1,
                               GA_machine_list_2= GA_machine_list_2, GA_ca_2= GA_ca_2, GA_u_2 = GA_u_2, GA_DD_2 = GA_DD_2,
                               GA_machine_list_3= GA_machine_list_3, GA_ca_3= GA_ca_3, GA_u_3 = GA_u_3, GA_DD_3 = GA_DD_3,
                               GA_machine_list_4= GA_machine_list_4, GA_ca_4= GA_ca_4, GA_u_4 = GA_u_4, GA_DD_4 = GA_DD_4,
                               GA_machine_list_5= GA_machine_list_5, GA_ca_5= GA_ca_5, GA_u_5 = GA_u_5, GA_DD_5 = GA_DD_5,
                               GA_machine_list_6= GA_machine_list_6, GA_ca_6= GA_ca_6, GA_u_6 = GA_u_6, GA_DD_6 = GA_DD_6,
                               PSO_machine_list_1= gbest_machine_1, PSO_ca_1= PSO_Ca_value_1, PSO_u_1= PSO_u_value_1, PSO_DD_1= PSO_DD_value_1,
                               PSO_machine_list_2= gbest_machine_2, PSO_ca_2= PSO_Ca_value_2, PSO_u_2= PSO_u_value_2, PSO_DD_2= PSO_DD_value_2,
                               PSO_machine_list_3= gbest_machine_3, PSO_ca_3= PSO_Ca_value_3, PSO_u_3= PSO_u_value_3, PSO_DD_3= PSO_DD_value_3,
                               PSO_machine_list_4= gbest_machine_4, PSO_ca_4= PSO_Ca_value_4, PSO_u_4= PSO_u_value_4, PSO_DD_4= PSO_DD_value_4,
                               PSO_machine_list_5= gbest_machine_5, PSO_ca_5= PSO_Ca_value_5, PSO_u_5= PSO_u_value_5, PSO_DD_5= PSO_DD_value_5,
                               PSO_machine_list_6= gbest_machine_6, PSO_ca_6= PSO_Ca_value_6, PSO_u_6= PSO_u_value_6, PSO_DD_6= PSO_DD_value_6,
                               TS_machine_list_1= TS_machine_list_1, TS_ca_1= TS_ca_1, TS_u_1= TS_u_1, TS_DD_1= TS_DD_1,
                               TS_machine_list_2= TS_machine_list_2, TS_ca_2= TS_ca_2, TS_u_2= TS_u_2, TS_DD_2= TS_DD_2,
                               TS_machine_list_3= TS_machine_list_3, TS_ca_3= TS_ca_3, TS_u_3= TS_u_3, TS_DD_3= TS_DD_3,
                               TS_machine_list_4= TS_machine_list_4, TS_ca_4= TS_ca_4, TS_u_4= TS_u_4, TS_DD_4= TS_DD_4,
                               TS_machine_list_5= TS_machine_list_5, TS_ca_5= TS_ca_5, TS_u_5= TS_u_5, TS_DD_5= TS_DD_5,
                               TS_machine_list_6= TS_machine_list_6, TS_ca_6= TS_ca_6, TS_u_6= TS_u_6, TS_DD_6= TS_DD_6,
                               scheduling_P1M1_plot_url = scheduling_P1M1_plot_url,scheduling_P1M2_plot_url = scheduling_P1M2_plot_url, scheduling_P1M3_plot_url = scheduling_P1M3_plot_url,
                               scheduling_P2M1_plot_url = scheduling_P2M1_plot_url,scheduling_P2M2_plot_url = scheduling_P2M2_plot_url, scheduling_P2M3_plot_url = scheduling_P2M3_plot_url,
                               scheduling_P3M1_plot_url = scheduling_P3M1_plot_url,scheduling_P3M2_plot_url = scheduling_P3M2_plot_url, scheduling_P3M3_plot_url = scheduling_P3M3_plot_url,
                               scheduling_P4M1_plot_url = scheduling_P4M1_plot_url,scheduling_P4M2_plot_url = scheduling_P4M2_plot_url, scheduling_P4M3_plot_url = scheduling_P4M3_plot_url,
                               scheduling_P5M1_plot_url = scheduling_P5M1_plot_url,scheduling_P5M2_plot_url = scheduling_P5M2_plot_url, scheduling_P5M3_plot_url = scheduling_P5M3_plot_url,
                               scheduling_P6M1_plot_url = scheduling_P6M1_plot_url,scheduling_P6M2_plot_url = scheduling_P6M2_plot_url, scheduling_P6M3_plot_url = scheduling_P6M3_plot_url,
                               ACO_P1M1_plot_url = ACO_P1M1_plot_url,ACO_P1M2_plot_url = ACO_P1M2_plot_url, ACO_P1M3_plot_url = ACO_P1M3_plot_url,
                               ACO_P2M1_plot_url = ACO_P2M1_plot_url,ACO_P2M2_plot_url = ACO_P2M2_plot_url, ACO_P2M3_plot_url = ACO_P2M3_plot_url,
                               ACO_P3M1_plot_url = ACO_P3M1_plot_url,ACO_P3M2_plot_url = ACO_P3M2_plot_url, ACO_P3M3_plot_url = ACO_P3M3_plot_url,
                               ACO_P4M1_plot_url = ACO_P4M1_plot_url,ACO_P4M2_plot_url = ACO_P4M2_plot_url, ACO_P4M3_plot_url = ACO_P4M3_plot_url,
                               ACO_P5M1_plot_url = ACO_P5M1_plot_url,ACO_P5M2_plot_url = ACO_P5M2_plot_url, ACO_P5M3_plot_url = ACO_P5M3_plot_url,
                               ACO_P6M1_plot_url = ACO_P6M1_plot_url,ACO_P6M2_plot_url = ACO_P6M2_plot_url, ACO_P6M3_plot_url = ACO_P6M3_plot_url,
                               PSO_P1M1_plot_url = PSO_P1M1_plot_url,PSO_P1M2_plot_url = PSO_P1M2_plot_url, PSO_P1M3_plot_url = PSO_P1M3_plot_url,
                               PSO_P2M1_plot_url = PSO_P2M1_plot_url,PSO_P2M2_plot_url = PSO_P2M2_plot_url, PSO_P2M3_plot_url = PSO_P2M3_plot_url,
                               PSO_P3M1_plot_url = PSO_P3M1_plot_url,PSO_P3M2_plot_url = PSO_P3M2_plot_url, PSO_P3M3_plot_url = PSO_P3M3_plot_url,
                               PSO_P4M1_plot_url = PSO_P4M1_plot_url,PSO_P4M2_plot_url = PSO_P4M2_plot_url, PSO_P4M3_plot_url = PSO_P4M3_plot_url,
                               PSO_P5M1_plot_url = PSO_P5M1_plot_url,PSO_P5M2_plot_url = PSO_P5M2_plot_url, PSO_P5M3_plot_url = PSO_P5M3_plot_url,
                               PSO_P6M1_plot_url = PSO_P6M1_plot_url,PSO_P6M2_plot_url = PSO_P6M2_plot_url, PSO_P6M3_plot_url = PSO_P6M3_plot_url,
                               GA_P1M1_plot_url = GA_P1M1_plot_url,GA_P1M2_plot_url = GA_P1M2_plot_url, GA_P1M3_plot_url = GA_P1M3_plot_url,
                               GA_P2M1_plot_url = GA_P2M1_plot_url,GA_P2M2_plot_url = GA_P2M2_plot_url, GA_P2M3_plot_url = GA_P2M3_plot_url,
                               GA_P3M1_plot_url = GA_P3M1_plot_url,GA_P3M2_plot_url = GA_P3M2_plot_url, GA_P3M3_plot_url = GA_P3M3_plot_url,
                               GA_P4M1_plot_url = GA_P4M1_plot_url,GA_P4M2_plot_url = GA_P4M2_plot_url, GA_P4M3_plot_url = GA_P4M3_plot_url,
                               GA_P5M1_plot_url = GA_P5M1_plot_url,GA_P5M2_plot_url = GA_P5M2_plot_url, GA_P5M3_plot_url = GA_P5M3_plot_url,
                               GA_P6M1_plot_url = GA_P6M1_plot_url,GA_P6M2_plot_url = GA_P6M2_plot_url, GA_P6M3_plot_url = GA_P6M3_plot_url,
                               TS_P1M1_plot_url = TS_P1M1_plot_url,TS_P1M2_plot_url = TS_P1M2_plot_url, TS_P1M3_plot_url = TS_P1M3_plot_url,
                               TS_P2M1_plot_url = TS_P2M1_plot_url,TS_P2M2_plot_url = TS_P2M2_plot_url, TS_P2M3_plot_url = TS_P2M3_plot_url,
                               TS_P3M1_plot_url = TS_P3M1_plot_url,TS_P3M2_plot_url = TS_P3M2_plot_url, TS_P3M3_plot_url = TS_P3M3_plot_url,
                               TS_P4M1_plot_url = TS_P4M1_plot_url,TS_P4M2_plot_url = TS_P4M2_plot_url, TS_P4M3_plot_url = TS_P4M3_plot_url,
                               TS_P5M1_plot_url = TS_P5M1_plot_url,TS_P5M2_plot_url = TS_P5M2_plot_url, TS_P5M3_plot_url = TS_P5M3_plot_url,
                               TS_P6M1_plot_url = TS_P6M1_plot_url,TS_P6M2_plot_url = TS_P6M2_plot_url, TS_P6M3_plot_url = TS_P6M3_plot_url,
                               MC_P1M1_plot_url = MC_P1M1_plot_url,MC_P1M2_plot_url = MC_P1M2_plot_url, MC_P1M3_plot_url = MC_P1M3_plot_url,
                               MC_P2M1_plot_url = MC_P2M1_plot_url,MC_P2M2_plot_url = MC_P2M2_plot_url, MC_P2M3_plot_url = MC_P2M3_plot_url,
                               MC_P3M1_plot_url = MC_P3M1_plot_url,MC_P3M2_plot_url = MC_P3M2_plot_url, MC_P3M3_plot_url = MC_P3M3_plot_url,
                               MC_P4M1_plot_url = MC_P4M1_plot_url,MC_P4M2_plot_url = MC_P4M2_plot_url, MC_P4M3_plot_url = MC_P4M3_plot_url,
                               MC_P5M1_plot_url = MC_P5M1_plot_url,MC_P5M2_plot_url = MC_P5M2_plot_url, MC_P5M3_plot_url = MC_P5M3_plot_url,
                               MC_P6M1_plot_url = MC_P6M1_plot_url,MC_P6M2_plot_url = MC_P6M2_plot_url, MC_P6M3_plot_url = MC_P6M3_plot_url,
                               bad_P1M1_plot_url = bad_P1M1_plot_url,bad_P1M2_plot_url = bad_P1M2_plot_url, bad_P1M3_plot_url = bad_P1M3_plot_url,
                               bad_P2M1_plot_url = bad_P2M1_plot_url,bad_P2M2_plot_url = bad_P2M2_plot_url, bad_P2M3_plot_url = bad_P2M3_plot_url,
                               bad_P3M1_plot_url = bad_P3M1_plot_url,bad_P3M2_plot_url = bad_P3M2_plot_url, bad_P3M3_plot_url = bad_P3M3_plot_url,
                               bad_P4M1_plot_url = bad_P4M1_plot_url,bad_P4M2_plot_url = bad_P4M2_plot_url, bad_P4M3_plot_url = bad_P4M3_plot_url,
                               bad_P5M1_plot_url = bad_P5M1_plot_url,bad_P5M2_plot_url = bad_P5M2_plot_url, bad_P5M3_plot_url = bad_P5M3_plot_url,
                               bad_P6M1_plot_url = bad_P6M1_plot_url,bad_P6M2_plot_url = bad_P6M2_plot_url, bad_P6M3_plot_url = bad_P6M3_plot_url,
                               SL_TF_tabu = SL_TF_tabu, GL_TF_tabu = GL_TF_tabu)
    


if __name__ == '__main__':
    ## 本機端輸入 IP + Port
    app.run(host='127.0.0.1', port=8000)
    app.run(debug = False)