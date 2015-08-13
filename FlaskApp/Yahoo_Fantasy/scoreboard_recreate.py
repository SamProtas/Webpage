import YOAuth  #import authentication function 
import yql, os, sqlite3, datetime, pandas as pd, numpy as np  #import authentification libraries and dataframe libraries
from yql.storage import FileTokenStore
from leagues import *
from convert_hidden_to_user import *

#create path to database
PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
DATABASE_SCOREBOARD = os.path.join(PROJECT_ROOT, 'data', 'fantasy_football.db')
#connect to database
conn = sqlite3.connect(DATABASE_SCOREBOARD)
c = conn.cursor()


#set yahoo developer keys
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


def get_scoreboard(league_number):
	
		
		
	query = "select * from fantasysports.leagues.scoreboard where league_key=" + league_number + " and week in (1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16)"
	data_yql=y3.execute(query, token=token)
	data = data_yql.rows
	
	
	for i in range(0,len(data)):   #iterate through each week scoreboard
		Total_Matchups = len(data[i]['scoreboard']['matchups']['matchup'])  #number of matchups in the given week
		
		for j in range(0, Total_Matchups):
			
			data_week=data[i]['scoreboard']['matchups']['matchup'] #step through to the matchup data and call it data_week to simplify
			
			year.append(int(data[i]['season']))
			league_id.append(int(data[i]['league_id']))
			playoffs.append(int(data_week[j]['is_playoffs'])) #whether matchup is playoffs(1) or not-playoffs(0)
			week.append(int(data_week[j]['week']))
			week_end_date.append(data_week[j]['week_end'])

			matchup.append(j+1)

			manager1_team.append(data_week[j]['teams']['team'][0]['name'])
			manager2_team.append(data_week[j]['teams']['team'][1]['name'])

			team1_points.append(float(data_week[j]['teams']['team'][0]['team_points']['total']))
			team1_projected.append(float(data_week[j]['teams']['team'][0]['team_projected_points']['total']))

			team2_points.append(float(data_week[j]['teams']['team'][1]['team_points']['total']))
			team2_projected.append(float(data_week[j]['teams']['team'][1]['team_projected_points']['total']))

			

			try:
				manager1_id.append(int(data_week[j]['teams']['team'][0]['managers']['manager']['manager_id']))
			except:
				manager1_id.append(int(data_week[j]['teams']['team'][0]['managers']['manager'][0]['manager_id']))
			
			try:
				manager2_id.append(int(data_week[j]['teams']['team'][1]['managers']['manager']['manager_id']))
			except:
				manager2_id.append(int(data_week[j]['teams']['team'][1]['managers']['manager'][0]['manager_id']))


			try:

				manager1_name_static = (data_week[j]['teams']['team'][0]['managers']['manager']['nickname'])
				manager1_name_static = modify_hidden_user(data_week[j]['teams']['team'][0]['name'], manager1_name_static) #send to a function that searches for teams I know have hidden managers or duplicate nicknames, the file then gives the correct nickname mnaually
				
				
			except:
				manager1_name_static = (data_week[j]['teams']['team'][0]['managers']['manager'][0]['nickname'])
				manager1_name_static = modify_hidden_user(data_week[j]['teams']['team'][0]['name'], manager1_name_static) #send to a function that searches for teams I know have hidden managers or duplicate nicknames, the file then gives the correct nickname mnaually
				#manager1_name.append(manager1_name_static)
				

			try:

				manager2_name_static = (data_week[j]['teams']['team'][1]['managers']['manager']['nickname'])
				manager2_name_static = modify_hidden_user(data_week[j]['teams']['team'][1]['name'], manager2_name_static) #send to a function that searches for teams I know have hidden managers or duplicate nicknames, the file then gives the correct nickname mnaually
				
			except:
				manager2_name_static = (data_week[j]['teams']['team'][1]['managers']['manager'][0]['nickname'])
				manager2_name_static = modify_hidden_user(data_week[j]['teams']['team'][1]['name'], manager2_name_static) #send to a function that searches for teams I know have hidden managers or duplicate nicknames, the file then gives the correct nickname mnaually
				#manager2_name.append(manager2_name_static)	
					
		

			try:
				email1 = (str(data_week[j]['teams']['team'][0]['managers']['manager']['email']))
			except:
				try:
		 			email1 = (str(data_week[j]['teams']['team'][0]['managers']['manager'][0]['email']))
		 		except:
		 			email1 = 'Null'

		 	try:
				email2 = (str(data_week[j]['teams']['team'][1]['managers']['manager']['email']))
			except:
				try:
		 			email2 = (str(data_week[j]['teams']['team'][1]['managers']['manager'][0]['email']))
		 		except:
		 			email2 = 'Null'

		 	manager1_name_final = modify_hidden_user_email(email1, manager1_name_static)
		 	manager2_name_final = modify_hidden_user_email(email2, manager2_name_static)

		 	manager1_name.append(manager1_name_final)	
		 	manager2_name.append(manager2_name_final)
	
