
import numpy as np
import pandas as pd

data=pd.read_csv("house_price_data.csv")
x=np.array(data[["Size_sqft","Bedrooms","Age_years"]])
x=(x-x.mean(axis=0))/x.std(axis=0)
y=np.array(data["Price_lakhs"])
w=np.array([9,2,5])
b=0

def linear_regression(X,W,b):
    y=np.dot(X,W)+b
    return y


def gradient_descent(X,y,W,b,lr=0.01,iteration=9000):
    m=X.shape[0]

    for i in range(iteration):
        f=np.dot(X,W)+b
        error=f-y
        dw=1/m*np.dot(X.T,error)
        db=1/m*np.sum(error)
        W=W-lr*dw
        b=b-lr*db
    return W,b
a,c=gradient_descent(x,y,w,b)
print(a,c)
f=linear_regression(x,a,c)
print(f)    
        

