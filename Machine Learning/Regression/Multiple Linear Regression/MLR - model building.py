import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Load the dataset
dataset = pd.read_csv(r"C:\Ds & AI ( my work)\Machine Learning\Regression\Multiple Linear Regression\Investment.csv")

# Independent Variable
x = dataset.iloc[:,:-1]
#Dependent Variable
y = dataset.iloc[:,-1]

x = pd.get_dummies(x, dtype=int)

from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x,y, test_size=0.20, random_state=0 )

# Building the machine Learning model
from sklearn.linear_model import LinearRegression
regressor = LinearRegression()
regressor.fit(x_train, y_train)

# Predict the test set
y_pred = regressor.predict(x_test)

bias = regressor.score(x_train, y_train)
bias

variance = regressor.score(x_test, y_test)
variance

slope = regressor.coef_
print(slope)

intercept = regressor.intercept_
print(intercept)

x = np.append(arr = np.ones((50,1)).astype(int), values = x, axis = 1)

import statsmodels.api as sm
x_opt = x[:,[0,1,2,3,4,5]]
#OrdinaryLeastSquares
regressor_OLS = sm.OLS(endog=y, exog=x_opt).fit()
regressor_OLS.summary()

#Backward Elimination 
import statsmodels.api as sm
x_opt = x[:,[0,1,2,3,5]]
#OrdinaryLeastSquares
regressor_OLS = sm.OLS(endog=y, exog=x_opt).fit()
regressor_OLS.summary()

import statsmodels.api as sm
x_opt = x[:,[0,1,2,3]]
#OrdinaryLeastSquares
regressor_OLS = sm.OLS(endog=y, exog=x_opt).fit()
regressor_OLS.summary()

import statsmodels.api as sm
x_opt = x[:,[0,1,3]]
#OrdinaryLeastSquares
regressor_OLS = sm.OLS(endog=y, exog=x_opt).fit()
regressor_OLS.summary()

import statsmodels.api as sm
x_opt = x[:,[0,1]]
#OrdinaryLeastSquares
regressor_OLS = sm.OLS(endog=y, exog=x_opt).fit()
regressor_OLS.summary()



