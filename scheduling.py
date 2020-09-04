# -*- coding: utf-8 -*-
"""
Created on Wed Jul  8 13:16:22 2020

@author: USER
"""

## 這個演算法是利用窮舉找出最佳解

import pandas as pd

def scheduling_main(thin, photo, etch, w1, w2, w3, w4, w5, w6, w7, w8, w9):
    
    ## 各Process的機台數量
    t_number = len(thin)
    p_number = len(photo)
    e_number = len(etch)
    
    ## 機台的list
    M1 = list(thin.index)
    M2 = list(photo.index)
    M3 = list(etch.index)
    
    if t_number == 0 or p_number == 0  or e_number == 0:
        machine_list=[]
                ## 取得最佳的結果
        best_machine = [ "No_machine", "No_machine", "No_machine"]
    #    best_machine = [M1[result[-1][0]],M2[result[-1][1]],M3[result[-1][2]]]
        best_ca_value = 0
        best_u_value = 0
        best_DD_value = 0
        
        
        ## 取得最差的結果
        worst_machine = [ "No_machine", "No_machine", "No_machine"]
        worst_ca_value = 0
        worst_u_value = 0
        worst_DD_value = 0
    else:
        value = []
        machine_list = []
        for i in range(t_number):
            for j in range(p_number):
                for k in range(e_number):
                    
                    ## 計算各組合的綜效值
                    cross_value = (w1*thin.Ca_mean[i]+ w1*photo.Ca_mean[j]+ w1*etch.Ca_mean[k]
                                 + w2*thin.Ca_std[i]+ w2*photo.Ca_std[j]+ w2*etch.Ca_std[k]
                                 + w3*thin.Ca_min[i]+ w3*photo.Ca_min[j]+ w3*etch.Ca_min[k]
                                 + w4*thin.Ca_max[i]+ w4*photo.Ca_max[j]+ w4*etch.Ca_max[k]
                                 + w5*thin.u_mean[i]+ w5*photo.u_mean[j]+ w5*etch.u_mean[k]
                                 + w6*thin.u_std[i]+ w6*photo.u_std[j]+ w6*etch.u_std[k]
                                 + w7*thin.u_min[i]+ w7*photo.u_min[j]+ w7*etch.u_min[k]
                                 + w8*thin.u_max[i]+ w8*photo.u_max[j]+ w8*etch.u_max[k]
                                 + w9*thin.DD[i]+ w9*photo.DD[j]+ w9*etch.DD[k])
                    
                    value.append(cross_value)
                    machine_list.append([i,j,k,cross_value])    

        
        ## 把machine list依照綜效值作排列       
        result = sorted(machine_list, key = lambda s: s[3])        
        ## 取得最佳的結果
        best_machine = [ M1[result[0][0]], M2[result[0][1]], M3[result[0][2]]]
    #    best_machine = [M1[result[-1][0]],M2[result[-1][1]],M3[result[-1][2]]]
        best_ca_value = round(thin.Ca_mean[result[0][0]]+ photo.Ca_mean[result[0][1]]+ etch.Ca_mean[result[0][2]],4)
        best_u_value = round(thin.u_mean[result[0][0]]+ photo.u_mean[result[0][1]]+ etch.u_mean[result[0][2]],4)
        best_DD_value = round(thin.DD[result[0][0]]+ photo.DD[result[0][1]]+ etch.DD[result[0][2]],4)
        
        
        ## 取得最差的結果
        worst_machine = [M1[result[-1][0]],M2[result[-1][1]],M3[result[-1][2]]]
        worst_ca_value = round(thin.Ca_mean[result[-1][0]]+ photo.Ca_mean[result[-1][1]]+ etch.Ca_mean[result[-1][2]],4)
        worst_u_value = round(thin.u_mean[result[-1][0]]+ photo.u_mean[result[-1][1]]+ etch.u_mean[result[-1][2]],4)
        worst_DD_value = round(thin.DD[result[-1][0]]+ photo.DD[result[-1][1]]+ etch.DD[result[-1][2]],4)
    
    #print ('Best Select  T:',M1[result[0][0]],'----> N:',M2[result[0][1]],'----> E:', M3[result[0][2]],'  ||| Value =',result[0][3])
    #print ('Worst Select  T:',M1[result[-1][0]],'----> N:',M2[result[-1][1]],'----> E:', M3[result[-1][2]],'  ||| Value =',result[-1][3])
    
    
    
    return machine_list, best_machine, best_ca_value, best_u_value, best_DD_value, worst_machine, worst_ca_value, worst_u_value,  worst_DD_value

if __name__ == "__main__":
    
    ## 3個 Process 的資料
    
#    thin = pd.read_csv('thin.csv',index_col="machine")
#    photo = pd.read_csv('photo.csv',index_col="machine")
#    etch = pd.read_csv('etch.csv',index_col="machine")
#    
    
    ## 權重的設置
    
    ## Ca
#    w1 = 0.4
#    w2 = 0.1
#    w3 = 0
#    w4 = 0
#    
    ## U
#    w5 = 0.4
#    w6 = 0.1
#    w7 = 0
#    w8 = 0
    
    ## DD
#    w9 = 1
    
    
    ##主程式
   machine_list, best_machine, best_ca_value, best_u_value, best_DD_value, worst_machine, worst_ca_value, worst_u_value,  worst_DD_value = scheduling_main(thin, photo, etch, w1, w2, w3, w4, w5, w6, w7, w8, w9)