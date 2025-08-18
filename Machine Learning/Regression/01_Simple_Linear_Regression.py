import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

#Load the dataset
dataset = pd.read_csv(r'C:\Ds & AI ( my work)\Machine Learning\Regression\Salary_Data.csv') 

#Independent Variable
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

#compare predicted and actual salaries from the test set
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

#future predi-1
y_12 = (m_slope*12) + c_intercept
print(y_12)

#future pred-2
y_20 = (m_slope*20) + c_intercept
print(y_20)