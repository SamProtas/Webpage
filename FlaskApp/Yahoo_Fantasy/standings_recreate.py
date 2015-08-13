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
###################
#END AUTHENTICATION
###################

def get_standings_data(league_number):

	query = "select * from fantasysports.leagues.standings where league_key=" + league_number
	data_yql=y3.execute(query, token=token)
	data = data_yql.rows
	data_id=data[0]
	data=data[0]['standings']['teams']['team']  #step through to dictionary with 14 teams

	for i in range(len(data)):
		curweek.append(int(data_id['current_week']))
		year.append(int(data[i]['team_points']['season']))
		league_id.append(int(data_id['league_id']))
		manager_team.append(data[i]['name'])
		manager_id.append(data[i]['team_id'])

		points_for.append(float(data[i]['team_standings']['points_for']))
		points_against.append(float(data[i]['team_standings']['points_against']))
		num_moves.append(int(data[i]['number_of_moves']))
		num_trades.append(int(data[i]['number_of_trades']))
		wins.append(int(data[i]['team_standings']['outcome_totals']['wins']))
		losses.append(int(data[i]['team_standings']['outcome_totals']['losses']))
		try:
			clinched_playoffs.append(int(data[i]['clinched_playoffs']))
		except:
			clinched_playoffs.append(0)
		if data[i]['team_standings']['rank'] != None:
			place.append(int(data[i]['team_standings']['rank']))
		else:
			place.append(0)

		try:
			manager = (str(data[i]['managers']['manager']['nickname']))
		except:
			manager = (str(data[i]['managers']['manager'][0]['nickname']))   #if two managers exist just take the first one
		manager = modify_hidden_user(data[i]['name'], manager) #send to a function that searches for teams I know have hidden managers or duplicate nicknames, the file then gives the correct nickname mnaually
		


			################		
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

			################	
		manager = modify_hidden_user_email(email, manager)

		manager_name.append(manager)

############################################################################################################
############################################################################################################


if __name__== "__main__":

	##############################
	#CREATE DRAFT DB FOR LM LEAGUE
	##############################

		#create empty lists to save data
	year=[]
	emails=[]
	league_id=[]
	manager_name = []
	manager_team = []
	manager_id = []
	points_for =[]
	points_against =[]
	num_moves = []
	num_trades = []
	wins = []
	losses= []
	clinched_playoffs = []
	place = []
	curweek = []
	x=get_league_ids_lm()

	
	for i in x:
		try:
			get_standings_data(i)
		except:
			pass	


	dict = {
					 
					'year': year,
					'league_id': league_id,
					'manager_name': manager_name,
					'manager_team': manager_team,
					'manager_id': manager_id,
					'points_for': points_for,
					'points_against': points_against,
					'num_moves': num_moves,
					'num_trades': num_trades,
					'wins': wins,
					'losses': losses,
					'clinched_playoffs': clinched_playoffs,
					'place': place,
					'curweek': curweek
					}


	data = pd.DataFrame(dict, columns=['year', 'league_id', 'manager_name', 'manager_team', 'manager_id', 'points_for', 'points_against', 
		                                 'num_moves', 'num_trades', 'wins', 'losses', 'clinched_playoffs', 'place', 'curweek'])	

	pd.DataFrame.to_sql(data, 'standings', conn, if_exists='replace', index=None)	
							
	conn.commit()


	##############################
	#CREATE DRAFT DB FOR EX LEAGUE
	##############################

	#create empty lists to save data
	year=[]
	emails=[]
	league_id=[]
	manager_name = []
	manager_team = []
	manager_id = []
	points_for =[]
	points_against =[]
	num_moves = []
	num_trades = []
	wins = []
	losses= []
	clinched_playoffs = []
	place = []
	curweek = []
	y=get_league_ids_ex()

	
	for i in y:
		try:
			get_standings_data(i)
		except:
			pass	


	dict = {
					 
					'year': year,
					'league_id': league_id,
					'manager_name': manager_name,
					'manager_team': manager_team,
					'manager_id': manager_id,
					'points_for': points_for,
					'points_against': points_against,
					'num_moves': num_moves,
					'num_trades': num_trades,
					'wins': wins,
					'losses': losses,
					'clinched_playoffs': clinched_playoffs,
					'place': place,
					'curweek': curweek
					}


	data = pd.DataFrame(dict, columns=['year', 'league_id', 'manager_name', 'manager_team', 'manager_id', 'points_for', 'points_against', 
		                                 'num_moves', 'num_trades', 'wins', 'losses', 'clinched_playoffs', 'place', 'curweek'])	

	pd.DataFrame.to_sql(data, 'standings_ex', conn, if_exists='replace', index=None)

	conn.commit()

#return data
#team, record, points for, points against, place, draft pick, qb_points for, wr_points for, RB_points for, kicker_points for...for each season
