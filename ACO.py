# -*- coding: utf-8 -*-
"""
Created on Wed Jul  8 15:51:41 2020

@author: 2007043
"""

## 這個演算法是利用螞蟻演算法可能次要解

import sys
import numpy as np
import pandas as pd
import random

## 計算一組解的各數值
def makespan(seq, machine_value):
    Ca = machine_value[seq[1]-1][1] + machine_value[seq[2]-1][1] + machine_value[seq[3]-1][1]
    u = machine_value[seq[1]-1][5] + machine_value[seq[2]-1][5] + machine_value[seq[3]-1][5]
    DD = machine_value[seq[1]-1][9] + machine_value[seq[2]-1][9] + machine_value[seq[3]-1][9]
    return Ca, u, DD

## 得到 machine的 seq
def machine(seq, M):
    M_seq = []
    for i in range(1,len(seq)):
        M_seq.append(M[seq[i]])
    return M_seq

## 費洛蒙初始化 Q
def pheromone(M, M1, M2, M3, Q):
    
    ## 初始化費洛蒙為 0
    phe = [[0 for i in range(len(M))] for j in range(len(M))]     

    ## 把可以走的路線設為Q
    for i in range(len(phe)):
        if (i == 0):
            for j in range(1, len(M1)+1):
                phe[i][j] = Q
        elif (0 < i <= len(M1)):
            for j in range(len(M1)+1,  len(M1)+len(M2)+1):
                phe[i][j] = Q
        elif (len(M1) < i <= len(M1)+len(M2)):
            for j in range(len(M1)+len(M2)+1,  len(M1)+len(M2)+len(M3)+1):
                phe[i][j] = Q
    return phe


## 機率更新
def trans_update(M1, M2, M3, trans, phe, vis_Ca, vis_u, vis_DD, alpha, beta, gamma, delta):
    for i in range(len(M1)+len(M2)+1):
        summ = 0
        
        ## 計算全部數值總和
        for j in range(len(trans)):
            summ += (phe[i][j]**alpha) * (vis_Ca[j-1]**beta) * (vis_u[j-1]**gamma) * (vis_DD[j-1]**delta)
        
        ## 個別/全部
        for j in range(len(trans)):
            trans[i][j] = ((phe[i][j]**alpha) * (vis_Ca[j-1]**beta) * (vis_u[j-1]**gamma) * (vis_DD[j-1]**delta)) / summ
    return

## 可見度設定
def visualization(machine_value, w1, w2, w3, w4, w5, w6, w7, w8, w9):
    vis_Ca = []
    vis_u = []
    vis_DD = []
    
    ## 各數值的倒豎
    for i in range(len(machine_value)):
        vis_Ca.append(1/( w1*machine_value[i][1]+ w2*machine_value[i][2]+ w3*machine_value[i][3]+ w4*machine_value[i][4]+1)) #+1是避免分母 0
        vis_u.append(1/( w5*machine_value[i][5]+ w6*machine_value[i][6]+ w7*machine_value[i][7]+ w8*machine_value[i][8]+1))  #+1是避免分母 0
        vis_DD.append(1/( w9*machine_value[i][9]+1))  #+1是避免分母 0
        
    return vis_Ca, vis_u, vis_DD


## 挑路徑與更新機率
def ACO_path(trans, M_num):
    
    path = []
    ## 已經走過的路，將他的trans歸零變成trans2
    
    ## 初始化trans2
    trans2 = [[0 for r in range(len(trans))]for s in range(len(trans))]
    
    for r in range(len(trans)):
        for s in range(len(trans)):
            trans2[r][s] = trans[r][s]
    
    start = 0
    path.append(start)
    ## 已經走過的路歸零
    for r in range(len(trans2)):
        trans2[r][0] = 0
    
    ## 開始挑路線
    for r in range(3):     
            nextt = random.choices(M_num ,weights = trans2[path[-1]], k = 1)
            path.append(nextt[0])
            for r in range(len(trans2)):
                trans2[r][nextt[0]] = 0
    return path


## 路徑上的費洛蒙(過去經驗)
def path_phe(path, phe2, Q, minn1, minn2, minn3):
    ## 每走完一隻螞蟻，紀錄他留下來的費洛蒙
    for r in range(len(path)-1):    
        phe2[path[r]][path[r+1]] = Q / (minn1 + minn2 + minn3)
        
    return phe2

