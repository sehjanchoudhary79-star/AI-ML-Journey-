import pandas as pd 
import  numpy as np 

from sklearn.model_selection import train_test_split

data =  pd.read_csv("decision_tree_dataset.csv")
pd.set_option('display.max_columns',None)

data["gender"]=data["gender"].map({"Male":1,"Female":0})
data["has_partner"]=data["has_partner"].map({"Yes":1,"No":0})
data["has_dependents"]=data["has_dependents"].map({"Yes":1,"No":0})
data["has_paperless_billing"]=data["has_paperless_billing"].map({"Yes":1,"No":0})
data["has_online_security"]=data["has_online_security"].map({"Yes":1,"No":0})
data["has_tech_support"]=data["has_tech_support"].map({"Yes":1,"No":0})
data["has_streaming_tv"]=data["has_streaming_tv"].map({"Yes":1,"No":0})

data=pd.get_dummies(data,columns=["contract_type","payment_method","internet_service"],drop_first=True,)
data[data.select_dtypes(bool).columns]=data.select_dtypes(bool).astype(int)

X=data.drop(columns=["customer_id","churn"]).to_numpy().astype(np.float64)
y=data.loc[:,"churn"].to_numpy().astype(np.float64)


def entropy(y):
    if len(y)==0:
        return 0
    p=np.sum(y==1)/len(y)
    p0=1-p
    if p==0 or p==1:
        return 0
    h=-p*np.log2(p)-p0*np.log2(p0)
    return h

def information_gain(y,y_left,y_right):
    h_root=entropy(y)
    left_w=len(y_left)/len(y)
    right_w=len(y_right)/len(y)
    weighted_entropy=left_w*entropy(y_left)+right_w*entropy(y_right)
    ig=h_root-weighted_entropy
    return ig 

def best_split(X,y):
    best_ig=-1
    best_feature=None
    best_threshold=None

    for feature in range(X.shape[1]):
        thresholds=np.unique(X[:,feature])

        for threshold in thresholds:
            mask_left=X[:,feature]<=threshold
            mask_right=X[:,feature]>threshold
            y_left=y[mask_left]
            y_right=y[mask_right]

            ig=information_gain(y,y_left,y_right) 

            if ig > best_ig:
                best_ig=ig
                best_feature=feature
                best_threshold=threshold

    return best_feature,best_threshold 



class Node:
    def __init__(self,feature=None,threshold=None,left=None,right=None,value=None):
        self.feature=feature
        self.threshold=threshold
        self.left=left
        self.right= right
        self.value = value 

def build_tree (X,y ,depth=0,max_depth=5):
        if len(np.unique(y))==1:
            return Node (value=int(y[0]))   

        if depth>=max_depth:
            majority=int(np.round(np.mean(y)))
            return Node (value=majority)

        feature,threshold=best_split(X,y)

        mask_left=X[:,feature]<=threshold
        mask_right= X[:,feature]>threshold 

        left=build_tree(X[mask_left],y[mask_left],depth+1,max_depth)
        right=build_tree(X[mask_right],y[mask_right],depth+1,max_depth)

        return Node (feature=feature,threshold=threshold,left=left,right=right)
    
def predict_one(node,sample):

    if node.value is not None:
        return node.value

    if sample[node.feature]<=node.threshold:
        return predict_one(node.left,sample)
    else:
        return predict_one(node.right,sample)

def predict(node,X):
    return np.array([predict_one(node,sample)for sample in X])

X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2,random_state=42)

tree=build_tree(X_train,y_train)
y_hat_train=predict(tree,X_train)
print("tree built")

y_hat=predict(tree,X_test)
print("predictions done")

y_hat=y_hat.astype(np.float64)

accuracy_train=np.sum(y_hat_train==y_train.astype(int))/len(y_train)*100
accuracy_test=np.sum(y_hat==y_test.astype(int))/len(y_test)*100
print(accuracy_train,accuracy_test)




        
                