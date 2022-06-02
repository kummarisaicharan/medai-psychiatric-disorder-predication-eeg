import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
from sklearn.preprocessing import StandardScaler, LabelEncoder, MinMaxScaler
from sklearn_som.som import SOM
from sklearn.model_selection import train_test_split




datasets_folder = '/Users/aiviewgroup/Desktop/projects/medAI/medai_models/datasets/'
data_file = datasets_folder + 'EEG.machinelearing_data_BRMH.csv'
som_image="som_map.png"

class SOM_Model_cb:
    def som_model():
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

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 42)
        X_train = X_train.to_numpy()
        y_train = y_train.to_numpy()
        X_test = X_test.to_numpy()
        y_test = y_test.to_numpy()
        eeg_data = X_train
        eeg_label = y_train
        eeg_som = SOM(m=7, n=1, dim=1145)
        eeg_som.fit(eeg_data)
        predictions = eeg_som.predict(X_test)
        pred_rsom=predictions
        acc_som = accuracy_score(y_test, predictions)
        inv_pred=md.inverse_transform(pred_rsom)
        pred_som=inv_pred[87]
        som_reslut=[]
        som_reslut.append(round(acc_som*100,3))
        som_reslut.append(pred_som)
        x_data = X_test[:,5]
        y_data = X_test[:,6]
        colors = ['red', 'green', 'blue', 'yellow', 'black', 'pink', 'cyan']


        # create plots side by side
        fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(10,5))
        ax[0].scatter(x_data, y_data, c=y_test, cmap=ListedColormap(colors))
        ax[0].title.set_text('Actual Classes')
        ax[1].scatter(x_data, y_data, c=predictions, cmap=ListedColormap(colors))
        ax[1].title.set_text('SOM Predictions')
        plt.savefig(som_image)
        som_reslut.append(som_image)
        som_reslut=dict(zip(['accuracy','prediction','image'],som_reslut))
        return som_reslut
# data=SOM_Model_cb.som_model()
# print(data)





