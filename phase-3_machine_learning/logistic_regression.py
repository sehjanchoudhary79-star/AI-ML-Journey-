import numpy as np 
import pandas as pd

import matplotlib.pyplot as plt

data=pd.read_csv("logistic_regression_dataset.csv")
x=np.array(data .iloc[:,0:7])
x=(x-x.mean(axis=0))/x.std(axis=0)
y=np.array(data.iloc[:,-1])

w=np.zeros(x.shape[1])
b=0

def logistic_regression(X,W,b):
    z=np.dot(X,W)+b
    f=1/(1+np.exp(-z))
    return f

def threshold(f):
    return np.where(f>=0.5,1,0)
    

def gradient_descent(X,y,W,b,lr=0.00023,iteration=52000):

    m=X.shape[0]

    for i in range (iteration):
        f=logistic_regression(X,W,b)
        error=f-y
        dw=1/m*np.dot(X.T,error)
        db=1/m*np.sum(error)
        W=W-lr*dw
        b=b-lr*db

    return W,b

def accuracy(y,y_hat):
    correct=np.sum(y==y_hat)
    wrong=np.sum(y!=y_hat)
    total=len(y)
    acc=correct/total*100
    print(f"correct:{correct}, wrong:{wrong}, total:{total}, accuracy:{acc}")

a,c=gradient_descent(x,y,w,b)
print(a,c)  

f=logistic_regression(x,a,c)
print(f[:10])    

y_hat=threshold(f)
print(y_hat[:10])

accuracy(y, y_hat)

for i in range(x.shape[1]):
    plt.scatter(x[:,i],y, color='red')
    sort=np.argsort(x[:,i])
    plt.plot(x[:,i][sort],f[sort], color='blue')
    plt.title(f"Feature {i+1} vs Target")
    plt.xlabel(f"Feature {i+1}")
    plt.ylabel("Target")
    plt.show()