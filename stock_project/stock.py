# 姓名：邱鈺珍
# 學號：406040084 
# 專案題目：快速尋找符合條件的標的股票
#------------------------------------------------------

#載入套件庫與讀入資料(進行數據分析之前常要引用的函式庫)
from pandas_datareader import data as web # 載入 pandas_datareader
import datetime as dt                     # 載入 datetime,別名為dt
import yfinance as yf                     # 載入 yfinance,別名為yf
import os                                 # 載入 os
# -----------------------------
import pandas as pd                       # 載入 pandas，別名為pd 
import glob                               # 載入 glob
import csv                                # 載入 csv
import time                               # 載入 time
# ----------------
import warnings                           # 載入 warnings
warnings.filterwarnings("ignore")
yf.pdr_override()

# yahoo_fun
def yahoo_fun():
# --函式功能說明---------------------------------------------------------------------
    '''抓取股票資料函式

    (1)設定捉取股票的起始日期/結束日期
    (2)讀取上市公司股票代號(TW.txt),並且寫入 stockTW 串列
    (3)讀取上櫃公司股票代號(TWO.txt),並且寫入 stockTW 串列
    (4)將 stockTW 資料依序讀取,並透過API至 Yahoo 捉取股票歷史股價資料. 且分別寫入 [股票代號.csv]檔案'''
 #-----------------------------------------------------------------------      
    localtime = time.localtime(time.time()) # 求本地的時間
    start = dt.datetime(2019, 5, 10)        # 資料從2019,5,10 開始取  (也可以從其他時間開始)  
    end = dt.datetime(localtime.tm_year+1, localtime.tm_mon, localtime.tm_mday)
    # 資料抓取時間，結束時間年份為現在的年份往後加一年(計算到現在的資料，補上今天)
    stockTW = []                            # 建立空字串
    fn = "TW.txt"
    with open(fn) as file_to_read:          # 開啟TW.txt檔案
        for line1 in file_to_read:          # for迴圈迭代
            j1 = str(line1[0:4]) + ".TW"    # 抓取上市股票代號
            stockTW.append(j1)              # 加入stockTW串列
    fn = "TWO.txt"
    with open(fn) as file_to_read:          # 開啟TWO.txt檔案
        for line2 in file_to_read:          # for迴圈迭代
            j2 = str(line2[0:4]) + ".TWO"   # 抓取上櫃股票代號
            stockTW.append(j2)              # 加入stockTW串列
    
    for k in stockTW :                      # for迴圈stockTW中的資料
        try : 
            df = web.get_data_yahoo([k],start, end) # 以股票代號，開始時間，結束時間抓資料(使用pandas_datareader下的data功能)
            if df.empty == False:                   # 如果有資料                
                df.to_csv(k[0:4] + '.csv')          # 將股價資料寫入csv文件。    
            else :
                pass                                # 沒有資料則不做任何事(pass)                                
        except :                                    # 例外                
            pass                                    # 不做任何事(pass)

# 計算 股票 DIF DEM 的值
def calculate_macd(fun_macd):
# ---函式功能說明------------------------------------------------------------------------------
    '''計算股票資料(DIF/DEM(MACD))函式

    (1)載入股票資料(xxxx.csv)
    (2)轉成 pandas 格式
    (3)只要三個欄位資料(Date/Volume/Close) 即可
    (4)使用收盤價(Close)計算 EMA_12/EMA_26
    (5)使用 EMA_12 及 EMA_26 計算 DIF
    (6)使用 DIF　計算　DEM 
    ps: DEM 又名　MACD'''
