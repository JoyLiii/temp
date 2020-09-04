# -*- coding: utf-8 -*-
"""
Created on Tue May  8 15:55:33 2018

@author: polatbilek
"""

## 這個演算法是利用塔布搜尋找出最小解

import pandas as pd
import numpy as np
from random import randint
import random

## 製造可以走的路徑圖 並給予值
def make_graph(M, M1, M2, M3, machine_value, w1, w2, w3, w4, w5, w6, w7, w8, w9):
    
    graph ={}
    
    
    for i in range(len(machine_value)+1):
        linklist = []
        for j in range(len(machine_value)+1):
            ## 起始點到 M1
            if(i == 0):
                if( 0 < j < len(M1)+1):
                    linklist.append([ j, w1*machine_value[j-1][1]+  w2*machine_value[j-1][2]+ w3*machine_value[j-1][3]+ w4*machine_value[j-1][4]
                                        + w5*machine_value[j-1][5]+ w6*machine_value[j-1][6]+ w7*machine_value[j-1][7]+ w8*machine_value[j-1][8] + w9*machine_value[j-1][9]])
                    graph[str(i)] = linklist
            ## M1 到 M2
            elif(0 < i < len(M1)+1):
                if( len(M1) < j < len(M1)+len(M2)+1):
                    linklist.append([ j, w1*machine_value[j-1][1]+  w2*machine_value[j-1][2]+ w3*machine_value[j-1][3]+ w4*machine_value[j-1][4]
                                        + w5*machine_value[j-1][5]+ w6*machine_value[j-1][6]+ w7*machine_value[j-1][7]+ w8*machine_value[j-1][8]+ w9*machine_value[j-1][9]])
                    graph[str(i)] = linklist
            ## M2 到 M3
            elif( len(M1) < i < len(M1)+len(M2)+1):
                if( len(M1)+len(M2) < j < len(M1)+len(M2)+len(M3)+1):
                    linklist.append([ j, w1*machine_value[j-1][1]+  w2*machine_value[j-1][2]+ w3*machine_value[j-1][3]+ w4*machine_value[j-1][4]
                                        + w5*machine_value[j-1][5]+ w6*machine_value[j-1][6]+ w7*machine_value[j-1][7]+ w8*machine_value[j-1][8]+ w9*machine_value[j-1][9]])
                    graph[str(i)] = linklist
            ## 結束
            else:
                linklist.append([ 0,0 ])
                graph[str(i)] = linklist
                break
    max_weight = max([machine_value[i][1] for i in range(len(M)-1)])
    
    return graph, max_weight
        
        
## 尋找其他可行解
def getNeighbors(M1, M2, M3, state, neighborhood_size, machine_value):
    for i in range(neighborhood_size):
        route = []
        # 隨機產生可行解
        path = []
        path.append(0)
        path.append(random.choices(range(1,len(M1)+1), weights = [1/machine_value[i][1] for i in range(len(M1))], k = 1)[0])
        path.append(random.choices(range(len(M1)+1,len(M1)+len(M2)+1), weights = [1/machine_value[i][1] for i in range(len(M1),len(M1)+len(M2)) ], k = 1)[0])
        path.append(random.choices(range(len(M1)+len(M2)+1,len(M1)+len(M2)+len(M3)+1), weights = [1/machine_value[i][1] for i in range(len(M1)+len(M2),len(M1)+len(M2)+len(M3)) ], k = 1)[0])
        route.append(path)
        
    return route


## 設定fitness函數 並加總
def fitness(route, graph):
    path_length = 0
    
    for i in range(len(route)):
        if(i+1 != len(route)):
            dist = weight_distance(route[i], route[i+1], graph)
            if dist != -1:
                path_length = path_length + dist
            else:
                return max_fitness 
                
        else:
            dist = weight_distance(route[i], route[0], graph)
            if dist != -1:
                path_length = path_length + dist
            else:
                return max_fitness 
    return path_length
            

## 判斷路徑是否可走或結束
def weight_distance(city1, city2, graph):
    global max_fitness
    
    neighbors = graph[str(city1)]
    
    for neighbor in neighbors:
        if neighbor[0] == int(city2):
            return neighbor[1]
        
    return -1 

