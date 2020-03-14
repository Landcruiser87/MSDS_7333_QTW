#%%
from sklearn.datasets import load_boston
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import Imputer


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


boston = load_boston()
#print(boston['DESCR'])
col_names = boston['feature_names']
#Setting up data
#Numpy way
# X = np.array(boston.data, dtype=[(n,'float64') for n in col_names])
# y = np.array(boston.target, dtype=[('PRICE','float64')])
X, y = load_boston(return_X_y=True) 


#pandas
bos = pd.DataFrame(data = boston['data'], columns = boston['feature_names'])
bos_target = boston['target']

print(bos.head(5))

#Summary and statistics of the dataset
# bos.info()
# bos.describe()

#Check missing values. 
bos.isnull().sum()

#Check histograms of data
bos.hist(bins=50, figsize = (20,15))

#Looking at correlation
plt.figure(figsize=(20,10))
sns.heatmap(bos.corr().round(2),vmax=1, annot=True, cmap = 'YlGnBu',annot_kws={"fontsize":14})

#Looking at outlier percentages outside 1st and 3rd Quantiles
for k, v in bos.items():
	q1 = v.quantile(0.25)
	q3 = v.quantile(0.75)
	irq = q3 - q1
	v_col = v[(v <= q1 - 1.5 * irq) | (v >= q3 + 1.5 * irq)]
	perc = np.shape(v_col)[0] * 100.0 / np.shape(bos)[0]
	print("%s outliers = %8.2f%%" % (k, perc))


#%%
# ======================================================================================
# Problem 1:
# Using Sklearn get the Boston Housing dataset.
# Fit a linear regressor to the data as a baeline.  
# There is no need to do Cross-Validation.  We are exploring the change in results

# What is the loss and what are the goodness of fit parameters?  This will be our baseline for comparison
# ======================================================================================

#Looking at a baseline RSME 
linreg = LinearRegression().fit(bos,bos_target)
y_pred = linreg.predict(bos)
baseline_MSE = mean_squared_error(bos_target,y_pred)
r2 = r2_score(bos_target, y_pred)

#Coefficients and intercept
# linreg.coef_
# linreg.intercept_
#Looking at Coefficients. 
print(pd.DataFrame(zip(bos.columns, linreg.coef_), columns = ['features', 'BaselineCoefficients']))
print("\nBaseline MSE is = %.2f" % baseline_MSE)
print("Goodness of fit (R_squared) is = %.2f" % r2)

#%%
# ======================================================================================
# Problem 2: (repeated)
# For select between 1, 5 10, 20, 33, and 50% of your data on a single column (Completely at random), replace the present value with a NAN and then perform an imputation of that value.   

# In. each case perform a fit with the imputed data and compare the loss and goodness of fit to your baseline.
# ======================================================================================


#Split that data like Paul Bunyan
# X = Housing Price target
# y = All other housing data
X_train, X_test, y_train, y_test = train_test_split(bos, bos_target, test_size=0.20, random_state = 42)

#Check shape of test/train
print(X_train.shape)
print(X_test.shape)
print(y_train.shape)
print(y_test.shape)

#Define function for SKlearn Imputer
def impute_nation(imputedata):
	impute = Imputer(missing_values=np.nan, strategy="mean")
	impute.fit(imputedata)
	impute.transform(imputedata)
	return


#Setup linear regressor function
def LinearMadness(X, y, perc = "", imp_col = []): 

	linreg = LinearRegression().fit(X,y)
	y_pred = linreg.predict(X)
	return_MSE = mean_squared_error(y,y_pred)
	r2 = r2_score(y, y_pred)


	print("\nThe MSE is = %.2f" % return_MSE)
	print("Goodness of fit (R_squared) is = %.2f" % r2)
	print('===============================')
#%%

perc_list = [1,5,10,20,33,50]
imp_col = 4 #NOX Column


for x in perc_list:
	np.random.seed(42)	
	bos_imp = X_train.copy()
	bos_imp.NOX[bos_imp.NOX.sample(frac=(x/100)).index] = np.nan
	bos_imp_nan = sum(np.isnan(bos_imp.NOX))

	impute_nation(bos_imp)

	LinearMadness(bos_imp, y_train)  # perc=x,imp_col=imp_col









