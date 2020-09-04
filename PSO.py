# -*- coding: utf-8 -*-
"""
Created on Fri Jul 10 15:36:26 2020

@author: 2007043
"""

## 這個演算法是利用鳥群/粒子化演算法找出最小解
import random
import pandas as pd
import numpy as np


## 設定fitness函數 weight*parameter
def fitness_function(position, w1, w2, w3, w4, w5, w6, w7, w8, w9):
    return w1*position[0] + w2*position[1] + w3*position[2]+ w4*position[3] + w5*position[4] + w6*position[5] + w7*position[6]+ w8*position[7]+ w9*position[8]


## 初始化vector數值 一組參數 size= 3*9
def init_vector(M1, M2, M3, thin, photo, etch,n_particles):
    
    cand = []
    
    for i in range(n_particles):
        t = random.choice(M1)
        p = random.choice(M2)
        e = random.choice(M3)
        cand.append([thin.Ca_mean[t], thin.Ca_std[t], thin.Ca_min[t], thin.Ca_max[t], thin.u_mean[t], thin.u_std[t], thin.u_min[t], thin.u_max[t], thin.DD[t]
                    ,photo.Ca_mean[p], photo.Ca_std[p], photo.Ca_min[p], photo.Ca_max[p], photo.u_mean[p], photo.u_std[p], photo.u_min[p], photo.u_max[p], photo.DD[p]
                    ,etch.Ca_mean[e], etch.Ca_std[e], etch.Ca_min[e], etch.Ca_max[e], etch.u_mean[e], etch.u_std[e], etch.u_min[e], etch.u_max[e], etch.DD[e]])
    
    vector = (np.array(cand))
    
    return vector

## 初始化vector為零 size= 3*9
def init_velo_vector(n_particles):
    
    vector =([np.array([0]*27) for _ in range(n_particles)])
    return vector

## 鳥群飛行
def PSO(w1, w2, w3, w4, w5, w6, w7, w8, w9, n_iterations, n_particles, W, c1, c2, particle_position_vector, velocity_vector, pbest_position, pbest_fitness_value, gbest_fitness_value, gbest_position):
    iteration = 0
    
    while iteration < n_iterations:
        for i in range(n_particles):
            ## 計算fitness
            fitness_cadidate = fitness_function(particle_position_vector[i], w1, w2, w3, w4, w5, w6, w7, w8, w9)
            #print('第',iteration,'代鳥群: value =',fitness_cadidate,'  |  position =',particle_position_vector[i])
            
            ## pbest更新條件(個體)
            if(pbest_fitness_value[i] > fitness_cadidate):
                pbest_fitness_value[i] = fitness_cadidate
                pbest_position[i] = particle_position_vector[i]
            
            ## gbest更新條件(群體)
            if(gbest_fitness_value > fitness_cadidate):
                gbest_fitness_value = fitness_cadidate
                gbest_position = particle_position_vector[i]
        
        ## 位置(向量)更新
        for i in range(n_particles):
            new_velocity = (W*velocity_vector[i]) + (c1*random.random()) * (pbest_position[i] - particle_position_vector[i]) + (c2*random.random()) * (gbest_position-particle_position_vector[i])
            new_position = new_velocity + particle_position_vector[i]
            particle_position_vector[i] = new_position
    
        iteration = iteration + 1
        
    return gbest_position


## PSO主程式
def PSO_main(thin, photo, etch, w1, w2, w3, w4, w5, w6, w7, w8, w9):
    
    start = ['start']
    M1 = list(thin.index)
    M2 = list(photo.index)
    M3 = list(etch.index)

    if len(M1) == 0 or len(M2) == 0  or len(M3) == 0 :
        gbest_machine = ["No_machine", "No_machine", "No_machine"]    
        Ca_value = 0
        u_value = 0
        DD_value = 0
    else:
    
        M = start+ M1 + M2 + M3
        M_num = [i for i in range(len(M))]
        ## 將表格整合
        machine_value = np.vstack((thin.values,photo.values,etch.values))
            
        ## 參數
        W = 0.7   # vector
        c1 = 0.5  # pbest
        c2 = 0.5  # gbest
        
        n_iterations = 10  # 迭代次數
        n_particles = 20   # 鳥個數
        
        ## 初始化vector數值
        particle_position_vector = init_vector(M1, M2, M3,thin, photo, etch, n_particles)
        
        ## 初始化pbest與資料型態設置
        pbest_position = particle_position_vector
        pbest_fitness_value = np.array([float('inf') for _ in range(n_particles)])
        gbest_fitness_value = float('inf')
        gbest_position = np.array([float('inf'), float('inf')])
        
        ## 初始化vector為零
        velocity_vector = init_velo_vector(n_particles)
        
        ## 將依次迭代中最好的結果設為 gbest
        gbest_position = PSO(w1, w2, w3, w4, w5, w6, w7, w8, w9, n_iterations, n_particles, W, c1, c2, particle_position_vector, velocity_vector, pbest_position, pbest_fitness_value, gbest_fitness_value, gbest_position)
        
        gbest_machine = []
        
        ## 找到對應機台名稱
        for i in range(len(M1)):
            if gbest_position[0] == float(thin.Ca_mean[i]):
                gbest_machine.append(M1[i])
                break
        
        for j in range(len(M2)):
            if gbest_position[9] == float(photo.Ca_mean[j]):
                gbest_machine.append(M2[j])
                break
        
        for k in range(len(M3)):
            if gbest_position[18] == float(etch.Ca_mean[k]):
                gbest_machine.append(M3[k])
                break
            
        #print("The best u position is ", gbest_machine)
        
        ## 計算各數值
        Ca_value = round(thin.loc[gbest_machine[0]][1] + photo.loc[gbest_machine[1]][1]+ etch.loc[gbest_machine[2]][1],4)
        u_value = round(thin.loc[gbest_machine[0]][5] + photo.loc[gbest_machine[1]][5]+ etch.loc[gbest_machine[2]][5],4)
        DD_value = round(thin.loc[gbest_machine[0]][9] + photo.loc[gbest_machine[1]][9]+ etch.loc[gbest_machine[2]][9],4)
    
    return gbest_machine, Ca_value, u_value, DD_value

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
    gbest_machine, Ca_value, u_value, DD_value = PSO_main(thin, photo, etch, w1, w2, w3, w4, w5, w6, w7, w8, w9)
    
    