# ---------------------------------------------------------------------------------
    sm = pd.read_csv(fun_macd) # 將 xxxx.csv 文件讀取入
    sm = pd.DataFrame(sm)      # 轉成 DataFrame
    sm = sm.dropna()           # 去掉 nan 值(已從市場下市、下櫃的股票) 
    sm = sm[['Date','Volume','Close']]             # 抓取欄位：日期，成交量，收盤價
    sm.columns = ['Date','Volume','Close']         # 回傳欄位名稱(取名稱)
    sm['Close'] = pd.to_numeric(sm['Close'])       # 將收盤價轉換為數字類型
    sm['Volume'] = pd.to_numeric(sm['Volume'])     # 將成交量轉換為數字類型
    sm['EMA_12'] = sm['Close'].ewm(span=12).mean() # 計算12日指數移動平均線
    sm['EMA_26'] = sm['Close'].ewm(span=26).mean() # 計算26日指數移動平均線
    sm['DIF'] = sm['EMA_12'] - sm['EMA_26']        # DIF = 12日指數移動平均線 - 26日指數移動平均線
    sm['DEM'] = sm['DIF'].ewm(span=9).mean()       # DEM 計算 
    return sm                                      # 回傳Date、Close、Volume、EMA_12、EMA_26、DIF、DEM 欄位
     
# ----
# 主程式
print ("---  MACD ==> DIF 突破 DEM 資料篩選 ---")                    # 印出程式目的提示
sel = input("結束離開程式9 : ")                                      # 使用者輸入(是否離開程式)
if (sel == '9'):                                                    # 如果輸入9
    exit()                                                          # 結束程式
yahoo_stock = 'N'                                                   # 預設為N
yahoo_stock = input("捉取股票資料 Y/N:")                             # 使用者輸入
if (yahoo_stock == 'Y' or yahoo_stock == 'y'):                      # 輸入Y or y表示要抓取資料
    print ("--- 歷史資料下載中(約10分鐘)...請稍後...")                
    localtime = time.localtime(time.time())                         # 求本地的時間
    print (time.strftime("%a %b %d %H:%M:%S %Y", time.localtime())) # 印出現在時間
    yahoo_fun()                                                     # 呼叫抓取股票資料函式，抓取歷史股價資料
    # print (yahoo_fun.__doc__)      　　　                       　 # 印出yahoo_fun函式說明
    localtime = time.localtime(time.time())                         # 本地時間
    print (time.strftime("%a %b %d %H:%M:%S %Y", time.localtime())) #　印出現在時間
    print (" --- 資料下載 完成 ---")
print (" --- 以下參數非必要,不要調整 ---")  
para1_str = input("請輸入 下區間(name:para1 default=-0.9):")   # 輸入參數1，預設-0.9                      
para2_str = input("請輸入 上區間(name:para2 default= 2.0):")   # 輸入參數2，預設2.0                                 
para3_str = input("請輸入 8次中符合條件次數下限(name:para3 default=3):")   # 輸入參數3，預設3                               
para4_str = input("請輸入 股票日成交張數下限(name:para4 default=800):")    # 輸入參數4，預設800                        
para5_str = input("請輸入 本次與上次差距下限(name:para5 default=0.0018):") # 輸入參數5，預設0.0018
if para1_str == '':           # 若沒有輸入參數
    para1 = -0.9              # 參數1保持預設：-0.9
else:    
    para1 = float(para1_str)  # 使用者輸入的數(浮點型態)
if para2_str == '':           # 若沒有輸入參數
    para2 = 2.0               # 參數2保持預設：2.0
else: 
    para2 = float(para2_str)  # 使用者輸入的數(浮點型態)
if para3_str == '':           # 使用者沒有輸入參數
    para3 = 3                 # 參數3為3，要成功(符合條件)3次
else:
    para3 = int(para3_str)    # 使用者輸入的次數(整數型態)
if para4_str == '':           # 使用者沒有輸入參數
    para4 = 800               # 參數4，保持成交量800張
else:
    para4 = int(para4_str)    # 使用者輸入的成交張數(整數型態)
if para5_str == '':           # 使用者沒有輸入參數 
    para5 = 0.0018            # 參數5為保持預設0.0018
else:
    para5 = float(para5_str)  # 使用者輸入的(浮點型態)

print ("para1=", para1 ,"para2=", para2, "para3=", para3, "para4=", para4, "para5=", para5 ) # 印出參數
# ------------------
path = "C:\\stock"                # 資料放在路徑C槽下的 stock 資料夾
if not os.path.isdir(path):       # 如果路徑下沒有此資料夾
    os.mkdir(path)                # 在路徑下建立資料夾
