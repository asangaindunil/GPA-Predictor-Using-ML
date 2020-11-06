#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
#import matplotlib.pyplot as plt
import pandas as pd
import pickle
from matplotlib import pyplot as plt


# In[2]:


dataset = pd.read_csv('ww.csv')
from sklearn.preprocessing import MinMaxScaler
sc=MinMaxScaler()
dataset.keys()


# In[3]:


Grade = {'A+': 95,'A': 85,'A-':77,'B+':72,'B':67,'B-':62,'C+':57,'C':50,'C-':42,'D':37,'D+':32,'E':15,'PC':50,'AB':0,'IC':0,'F':0,'R':0,'WH':0} 


# In[4]:


dataset.IP = [Grade[item] for item in dataset.IP] 
dataset.ICS = [Grade[item] for item in dataset.ICS] 
dataset.MC = [Grade[item] for item in dataset.MC] 
dataset.CS = [Grade[item] for item in dataset.CS] 
dataset.OOC= [Grade[item] for item in dataset.OOC] 
dataset.SPM = [Grade[item] for item in dataset.SPM] 
dataset.PS1 = [Grade[item] for item in dataset.PS1] 
dataset.EAP = [Grade[item] for item in dataset.EAP] 
dataset.ISDM = [Grade[item] for item in dataset.ISDM] 
dataset.IWT = [Grade[item] for item in dataset.IWT] 
dataset.SE = [Grade[item] for item in dataset.SE] 
dataset.OOP = [Grade[item] for item in dataset.OOP] 
dataset.DBMS = [Grade[item] for item in dataset.DBMS] 
dataset.OSSA = [Grade[item] for item in dataset.OSSA] 
dataset.MAD = [Grade[item] for item in dataset.MAD] 
dataset.DSA = [Grade[item] for item in dataset.DSA] 
dataset.CN = [Grade[item] for item in dataset.CN]  
dataset.ITP = [Grade[item] for item in dataset.ITP] 
dataset.PS2 = [Grade[item] for item in dataset.PS2] 
dataset.ESD1 = [Grade[item] for item in dataset.ESD1] 
dataset.NDM = [Grade[item] for item in dataset.NDM] 
dataset.DS = [Grade[item] for item in dataset.DS] 
dataset.PAF = [Grade[item] for item in dataset.PAF] 
dataset.ITPM = [Grade[item] for item in dataset.ITPM] 
dataset.ESD2 = [Grade[item] for item in dataset.ESD2] 
dataset.HCI = [Grade[item] for item in dataset.HCI] 
dataset.IAS = [Grade[item] for item in dataset.IAS] 
dataset.DA = [Grade[item] for item in dataset.DA] 
dataset.BMIT = [Grade[item] for item in dataset.BMIT] 


# In[5]:


X = dataset.iloc[:,[3,4,5,6,8,9,10,11,12,13,15,16,17,18,20,21,22,23,24,25,27,28,29,30,31]].values
y = dataset.iloc[:, 1].values


# In[6]:


from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state=9)

from sklearn import linear_model
import statsmodels.api as sm
regr = linear_model.LinearRegression()
regr.fit(X_train, y_train)
plt.plot(X_train, y_train, 'o')


# In[7]:


pred = regr.predict(X_test)
pred


# In[8]:


import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_boston
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
test_set_rmse = (np.sqrt(mean_squared_error(y_test, pred)))
test_set_r2 = r2_score(y_test, pred)


# In[9]:


print(test_set_rmse)
print(test_set_r2)


# In[10]:


pred = regr.predict([[32, 15,  0, 57, 50, 57, 15, 57, 50, 50, 50,  0, 37, 15,  0, 32, 62, 67, 67, 50, 32,  0,  0, 72, 85]])
# pred = regr.predict(X_test)
pred


# In[11]:


X[90]


# In[19]:


accuracy = regr.score(X_test,y_test)
print(accuracy*100,'%')


# In[20]:
pickle.dump(regr, open('gpa_pred_model.pkl','wb'))


model =pickle.load( open('gpa_pred_model.pkl','rb'))



