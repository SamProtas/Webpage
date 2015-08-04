import YOAuth  #import authentication function 
import yql, os, sqlite3, datetime, pandas as pd, numpy as np  #import authentification libraries and dataframe libraries
from yql.storage import FileTokenStore
from leagues import *

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
######################
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


#CREATE FUNCTION TO SIFT THROUGH QUERY AND GET DRAFT DATA FOR A GENERIC LEAGUE

def get_draft_results(league_number):

	query = "select * from fantasysports.draftresults where league_key=" + league_number
	data_yql=y3.execute(query, token=token)
	data = data_yql.rows

	data=data[0]
	add_or_not = int(data['current_week'])
	if not add_or_not == 1:
		for i in range(int(data['num_teams'])):
			year.append(int(data['season']))
			league_id.append(int(data['league_id']))
			pick.append(int(data['draft_results']['draft_result'][i]['pick']))
			try:
				team_id.append(int(data['draft_results']['draft_result'][i]['team_key'][-2:]))
			except:
				team_id.append(int(data['draft_results']['draft_result'][i]['team_key'][-1:]))




############################################################################################################
############################################################################################################


if __name__== "__main__":

	##############################
	#CREATE DRAFT DB FOR LM LEAGUE
	##############################

	#create empty lists to save data
	year=[]
	league_id=[]
	pick = []
	team_id = []

	x=get_league_ids_lm()

	for i in x:
		try:
			get_draft_results(i)
		except:
			pass	

	dict = {		 
					'year': year,
					'league_id': league_id,
					'pick': pick,
					'team_id': team_id,
					}

	data1 = pd.DataFrame(dict, columns=['year', 'league_id', 'pick', 'team_id'])
	pd.DataFrame.to_sql(data1, 'draft_LM', conn, if_exists='replace', index=None)	
							
	conn.commit()


	##############################
	#CREATE DRAFT DB FOR EX LEAGUE
	##############################

	#create empty lists to save data
	year=[]
	league_id=[]
	pick = []
	team_id = []

	y=get_league_ids_ex()

	for j in y:
		try:
			get_draft_results(j)
		except:
			pass	

	dict = {		 
					'year': year,
					'league_id': league_id,
					'pick': pick,
					'team_id': team_id,
					}

	data1 = pd.DataFrame(dict, columns=['year', 'league_id', 'pick', 'team_id'])
	pd.DataFrame.to_sql(data1, 'draft_EX', conn, if_exists='replace', index=None)	

	
#team, record, points for, points against, place, draft pick, qb_points for, wr_points for, RB_points for, kicker_points for...for each season
#text message to those who are performing well/poorly/close etc. during the season
