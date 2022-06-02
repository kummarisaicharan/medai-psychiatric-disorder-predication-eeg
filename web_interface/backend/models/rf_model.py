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



datasets_folder = '/Users/aiviewgroup/Desktop/projects/medAI/medai_models/datasets/'
data_file = datasets_folder + 'EEG.machinelearing_data_BRMH.csv'
rf_image="rf_tree.png"

class RF_Model_cb:
    def rf_model():
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
        sc = MinMaxScaler()

        X_train = sc.fit_transform(X_train)
        X_test = sc.fit_transform(X_test)
        rfc = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)  
        # use random forest regressor to train the data

        rfc.fit(X_train, y_train)
        estimator = rfc.estimators_[5]

        pred_rfc = rfc.predict(X_test)
        from sklearn.tree import export_graphviz
        # Export as dot file
        export_graphviz(estimator, 
                        out_file='tree.dot', 
                        feature_names = X.columns,
                        class_names = data_copy['md'].unique(),
                        rounded = True, proportion = False, 
                        precision = 2, filled = True)
        # convert dot to png in the current working directory
        from subprocess import call
        call(['dot', '-Tpng', 'tree.dot', '-o', rf_image, '-Gdpi=600'])
        # print(classification_report(y_test, pred_rfc))
        acc_rf=accuracy_score(y_test, pred_rfc)
        inv_pred=md.inverse_transform(pred_rfc)
        pred_rf=inv_pred[87]
        rf_result=[]
       # limit accuracy to 3 decimal places
        rf_result.append(round(acc_rf*100,3))
        rf_result.append(pred_rf)
        rf_result.append(rf_image)
        # convert rf_result to dictionary
        rf_result=dict(zip(['accuracy','prediction','image'],rf_result))
        return rf_result

