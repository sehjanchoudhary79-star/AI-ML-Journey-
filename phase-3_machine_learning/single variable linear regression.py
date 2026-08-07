

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

data=pd.read_csv("linear_clean.csv")
x=np.array(data['x'])
y=np.array(data['y'])



w=0
b=0

def linear_regression(x,w,b):
       f=w*x+b
       return f

def gradient_descent(x,y,w,b,learning_rate=0.01,iteration=10000):
    n=len(x)
    for i in range(iteration):
        f=w*x+b
        error=f-y
        w_derivative=1/n * np.sum(error*x)
        b_derivative=1/n * np.sum(error)
        w_temp=w- (learning_rate * w_derivative)
        b_temp=b- (learning_rate * b_derivative)
        w=w_temp    
        b=b_temp
        
    return w,b



plt.scatter(x,y)  
plt.xlabel("square feet")
plt.ylabel("price") 
plt.title("housing price")
plt.show()

a,b=gradient_descent(x,y,w,b,)
print(a,b)
f=linear_regression(x,a,b)
print(f)     
