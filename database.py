# -*- coding: utf-8 -*-
"""
Created on Thu Jul 30 08:18:17 2020

@author: 2007043
"""

# Ca U DD資料的撈取

import os
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
os.environ['path'] = r'D:/oracle/product/11.2.0/client_1/instantclient-basic-windows.x64-11.2.0.4.0/instantclient_11_2/' 

import cx_Oracle #import cx_oracle這個lib 讓你可以使用連線oracle
import pandas as pd #透過pd.df取用資料
import numpy as np
import pyodbc #ODBC 連接SQL SERVER
from sqlalchemy import create_engine,text


def dataprocessing(start, end, OP_ID, product, SPC_ITEM, tabu, SL_TF_tabu, GL_TF_tabu):
    
    
    ## 存取 OP_ID, EQP_ID的對照表
    table = pd.read_csv(r'C:\Users\JoyWCLi\Desktop\新產品\A+0827\table.csv')
    
	## 找出CHARTID
    for i in range(len(table)):
        check = table.CHARTID[i].split('/')
        if (table.OP_ID_1[i]== OP_ID and check[0] == product and check[3] == SPC_ITEM):
            CHART_ID = table.CHARTID[i]
            break
    
    
    ## Oracle取得 Ca與 U Data
    conn = cx_Oracle.connect('L6AINT_AP', 'L6AINT$AP', 'TCSPC111:1523/6AHMTS') #設定連線資料
    curs = conn.cursor() #cursor是一個暫時儲存查詢結果的指標
    
    sql = "select to_char(mtimestamp,'yyyy-mm-dd hh24:MI:SS') mtimestamp "
    sql = sql + ", chartid "
    sql = sql + ", monitoritemvalue spc_value "
    sql = sql + ", tg.USL, tg.LSL "
    sql = sql + ", inforvalue7 lot_id "
    sql = sql + ", inforvalue5 sheet_id "
    sql = sql + ", inforvalue16 op_id_1 "
    sql = sql + ", inforvalue13 eqp_id_1 "
    sql = sql + ", trim(RAWITEMVALUES) RAWITEMVALUES "
    
    sql = sql + "from l6aaryspch.spchis spc, l6aaryspchsn.graph tg "
    
    sql = sql + "where spc.MTIMESTAMP between to_date('"+ start +" 01:30:00', 'yyyy-mm-dd hh24:MI:SS') and to_date('"+ end +" 23:30:00','yyyy-mm-dd hh24:MI:SS') "
    sql = sql + "and spc.graphtype = tg.graph_type "
    sql = sql + "and tg.active_flag = 'Y' "
    sql = sql + "and tg.chart_id = spc.chartid "
    sql = sql + "and spc.inforvalue5 not like 'M%' "
    sql = sql + "and (spc.chartid like '%/AD%' OR spc.chartid like '%/AF%' OR spc.chartid like '%/AS%' OR spc.chartid like '%/AE%' OR spc.chartid like '%/TEG%' OR spc.chartid like '%/TENG%' OR spc.chartid like '%/Test%' OR spc.chartid like '%BSITO/AFI/RS%') "
    sql = sql + "and spc.graphtype = tg.graph_type "
    sql = sql + "and spc.graphtype in ('X')"
    sql = sql + "and chart_id = '"+ CHART_ID +"'"
    
    curs.execute(sql) #執行 SQL語法
    
    # 將資料讀成panda表單
    OP_ID_data = pd.read_sql(sql, con = conn) 
    OP_ID_data = OP_ID_data.fillna(0)
        
    curs.close() # corsor關閉
    conn.close() # conn關閉
    
    
    
    ca_value = []
    u_value = []
    
    
    for i in range(len(OP_ID_data)):
        ## Ca的計算
        a = (float(OP_ID_data.USL[i])- float(OP_ID_data.LSL[i]))/2
        b = (float(OP_ID_data.USL[i])+ float(OP_ID_data.LSL[i]))/2
        value = abs((float(OP_ID_data.SPC_VALUE[i])- b))/ a
        ca_value.append(value)
        
        seq = OP_ID_data.RAWITEMVALUES[i]
        seq = seq.split(',')
        
        for j in range(len(seq)):
            seq[j] = float(seq[j])
            
        ## U的計算
        mini = float(min(seq))
        maxi = float(max(seq))
        value = (maxi - mini) / (maxi + mini)
        u_value.append(value)
        
    OP_ID_data['Ca'] = ca_value
    OP_ID_data['U'] = u_value
    OP_ID_data['DEFECT_DENSITY'] = 0
    
    ## 依機台找出所需的值
    mean = OP_ID_data.groupby('EQP_ID_1').mean()
    std = OP_ID_data.groupby('EQP_ID_1').std()
    mini = OP_ID_data.groupby('EQP_ID_1').min()
    maxi = OP_ID_data.groupby('EQP_ID_1').max()
    
    ## 設定 frame的 col name
    col = ['machine','OP_ID', 'Ca_mean','Ca_std','Ca_min','Ca_max','u_mean', 'u_std', 'u_min', 'u_max']
    
    rows = []
    
    for i in range(len(mean)):
        attribute = [mean.index[i], OP_ID, mean.Ca[i], std.Ca[i], mini.Ca[i], maxi.Ca[i],mean.U[i], std.U[i], mini.U[i], maxi.U[i]]
        rows.append(attribute)
    
    ## 產出有 U 和 Ca資料的 frame
    frame = pd.DataFrame(rows, columns = col)
    frame.set_index("machine" , inplace=True)