# 符合條件的股票 存放的檔案
key1 = "c:\stock\keystock.txt"    # 路徑c:\stock\keystock.txt，變數key1
key_f2 = open(key1,'w')           # 開啟檔案
# ---------------------
all_csv_file = glob.glob("*.csv") # 讀取所有的.csv文件檔名

print ("--- MACD 計算中(約1分鐘)...請稍後...")
localtime = time.localtime(time.time())      # 求本地時間
print ("開始時間 ", time.strftime("%a %b %d %H:%M:%S %Y", time.localtime())) # 印出開始時間
stock_data = ''                              # 初值為空
for iout in (all_csv_file):                  # for迴圈迭代所有股票代號
    stock_data = iout                        # 股票代號，變數stock_data
    m_sm_data = calculate_macd(stock_data)   # 呼叫　計算股票資料(DIF/DEM(MACD))函式 
    # print (calculate_macd.__doc__)       　# 印出calculate_macd函式說明
    if (len(m_sm_data) <= 30):               # 上市or上櫃歷史資料小於30天以下的不處理         
        continue                             # 回到for迴圈，判斷下一支股票
    m_sm_data = m_sm_data.sort_values(by='Date', ascending=False)  # 反排序
    # 每一隻股票 計算 macd 是否有突破趨勢(DIF 往上  DEM 往下)
    t_ans_count = 0           # t_ans_count初值為0
    for i in range(0, 8, 1):  # 迴圈迭代，取前八筆(最近的)資料
            DIF_Value = m_sm_data.iloc[i]['DIF']         # DIF欄的資料放入DIF_Value
            DEM_Value = m_sm_data.iloc[i]['DEM']         # DEM欄的資料放入DEM_Value
            Volume_Value = m_sm_data.iloc[i]['Volume']   # Volume欄的資料放入Volume_Value
            if (i == 0 and (Volume_Value/1000) < para4): # 成交量(股數)/1000股 = 張數 ，如成交張數<800張
                break                                    # 這支股票跳出不做
            if (i == 0):
                if (DIF_Value >= para1 and DIF_Value <= para2): # 區間在>=0.9和<=2之間
                    t_ans_count = t_ans_count + 1        # t_ans_coun加1，表示成功次數+1            
                    DIFf = DIF_Value                     # 存入 DIFf變數                              
                    DEMm = DEM_Value                     # 存入 DEMm變數
                    continue                             # 繼續，同支股票回去判斷下一筆(日期)資料
                else:
                    break                                # 這支股票跳出不做      
            else:
                if (i==2 and (DIF_Value > DEM_Value)):   # 此條件判斷此隻股票2天前DIF已經大於DEM則不處理（表示2天前已漲價,不符合我們條件）
                   break                                 # 這支股票跳出不做
                if ((DIFf - DIF_Value) >= para5 and (DEM_Value - DEMm) >= para5):  # 如果DIF和前一日DIF相差、DEM和前一日DEM相差都符合>=參數5的條件 
                    t_ans_count = t_ans_count + 1        # t_ans_coun加1，表示成功次數+1 
                DIFf = DIF_Value      # 存到DIFf變數
                DEMm = DEM_Value      # 存到DEMm變數
# ---------------------------------------------------------------    
    if (t_ans_count >= para3):        # 成功3次以上
        key_f2.write(stock_data[0:4]) # 將股票代號寫入
        key_f2.write("\n")            # 換行
key_f2.close()                        # 關閉c:\stock\keystock.txt檔案 
print ("--- MACD 計算完成 ...")
localtime = time.localtime(time.time()) # 求本地時間
print ("結束時間 ", time.strftime("%a %b %d %H:%M:%S %Y", time.localtime())) # 印出結束時間
print ("--- 計算完成的資料 存放在 c:\stock 的 keystock.txt ---")              # 印出存放(標的股票)結果的目錄

