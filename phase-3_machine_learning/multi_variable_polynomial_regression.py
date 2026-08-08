import numpy as np 
import pandas as pd 

import matplotlib.pyplot as plt

data=pd.read_csv("house_price_data2.csv")
x=np.array(data.iloc[:,0:3])
sq=x**2
x=(x-x.mean(axis=0))/x.std(axis=0)
sq=(sq-sq.mean(axis=0))/sq.std(axis=0)
x=np.column_stack((x,sq))
y=np.array(data.iloc[:,3])

plt.scatter(x[:,0],y, color='red')
plt.scatter(x[:,1],y, color='blue')
plt.scatter(x[:,3],y, color='green')
plt.title("House Price Data")
plt.xlabel("Size_sqft, Bedrooms, Age_years")
plt.ylabel("Price_lakhs")
plt.show()


w=np.array([9,2,5,1,1,1])
b=0

def polynomial_regression(X,W,b):
    y=np.dot(X,W)+b
    return y

def gradient_descent(X,y,W,b,lr=0.001,iteration=7000):
    m=X.shape[0]

    for i in range (iteration):
        f_wb=np.dot(X,W)+b
        error=f_wb-y
        dw=1/m*np.dot(X.T,error)
        db=1/m*np.sum(error)
        W=W-lr*dw
        b=b-lr*db
    return W,b  

p,q=gradient_descent(x,y,w,b)
print(p,q)
f=polynomial_regression(x,p,q)
print(f)
