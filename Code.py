import pandas as pd
import math
from scipy.stats import norm 

def calculate_Call_Delta(div, t, d1):
    Call_Delta = e**(-div*t) * norm.cdf(d1)
    return Delta

def calculate_Call_Theta(T, S_0, v, div, t, d1, r, X, d2):
    Call_Theta = 1/T * (-(S_0* v * e**(-(div*t)) / (2 * sqrt(t)) * 1/(sqrt(2 * pi)) * e**((-(d1)**2)/2))
                      - (r * X * e**(-(r*t)) * norm.cdf(d2)) + div * S_0 * e**(-(div*t)) * norm.cdf(d1))
    return Call_Theta

def calculate_Gamma(div, t, S_0, v, d1):
    Gamma = (e**(-div*t)) / (S_0 * v * sqrt(t)) * (1/(sqrt(2*pi))) * e**((-(d1)**2)/2) 
    return Gamma

def calculate_Vega(S_0, div, t, d1):
    Vega = 1/100.0 * (S_0 * e**(-(div*t)) * sqrt(t)) * (1 / (sqrt(2 * pi))) * e**((-(d1)**2)/2) 
    return Vega

def calculate_Rho(X, t, r, d2):
    Rho = (1/100.0) * (X * t *math.e**(-(r*t))) * (norm.cdf(d2))
    return Rho

def calculate_d1(S_0, X, t, r, div, v):
    d1 = (log(S_0/X) + t * (r - div + (v**2)/2)) / (v * sqrt(t))
    return d1

def calculate_d2(d1, v, t):
    d2 = (d1 - v * sqrt(t))
    return d2

def load_excel_file(filename, tabname):
    data = pd.read_excel(filename, tabname, parse_date=True)

    return data
    
data = load_excel_file('Options_Test.xlsx', 'Hoja1')
data.head()

def clean_data(data_file):
    to_delete = [
        #"EX"
        "Open Interest",
        "Settle",
        #"Data",
        #"Source",
        "Time[L]",
        "Type",
        "Qualifiers"]

    for key in to_delete:
        del data[key]
clean_data(data)

for key in data.RIC.keys():
    data.RIC[key] = data.RIC[key].replace('.','')

data['Rho'] = 0.025


data['Days_to_Exp'] = (data.Exp_Date - data.Date)
data = data.dropna()
data = data.sort('Date')

data['Days_to_Exp'] = (data.Exp_Date - data.Date)
data = data.dropna()
data = data.sort('Date')

data['Stock'] = data.RIC[key][0:4]

Strike = []
for key in data.RIC.keys():
    a = data.RIC[key][-6:-2]
    Strike.append(a)

data['Strike'] = Strike    
    
d1 = []
for key in data.Stock_Price.keys():
    b = calculate_d1(data.Stock_Price[key], 400, 1, 0.02, 0, 0.50)
    d1.append(b)
    
data['d1'] = d1

d2 = []
for key in data.d1.keys():
    c = calculate_d2(data.d1[key], 0.50, 1)
    d2.append(c)

data['d2'] = d2

Theta = []
for key in data.Stock_Price.keys():
    d = calculate_Call_Theta(365, data.Stock_Price[key], 0.50, 0.0, 1.0, data.d1[key], 0.02, 400, data.d2[key])
    Theta.append(d)
    
data['Theta'] = Theta

Gamma = []
for key in data.Stock_Price.keys():
    e = calculate_Gamma(0, 1, data.Stock_Price[key], 0.50, data.d1[key])
    Gamma.append(e)
    
data['Gamma'] = Gamma

Vega = []
for key in data.Stock_Price.keys():
    f = calculate_Vega(data.Stock_Price[key], 0, 1, data.d1[key])
    Vega.append(f)
    
data['Vega'] = Vega

Rho = []
for key in data.Strike.keys():
    g = calculate_Rho(365, 1, 0.02, data.d2[key])
    Rho.append(g)
    
data['Rho'] = Rho


	
	
