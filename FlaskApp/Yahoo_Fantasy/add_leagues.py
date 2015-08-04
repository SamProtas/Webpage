import time, sqlite3, os, pandas as pd, yql
from yql.storage import FileTokenStore

######################
#  DATABASE CONNECTION
######################
PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__)) #create path to database
DATABASE_SCOREBOARD = os.path.join(PROJECT_ROOT, 'data', 'fantasy_football.db')

conn = sqlite3.connect(DATABASE_SCOREBOARD) #connect to database
c = conn.cursor()
######################
# END DATAABASE 
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
	try:
		token = y3.check_token(stored_token)
		if token != stored_token:
			token_store.set('foo', token)
	except:
		print "sorry, you are not connected to the internet...terminating program"

###################
#END AUTHENTICATION
###################


print "Hey there..."
time.sleep(0.5)
print "Here are you current fantasy leagues"
time.sleep(0.5)
print ""

yes_no = raw_input("Do you want to add a new league?    ")

if (yes_no.lower())[0:2] == 'ye':
	
	for i in range(3):
		league_type = raw_input("Pleae specify whether it is EX or LM --->   ")

		if league_type.lower() == 'lm':
			sport_id = str(raw_input("Please enter fantasy football year ID...   "))
			league_id = str(raw_input("Pleaes enter league ID as shown in leagues settings...   "))
			year = int(raw_input("Pleaes enter the year of the league...   "))
			query = "select * from fantasysports.leagues.standings where league_key=" + "'" + sport_id + ".l." +league_id+"'"

			try:
				data_yql=y3.execute(query, token=token)
				data = data_yql.rows
				data=data[0] #ensures the query doesn't return a blank list and actually is a real league with data
				c.execute('INSERT INTO leagues VALUES (?, ?, ?, "LM")', [sport_id, league_id, year])
				conn.commit()
				print "Thank you for adding your new league..."
				time.sleep(0.5)
				print "The new EX leagues are now..."
				print pd.read_sql("SELECT * FROM leagues WHERE type='LM' GROUP BY year", conn)
				break

			except:
				print "sorry that league does not exist, please rerun the program"
				break		

		elif league_type.lower() == 'ex':
			sport_id = str(raw_input("Please enter fantasy football year ID...   "))
			league_id = str(raw_input("Pleaes enter league ID as shown in leagues settings...   "))
			year = int(raw_input("Pleaes enter the year of the league...   "))
			query = "select * from fantasysports.leagues.standings where league_key=" + "'" + sport_id + ".l." +league_id+"'"
			try:
				data_yql=y3.execute(query, token=token)
				data = data_yql.rows
				data=data[0]
				c.execute('INSERT INTO leagues VALUES (?, ?, ?, "EX")', [sport_id, league_id, year])
				conn.commit()

				print "Thank you for adding your new league..."
				time.sleep(.5)
				print "The new EX leagues are now..."
				print pd.read_sql("SELECT * FROM leagues WHERE type='EX' GROUP BY year", conn)

				break

			except: 
				print "sorry that league does not exist, please rerun the program"
				break	
		else:
			print "I'm sorry but that isn't an option, please try again..."
			break
else:
	print "Ok, come back when a new season starts"

