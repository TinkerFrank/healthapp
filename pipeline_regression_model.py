

# Goal: Output the model coefficients into the SQL database as table:'coef'
# Regression Model Winner: DF4 🥳 

from sklearn.metrics import mean_squared_error
import pandas as pd
from sklearn import linear_model 
from sklearn.model_selection import train_test_split
import math
import sqlite3
import pickle

#import model data from pipeline, in this case CSV in same folder 
df = pd.read_csv('df4.csv',sep=',',skipinitialspace=True)
df = df.drop('Unnamed: 0', axis=1)

#split the data in train and test sets with agreed 0.2 size and 42 as seed for the random state
train, test = train_test_split(df, test_size=0.2, random_state=42)
X = train.drop(columns=['lifespan'])
y = train.lifespan

#fit the model
regr = linear_model.LinearRegression()
regr.fit(X, y) 

#R-squared model score
score = regr.score(test.drop(columns=['lifespan']),test.lifespan)
rsquaredscore = score

#Root-Mean-Squared-Error (RMSE)
p_test = regr.predict(test.drop(columns=['lifespan']))
mse = mean_squared_error(test.lifespan, p_test)
rmse = (math.sqrt(mse))

#Regression Coefficients
coef = regr.coef_
intercept = regr.intercept_

#Store variables in SQL table
dbConnection = sqlite3.connect('db.sqlite3')
dfdrop = df.drop(columns=['lifespan'])
df_coef = pd.DataFrame({'feature':dfdrop.columns,'coef': coef,'intercept': intercept,'rsquared':score,'rmse':rmse})
df_coef.to_sql('coef', if_exists='replace', con=dbConnection)


pickle.dump(regr,open('state.bin','wb'))

dbConnection.close()




