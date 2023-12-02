import MetaTrader5 as mt5
import numpy as np
import pandas as pd
import math as mth
import seaborn as sns
import matplotlib.pyplot as plt
import time as t
from datetime import datetime as dt 
from scipy.stats import norm


if not mt5.initialize():
    print("initialize() failed, error code =",mt5.last_error())
    quit()

pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1500)   

##############################################################################

All_instrument= ["XAUUSD", "GBPUSD", "EURUSD", "USDJPY"]

All_TF = ["M1", "M2", "M3", "M4", "M5", "M6", "M10", "M12", "M15", "M20",
"M30", "H1", "H2","H3", "H4", "H6", "H8", "H12"]

'''
Available Instrument:
    Depends on broker, Please check personal account.
    
Available Timeframe:
    "M1", "M2", "M3", "M4", "M5", "M6", "M10", "M12", "M15", "M20",
    "M30", "H1", "H2","H3", "H4", "H6", "H8", "H12", "D1"

'''

batch = 2000 #data per collection

##############################################################################
    
def SS(P):
    if np.mean(P) == 0:
        return 0
    else:
        conf=0.99
        err=0.05
        z = norm.ppf((1 + conf) / 2)
        ss = (z * np.std(P) / (err*np.mean(P))) ** 2   
        return ss
    
def P(rates):
    col_del = ['time', 'tick_volume', 'spread', 'real_volume']
    P = rates[[col for col in rates.dtype.names if col not in col_del]]
    return np.array(P.tolist())

def P_Rho(rates):
    col_del = ['time', 'tick_volume', 'spread', 'real_volume']
    P = rates[[col for col in rates.dtype.names if col not in col_del]]
    P_Rho=[]
    for p in P:
        P_Rho.append(abs((p[1]-p[2])/p[0]))
    return np.array(P_Rho)

def P_Delta(rates):
    col_del = ['time', 'tick_volume', 'spread', 'real_volume']
    P = rates[[col for col in rates.dtype.names if col not in col_del]]
    P_Delta=[]
    for p in P:
        P_Delta.append(abs((p[0]-p[3])/p[0]))
    return np.array(P_Delta)

def CountNeg(c, g):
    count=0
    for p in range(np.argmin(g)+1):
        if g[np.argmin(g)-p]<0:
            count+=1
        else:
            break
    c.append(count)
    return

def CountPos(c, g):
    count=0
    for p in range(np.argmax(g)+1):
        if g[np.argmax(g)-p]>0:
            count+=1
        else:
            break
    c.append(count)
    return

def C_Alg(Q, n_qr, tp):
    c=[] 
    for i in range(len(Q)-(n_qr-1)):
        gh=[]
        gl=[]
        for q in range(n_qr):  
            gh.append((Q[i+q][1]-Q[i][0])/Q[i][0])
            gl.append((Q[i+q][2]-Q[i][0])/Q[i][0]) 
        gh=np.array(gh)
        gl=np.array(gl)
        if np.max(gh)>=tp and np.min(gl)<=-tp:
            if np.argmax(gh)<np.argmin(gl):
                gl=gl[:np.argmax(gh)+1]
                CountNeg(c, gl)
            elif np.argmax(gh)>np.argmin(gl):
                gh=gh[:np.argmin(gl)+1]
                CountPos(c, gh)
            else:
                if abs(np.max(gh))>abs(np.min(gl)):
                    gl=gl[:np.argmax(gh)+1]
                    CountNeg(c, gl)
                elif abs(np.max(gh))<abs(np.min(gl)):
                    gh=gh[:np.argmax(gh)+1]
                    CountPos(c, gh)
                else:
                    pass
        elif np.max(gh)>=tp:
            CountNeg(c, gl)
        elif np.min(gl)<=-tp:
            CountPos(c, gh)
        else:
            pass
    return np.array(c)

def Collect(instrument, tu, start, n):
    timeframes = {
        "M1": 1,
        "M2": 2,
        "M3": 3,
        "M4": 4,
        "M5": 5,
        "M6": 6,
        "M10": 10,
        "M12": 12,
        "M15": 15,
        "M20": 20,
        "M30": 30,
        "H1": 60,
        "H2": 120,
        "H3": 180,
        "H4": 240,
        "H6": 360,
        "H8": 480,
        "H12": 720,
        "D1": 1440
    }

    if tu in timeframes:
        timeframe_value = timeframes[tu]
        return [mt5.copy_rates_from_pos(instrument, getattr(mt5, f"TIMEFRAME_{tu}"), start, n), timeframe_value]
    else:
        return '''The selected timeframe is not a default timeframe. 
                Please select a default MT5 timeframe.'''
                
