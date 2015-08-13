import sys, os, sqlite3, yql
from yql.storage import FileTokenStore 
import pandas as pd
from Send_Text import *
from send_text_test import *




######################
#  DATABASE CONNECTION
######################
PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__)) #makes the folder this file is stored in the root folder
DATABASE_SCOREBOARD = os.path.join(PROJECT_ROOT, 'data', 'fantasy_football.db') 
conn = sqlite3.connect(DATABASE_SCOREBOARD) #connect to database scoreboard lcoated in data folder
c = conn.cursor()
######################
# END DATABASE  
######################
##########################################################################################################################################################

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
##########################################################################################################################################################
##########################################################################################################################################################
##########################################################################################################################################################

def career_record(table, mobile, carrier, manager, opponent, week, i):
	#career record against that opponent#
	#Gets total career matchups (including playoffs)
	x = int(pd.read_sql("SELECT COUNT(*) AS total FROM %s WHERE (manager1_name = %s AND manager2_name = %s AND team1_points>0) OR (manager2_name = %s AND manager1_name = %s AND team1_points>0)" % (table, manager, opponent, manager, opponent), conn)['total'][0])
	#Gets total matchups won by manager
	y = int(pd.read_sql("SELECT COUNT(*) AS total FROM %s WHERE ((manager1_name = %s AND manager2_name = %s) AND team1_points > team2_points) OR ((manager2_name = %s AND manager1_name = %s) AND team2_points > team1_points)" % (table, manager, opponent, manager, opponent), conn)['total'][0])
	
	try: 
		career_winning_percentage = '{:.2%}'.format(float(y)/float(x))
	except ZeroDivisionError:
		career_winning_percentage = 0
	wins= str(y)
	losses = x-y
	losses = str(losses)
	message = "Goodmorning %s, today you play %s in fantasy football. Your career winning perc is %s with a record of %s - %s." %(manager, opponent, career_winning_percentage, wins, losses)
	#message = 'This is a test, you are receiving this b/c you are in Calverts Fantasy Football League'
	
	for ii in mobile:

		Send_Text_Test(ii, message, carrier)  #function to send text via gmail



def current_projections(mobile,carrier, week, manager, manager_projected, opponent, opponent_projected):

	difference = float(abs(manager_projected - opponent_projected)) #absolute difference in projections
	if manager_projected - opponent_projected > 0:  #labels binary variable a to show whether manager is favored
		is_favored = True
	else:
		is_favored = False

	c.execute("SELECT COUNT(*) AS total FROM projected_points WHERE projdiff > %s" %difference)
	x = c.fetchone()[0]

	y = (pd.read_sql ( "SELECT COUNT(*) AS total FROM \
		(\
	SELECT * from scoreboard WHERE (team1_projected - team2_projected >%s) AND ( team1_points > team2_points) \
	UNION ALL \
	SELECT * from scoreboard WHERE (team2_projected - team1_projected >%s) AND ( team2_points > team1_points) \
	UNION ALL \
	SELECT * from scoreboard_ex WHERE (team1_projected - team2_projected >%s) AND ( team1_points > team2_points)\
	UNION ALL \
	SELECT * from scoreboard_ex WHERE (team2_projected - team1_projected >%s) AND ( team2_points > team1_points)\
    )" %(difference, difference, difference, difference), conn))['total'][0]


	if is_favored:
		rate_win = '{:.2%}'.format(float(y)/float(x))
		message = "Historically in Calvert's fantasy leagues a player with a positive %s projected points differential wins %s of the time" %(difference, rate_win)
	else:
		rate_win = '{:.2%}'.format((float(1-(y)/float(x))))
		message = "Historically in Calvert's fantasy leagues a player with a negative %s projected points differential wins %s of the time" %(difference, rate_win)
	
	for ii in mobile:

		Send_Text_Test(ii, message, carrier)

	

def career_avg_points(league, manager, oppoenent, week):
	#career avg points in this week
	#career avg poitns against this opponent

	pass



##########################################################################################################################################################
##########################################################################################################################################################
##########################################################################################################################################################


