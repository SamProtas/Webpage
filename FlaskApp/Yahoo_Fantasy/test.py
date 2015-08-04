import YOAuth  #import authentication function 
import yql, os, sqlite3, datetime, pandas as pd, numpy as np  #import authentification libraries and dataframe libraries
from yql.storage import FileTokenStore
from leagues import *
from convert_hidden_to_user import *

######################
#  DATABASE CONNECTION
######################
PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__)) #create path to database
DATABASE_SCOREBOARD = os.path.join(PROJECT_ROOT, 'data', 'fantasy_football.db')

conn = sqlite3.connect(DATABASE_SCOREBOARD) #connect to database
c = conn.cursor()
######################
# END DATABASE 
######################

######################
# YAHOO DEV. AUTH
####################
consumer_key = ('dj0yJmk9SGRrbkt5SHFSd2hVJmQ9WVdrOVJqUTRiMVZLTXpRbWNHbzlNQS0tJnM9Y29uc3VtZXJzZWNyZXQmeD1iNQ--')
consumer_secret = ('3deb9f91d5086dec9c9dfe1ac8925eecb5741070')

y3 = yql.ThreeLegged(consumer_key, consumer_secret)
_cache_dir = os.path.expanduser(PROJECT_ROOT)

if not os.access(_cache_dir,os.R_OK):
	os.mkdir(_cache_dir)
token_store = FileTokenStore(_cache_dir, secret=consumer_secret)

stored_token = token_store.get('foo')

if not stored_token:
	#get access token, visit website and grant yourself access to league information
	request_token, auth_url = y3.get_token_and_auth_url()
	print "Visit url %s and get a verifier string" % auth_url
	verifier = raw_input("Enter the code: ") 
	token = y3.get_access_token(request_token, verifier)
	token_store.set('foo', token)

else:
	# Check access_token is within 1hour-old and if not refresh it and stash it
	token = y3.check_token(stored_token)
	if token != stored_token:
		token_store.set('foo', token)


##################################################################################################################
#################################          END AUTHENTICATION       ##############################################
##################################################################################################################





def get_standings_data(league_number):

	query = "select * from fantasysports.leagues.standings where league_key=" + league_number
	
	data_yql=y3.execute(query, token=token)
	data = data_yql.rows
	data_id=data[0]
	data=data[0]['standings']['teams']['team']  #step through to dictionary with 14 teams
	print len(data)
	for i in range(len(data)):
		
		manager_team.append(data[i]['name'])
		
		
		try:
			manager = (str(data[i]['managers']['manager']['nickname']))
			
		except:
			manager = (str(data[i]['managers']['manager'][0]['nickname']))   #if two managers exist just take the first one
			

		manager = modify_hidden_user(data[i]['name'], manager, email) #send to a function that searches for teams I know have hidden managers or duplicate nicknames, the file then gives the correct nickname mnaually
		
		try:
			email = (str(data[i]['managers']['manager']['email']))
			emails.append(email)
		except:
			try:
		 		email = (str(data[i]['managers']['manager'][0]['email']))
		 		emails.append(email)
		 	except:
		 		email = 'Null'
		 		emails.append(email)
		manager = 



#append final found manager
		manager_name.append(manager)
		
	
	


############################################################################################################
############################################################################################################


if __name__== "__main__":

	##############################
	#CREATE DRAFT DB FOR LM LEAGUE
	##############################

	#create empty lists to save data

	manager_name = []
	manager_team = []
	emails = []

	y=get_league_ids_lm()

	
	for i in y:
		try:
			get_standings_data(i)
			
		except:
			pass	
	
	print manager_team
	print emails
	
	dict = {
					 
					
					'manager_name': manager_name,
					'manager_team': manager_team,
					'email': emails
	
					}


	data = pd.DataFrame(dict, columns=['manager_name', 'manager_team', 'email'])	

	pd.DataFrame.to_sql(data, 'test', conn, if_exists='replace', index=None)

	conn.commit()

	

	##############################
	#CREATE DRAFT DB FOR EX LEAGUE
	##############################

	#create empty lists to save data

	manager_name = []
	manager_team = []
	emails = []

	y=get_league_ids_ex()

	
	for i in y:
		try:
			get_standings_data(i)
		except:
			pass	

		
	dict = {
					 
					'manager_name': manager_name,
					'manager_team': manager_team,
					'email': emails
	
					}

	
	data = pd.DataFrame(dict, columns=['manager_name', 'manager_team', 'email'])	

	pd.DataFrame.to_sql(data, 'test', conn, if_exists='replace', index=None)

	conn.commit()

