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

def get_standings_data(league_number, table):

	query = "select * from fantasysports.leagues.standings where league_key=" + league_number
	print query
	data_yql=y3.execute(query, token=token)
	data = data_yql.rows
	data_id=data[0]
	data=data[0]['standings']['teams']['team']  #step through to dictionary with 14 teams

	for i in range(len(data)):
		curweek=int(data_id['current_week'])
		year=int(data[i]['team_points']['season'])
		league_id=int(data_id['league_id'])
		manager_team=data[i]['name']
		manager_id=data[i]['team_id']
		points_for=float(data[i]['team_standings']['points_for'])
		points_against=float(data[i]['team_standings']['points_against'])
		num_moves=int(data[i]['number_of_moves'])
		num_trades=int(data[i]['number_of_trades'])
		wins=int(data[i]['team_standings']['outcome_totals']['wins'])
		losses=int(data[i]['team_standings']['outcome_totals']['losses'])
		try:
			clinched_playoffs=int(data[i]['clinched_playoffs'])
		except:
			clinched_playoffs=0
		if data[i]['team_standings']['rank'] != None:
			place = int(data[i]['team_standings']['rank'])
		else:
			place=0
		try:
			manager = (str(data[i]['managers']['manager']['nickname']))
		except:
			manager = (str(data[i]['managers']['manager'][0]['nickname']))   #if two managers exist just take the first one
		
		manager = modify_hidden_user(data[i]['name'], manager) #send to a function that searches for teams I know have hidden managers or duplicate nicknames, the file then gives the correct nickname mnaually		

		################		
		try:
			email = (str(data[i]['managers']['manager']['email']))
		except:
			try:
		 		email = (str(data[i]['managers']['manager'][0]['email']))
		 	except:
		 		email = 'Null'

		################	
		manager_name = modify_hidden_user_email(email, manager)
		#cur.execute("INSERT INTO {} VALUES(?, ?)".format(group), (food, 1))
		
		c.execute("INSERT OR REPLACE INTO {} (year,league_id,manager_name,manager_team,manager_id,points_for, points_against,\
				      num_moves,num_trades,wins,losses,clinched_playoffs,place,curweek) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?);".format(table),\
				      (year,league_id,manager_name,manager_team,manager_id,points_for,points_against,num_moves,num_trades,\
				       wins,losses,clinched_playoffs,place,curweek))
		conn.commit()
		
############################################################################################################
############################################################################################################


if __name__== "__main__":

	##############################
	#CREATE OR UPDATE STANDINGS DB FOR LM LEAGUE
	##############################

	#x=get_league_ids_lm()
	c.execute("SELECT max(year) AS year, sport_id, league_id FROM leagues WHERE type = 'LM';")
	x=c.fetchone()
	x= '"'+ x[1] + '.l.' + x[2] + '"'

	table = 'standings'
	
	print "checking updates for league " + x
	get_standings_data(x, table)
		
	##############################
	#CREATE OR UPDATE STANDINGS DB FOR EX LEAGUE
	##############################
	
	#y=get_league_ids_ex()
	c.execute("SELECT max(year) AS year, sport_id, league_id FROM leagues WHERE type = 'EX';")
	y=c.fetchone()
	print y
	y= '"'+ y[1] + '.l.' + y[2] + '"'
	
	table = 'standings_ex'
	
	print "checking updates for league " + y
	get_standings_data(y, table)
	
