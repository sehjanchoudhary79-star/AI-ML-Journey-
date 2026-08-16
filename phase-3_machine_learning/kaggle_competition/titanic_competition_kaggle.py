import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix

data=pd.read_csv("train.csv")

data["Title"]=data["Name"].str.extract (r"([A-Za-z]+)\.",expand=False)
rare_titles=["Lady","Countess","Capt","Col","Don","Dr","Major","Rev","Sir","Jonkheer","Dona"]
data["Title"]=data["Title"].replace(rare_titles,"Rare")
data["Title"]=data["Title"].replace(["Mlle","Ms"],"Miss")
data["Title"]=data["Title"].replace("Mme","Mrs")

data["FamilySize"]=data["SibSp"]+data["Parch"]+1
data["IsAlone"]=(data["FamilySize"]==1).astype(int)

data["Age"]=data["Age"].fillna(data["Age"].median())
data["Fare"]=data["Fare"].fillna(data["Fare"].median())
data["Sex"]=data["Sex"].map({"male":0,"female":1})
data["Deck"]=data["Cabin"].fillna("U").str[0]
data=pd.get_dummies(data,columns=["Title"],drop_first=True,)
data=pd.get_dummies(data,columns=["Deck"],drop_first=True,)
data=pd.get_dummies(data,columns=["Embarked"],drop_first=True,)
data=pd.get_dummies(data,columns=["Pclass"],drop_first=True,)

X=data.drop( columns=["PassengerId","Survived","Name","Ticket","Cabin"])
feature_columns=X.columns
X= np.column_stack([X[col].to_numpy().astype(np.float64) for col in X.columns])

x_st=X.std(axis=0)
x_mean=X.mean(axis=0)
x_std=X.std(axis=0)
x_std[x_std==0]=1.0
X=(X-X.mean(axis=0))/x_std
y=data["Survived"]
y=y.to_numpy().astype(np.float64)


w=np.zeros(X.shape[1])
b=0

def logistic_regression(X,W,b):
    z=np.dot(X,W)+b
    f=1/(1+np.exp(-z))
    return f

def gradient_descent(X,W,y,b,lr=0.0053,iterations=99000):

    m=X.shape[0]
    costs=[]

    for i in range (iterations):
        z=np.dot(X,W)+b
        g=1/(1+np.exp(-z))
        error=g-y
        dw=1/m*np.dot(X.T,error)
        db=1/m* np.sum(error)
        W=W-lr*dw
        b=b-lr*db

        epsilon=1e-15
        f_bounded=np.clip(g,epsilon,1-epsilon)
        cost=-(1/m)*np.sum(y*np.log(f_bounded)+(1-y)*np.log(1-f_bounded))
        costs.append(cost)
    return W,b,costs    

def accuracy(y,y_hat):
    correct= np.sum(y==y_hat)
    wrong=np.sum(y!=y_hat)
    total=len(y)
    acc=correct/total*100
    print(f"correct:{correct}, wrong:{wrong}, total:{total}, accuracy:{acc}")

def threshold(y_hat):
    return np.where(y_hat>=0.5,1,0)      

sns.set_theme(style="whitegrid")

def cost_chart(costs):
    plt.figure(figsize=(8, 4))
    plt.plot(costs, color="#2ecc71", linewidth=2)
    plt.title("Gradient Descent Loss (Cost) Convergence")
    plt.xlabel("Iterations")
    plt.ylabel("Binary Cross-Entropy Loss")
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.show()

def ConfusionMatrix(y,y_hat):
    cm = confusion_matrix(y, y_hat)
    plt.figure(figsize=(5, 4))
    sns.heatmap(
        cm,
        annot=True,
        fmt="d",
        cmap="Blues",
        cbar=False,
        xticklabels=["Perished (0)", "Survived (1)"],
        yticklabels=["Perished (0)", "Survived (1)"],
    )
    plt.title("Training Confusion Matrix")
    plt.xlabel("Predicted Label")
    plt.ylabel("Actual Label")
    plt.show()

def features_importance(feature_columns,w):
    weights_df = pd.DataFrame({"Feature": feature_columns, "Weight": w})
    weights_df = weights_df.sort_values(by="Weight", ascending=False)

    plt.figure(figsize=(10, 6))
    sns.barplot(x="Weight", y="Feature", data=weights_df, palette="viridis")
    plt.axvline(0, color="red", linestyle="--", linewidth=1.5)
    plt.title("Learned Feature Importance ($w$)")
    plt.xlabel("Weight Value (Positive = Helps Survival)")
    plt.tight_layout()
    plt.show()

p,q,costs=gradient_descent(X,w,y,b)    
print(p,q) 
y_hat=logistic_regression(X,p,q)
y_h=threshold(y_hat)
accuracy(y,y_h)

cost_chart(costs)
ConfusionMatrix(y,y_h)
features_importance(feature_columns,p)


test_data = pd.read_csv("test.csv")

test_data["Title"] = test_data["Name"].str.extract(r" ([A-Za-z]+)\.", expand=False)
test_data["Title"] = test_data["Title"].replace(rare_titles, "Rare")
test_data["Title"] = test_data["Title"].replace(["Mlle", "Ms"], "Miss")
test_data["Title"] = test_data["Title"].replace("Mme", "Mrs")

data["Age"]=data["Age"].fillna(data["Age"].median())
data["Fare"]=data["Fare"].fillna(data["Fare"].median())

test_data["FamilySize"] = test_data["SibSp"] + test_data["Parch"] + 1
test_data["IsAlone"] = (test_data["FamilySize"] == 1).astype(int)
test_data["Deck"] = test_data["Cabin"].fillna("U").str[0]
test_data["Sex"] = test_data["Sex"].map({"male": 0, "female": 1})
test_data = pd.get_dummies(test_data, columns=["Title", "Deck", "Embarked", "Pclass"], drop_first=True)

X_test_df = test_data.drop(columns=["PassengerId", "Name", "Ticket", "Cabin"])
X_test_df = X_test_df.reindex(columns=feature_columns, fill_value=0)


X_test = X_test_df.values.astype(float)
X_test_scaled = (X_test - x_mean) / x_st


test_probs = logistic_regression(X_test_scaled, p, q)
y_hat_test = threshold(test_probs)

submission = pd.DataFrame(
    {"PassengerId": test_data["PassengerId"], "Survived": y_hat_test}
)

submission.to_csv("submission.csv", index=False)
print(" Success! 'submission.csv' generated in your current folder.")

            