## 禁忌搜尋過程
def tabu_search(M, M1, M2, M3, machine_value, neighborhood_size, stoppingTurn, maxTabuSize, w1, w2, w3, w4, w5, w6, w7, w8, w9):
    global max_fitness
    
    ## 製造可以走的路徑圖 並給予值
    graph, max_weight = make_graph(M, M1, M2, M3, machine_value, w1, w2, w3, w4, w5, w6, w7, w8, w9)
    
    ## 隨機產生可行解
    s0 = []
    s0.append(0)
    s0.append(random.choices(range(1,len(M1)+1), weights = [1/machine_value[i][1] for i in range(len(M1))], k = 1)[0])
    s0.append(random.choices(range(len(M1)+1,len(M1)+len(M2)+1), weights = [1/machine_value[i][1] for i in range(len(M1),len(M1)+len(M2)) ], k = 1)[0])
    s0.append(random.choices(range(len(M1)+len(M2)+1,len(M1)+len(M2)+len(M3)+1), weights = [1/machine_value[i][1] for i in range(len(M1)+len(M2),len(M1)+len(M2)+len(M3)) ], k = 1)[0])

    ## 賦予max_fitness初始值(最差)
    max_fitness = ((max_weight) * (len(s0)))+1
    sBest = s0
    ## 計算fitness數值
    vBest = fitness(s0, graph)
    bestCandidate = s0
    ## 更新tabu list
    tabuList = []
    tabuList.append(s0)
    stop = False
    best_keep_turn = 0
    
    ## 迭代
    while not stop :
        ## 尋找其他可行解
        sNeighborhood = getNeighbors(M1, M2, M3, bestCandidate, neighborhood_size, machine_value)
        bestCandidate = sNeighborhood[0]
        
        ## 找出其他可行解中最好的解
        for sCandidate in sNeighborhood:
            if (sCandidate not in tabuList) and ((fitness(sCandidate, graph) < fitness(bestCandidate, graph))):
                bestCandidate = sCandidate
        ## 更新條件
        if (fitness(bestCandidate, graph) < fitness(sBest, graph)):
            sBest = bestCandidate
            vBest = fitness(sBest, graph)
            best_keep_turn = 0

        tabuList.append(bestCandidate)
        if (len(tabuList) > maxTabuSize):
            tabuList.pop(0)
            
        if best_keep_turn == stoppingTurn:
            stop = True
            
        best_keep_turn += 1
    
    return sBest, vBest

## 主程式   
def TS_main(thin, photo, etch, w1, w2, w3, w4, w5, w6, w7, w8, w9):
    
    start = ['start']
    M1 = list(thin.index)
    M2 = list(photo.index)
    M3 = list(etch.index)

    
    if len(M1) == 0 or len(M2) == 0  or len(M3) == 0 :
        return  [ "No_machine", "No_machine", "No_machine"] , 0, 0, 0

    else:
    
        M = start+ M1 + M2 + M3
        M_num = [i for i in range(len(M))]
        
        ## 將表格整合
        machine_value = np.vstack((thin.values,photo.values,etch.values))
        
        ## 參數
        maxTabuSize = 5         # tabu list的 size
        neighborhood_size = 10  # 迭代一次的可行解
        stoppingTurn = 5        # 迭代次數
        
        ## 禁忌搜尋過程
        solution, value = tabu_search(M, M1, M2, M3, machine_value, neighborhood_size, stoppingTurn, maxTabuSize, w1, w2, w3, w4, w5, w6, w7, w8, w9)
        
        ## 計算各數值
        ca_value = round(thin.loc[M1[solution[1]-1]][1] + photo.loc[M2[solution[2]-1-len(M1)]][1]+ etch.loc[M3[solution[3]-1-len(M1)-len(M2)]][1],4)
        u_value = round(thin.loc[M1[solution[1]-1]][5] + photo.loc[M2[solution[2]-1-len(M1)]][5]+ etch.loc[M3[solution[3]-1-len(M1)-len(M2)]][5],4)
        DD_value = round(thin.loc[M1[solution[1]-1]][9] + photo.loc[M2[solution[2]-1-len(M1)]][9]+ etch.loc[M3[solution[3]-1-len(M1)-len(M2)]][9],4)
        
        return [M1[solution[1]-1],M2[solution[2]-1-len(M1)],M3[solution[3]-1-len(M1)-len(M2)]], ca_value, u_value, DD_value


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
    machine_list, ca ,u, DD = TS_main(thin, photo, etch, w1, w2, w3, w4, w5, w6, w7, w8, w9)
    

            
