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


Grade = {
         'A+': 95,
         'A': 85,
         'A-':77,
         'B+':72,
         'B':67,
         'B-':62,
         'C+':57,
         'C':50,
         'C-':42,
         'D':37,
         'D+':32,
         'E':15,
         'PC':50,
         'AB':0,
         'IC':0,
         'F':0,
         'R':0,
         'WH':0
        } 


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


Programming_previous_grades = dataset.iloc[:,[3,8,13,16,18,20,22,23,29]].values
Programming_grade = dataset.iloc[:, 33].values
Networking_previous_grades = dataset.iloc[:,[21,27]].values
Networking_grade = dataset.iloc[:, 34].values
Database_previous_grades = dataset.iloc[:,[12,17,28]].values
Database_grade = dataset.iloc[:, 35].values
Genaral_previous_grades = dataset.iloc[:,[4,5,6,9,10,11,15,24,25,30,31]].values
Genaral_grade = dataset.iloc[:, 36].values

            


# In[6]:


# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state=9)


from sklearn.model_selection import train_test_split
Programming_previous_grades_train, Programming_previous_grades_test, Programming_grade_train, Programming_grade_test = train_test_split(Programming_previous_grades, Programming_grade, test_size = 0.2, random_state=9)
Networking_previous_grades_train, Networking_previous_grades_test, Networking_grade_train, Networking_grade_test = train_test_split(Networking_previous_grades, Networking_grade, test_size = 0.2, random_state=9)
Database_previous_grades_train, Database_previous_grades_test, Database_grade_train, Database_grade_test = train_test_split(Database_previous_grades, Database_grade, test_size = 0.2, random_state=9)
Genaral_previous_grades_train, Genaral_previous_grades_test, Genaral_grade_train, Genaral_grade_test = train_test_split(Genaral_previous_grades, Genaral_grade, test_size = 0.2, random_state=9)


# In[7]:


from sklearn import linear_model


# In[8]:


ProgrammingRegr = linear_model.LinearRegression()
ProgrammingRegr.fit(Programming_previous_grades_train, Programming_grade_train)
NetworkingRegr = linear_model.LinearRegression()
NetworkingRegr.fit(Networking_previous_grades_train, Networking_grade_train)
DatabaseRegr = linear_model.LinearRegression()
DatabaseRegr.fit(Database_previous_grades_train, Database_grade_train)
GenaralRegr = linear_model.LinearRegression()
GenaralRegr.fit(Genaral_previous_grades_train, Genaral_grade_train)


# In[38]:


ProgrammingPred = ProgrammingRegr.predict(Programming_previous_grades_test)
NetworkingPred = NetworkingRegr.predict(Networking_previous_grades_test)
DatabasePred = DatabaseRegr.predict(Database_previous_grades_test)
GenaralPred = GenaralRegr.predict(Genaral_previous_grades_test)


# In[39]:


#Grade = {'A+': 95,'A': 85,'A-':77,'B+':72,'B':67,'B-':62,'C+':57,'C':50,'C-':42,'D':37,'D+':32,'E':15,'PC':50,'AB':0,'IC':0,'F':0,'R':0,'WH':0} 
def gradeMe( Num ):
    if(Num>=95):
            pred = "A+"
    elif (Num>=85):
            pred = "A"
    elif (Num>=77):
            pred = "A-"
    elif (Num>=72):
            pred = "B+"
    elif (Num>=67):
            pred = "B"
    elif (Num>=62):
            pred = "B-"
    elif (Num>=57):
            pred = "C+"
    elif (Num>=45):
            pred = "C"
    elif (Num>=42):
            pred = "C-"
    elif (Num>=35):
            pred = "D"
    else:
            pred = "F"
            
    return pred

     


# In[40]:


print("Predicted Programming Grades  :-  " + gradeMe(ProgrammingPred[0]))

print("Predicted Networking Grades  :-  " + gradeMe(NetworkingPred[0]))

print("Predicted Database Grades  :-  " + gradeMe(DatabasePred[0]))

print("Predicted Genaral Grades  :-  " +gradeMe(GenaralPred[0]))


pickle.dump(ProgrammingPred, open('database_pred_model.pkl','wb'))
pickle.dump(ProgrammingPred, open('networking_pred_model.pkl','wb'))
pickle.dump(ProgrammingPred, open('genarel_pred_model.pkl','wb'))
pickle.dump(ProgrammingPred, open('programming_pred_model.pkl','wb'))


model1 =pickle.load( open('database_pred_model.pkl','rb'))
model2 =pickle.load( open('networking_pred_model.pkl','rb'))
model3 =pickle.load( open('genarel_pred_model.pkl','rb'))
model4 =pickle.load( open('programming_pred_model.pkl','rb'))

# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




