from sklearn.ensemble import ExtraTreesRegressor
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
import sklearn.metrics
import pandas as pd 
import numpy as np


#import file
df=pd.read_csv('data/cleandata.csv')
#transform categorical data
le_Gender = LabelEncoder()
le_family_history_with_overweight = LabelEncoder()
le_FAVC = LabelEncoder()
le_CAEC = LabelEncoder()
le_SMOKE = LabelEncoder()
le_SCC = LabelEncoder()
le_CALC = LabelEncoder()
le_MTRANS = LabelEncoder()
le_NObeyesdad = LabelEncoder()



df['NObeyesdad'] = le_NObeyesdad.fit_transform(df['NObeyesdad'])


df['Gender'] = le_Gender.fit_transform(df['Gender'])
df['family_history_with_overweight'] = le_family_history_with_overweight.fit_transform(df['family_history_with_overweight'])
df['FAVC'] = le_FAVC.fit_transform(df['FAVC'])
df['CAEC'] = le_CAEC.fit_transform(df['CAEC'])
df['SMOKE'] = le_SMOKE.fit_transform(df['SMOKE'])
df['SCC'] = le_SCC.fit_transform(df['SCC'])
df['CALC'] = le_CALC.fit_transform(df['CALC'])
df['MTRANS'] = le_MTRANS.fit_transform(df['MTRANS'])

variables = ['Gender', 'Age','family_history_with_overweight', 'FAVC', 'FCVC', 'NCP','CAEC', 'SMOKE',
           'CH2O','SCC', 'FAF', 'TUE','CALC', 'MTRANS']


X = df[variables]
sc = StandardScaler()
X = sc.fit_transform(X) 
Y = df['NObeyesdad']

X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.1)

#train model
regressor = ExtraTreesRegressor(n_estimators = 200)
regressor.fit(X_train,y_train)

#prediction and evaluation
y_train_pred = regressor.predict(X_train)
y_test_pred = regressor.predict(X_test)

print("Test RMSE: ", np.sqrt(sklearn.metrics.mean_squared_error(y_test, y_test_pred)))

def absoluteError():
    return sklearn.metrics.mean_absolute_error(y_test, y_test_pred)


def squaredError():
    return np.sqrt(sklearn.metrics.mean_squared_error(y_test, y_test_pred))

def obPredict(gender,age,history, favc, fcvc, ncp, caec, smoke, ch2o, scc, faf, tue, calc, mtrans):
    print('Predicting on new data\n\n')
    #(gender:m/f, age, family history:y/n, favc:y/n,fcvc:1 to 3, Ncp: 1 to 3, caec: sometimes,frequently, always, no, Smoke:y/n, CH2O: 0 to 3, SCC:y/n, Faf: 0 to 2, tue: 0 to 1, calc: sometimes,frequently, always, no, Mtrans: Public_Transportation)
    person = [gender,float(age),history, favc, float(fcvc), float(ncp), caec, smoke, float(ch2o), scc, float(faf), float(tue), calc, mtrans]
    # person = ['Male',20,'no','yes',3.0,3.0,'Sometimes','no',1.7,'no',0.4,0.5,'Frequently','Public_Transportation']
    print('person - ',str(person))

    

    person[0] = le_Gender.transform([person[0]])[0] 
    person[2] = le_family_history_with_overweight.transform([person[2]])[0] 
    person[3] = le_FAVC.transform([person[3]])[0] 
    person[6] = le_CAEC.transform([person[6]])[0] 
    person[7] = le_SMOKE.transform([person[7]])[0] 
    person[9] = le_SCC.transform([person[9]])[0] 
    person[12] = le_CALC.transform([person[12]])[0] 
    person[13] = le_MTRANS.transform([person[13]])[0] 

    X = sc.transform([person])

    obesity_level = regressor.predict(X)[0]
    obesity_level = round(obesity_level)
    if obesity_level == 0:
        display = 'Insufficient_Weight'
    elif obesity_level == 1:
        display = 'Normal_Weight'
    elif obesity_level == 2:
        display = 'Overweight_Level_I'
    elif obesity_level == 3:
        display = 'Overweight_Level_II'
    elif obesity_level == 4:
        display = 'Obesity_Type_I'
    elif obesity_level == 5:
        display = 'Obesity_Type_II'
    elif obesity_level == 6:
        display = 'Obesity_Type_III'
    else:
        display = 'no value'

    return display
    



