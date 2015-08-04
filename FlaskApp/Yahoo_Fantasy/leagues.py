import os, sqlite3, pandas as pd  #import authentification libraries and dataframe libraries


#create path to database
PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
DATABASE_SCOREBOARD = os.path.join(PROJECT_ROOT, 'data', 'fantasy_football.db')
#connect to database
conn = sqlite3.connect(DATABASE_SCOREBOARD)
c = conn.cursor()

data_lm = pd.read_sql("SELECT * from leagues WHERE type='LM' GROUP BY year", conn)
data_ex = pd.read_sql("SELECT * from leagues WHERE type='EX' GROUP BY year", conn)

def get_league_ids_lm():
	concat_lm=[]
	for i in range(len(data_lm)):
		concat_lm.append( '"' + data_lm['sport_id'][i] + ".l." + data_lm['league_id'][i] + '"')
	return concat_lm


def get_league_ids_ex():
	concat_ex=[]
	for i in range(len(data_ex)): 
		concat_ex.append( '"' + data_ex['sport_id'][i] + ".l." + data_ex['league_id'][i] + '"')
	return concat_ex 


