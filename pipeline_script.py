
import sqlite3
import pandas as pd


dbName = "rest_server_new/medisch_centrum_randstad/db.sqlite3"
tableName = "rest_api_netlify"
url = "http://localhost:8080/medish_centrum_randstad/api/netlify?page=1"
csvFile = "rest_server_new/medisch_centrum_randstad/data/data.csv"

##########################
### Read from REST API ###
##########################

# response = requests.get(url)
# file_contents= response.json()  #dictionary
# df = pd.DataFrame.from_dict(file_contents['data']) #all the needed info was condensed into one data column called 'data'
# df3 = df.copy() #keep original for df3 

######################
### Read from .csv ###
######################
#df pd.read_csv('csvFile',skipinitialspace=True)
#df3 = df.copy() #keep original for df3 

############################
### Read from SQlite3 db ###
############################
dbConnection = sqlite3.connect(dbName)

#query db and write to pd:
dfFromDB = pd.read_sql_query(f"SELECT * FROM {'rest_api_netlify'}", dbConnection)
#sql adds index, remove:
df = dfFromDB.drop('id', axis=1)
pd.set_option('display.max_columns', 10)
#print(df.head())

df3 = df.copy() #keep original for df3 

########################
### CLEANING for DF1 ### drop NA, drop duplicates, convert types to float64
########################

df = df.dropna()

duplicate_rows_df = df[df.duplicated()]
print ("Number of duplicate rows: ", duplicate_rows_df.shape)

if duplicate_rows_df.shape == (0, 8):
    print ('There are no unexcpected duplicates')
else:
    print ('There are unexcpected duplicates please look at the data')
    print(duplicate_rows_df)
    x=input('Do you want to delete the duplicates? Y/n') 
    if x == 'Y':
        df=df.drop_duplicates()

df = df.apply(lambda x: pd.to_numeric(x, errors='coerce') if x.dtype == 'object' else x)
df.astype('float64').dtypes

df.to_sql('df1',if_exists='replace',con=dbConnection)
print('Generated DF1: succesfully written to SQL database')
df.to_csv('df1.csv')
print('Generated DF1: succesfully written to df1.csv')

########################

df['BMI']=df['mass']/((df['length']/100)**2)

df.to_sql('df2',if_exists='replace',con=dbConnection)
print('Generated DF2: succesfully written to SQL database')
df.to_csv('df2.csv')
print('Generated DF2: succesfully written to df2.csv')

########################
### CLEANING for DF3 ### df but imputed drop NA with avg, drop duplicates, convert types to float64, outliers IQR method, BMI feature
########################

dfmean = df.mean()
df3 = df3.fillna(dfmean)

Q1 = df3.quantile(0.25)
Q3 = df3.quantile(0.75)
IQR = Q3 - Q1
df3 = df3[~((df3 < (Q1 - 1.5 * IQR)) |(df3 > (Q3 + 1.5 * IQR))).any(axis=1)]

df3 = df.drop_duplicates()
df3 = df.apply(lambda x: pd.to_numeric(x, errors='coerce') if x.dtype == 'object' else x)
df3.astype('float64').dtypes

df3.to_sql('df3',if_exists='replace',con=dbConnection)
print('Generated DF3: succesfully written to SQL database')
df3.to_csv('df3.csv')
print('Generated DF3: succesfully written to df3.csv')


dbConnection.commit
dbConnection.close()