## 路徑上的費洛蒙(現在經驗)
def current_phe( eva, phe, phe_updated):
    ## 走完一代的全部螞蟻後，更新費洛盟
    for j in range(len(phe)):       
            for r in range(len(phe)):
                phe[j][r] = (1-eva) * phe[j][r] + phe_updated[j][r]
    return phe


## 螞蟻走路
def ACO(Q, eva ,M, M1 ,M2 ,M3, M_num, machine_value ,epoch, ant, trans, phe, vis_Ca, vis_u, vis_DD, alpha, beta, gamma, delta, minn1, minn2, minn3):
    
    for k in range(epoch):
        #print('第',k,'個epoch')
        
        ## 機率更新
        trans_update( M1 ,M2 ,M3 ,trans, phe, vis_Ca, vis_u, vis_DD, alpha, beta, gamma, delta)
        ## 紀錄每有螞蟻走過，留下的費洛蒙
        phe2 = [[0 for i in range(len(M))] for j in range(len(M))]      
        
        
        ##每隻螞蟻開始走
        for j in range(ant):   
            ## 挑路徑與更新機率
            path = ACO_path(trans, M_num)
            
            ## 計算一組解的各數值
            Ca, u, DD = makespan(path, machine_value)
            
            ## 更新條件 找極端值(可能不同於最佳解)
            if (Ca < minn1 and u < minn2 and DD< minn3):
                minn1 = Ca
                minn2 = u
                minn3 = DD
                M_path = machine(path, M)
                #print(path,'=>',M_path, '-------Ca =',minn1, '  u =',minn2)
            
            ## 路徑上的費洛蒙(過去經驗)
            update_phe = path_phe(path, phe2, Q, minn1, minn2, minn3)
        ## 路徑上的費洛蒙(現在經驗)
        phe = current_phe( eva, phe, update_phe)
        
    return path, M_path, minn1, minn2,minn3


## ACO主程式
def ACO_main(thin, photo, etch, w1, w2, w3, w4, w5, w6, w7, w8, w9):
    
    
    
    start = ['start']
    M1 = list(thin.index)
    M2 = list(photo.index)
    M3 = list(etch.index)

    if len(M1) == 0 or len(M2) == 0  or len(M3) == 0 :
        path = ["No_machine", "No_machine", "No_machine"]    
        M_path = ["No_machine", "No_machine", "No_machine"] 
        minn1 = 0
        minn2 = 0
        minn3 = 0
    else:
        
        M = start + M1 + M2 + M3
        M_num = [i for i in range(len(M))]
        
        ## 將表格整合
        machine_value = np.vstack((thin.values,photo.values,etch.values))
        
        ## 參數設置
        epoch = 20   # 世代數
        ant = 10   # 螞蟻數量
        eva = 0.2    # 蒸發率
        Q = 50      # 費洛蒙初始
        alpha = 1    # 費洛蒙權重
        beta = 1     # Ca權重
        gamma = 1    # u權重
        delta = 1    # DD權重
    
        ## 費洛蒙初始化 Q
        phe = pheromone(M, M1, M2, M3,Q)
        
        ## 可見度設定
        vis_Ca, vis_u, vis_DD = visualization(machine_value, w1, w2, w3, w4, w5, w6, w7, w8, w9)
        
        #初始化transition rule
        trans = [[0 for i in range(len(M))]for j in range(len(M))]
    
        #開始走
        minn1 = sys.maxsize
        minn2 = sys.maxsize
        minn3 = sys.maxsize
        
       
        path, M_path, minn1, minn2, minn3 = ACO(Q, eva ,M, M1 ,M2 ,M3, M_num, machine_value ,epoch, ant, trans, phe, vis_Ca, vis_u, vis_DD, alpha, beta, gamma, delta, minn1, minn2, minn3)
        minn1 = round(minn1,4)
        minn2 = round(minn2,4)
        minn3 = round(minn3,4)
    
    return path, M_path, minn1, minn2, minn3
    
    

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
    path, M_path, minn1, minn2, minn3 = ACO_main(thin, photo, etch, w1, w2, w3, w4, w5, w6, w7, w8, w9)