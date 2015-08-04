import os, sqlite3, datetime, pandas as pd, numpy as np  #import authentification libraries and dataframe libraries

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

################################################################################
#BEGIN QUERIES
################################################################################

def projections_vs_totals_win_rate_all():
	
	x = (pd.read_sql("SELECT COUNT(*) AS total FROM (SELECT * from scoreboard UNION ALL SELECT * FROM scoreboard_ex) WHERE team1_points>0", conn))['total'][0]

	
	y= (pd.read_sql("SELECT COUNT(*) AS total from (SELECT * from scoreboard UNION ALL SELECT * from scoreboard_ex)\
    				WHERE team1_projected > team2_projected AND team1_points > team2_points\
    				OR (team2_projected > team1_projected AND team2_points > team1_points)\
    				AND team1_points>0", conn))['total'][0]
	print x 
	print y

	rate_win = float(y)/float(x)
	rate_lose = float(1-rate_win)
	
	print round(rate_win, 2), round(rate_lose,2)


def projections_vs_totals_win_rate_greater_than_20():
	
	
	x = (pd.read_sql ( "SELECT COUNT(*) AS total FROM \
		(\
	SELECT * from scoreboard WHERE (team1_projected - team2_projected >20) OR (team2_projected - team1_projected >20) \
	UNION ALL \
	SELECT * from scoreboard_ex WHERE (team1_projected - team2_projected >20) OR (team2_projected - team1_projected >20)\
    )", conn))['total'][0]


	y = (pd.read_sql ( "SELECT COUNT(*) AS total FROM \
		(\
	SELECT * from scoreboard WHERE (team1_projected - team2_projected >20) AND ( team1_points > team2_points) \
	UNION ALL \
	SELECT * from scoreboard WHERE (team2_projected - team1_projected >20) AND ( team2_points > team1_points) \
	UNION ALL \
	SELECT * from scoreboard_ex WHERE (team1_projected - team2_projected >20) AND ( team1_points > team2_points)\
	UNION ALL \
	SELECT * from scoreboard_ex WHERE (team2_projected - team1_projected >20) AND ( team2_points > team1_points)\
    )", conn))['total'][0]

	
	rate_win = float(y)/float(x)
	rate_lose = float(1-rate_win)
	
	return round(rate_win, 2), round(rate_lose,2)


def projections_vs_totals_win_rate_greater_than_10():
	
	
	x = (pd.read_sql ( "SELECT COUNT(*) AS total FROM \
		(\
	SELECT * from scoreboard WHERE (team1_projected - team2_projected >10) OR (team2_projected - team1_projected >10) \
	UNION ALL \
	SELECT * from scoreboard_ex WHERE (team1_projected - team2_projected >10) OR (team2_projected - team1_projected >10)\
    )", conn))['total'][0]


	y = (pd.read_sql ( "SELECT COUNT(*) AS total FROM \
		(\
	SELECT * from scoreboard WHERE (team1_projected - team2_projected >10) AND ( team1_points > team2_points) \
	UNION ALL \
	SELECT * from scoreboard WHERE (team2_projected - team1_projected >10) AND ( team2_points > team1_points) \
	UNION ALL \
	SELECT * from scoreboard_ex WHERE (team1_projected - team2_projected >10) AND ( team1_points > team2_points)\
	UNION ALL \
	SELECT * from scoreboard_ex WHERE (team2_projected - team1_projected >10) AND ( team2_points > team1_points)\
    )", conn))['total'][0]

	
	rate_win = float(y)/float(x)
	rate_lose = float(1-rate_win)
	
	return round(rate_win, 2), round(rate_lose,2)



def projections_vs_totals_win_rate_greater_than_5():
	
	
	x = (pd.read_sql ( "SELECT COUNT(*) AS total FROM \
		(\
	SELECT * from scoreboard WHERE (team1_projected - team2_projected >5) OR (team2_projected - team1_projected >5) \
	UNION ALL \
	SELECT * from scoreboard_ex WHERE (team1_projected - team2_projected >5) OR (team2_projected - team1_projected >5)\
    )", conn))['total'][0]

	print x

	y = (pd.read_sql ( "SELECT COUNT(*) AS total FROM \
		(\
	SELECT * from scoreboard WHERE (team1_projected - team2_projected >5) AND ( team1_points > team2_points) \
	UNION ALL \
	SELECT * from scoreboard WHERE (team2_projected - team1_projected >5) AND ( team2_points > team1_points) \
	UNION ALL \
	SELECT * from scoreboard_ex WHERE (team1_projected - team2_projected >5) AND ( team1_points > team2_points)\
	UNION ALL \
	SELECT * from scoreboard_ex WHERE (team2_projected - team1_projected >5) AND ( team2_points > team1_points)\
    )", conn))['total'][0]

	print y

	rate_win = float(y)/float(x)
	rate_lose = float(1-rate_win)
	
	print round(rate_win, 2), round(rate_lose,2)

def projections_vs_totals_win_rate_greater_than_30():
	 
	
	x = (pd.read_sql ( "SELECT COUNT(*) AS total FROM \
		(\
	SELECT * from scoreboard WHERE (team1_projected - team2_projected >30) OR (team2_projected - team1_projected >30) \
	UNION ALL \
	SELECT * from scoreboard_ex WHERE (team1_projected - team2_projected >30) OR (team2_projected - team1_projected >30)\
    )", conn))['total'][0]


	y = (pd.read_sql ( "SELECT COUNT(*) AS total FROM \
		(\
	SELECT * from scoreboard WHERE (team1_projected - team2_projected >30) AND ( team1_points > team2_points) \
	UNION ALL \
	SELECT * from scoreboard WHERE (team2_projected - team1_projected >30) AND ( team2_points > team1_points) \
	UNION ALL \
	SELECT * from scoreboard_ex WHERE (team1_projected - team2_projected >30) AND ( team1_points > team2_points)\
	UNION ALL \
	SELECT * from scoreboard_ex WHERE (team2_projected - team1_projected >30) AND ( team2_points > team1_points)\
    )", conn))['total'][0]

	
	rate_win = float(y)/float(x)
	rate_lose = float(1-rate_win)
	print rate_win	
	return round(rate_win, 2), round(rate_lose,2)





#############################
if __name__ == "__main__":
	projections_vs_totals_win_rate_all()
	projections_vs_totals_win_rate_greater_than_5()
#############################

