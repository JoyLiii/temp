# -*- coding: utf-8 -*-
"""
Created on Wed Jul  8 14:26:27 2020

@author: USER
"""

## 這個演算法是利用蒙地卡羅找出最小解

import random
import pandas as pd


## 主程式
def MC_main(thin, photo, etch, w1, w2, w3, w4, w5, w6, w7, w8, w9):

    t_number = len(thin)
    p_number = len(photo)
    e_number = len(etch)
    
    M1 = list(thin.index)
    M2 = list(photo.index)
    M3 = list(etch.index)
    
    if len(M1) == 0 or len(M2) == 0  or len(M3) == 0 :
        select = [ "No_machine", "No_machine", "No_machine"]    
        Ca_value = 0
        u_value = 0
        DD_value = 0
    else:
        times = 20
        ## 隨機挑選各process中的一組機台當初始解
        t = random.randint(0, t_number-1)
        p = random.randint(0, p_number-1)
        e = random.randint(0, e_number-1)
        
        ## 綜效數值
        value = (  w1*thin.Ca_mean[t]+ w1*photo.Ca_mean[p]+ w1*etch.Ca_mean[e]
                 + w2*thin.Ca_std[t]+ w2*photo.Ca_std[p]+ w2*etch.Ca_std[e]
                 + w3*thin.Ca_min[t]+ w3*photo.Ca_min[p]+ w3*etch.Ca_min[e]
                 + w4*thin.Ca_max[t]+ w4*photo.Ca_max[p]+ w4*etch.Ca_max[e]
                 + w5*thin.u_mean[t]+ w5*photo.u_mean[p]+ w5*etch.u_mean[e]
                 + w6*thin.u_std[t]+ w6*photo.u_std[p]+ w6*etch.u_std[e]
                 + w7*thin.u_min[t]+ w7*photo.u_min[p]+ w7*etch.u_min[e]
                 + w8*thin.u_max[t]+ w8*photo.u_max[p]+ w8*etch.u_max[e]
                 + w9*thin.DD[t]+ w9*photo.DD[p]+ w9*etch.DD[e])
        
        
        select = [M1[t], M2[p], M3[e]]
        
        classification =['thin','photo','etch']
        
        for i in range(times):
            
            ## 隨機選擇三個process中的一個
            current_select = random.randint(0, len(classification)-1)
        
            ## 挑選 thin
            if current_select == 0:
                ## 隨機挑選一組機台
                current_t = random.randint(0, t_number-1)
                current_value = (  w1*thin.Ca_mean[current_t]+ w1*photo.Ca_mean[p]+ w1*etch.Ca_mean[e]
                                 + w2*thin.Ca_std[current_t]+ w2*photo.Ca_std[p]+ w2*etch.Ca_std[e]
                                 + w3*thin.Ca_min[current_t]+ w3*photo.Ca_min[p]+ w3*etch.Ca_min[e]
                                 + w4*thin.Ca_max[current_t]+ w4*photo.Ca_max[p]+ w4*etch.Ca_max[e]
                                 + w5*thin.u_mean[current_t]+ w5*photo.u_mean[p]+ w5*etch.u_mean[e]
                                 + w6*thin.u_std[current_t]+ w6*photo.u_std[p]+ w6*etch.u_std[e]
                                 + w7*thin.u_min[current_t]+ w7*photo.u_min[p]+ w7*etch.u_min[e]
                                 + w8*thin.u_max[current_t]+ w8*photo.u_max[p]+ w8*etch.u_max[e]
                                 + w9*thin.DD[current_t]+ w9*photo.DD[p]+ w9*etch.DD[e])
                ## 更新條件
                if (current_value < value):
                    value = current_value
                    select = [M1[current_t], M2[p], M3[e]]
            
            ## 挑選 photo
            elif current_select == 1:
                ## 隨機挑選一組機台
                current_p = random.randint(0, p_number-1)
                current_value = (  w1*thin.Ca_mean[t]+ w1*photo.Ca_mean[current_p]+ w1*etch.Ca_mean[e]
                                 + w2*thin.Ca_std[t]+ w2*photo.Ca_std[current_p]+ w2*etch.Ca_std[e]
                                 + w3*thin.Ca_min[t]+ w3*photo.Ca_min[current_p]+ w3*etch.Ca_min[e]
                                 + w4*thin.Ca_max[t]+ w4*photo.Ca_max[current_p]+ w4*etch.Ca_max[e]
                                 + w5*thin.u_mean[t]+ w5*photo.u_mean[current_p]+ w5*etch.u_mean[e]
                                 + w6*thin.u_std[t]+ w6*photo.u_std[current_p]+ w6*etch.u_std[e]
                                 + w7*thin.u_min[t]+ w7*photo.u_min[current_p]+ w7*etch.u_min[e]
                                 + w8*thin.u_max[t]+ w8*photo.u_max[current_p]+ w8*etch.u_max[e]
                                 + w9*thin.DD[t]+ w9*photo.DD[current_p]+ w9*etch.DD[e])
                
                if (current_value < value ):
                    value = current_value
                    select = [M1[t], M2[current_p], M3[e]]
            
            ## 挑選 etch
            else:
                ## 隨機挑選一組機台
                current_e = random.randint(0, e_number-1)
                current_value = (  w1*thin.Ca_mean[t]+ w1*photo.Ca_mean[p]+ w1*etch.Ca_mean[current_e]
                                 + w2*thin.Ca_std[t]+ w2*photo.Ca_std[p]+ w2*etch.Ca_std[current_e]
                                 + w3*thin.Ca_min[t]+ w3*photo.Ca_min[p]+ w3*etch.Ca_min[current_e]
                                 + w4*thin.Ca_max[t]+ w4*photo.Ca_max[p]+ w4*etch.Ca_max[current_e]
                                 + w5*thin.u_mean[t]+ w5*photo.u_mean[p]+ w5*etch.u_mean[current_e]
                                 + w6*thin.u_std[t]+ w6*photo.u_std[p]+ w6*etch.u_std[current_e]
                                 + w7*thin.u_min[t]+ w7*photo.u_min[p]+ w7*etch.u_min[current_e]
                                 + w8*thin.u_max[t]+ w8*photo.u_max[p]+ w8*etch.u_max[current_e]
                                 + w9*thin.DD[t]+ w9*photo.DD[p]+ w9*etch.DD[current_e])
                ## 更新條件
                if (current_value < value ):
                    value = current_value
                    select = [M1[t], M2[p], M3[current_e]]
       
        ## 計算各數值
        Ca_value = round(thin.loc[select[0]][1]+ photo.loc[select[1]][1]+ etch.loc[select[2]][1],4)
        u_value = round(thin.loc[select[0]][5]+ photo.loc[select[1]][5]+ etch.loc[select[2]][5],4)
        DD_value = round(thin.loc[select[0]][9]+ photo.loc[select[1]][9]+ etch.loc[select[2]][9],4)
    
    return select, Ca_value, u_value, DD_value

if __name__ == "__main__":
    
    ## 3個 Process 的資料
     
#    thin = pd.read_csv('thin.csv',index_col="machine")
#    photo = pd.read_csv('photo.csv',index_col="machine")
#    etch = pd.read_csv('etch.csv',index_col="machine")
    
    ## 權重的設置
    
    ## Ca
#    w1 = 0.4
#    w2 = 0.1
#    w3 = 0
#    w4 = 0
    
    ## U
#    w5 = 0.4
#    w6 = 0.1
#    w7 = 0
#    w8 = 0

    ## DD
#    w9 = 1
    
    ## 主程式
    select, Ca_value, u_value, DD_value = MC_main(thin, photo, etch, w1, w2, w3, w4, w5, w6, w7, w8, w9)
    