############################################################################################################
############################################################################################################


if __name__== "__main__":

	#create blank lists to store data
	year=[]
	league_id=[]
	week = []
	week_end_date = []
	matchup = []
	manager1_name = []
	manager1_team = []
	manager1_id=[]
	player_id = []
	manager2_name = []
	manager2_team = []
	manager2_id=[]
	team1_points =[]
	team1_projected = []
	team2_points =[]
	team2_projected=[]
	playoffs=[]


	##############################
	#CREATE SCOREBOARD DB FOR LM LEAGUE
	##############################
	x=get_league_ids_lm()

	for i in x:
		
		try:
			get_scoreboard(i)
			
		except:
			pass

	dict = {
				 
				'year': year,
				'league_id': league_id,
				'week': week,
				'week_end': week_end_date,
				'matchup': matchup,
				'manager1_name': manager1_name,
				'manager1_team': manager1_team,
				'manager1_id': manager1_id,
				'manager2_name': manager2_name,
				'manager2_team': manager2_team,
				'manager2_id': manager2_id,
				'team1_points': team1_points,
				'team1_projected': team1_projected,
				'team2_points': team2_points,
				'team2_projected': team2_projected,
				
				}
				
	
	data = pd.DataFrame(dict, columns=['year', 'league_id', 'week', 'week_end', 'matchup', 'manager1_name', 'manager1_team', 'manager1_id', 
		                                 'manager2_name', 'manager2_team', 'manager2_id', 'team1_points', 'team1_projected', 'team2_points', 
		                                 'team2_projected'])	
	pd.DataFrame.to_sql(data, 'scoreboard', conn, if_exists='replace', index=None)							
	conn.commit()		


	##############################
	#CREATE SCOREBOARD DB FOR EX LEAGUE
	##############################

	year=[]
	league_id=[]
	week = []
	week_end_date = []
	matchup = []
	manager1_name = []
	manager1_team = []
	manager1_id=[]
	player_id = []
	manager2_name = []
	manager2_team = []
	manager2_id=[]
	team1_points =[]
	team1_projected = []
	team2_points =[]
	team2_projected=[]
	playoffs=[]

	x=get_league_ids_ex()

	for i in x:
		try:
			print i
			get_scoreboard(i)
		except:
			pass

	dict = {
				 
				'year': year,
				'league_id': league_id,
				'week': week,
				'week_end': week_end_date,
				'matchup': matchup,
				'manager1_name': manager1_name,
				'manager1_team': manager1_team,
				'manager1_id': manager1_id,
				'manager2_name': manager2_name,
				'manager2_team': manager2_team,
				'manager2_id': manager2_id,
				'team1_points': team1_points,
				'team1_projected': team1_projected,
				'team2_points': team2_points,
				'team2_projected': team2_projected,
				
				}


	data = pd.DataFrame(dict, columns=['year', 'league_id', 'week', 'week_end', 'matchup', 'manager1_name', 'manager1_team', 'manager1_id', 
		                                 'manager2_name', 'manager2_team', 'manager2_id', 'team1_points', 'team1_projected', 'team2_points', 
		                                 'team2_projected'])	
	pd.DataFrame.to_sql(data, 'scoreboard_ex', conn, if_exists='replace', index=None)							
	conn.commit()
		
#13 weeks * 7 matchups/week + 1 week * 6 matchups + 2 weeks * 4 matchups= 106 total matchups...should be 106 rows in dataframe
#data[0]['scoreboard']['matchups']['matchup'][0]['teams']['team'][0]['name']  #gets 1st teamname of 1st matchup in week1