#    frame = frame.append(['No_machine','GL-WMA', 0,0,0,0,0,0,0,0],ignore_index=True)
#    frame = frame.append(['No_machine','PX1-IEX',0,0,0,0,0,0,0,0],ignore_index=True)
#    frame = frame.append(['No_machine','AS-CVD', 0,0,0,0,0,0,0,0],ignore_index=True)
#    frame = frame.append(['No_machine','PX2-SPT',0,0,0,0,0,0,0,0],ignore_index=True)
#    frame = frame.append(['No_machine','AS-IEX', 0,0,0,0,0,0,0,0],ignore_index=True)
#    frame = frame.append(['No_machine','PX1-WTO',0,0,0,0,0,0,0,0],ignore_index=True)
#    frame = frame.append(['No_machine','PX-IEX', 0,0,0,0,0,0,0,0],ignore_index=True) ##
#    frame = frame.append(['No_machine','SL-WMA', 0,0,0,0,0,0,0,0],ignore_index=True)
#    frame = frame.append(['No_machine','SL-RIE', 0,0,0,0,0,0,0,0],ignore_index=True) ##
#    frame = frame.append(['No_machine','TH-IEX', 0,0,0,0,0,0,0,0],ignore_index=True)
#    frame = frame.append(['No_machine','PX2-WTO',0,0,0,0,0,0,0,0],ignore_index=True)
#    frame = frame.append(['No_machine','PV-CVD', 0,0,0,0,0,0,0,0],ignore_index=True)
#    frame = frame.append(['No_machine','TH-RIE', 0,0,0,0,0,0,0,0],ignore_index=True)
#    frame = frame.append(['No_machine','GL-IEX', 0,0,0,0,0,0,0,0],ignore_index=True)
#    frame = frame.append(['No_machine','SL-IEX', 0,0,0,0,0,0,0,0],ignore_index=True)
#    frame = frame.append(['No_machine','PX2-IEX',0,0,0,0,0,0,0,0],ignore_index=True)
#    frame = frame.append(['No_machine','PX-WTO', 0,0,0,0,0,0,0,0],ignore_index=True) ##
#    frame = frame.append(['No_machine','AS-RIE', 0,0,0,0,0,0,0,0],ignore_index=True)
#    frame = frame.append(['No_machine','PX1-SPT', 0,0,0,0,0,0,0,0],ignore_index=True)
#    frame = frame.append(['No_machine','GL-SPT',0,0,0,0,0,0,0,0],ignore_index=True)
#    frame = frame.append(['No_machine','PX-SPT',0,0,0,0,0,0,0,0],ignore_index=True) ##
#    frame = frame.append(['No_machine','SL+IEX',0,0,0,0,0,0,0,0],ignore_index=True) ##
#    frame = frame.append(['No_machine','PX2+SPT',0,0,0,0,0,0,0,0],ignore_index=True) ##
#    frame = frame.append(['No_machine','SL-SPT',0,0,0,0,0,0,0,0],ignore_index=True)
#    frame = frame.append(['No_machine','PX+SPT',0,0,0,0,0,0,0,0],ignore_index=True) ##
#    frame = frame.append(['No_machine','GL+IEX',0,0,0,0,0,0,0,0],ignore_index=True) ##
#    frame = frame.append(['No_machine','PX1+SPT',0,0,0,0,0,0,0,0],ignore_index=True) ##
#
#    frame = frame.append(['No_machine','RS',0,0,0,0,0,0,0,0],ignore_index=True) ##    
#    frame = frame.append(['No_machine','CD01',0,0,0,0,0,0,0,0],ignore_index=True) ##     
#    frame = frame.append(['No_machine','THK_SiNx',0,0,0,0,0,0,0,0],ignore_index=True) ##
#    frame = frame.append(['No_machine','THK_PV',0,0,0,0,0,0,0,0],ignore_index=True) ##
    ## 缺值補 0
    frame = frame.fillna(0)
    
    ## 將使用者填入的機台名分割
    tabu = tabu.split('、')
    
    ## 刪除使用者不要的機台
    for i in range(len(tabu)):
        if(tabu[i] in frame.index):
            frame = frame.drop([tabu[i]])
    
    ## 刪除TL大的機台
    for i in range(len(SL_TF_tabu)):
        if(SL_TF_tabu[i] in frame.index):
            frame = frame.drop([SL_TF_tabu[i]])
    
    ## 刪除TL大的機台
    for i in range(len(GL_TF_tabu)):
        if(GL_TF_tabu[i] in frame.index):
            frame = frame.drop([GL_TF_tabu[i]])
    
    ## 存取 OP_ID, DD的對照表
    DD_table = pd.read_excel(r'C:\Users\JoyWCLi\Desktop\新產品\A+0827\defect_code_list.xlsx')
    DD = []
    for i in range(len(DD_table)):
        if (DD_table.OP_ID[i] == OP_ID):
            a = DD_table.iloc[i][0].replace(' ','')
            DD.append("".join(a.split()))
    
    # load DD data
    sql_conn = pyodbc.connect('DRIVER={SQL Server};SERVER=10.96.50.184;DATABASE=system;UID=sa;PWD=Auo+123456;CharSet=utf8')
    
    for i in range(len(DD)):
        if (i == 0):
            GL_SPT = """select A.mfg_day mfg_day, A.eqp_id eqp_id, SUM(A.d_count) sheet_cnt, SUM(A.u_count) defect, A.op_id op_id, 1 lot_id 
                                from ( select product_code, model_no, mfg_day, eqp_id, op_id, SUM(u_count) u_count, d_count 
                                          from dbo.defect_density_eqp_daily A 
                                          where mfg_day>='"""+ start +"""' and mfg_day<='"""+ end +"""' and  product_code = '"""+ product +"""' and defect IN ('"""+ DD[i] +"""') and op_id = '"""+ OP_ID +"""' group by product_code, model_no, mfg_day, eqp_id, op_id, d_count ) A group by A.mfg_day, A.eqp_id, A.op_id order by A.mfg_day, A.eqp_id"""
            GL_SPT_DD_category = pd.read_sql(GL_SPT, con=sql_conn)
            GL_SPT_DD_total = GL_SPT_DD_category.groupby('eqp_id').sum()
            GL_SPT_DD = pd.DataFrame(index = GL_SPT_DD_total.index )
            GL_SPT_DD['DD_'+str(i+1)] = GL_SPT_DD_total.defect
            
        else:
            GL_SPT = """select A.mfg_day mfg_day, A.eqp_id eqp_id, SUM(A.d_count) sheet_cnt, SUM(A.u_count) defect, A.op_id op_id, 1 lot_id 
                                from ( select product_code, model_no, mfg_day, eqp_id, op_id, SUM(u_count) u_count, d_count 
                                          from dbo.defect_density_eqp_daily A 
                                          where mfg_day>='"""+ start +"""' and mfg_day<='"""+ end +"""' and  product_code = '"""+ product +"""' and defect IN ('"""+ DD[i] +"""') and op_id = '"""+ OP_ID +"""' group by product_code, model_no, mfg_day, eqp_id, op_id, d_count ) A group by A.mfg_day, A.eqp_id, A.op_id order by A.mfg_day, A.eqp_id"""
            GL_SPT_DD_category = pd.read_sql(GL_SPT, con=sql_conn)
            
            if(len(GL_SPT_DD_category) !=0):
                GL_SPT_DD_total = GL_SPT_DD_category.groupby('eqp_id').sum()
                GL_SPT_DD['DD_'+str(i+1)] = GL_SPT_DD_total.defect
            
    ## DD的計算
    GL_SPT_DD['DD_sum']= GL_SPT_DD.sum(axis=1)
    GL_SPT_DD['sheet'] = GL_SPT_DD_total.sheet_cnt
    
    GL_SPT_DD['DD'] = list(map(lambda x,y: x/y, GL_SPT_DD['DD_sum'],GL_SPT_DD['sheet']))
    frame_DD = pd.DataFrame(index = GL_SPT_DD.index )
    frame_DD['DD'] = GL_SPT_DD['DD']
