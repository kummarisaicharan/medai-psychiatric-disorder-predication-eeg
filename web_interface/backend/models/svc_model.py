import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
from sklearn.preprocessing import StandardScaler, LabelEncoder, MinMaxScaler
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn_som.som import SOM
from sklearn_som.som import SOM
from sklearn import datasets
import numpy as np

datasets_folder = '/Users/aiviewgroup/Desktop/projects/medAI/medai_models/datasets/'
data_file = datasets_folder + 'EEG.machinelearing_data_BRMH.csv'
svc_image="svc_decision.png"

class SVC_Model_cb:
    def svc_model():
        data=pd.read_csv(data_file)
        #print(data.head())
        # find the number of rows and columns in the dataset
        # print(data.shape)
        # find all the cloumns in the dataset  
        # print(data.columns)
        # show all the data in the output
        # print(data.info())
        data=data.rename(columns={"specific.disorder": "sd", "main.disorder": "md"})
        # find null values in the dataset
        # print(data.isnull().sum())
        # replace NA values with 0
        data = data.fillna(0)

        # remove the date column
        data = data.drop(['eeg.date'], axis=1)
        data=data.drop(['no.'], axis=1)
        data_copy=data.copy()
        md = LabelEncoder()
        data['md'] = md.fit_transform(data['md'])
        data['md'].value_counts()
        # encode column with values 1 and 0
        sd=LabelEncoder()
        data['sex'] = sd.fit_transform(data['sex'])
        data['sex'].value_counts()
        data=data.drop(['sd'], axis=1)
        X = data.drop('md', axis = 1)
        y = data['md']

        X=X.drop(['IQ','sex','education'], axis=1)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 42)
        # remove first row of the dataframe
        X_train = X_train.drop(X_train.index[0])
        y_train = y_train.drop(y_train.index[0])
        sc = StandardScaler()

        X_train = sc.fit_transform(X_train)
        X_test = sc.fit_transform(X_test)
        svc = SVC(kernel='sigmoid')
        svc.fit(X_train, y_train)
        pred_svc = svc.predict(X_test)
        acc_rf=accuracy_score(y_test, pred_svc)
        inv_pred=md.inverse_transform(pred_svc)
        pred_rf=inv_pred[87]
        svc_result=[]
        fig, ax = plt.subplots()
        # title for the plots
        title = ('Decision surface of sigmoid SVC ')
        # Set-up grid for plotting.
        X=X_train[:,4:6]
        y=y_train
        X0, X1 = X[:, 0], X[:, 1]
        xx, yy = make_meshgrid(X0, X1)
        svc = SVC(kernel='sigmoid')
        svc.fit(X, y)

        plot_contours(ax, svc, xx, yy, cmap=plt.cm.coolwarm, alpha=0.8)
        ax.scatter(X0, X1, c=y, cmap=plt.cm.coolwarm, s=20, edgecolors='k')
        ax.set_ylabel('AB.A.delta.c.F7')
        ax.set_xlabel('AB.A.theta.c.F7')
        ax.set_xticks(())
        ax.set_yticks(())
        ax.set_title(title)
        ax.legend()
        # save plot to file
        plt.savefig(svc_image)
       # limit accuracy to 3 decimal places
        svc_result.append(round(acc_rf*100,3))
        svc_result.append(pred_rf)
        svc_result.append(svc_image)
        # convert rf_result to dictionary
        svc_result=dict(zip(['accuracy','prediction','image'],svc_result))
        return svc_result

def make_meshgrid(x, y, h=.02):
    x_min, x_max = x.min() - 1, x.max() + 1
    y_min, y_max = y.min() - 1, y.max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))
    return xx, yy

def plot_contours(ax, svc, xx, yy, **params):
    Z = svc.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)
    out = ax.contourf(xx, yy, Z, **params)
    return out

print(SVC_Model_cb.svc_model())