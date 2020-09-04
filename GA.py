# -*- coding: utf-8 -*-
"""
Created on Mon Jul 13 16:18:40 2020

@author: 2007043
"""

## 這個演算法是利用基因演算法找出最小解

import random
import itertools
import numpy as np
import pandas as pd

## 參數
pop_size= 10    #子代個數
n_generations = 5  #世代數
tournment= 5   #挑選的子代數
mutation= 1
crossover= 1

## 製造可以走的路徑圖 並給予值
def makearr (machine_value, M1, M2, M3, w1, w2, w3, w4, w5, w6, w7, w8, w9):
	
	arr = [[np.inf for i in range(len(machine_value)+1)] for j in range(len(machine_value)+1)]
	for i in range(len(machine_value)+1):
		for j in range(len(machine_value)+1):
			if(i == j):
				arr[i][j] = 0
            ## 起始點到 M1
			elif(i == 0):
				if(0 < j < len(M1)+1):
					arr[i][j]= (w1*machine_value[j-1][1]+ w2*machine_value[j-1][2]+ w3*machine_value[j-1][3]+ w4*machine_value[j-1][4]
							+ w5*machine_value[j-1][5]+ w6*machine_value[j-1][6]+ w7*machine_value[j-1][7]+ w8*machine_value[j-1][8]+ w9*machine_value[j-1][9])
			## M1到 M2
			elif( 0 < i < len(M1)+1):
				if(len(M1) < j < len(M1)+len(M2)+1):
					arr[i][j]= (w1*machine_value[j-1][1]+ w2*machine_value[j-1][2]+ w3*machine_value[j-1][3]+ w4*machine_value[j-1][4]
							+ w5*machine_value[j-1][5]+ w6*machine_value[j-1][6]+ w7*machine_value[j-1][7]+ w8*machine_value[j-1][8]+ w9*machine_value[j-1][9])
			## M2 到 M3
			elif( len(M1) < i < len(M1)+len(M2)+1):
				if(len(M1)+len(M2) < j <= len(M1)+len(M2)+len(M3)):
					arr[i][j]= (w1*machine_value[j-1][1]+ w2*machine_value[j-1][2]+ w3*machine_value[j-1][3]+ w4*machine_value[j-1][4]
							+ w5*machine_value[j-1][5]+ w6*machine_value[j-1][6]+ w7*machine_value[j-1][7]+ w8*machine_value[j-1][8]+ w9*machine_value[j-1][9])
	return arr

## 設定fitness函數 並加總
def fitness(r, arr):
	distance = 0
	for i in range(len(r)-1):
		distance= distance + arr[r[i]-1][r[i+1]-1]
	return distance

## 加總fitness函數
def sum_distance(gen):
	sum_d = 0
	for i in range(pop_size):
		sum_d = sum_d + gen[i][4]
	return sum_d

## 是否成為母代的機率
def prob(r,gen):
	return 1-( r[4]/ sum_distance(gen))	

## 選擇
def selection(gen):
	selected=[]
	count = 0
	
	for i in range(pop_size):
		sel= gen[i]
		if count==tournment:
		  break
		if sel in selected:
		  continue
		for j in range(pop_size):
		  if(prob(sel,gen)<prob(gen[j],gen) and gen[j] not in selected):
		    sel=gen[j]
		selected.append(sel)
		count=count+1
	return selected

## 交配
def crossover(p1,p2):
    child_rt1 = []
    child_rt2 = []
    ## 初始化
    for x in range(0,len(p1)):
        child_rt1.append(None) 
        child_rt2.append(None)
    ## 隨機挑選
    start_pos = random.randint(0,len(p1))
    end_pos = random.randint(0,len(p1))
   
    ## 變化子代的方法
    if start_pos == end_pos:
      if start_pos > 0: 
          start_pos - 1
      else: 
          end_pos + 1		  
   
    elif start_pos < end_pos:
        for x in range(start_pos,end_pos):
            a = p1[x]
            b = p2[x]
            child_rt1[x] = b
            child_rt2[x] = a
            
    else:    
        for i in range(end_pos,start_pos):
            a=p1[i]
            b=p2[i]			
            child_rt2[i] = a 
            child_rt1[i] = b
 
    for i in range(len(p1)): 
        if not p2[i] in child_rt2:
            for x in range(len(child_rt2)):
                if child_rt2[x] == None:
                    child_rt2[x] = p2[i]
                    break
						
        if not p1[i] in child_rt1:
            for x in range(len(child_rt1)):
                if child_rt1[x] == None:
                    child_rt1[x] = p1[i]
                    break
    return child_rt1, child_rt2