#    frame_DD = frame_DD.append(['No_machine',0, 0])   
    
    
    ## 表格合併
    if (len(frame_DD)==0):
        frame['DD']= 0
        res = frame
    else:    
        res = pd.merge(frame,frame_DD, left_index=True, right_index=True, how='inner')
    
    return res


if __name__ == "__main__":
    
    OP_ID = 'GL-WMA'
    product = 'M270HAN02'
    SPC_ITEM = 'CD01'
    tabu = 'AASPT800、AASPTH00'
    
#    PEP1 = ['GL-SPT','RS','GL-IEX','CD01', 'GL-WMA','CD01']
#    PEP2 = ['AS-CVD','THK_SiNx','AS-IEX','CD01','AS-RIE','CD01']
#    PEP2 = ['AS-CVD','THK_SiNx','AS-IEX','CD01','AS-IEX','CD01']
#    PEP3 = ['SL-SPT','RS','SL-IEX','CD01','SL-WMA','CD01']
#    PEP4 = ['PX1-SPT','RS','PX1-IEX','CD01','PX1-WTO','CD01']
#    PEP5 = ['PV-CVD','THK_PV','TH-IEX','CD01','TH-RIE','CD01']
#    PEP6 = ['PX2-SPT','RS','PX2-IEX','CD01','PX2-WTO','CD01']
 
    start = '2020-07-06'
    end = '2020-08-18'
    
    frame = dataprocessing(start, end, OP_ID, product, SPC_ITEM, tabu, SL_TF_tabu, GL_TF_tabu)




## 直接將pandas.df表單上傳至Oracle

#DBuser = '2007043'
#password = '1EA003'
#server = '10.96.48.97:60652' #IP:p:port
#database = 'system'
#
#conn_str = r'mssql+pymssql://'+DBuser+':'+password+'@'+server+'/'+database
#engine = create_engine(conn_str)
#conn = engine.connect()
#               #DB表單名稱         #SQL語法
#frame.to_sql('test0724', engine, if_exists = 'replace', index = False)