if __name__ == "__main__":
	#get current year, leagueid, etc.
	league_data_lm = pd.read_sql("SELECT max(year) AS year, sport_id, league_id FROM leagues WHERE type = 'LM';", conn)
	league_data_ex = pd.read_sql("SELECT max(year) AS year, sport_id, league_id FROM leagues WHERE type = 'EX';", conn)

	year_lm = str((league_data_lm)['year'][0])
	sport_id_lm = str(league_data_lm['sport_id'][0])
	league_id_lm = str(league_data_lm['league_id'][0])

	year_ex = str((league_data_ex)['year'][0])
	sport_id_ex = str(league_data_ex['sport_id'][0])
	league_id_ex = str(league_data_ex['league_id'][0])

	current_managers_lm = pd.read_sql("SELECT manager_name AS managers FROM standings WHERE year = %s GROUP BY managers" %year_lm, conn)['managers'].tolist()
	current_managers_ex = pd.read_sql("SELECT manager_name AS managers FROM standings_ex WHERE year = %s GROUP BY managers" %year_ex, conn)['managers'].tolist()	

	query_lm = "select * from fantasysports.leagues.scoreboard where league_key='" + sport_id_lm + ".l." + league_id_lm + "' and week in (1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16)"
	query_ex = "select * from fantasysports.leagues.scoreboard where league_key='" + sport_id_ex + ".l." + league_id_ex + "' and week in (1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16)"

	data_yql_lm=y3.execute(query_lm, token=token)
	data_lm = data_yql_lm.rows
	current_week_lm = int(data_lm[0]['current_week'])

	data_yql_ex=y3.execute(query_ex, token=token)
	data_ex = data_yql_ex.rows
	current_week_ex = int(data_ex[0]['current_week'])
	
	
	for i in current_managers_lm:
		manager = "'" + i + "'"

		try:
			current_week_data_lm = pd.read_sql("SELECT manager1_name AS opponent, team1_projected AS opponent_projected, team2_projected AS manager_projected FROM scoreboard WHERE year = %s AND week = %s AND manager2_name = %s"  %(year_lm, current_week_lm, manager), conn)
			manager_opponent = current_week_data_lm['opponent'][0]
			opponent_projected = current_week_data_lm['opponent_projected'][0]
			manager_projected = current_week_data_lm['manager_projected'][0]
		except:
			try:
				current_week_data_lm = pd.read_sql("SELECT manager2_name AS opponent, team2_projected AS opponent_projected, team1_projected AS manager_projected FROM scoreboard WHERE year = %s AND week = %s AND manager1_name = %s"  %(year_lm, current_week_lm, manager), conn)
				manager_opponent = current_week_data_lm['opponent'][0]
				opponent_projected = current_week_data_lm['opponent_projected'][0]
				manager_projected = current_week_data_lm['manager_projected'][0]
			except:
				print "failed to find opponent for " + i + "in local database"
				print "skipping all processes for " + i
				continue
		
		manager_opponent = "'" + manager_opponent + "'"
		
		mobile = pd.read_sql("SELECT number FROM mobile WHERE nickname = %s AND type = 'LM'" %manager, conn)['number'].tolist()
		carrier = str(pd.read_sql("SELECT carrier FROM mobile WHERE nickname = %s" %manager, conn)['carrier'][0])
		table = 'scoreboard'

		#################### SEND TO FUNCTIONS #######################
		try:
			career_record(table, mobile, carrier, manager, manager_opponent, current_week_lm, i)
			print "corrctly ran analytics for manager " +i
		except:
			print "failed to send text message to " + i + " due to error in function career_record",  sys.exc_info()[0]
		try:	
			current_projections(mobile, carrier, current_week_lm, manager, manager_projected, manager_opponent, opponent_projected)
			print "corrctly ran analytics for manager " + i
		except:
			print "failed to send text message to " + i + " due to error in function current_projections", sys.exc_info()[0]
		#################### SEND TO FUNCTIONS #######################


	for i in current_managers_ex:
		manager = "'" + i + "'"

		try:
			current_week_data_ex = pd.read_sql("SELECT manager1_name AS opponent, team1_projected AS opponent_projected, team2_projected AS manager_projected FROM scoreboard_ex WHERE year = %s AND week = %s AND manager2_name = %s"  %(year_ex, current_week_ex, manager), conn)
			manager_opponent = current_week_data_ex['opponent'][0]
			opponent_projected = current_week_data_ex['opponent_projected'][0]
			manager_projected = current_week_data_ex['manager_projected'][0]
		except:
			try:
				current_week_data_ex = pd.read_sql("SELECT manager2_name AS opponent, team2_projected AS opponent_projected, team1_projected AS manager_projected FROM scoreboard_ex WHERE year = %s AND week = %s AND manager1_name = %s"  %(year_ex, current_week_ex, manager), conn)
				manager_opponent = current_week_data_ex['opponent'][0]
				opponent_projected = current_week_data_ex['opponent_projected'][0]
				manager_projected = current_week_data_ex['manager_projected'][0]
			except:
				print "failed to find opponent for " + i + "in local database"
				print "skipping all processes for " + i
				continue

		manager_opponent = "'" + manager_opponent + "'"
		
		mobile = pd.read_sql("SELECT number FROM mobile WHERE nickname = %s AND type = 'EX'" %manager, conn)['number'].tolist()
		carrier = str(pd.read_sql("SELECT carrier FROM mobile WHERE nickname = %s" %manager, conn)['carrier'][0])
		table = 'scoreboard_ex'

		
		#################### SEND TO FUNCTIONS #######################
		try:
			career_record(table, mobile, carrier, manager, manager_opponent, current_week_ex)
			print "corrctly ran analytics for manager " + i
		except:
			print "failed to send text message to " + i + " due to error in function career_record",   sys.exc_info()[0]
		try:
			current_projections(mobile,carrier, current_week_ex, manager, manager_projected, manager_opponent, opponent_projected)
			print "corrctly ran analytics for manager " + i
		except:
			print "failed to send text message to " + i + " due to error in function current_projections",  sys.exc_info()[0]
		#################### SEND TO FUNCTIONS #######################

		#CRONTAB runs this program every sunday 

