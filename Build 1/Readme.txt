Make sure the db.sqlite is in the same folder then:

First run start_build.sh this will create the best scoring data model and automatically will start producing the regression model. 

Second run the start_cli_interface.sh for the command line input interface. Here you can input data for the different features and get a prediction for the lifespan as output.

Libraries used:
logging
pandas
sqlite3
sklearn
math
os
sys
pickle

