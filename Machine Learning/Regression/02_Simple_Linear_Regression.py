import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Load the dataset
dataset = pd.read_csv(r'C:\Ds & AI ( my work)\Machine Learning\Regression\Dataset\Salary_Data.csv') 

# Independent Variable
x = dataset.iloc[:,:-1]
#Dependent Variable
y = dataset.iloc[:,-1]

from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x,y, test_size=0.20, random_state=0 )

from sklearn.linear_model import LinearRegression
regressor = LinearRegression()
regressor.fit(x_train, y_train)

# Predict the test set
y_pred = regressor.predict(x_test)

# compare predicted and actual salaries from the test set
comparison = pd.DataFrame({'Actual': y_test, 'Predicted':y_pred})
print(comparison)

# Visualize the test set
plt.scatter(x_test, y_test, color='red')
plt.plot(x_train, regressor.predict(x_train), color='blue')
plt.title('Salary vs Experience(Test set)')
plt.xlabel('Year of Experience')
plt.ylabel('Salary')
plt.show()

m_slope = regressor.coef_
print(m_slope)

c_intercept = regressor.intercept_
print(c_intercept)

# future predi-1
y_12 = (m_slope*12) + c_intercept
print(y_12)

# future pred-2
y_20 = (m_slope*20) + c_intercept
print(y_20)

#Mean
dataset.mean()
dataset['Salary'].mean()

# Median 
dataset.median()
dataset['Salary'].median

# Mode
dataset.mode()

# Variance
dataset.var()  # gives variance of entire dataframe
dataset['Salary'].var() # variance of particular column

# Standard Deviation
dataset.std()   # standard deviation of entire dataframe
dataset['Salary'].std()

# Coefficient of Variation(cv)
from scipy.stats import variation
variation(dataset.values)

variation(dataset['Salary'])

# Correlation
dataset.corr()
dataset['Salary'].corr(dataset['YearsExperience'])

# Skewness
dataset.skew()
dataset['Salary'].skew()

# Standard Error
dataset.sem()
dataset['Salary'].sem()

# Z-score
import scipy.stats as stats
dataset.apply(stats.zscore)
stats.zscore(dataset['Salary'])

# Degree of freedom
a = dataset.shape[0]  # will give us num.of rows
b = dataset.shape[1]  # will give us num.of cloumns
print(a, "And",b)
print(a-b)

# SSR
y_mean = np.mean(y)
SSR = np.sum((y_pred-y_mean))**2
print(SSR)

# SSE
y=y[0:6]
SSE = np.sum((y-y_pred)**2)
print(SSE)

# SST
SST = SSR + SSE
print(SST)

# R_SQUARE
r_square = 1- (SSR / SST)
r_square

bias = regressor.score(x_train, y_train)
print(bias)

variance = regressor.score(x_test,y_test)
print(variance)


from sklearn.metrics import mean_squared_error
train_mse = mean_squared_error(y_train, regressor.predict(x_train))
test_mse = mean_squared_error(y_test, y_pred)


################

import pickle
 
#save the trained model to disk
filename = 'Linear_Regression_model.pkl'

# open a file in write-binary mode and dump the model
with open(filename, 'wb') as file:
    pickle.dump(regressor, file)

print("Model has been pickled and saved as Linear_Regression_model.pkl")

import os
os.getcwd()














