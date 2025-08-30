import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

dataset = pd.read_csv(r"C:\Ds & AI ( my work)\Machine Learning\Polynomial Regression Model\emp_sal.csv")

x = dataset.iloc[:, 1:2].values
y = dataset.iloc[:,2].values

#Linear model -- linear algor (degree -1)
from sklearn.linear_model import LinearRegression
lin_reg = LinearRegression()
lin_reg.fit(x,y)

plt.scatter(x, y, color = 'red')
plt.plot_date(x, lin_reg.predict(x), color = 'blue')
plt.title('Linear regression model (Linear Regression)')
plt.xlabel('Position level')
plt.ylabel('Salary')
plt.show()

lin_model_pred = lin_reg.predict([[6]])
lin_model_pred

# Modeling Polynomial Regression Model
from sklearn.preprocessing import PolynomialFeatures
poly_reg = PolynomialFeatures(degree= 5)
x_poly = poly_reg.fit_transform(x)

poly_reg.fit(x_poly, y)

lin_reg_2 = LinearRegression()
lin_reg_2.fit(x_poly, y)

plt.scatter(x, y, color = 'red')
plt.plot_date(x, lin_reg_2.predict(poly_reg.fit_transform(x)), color = 'blue')
plt.title('polymodel (Polynomial Regression)')
plt.xlabel('Position level')
plt.ylabel('Salary')
plt.show()

poly_model_pred = lin_reg_2.predict(poly_reg.fit_transform([[6]]))
poly_model_pred




 # SVR model 
 
  
from sklearn.svm import SVR   
svr_reg = SVR(kernel="poly",degree=5, gamma="scale")
svr_reg.fit(x,y)

svr_pred = svr_reg.predict([[6]])
print(svr_pred)


from sklearn.svm import SVR   
svr_reg = SVR(kernel="poly",degree=5)
svr_reg.fit(x,y)

svr_pred = svr_reg.predict([[6]])
print(svr_pred)

from sklearn.svm import SVR   
svr_reg = SVR(kernel="rbf",degree=5)
svr_reg.fit(x,y)

svr_pred = svr_reg.predict([[6]])
print(svr_pred)

from sklearn.svm import SVR   
svr_reg = SVR(kernel="linear",degree=5)
svr_reg.fit(x,y)

svr_pred = svr_reg.predict([[6]])
print(svr_pred)




# KNN Model

from sklearn.neighbors import KNeighborsRegressor   
knn_reg = KNeighborsRegressor(n_neighbors=3)
knn_reg.fit(x,y)

knn_pred = knn_reg.predict([[6]])
print(knn_pred)