## 突變	
def mutate( route_to_mut):
    
    ## 隨機決定是否突變
    if random.random() < mutation:

        mut_pos1 = random.randint(0,len(route_to_mut)-1)
        mut_pos2 = random.randint(0,len(route_to_mut)-1)
        if mut_pos1 == mut_pos2:
            return route_to_mut

        city1 = route_to_mut[mut_pos1]
        city2 = route_to_mut[mut_pos2]
        route_to_mut[mut_pos2] = city1
        route_to_mut[mut_pos1] = city2

    return route_to_mut

## 隨機生成子代
def evolve_population(s, M1, M2, M3, machine_value, arr):
	
	first_gen =[]
	for population in range(pop_size):
		route = []
		route.append(1)
		route.append(random.choices(range(2,len(M1)+2), weights = [1/machine_value[i][1] for i in range(len(M1))], k = 1)[0])
		route.append(random.choices(range(len(M1)+2,len(M1)+len(M2)+2), weights = [1/machine_value[i][1] for i in range(len(M1),len(M1)+len(M2)) ], k = 1)[0])
		route.append(random.choices(range(len(M1)+len(M2)+2,len(M1)+len(M2)+len(M3)+2), weights = [1/machine_value[i][1] for i in range(len(M1)+len(M2),len(M1)+len(M2)+len(M3)) ], k = 1)[0])
		route.append(fitness(route,arr))
		first_gen.append(route)
	
	next_g = first_gen
	
	return next_g	
	
## 演化過程	
def GA( gen, arr, M1, M2, M3, machine_value, n=0):
	
	def run(gen):
		children = []
        ## 選擇
		p = selection(gen)
        ## 目前最好的
		best_route_yet= p[0]
		
		## 開始變化
		for index, item in enumerate(p):
			next = index + 1
			if next < len(p):
					
				f1= p[index].pop()
				f2= p[next].pop()
				## 交配
				c1, c2 = crossover(p[index],p[next])
				
				## 突變
				c1= mutate(c1)
				c2= mutate(c2)
				## 計算 fitness
				c1.append(fitness(c1,arr))
				c2.append(fitness(c2,arr))
				children.append(c1)
				children.append(c2)
				p[index].append(f1)
				p[next].append(f2)
			
		return children	,best_route_yet	

	## 母代
	children,best_route_yet = run(gen)
	## 子代
	next_gen = evolve_population(children, M1, M2, M3, machine_value, arr)
	
	## 更新條件
	if selection(next_gen)[0][4] < best_route_yet[4]:
		best_route_yet = selection(next_gen)[0]
	
	for n in itertools.count():
		if n< n_generations:
			n+=1
			run(next_gen)
		else:
			return best_route_yet


## 主程式
def GA_main(thin, photo, etch, w1, w2, w3, w4, w5, w6, w7, w8, w9):
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
    	## 製造可以走的路徑圖 並給予值
        arr = makearr(machine_value, M1, M2, M3, w1, w2, w3, w4, w5, w6, w7, w8, w9)
        
    	## 初始化一個可行解
        first_gen =[]
        for population in range(pop_size):
            route = []
            route.append(1)
            route.append(random.choice(range(2,len(M1)+2)))
            route.append(random.choice(range(len(M1)+2,len(M1)+len(M2)+2)))
            route.append(random.choice(range(len(M1)+len(M2)+2,len(M1)+len(M2)+len(M3)+2)))
            route.append(fitness(route,arr))
            first_gen.append(route)
    	
    	## 演化過程
        s= GA( first_gen, arr, M1, M2, M3, machine_value)
    	
        ## 計算各數值
        Ca_value = round(thin.loc[M1[s[1]-2]][1] + photo.loc[M2[s[2]-2-len(M1)]][1]+ etch.loc[M3[s[3]-2-len(M1)-len(M2)]][1],4)
        u_value = round(thin.loc[M1[s[1]-2]][5] + photo.loc[M2[s[2]-2-len(M1)]][5]+ etch.loc[M3[s[3]-2-len(M1)-len(M2)]][5],4)
        DD_value = round(thin.loc[M1[s[1]-2]][9] + photo.loc[M2[s[2]-2-len(M1)]][9]+ etch.loc[M3[s[3]-2-len(M1)-len(M2)]][9],4)
        
        return [M1[s[1]-2],M2[s[2]-2-len(M1)],M3[s[3]-2-len(M1)-len(M2)]], Ca_value, u_value, DD_value
               

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
    machine_list, ca, u, DD = GA_main(thin, photo, etch, w1, w2, w3, w4, w5, w6, w7, w8, w9)
	
	