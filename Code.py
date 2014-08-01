import pandas as pd
import math
from scipy.stats import norm 

# here we delete the columns we dont need. We set that index to dates and parse dates
#options = pd.read_excel('Options_Test.xlsx', 'Hoja1', index_col='Date[L]', parse_date=True)

def load_options_from_file(filename, tabname):
	options = pd.read_excel(filename, tabname, parse_date=True)

	return options

def clean_options_data(options):
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
		del options[key]
	

""" Angela skip esto
#S_0 = underlying price (USD per share)
#X = strike price (USD per share)
#v = volatility (% in fraction)
#r = continuously compounded risk-free interest rate (% in fraction)
#div = continuously compounded dividend yield (% in fraction)
#N = where N(x) is the standard normal cumulative distribution function.
#t = time to expiration (in x/365 formula) so basically as a fraction
#x = is number of days to exp. that will be used in function to get t
#T = Total calendar days in 1 year

x = 266 
v = 0.39
div = 0.0
t = x/365.0
S_0 = 107.87
X = 105.0
T = 365.0 
pi = math.pi

d1 = (log(S_0/X) + t * (r - div + (v**2)/2)) / (v * math.sqrt(t)) #CORRECT
d2 = (d1 - v * math.sqrt(t)) #CORRECT
call_delta = e**(-div*t) * norm.cdf(d1)  #CORRECT
call_theta = 1/T * (-(S_0* v * e**(-(div*t)) / (2 * math.sqrt(t)) * 1/(math.sqrt(2 * pi)) * e**((-(d1)**2)/2))
                      - (r * X * e**(-(r*t)) * norm.cdf(d2)) + div * S_0 * e**(-(div*t)) * norm.cdf(d1)) #CORRECT
Gamma = e**(-(div*t)) / (S_0 * v * math.sqrt(t)) * (1/(math.sqrt(2*pi))) * e**((-(d1)**2)/2) #CORRECT
Vega = 1/100.0 * (S_0 * e**(-(div*t)) * math.sqrt(t)) * (1 / (math.sqrt(2 * pi))) * e**((-(d1)**2)/2) #CORRECT
Rho = (1/100.0) * (X * t * e**(-(r*t))) * (norm.cdf(d2)) #CORRECT

#S_0 = Last
#X = aca hay un problema pero con q me diga como funcinan los demas despues yo lo cambio. pero dejemoslo como una constante(300)
#v = una cosntante ex 0.40
#r = constante (0.025)
#div = en este ejemplo - pero puede cambiar tiene su columna
#N = esta es el norm.cdf(d1 0 d2)
#t = es el numero de dias q faltan q esta en options.Days_to_Exp
"""

""" Angela esta es la descrip + lo q falta de code
r = 0.1 #this needs to be either a constant or we need to add a source this data from
v = 0.1 # still need to get the formula for implied vol.
div = 0.1 #need to add a column for it to check what the div. is
T = 365.0 # number of days per year (could be calendar days or business days depends what u want to use)
t = 1.0 
S_0 = 10.0 
X = 10.0
pi = math.pi
"""


def calculate(S_0):
	x = 266 # number of days to exp.
	r = 0.05
	v = 0.39
	div = 0.0
	t = x/365.0
	X = 90.0
	pi = math.pi
	T = 365.0

	d1 = (math.log(S_0/X) + t * (r - div + (v**2)/2)) / (v * math.sqrt(t)) #CORRECT
	d2 = (d1 - v * math.sqrt(t)) #CORRECT

	call_delta = math.e**(-div*t) * norm.cdf(d1)  #CORRECT
	call_theta = 1/T * (-(S_0* v *math.e**(-(div*t)) / (2 * math.sqrt(t)) * 1/(math.sqrt(2 * pi)) *math.e**((-(d1)**2)/2))
	                      - (r * X *math.e**(-(r*t)) * norm.cdf(d2)) + div * S_0 *math.e**(-(div*t)) * norm.cdf(d1)) #CORRECT
	Gamma = (math.e**(-div*t)) / (S_0 * v * math.sqrt(t)) * (1/(math.sqrt(2*pi))) *math.e**((-(d1)**2)/2) #CORRECT
	Vega = 1/100.0 * (S_0 *math.e**(-(div*t)) * math.sqrt(t)) * (1 / (math.sqrt(2 * pi))) *math.e**((-(d1)**2)/2) #CORRECT
	Rho = (1/100.0) * (X * t *math.e**(-(r*t))) * (norm.cdf(d2)) #CORRECT

	return Rho


if __name__ == "__main__":
	options = load_options_from_file(filename='Options_Test.xlsx', tabname='Hoja1')
	clean_options_data(options)

	options['Days_to_Exp'] = (options.Exp_Date - options.Date)
	options.head()
	#We need to drop the NaN to make sure we get the rows that contain important data. Since all the data from reuters comes w/
	#all 24 hours of data. Or in case of EOD it has 7 days.
	options = options.dropna()
	options = options.sort('Date')

	new_col = {}
	all_last = options['Last']
	for key in all_last.keys():
		value = calculate(all_last[key])
		new_col[key] = value

	print options
	print new_col
	
	