##############################################################################

start_time_tot= t.time()

for instrument in All_instrument:
    start_time= t.time()
    print("-----------------------------------------------------------------")
    print(f"Computing {instrument} E[V].....")
    print("-----------------------------------------------------------------\n")
    
    df_pips = pd.DataFrame(columns=All_TF, index=All_TF)
    df_rrr = pd.DataFrame(columns=All_TF, index=All_TF)
        
    for TF_Q in range(len(All_TF)):
        
        #Q
        Q, n_q = Collect(instrument, All_TF[TF_Q], 0, batch)
        Q_Delta = P_Delta(Q)
        end = batch
        
        while len(Q_Delta) < SS(Q_Delta):
            Q_Delta = np.concatenate((
                    Q_Delta, 
                    P_Delta(Collect(instrument, All_TF[TF_Q]
                                  , end, batch)[0])))
            end += batch
            
        for TF_R in range(len(All_TF)-TF_Q):
            
            #R
            R, n_r = Collect(instrument, All_TF[TF_R+TF_Q], 0, batch)
            R_Rho = P_Rho(R)
            end = batch
            
            while len(R_Rho) < SS(R_Rho):
                R_Rho = np.concatenate((
                        R_Rho, 
                        P_Rho(Collect(instrument, All_TF[TF_R+TF_Q]
                                      , end, batch)[0])))
                end += batch
                        
            #c
            Q = P(Collect(instrument, All_TF[TF_Q], 0, batch)[0])
            tp = np.mean(R_Rho) ##should be through E[x] of a prob.dist
            n_qr = mth.floor(n_r/n_q)
            
            c = C_Alg(Q, n_qr, tp)  
            end = batch
            
            while len(c) < SS(c) or len(c)<1000:
                if Collect(instrument, All_TF[TF_Q], end, batch)[0] is None:
                    break
                else:
                    Q = P(Collect(instrument, All_TF[TF_Q], end, batch)[0])
                    c=np.concatenate((
                        c, 
                        C_Alg(Q, n_qr, tp)))
                    end+=batch
            
            cprice = P(Collect(instrument, "M1", 0, 1)[0])[0, 3]
                                   
            df_pips.at[All_TF[TF_Q], All_TF[TF_Q+TF_R]
                       ] = "{:.5f}".format(
                           np.mean(c)*np.mean(Q_Delta)*cprice)
            
            df_rrr.at[All_TF[TF_Q], All_TF[TF_Q+TF_R]
                       ] = "{:.2f}".format(
                           tp/(np.mean(c)*np.mean(Q_Delta)))
    
    print(f"({instrument}) Expected Retracement Table")
    print(df_pips)
    
    print(f"\n({instrument}) Suggested RRR Table")
    print(df_rrr)  
    
    end_time= t.time()
    elapsed_time = dt.utcfromtimestamp(end_time - start_time)
    elapsed_time_formatted = elapsed_time.strftime("%H:%M:%S")
    print(f"\n{instrument} took {elapsed_time_formatted} to complete.")
    
    plt.figure(figsize=(8, 6))  # Set the figure size
    sns.heatmap(df_pips.astype(float), annot=False, cmap='coolwarm', linewidths=1)
    plt.xlabel('R (closing interval)')
    plt.ylabel('Q (entry timeframe)')
    plt.title(f'Heatmap of the Expected Retracement Value, ({instrument})')
    plt.show()
    
    plt.figure(figsize=(8, 6))  # Set the figure size
    sns.heatmap(df_rrr.astype(float), annot=False, cmap='coolwarm', linewidths=1)
    plt.xlabel('R (closing interval)')
    plt.ylabel('Q (entry timeframe)')
    plt.title(f'Heatmap of the Suggested RRR Value, ({instrument})')
    plt.show()
    
end_time_tot= t.time()
elapsed_time = dt.utcfromtimestamp(end_time_tot - start_time_tot)
elapsed_time_formatted = elapsed_time.strftime("%H:%M:%S")
print(f"\nAll Process took {elapsed_time_formatted} to complete.")

##############################################################################













    


