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


#FIND LIST OF SEASONS TO DATE AND CORRESPONDING YAHOO DEVELOPER CODES
####################
years_lm = (pd.read_sql("SELECT year FROM leagues WHERE type='LM' ORDER BY year DESC", conn)['year']).tolist()
years_ex = (pd.read_sql("SELECT year FROM leagues WHERE type='EX' ORDER BY year DESC", conn)['year']).tolist()


#QUERY LM LEAGES FOR VARIOUS STATISTICS 
####################
total_points_by_year = (pd.read_sql("SELECT SUM(points_for) AS points, year FROM standings GROUP BY year ORDER BY year DESC", conn))['points'] 
avg_points_by_year = (pd.read_sql("SELECT AVG(points_for) AS points, year  FROM standings GROUP BY year ORDER BY year DESC", conn))['points'] #first entry is year 2014 and so on

points_by_manager_list_dfs = [] #create a list of dataframes for each year
for i in years_lm:
	query = ("SELECT DISTINCT N.`manager_name`, D.`points_for`, Y.`year`\
	    FROM `standings` Y LEFT JOIN (SELECT DISTINCT `manager_name` FROM `standings`) N ON 1=1\
	    LEFT JOIN `standings` D ON  D.`year` = Y.`year` AND D.`manager_name` = N.`manager_name`\
	    WHERE Y.`year` = %s ORDER BY N.`manager_name`" %i) 
	#this query returns all names and points scored for each year regardless of whether that name was in the league that year
	#each dataframe is for a different year, alphabetical order by name  
	df=pd.read_sql(query, conn)
	#df=df.fillna(0)
	points_by_manager_list_dfs.append(df) #first dataframe in list is most recent year and so on


totals_lm = (pd.read_sql("SELECT SUM(points_for) AS points_for, SUM(points_against) AS points_against,\
							  SUM(num_moves) AS moves, SUM(num_trades) AS trades, SUM(wins) AS wins,\
							  SUM(losses) AS losses, SUM(clinched_playoffs) AS playoffs, manager_name FROM standings GROUP BY manager_name", conn))

averages_lm = (pd.read_sql("SELECT AVG(points_for) AS points_for, AVG(points_against) AS points_against, \
						  AVG(num_moves) AS moves, AVG(num_trades) AS trades, AVG(wins) AS wins, AVG(losses) AS losses, \
						  manager_name FROM standings WHERE curweek > 14 GROUP BY manager_name", conn))

seasons_played = (pd.read_sql("SELECT COUNT(*) AS seasons, manager_name FROM standings WHERE curweek > 14 GROUP BY manager_name", conn))

draft_position_lm = (pd.read_sql("SELECT draft_LM.year, manager_name, AVG(pick) AS pick FROM standings JOIN draft_LM ON standings.manager_id = \
					draft_LM.team_id AND standings.year = draft_LM.year WHERE curweek !=1 GROUP BY manager_name", conn))
avg_place_by_draft = (pd.read_sql("SELECT AVG(place) AS avg_place, pick FROM standings \
					JOIN draft_LM ON standings.manager_id = draft_LM.team_id WHERE curweek > 15 GROUP BY draft_LM.pick", conn))
avg_points_by_draft = (pd.read_sql("SELECT AVG(points_for) AS avg_points, pick FROM standings \
					JOIN draft_LM ON standings.manager_id = draft_LM.team_id WHERE curweek >15 GROUP BY draft_LM.pick", conn))

draft_vs_place = []
for i in years_lm:

	query = ("SELECT draft_lm.year, manager_name, manager_team, pick, place FROM standings \
							 JOIN draft_lm ON standings.manager_id = draft_lm.team_id AND standings.year = draft_lm.year \
							 WHERE draft_lm.year = %s AND curweek >14 GROUP BY manager_team" % i) 
	df = pd.read_sql(query, conn)
	draft_vs_place.append(df)
draft_vs_place = pd.concat(draft_vs_place)





#QUERY EX LEAGES FOR VARIOUS STATISTICS 
####################
total_points_by_year_ex = (pd.read_sql("SELECT SUM(points_for) AS points, year FROM standings_ex GROUP BY year ORDER BY year DESC", conn))['points'] 
avg_points_by_year_ex = (pd.read_sql("SELECT AVG(points_for) AS points, year  FROM standings_ex GROUP BY year ORDER BY year DESC", conn))['points'] #first entry is year 2014 and so on

totals_ex = (pd.read_sql("SELECT SUM(points_for) AS points_for, SUM(points_against) AS points_against,\
							  SUM(num_moves) AS moves, SUM(num_trades) AS trades, SUM(wins) AS wins,\
							  SUM(losses) AS losses, SUM(clinched_playoffs) AS playoffs, manager_name FROM standings_ex GROUP BY manager_name", conn))

averages_ex = (pd.read_sql("SELECT AVG(points_for) AS points_for, AVG(points_against) AS points_against, \
						  AVG(num_moves) AS moves, AVG(num_trades) AS trades, AVG(wins) AS wins, AVG(losses) AS losses, \
						  manager_name FROM standings_ex WHERE curweek > 14 GROUP BY manager_name", conn))

points_by_manager_list_dfs_ex = [] #create a list of dataframes for each year
for i in years_ex:
	query = ("SELECT DISTINCT N.`manager_name`, D.`points_for`, Y.`year`\
	    FROM `standings_ex` Y LEFT JOIN (SELECT DISTINCT `manager_name` FROM `standings_ex`) N ON 1=1\
	    LEFT JOIN `standings_ex` D ON  D.`year` = Y.`year` AND D.`manager_name` = N.`manager_name`\
	    WHERE Y.`year` = %s ORDER BY N.`manager_name`" %i) 
	#this query returns all names and points scored for each year regardless of whether that name was in the league that year
	#each dataframe is for a different year, alphabetical order by name  
	df=pd.read_sql(query, conn)
	points_by_manager_list_dfs_ex.append(df) #first dataframe in list is most recent year and so on

seasons_played_ex = (pd.read_sql("SELECT COUNT(*) AS seasons, manager_name FROM standings_ex WHERE curweek >14 GROUP BY manager_name", conn))


draft_position_ex = (pd.read_sql("SELECT draft_EX.year, manager_name, AVG(pick) AS pick FROM standings_ex JOIN draft_EX ON standings_ex.manager_id = \
					draft_EX.team_id AND standings_ex.year = draft_EX.year WHERE curweek !=1 GROUP BY manager_name", conn))

avg_place_by_draft_ex = (pd.read_sql("SELECT AVG(place) AS avg_place, pick FROM standings_ex \
					JOIN draft_EX ON standings_ex.manager_id = draft_EX.team_id WHERE curweek >15 GROUP BY draft_EX.pick", conn))
avg_points_by_draft_ex = (pd.read_sql("SELECT AVG(points_for) AS avg_points, pick FROM standings_ex \
					JOIN draft_EX ON standings_ex.manager_id = draft_EX.team_id WHERE curweek >15 GROUP BY draft_EX.pick", conn))

draft_vs_place_ex = []

for i in years_ex:

	query = ("SELECT draft_EX.year, manager_name, manager_team, pick, place FROM standings_ex \
							 JOIN draft_EX ON standings_ex.manager_id = draft_EX.team_id AND standings_ex.year = draft_EX.year \
							 WHERE draft_EX.year = %s AND  curweek >14 GROUP BY manager_team" % i) 
	df = pd.read_sql(query, conn)
	draft_vs_place_ex.append(df)
draft_vs_place_ex = pd.concat(draft_vs_place_ex)

#######################################################################################################################################
#END QUERIES
#######################################################################################################################################

############################################################
#POINTS ABOVE AVERAGE FUNCTIONS FOR BOTH LEAGUES
############################################################

def points_above_average_LM():
	global points_by_manager_list_dfs #4 dataframes in a list
	points_above_average_dicts_lm = []


	for i in range(len(points_by_manager_list_dfs)):  #for i in 1-length
		points=[]
		names=[]
		year=[]
		for j in range(len(points_by_manager_list_dfs[i])):

			points_check = (points_by_manager_list_dfs[i]['points_for'][j] - avg_points_by_year[i]) / (avg_points_by_year[i]) *100 #check to see if result is float or nan
			if np.isnan(points_check):  #if value is nan (because manager didnt play that year then return 0)
				points.append(0)
			else:
				points.append(points_check)
			
			names.append(points_by_manager_list_dfs[i]['manager_name'][j])
			year.append(points_by_manager_list_dfs[i]['year'][j])
			
		dict_return = { 
			'points': points,
			'names': names,
			'year': year
					}
		points_above_average_dicts_lm.append(dict_return)
	names = dict_return['names']
	return points_above_average_dicts_lm, names  #returns list of dataframes, most recent year being first in the list!

def points_above_average_EX():
	global points_by_manager_list_dfs_ex #4 dataframes in a list
	points_above_average_dicts_ex = []

	for i in range(len(points_by_manager_list_dfs_ex)):  #for i in 1-length
		points=[]
		names=[]
		year=[]
		for j in range(len(points_by_manager_list_dfs_ex[i])):

			points_check = (points_by_manager_list_dfs_ex[i]['points_for'][j] - avg_points_by_year_ex[i]) / (avg_points_by_year_ex[i]) *100 #check to see if result is float or nan
			if np.isnan(points_check):  #if value is nan (because manager didnt play that year then return 0)
				points.append(0)
			else:
				points.append(points_check)
			
			names.append(points_by_manager_list_dfs_ex[i]['manager_name'][j])
			year.append(points_by_manager_list_dfs_ex[i]['year'][j])
			
		dict_return = { 
			'points': points,
			'names': names,
			'year': year
					}
		points_above_average_dicts_ex.append(dict_return)
	names = dict_return['names']
	return points_above_average_dicts_ex, names  #returns list of dataframes, most recent year being first in the list!

############################################################
#COUNTING STATS FUNCTIONS FOR BOTH LEAGUES
############################################################

def averages_LM():
	global averages_lm
	return averages_lm

def draft_pos_LM():
	global draft_position_lm
	return draft_position_lm

def counting_stats_LM():
	global totals_lm
	
	return totals_lm
	

def averages_EX():
	global averages_ex
	return averages_ex

def draft_pos_EX():
	global draft_position_ex
	return draft_position_ex

def counting_stats_EX():
	global totals_ex
	return totals_ex
	
############################################################
#DRAFT PICK ANALYITIC FUNCTIONS FOR BOTH LEAGUES
############################################################
def pick_vs_place_LM():
	global draft_vs_place 
	return draft_vs_place

def points_vs_pick_LM():
	global avg_points_by_draft
	global avg_place_by_draft

	return ( avg_points_by_draft['avg_points'].tolist(), avg_points_by_draft['pick'].tolist(), 
			avg_place_by_draft['avg_place'].tolist(), avg_place_by_draft['pick'].tolist() )

def pick_vs_place_ex():
	global draft_vs_place_ex 
	return draft_vs_place_ex

def points_vs_pick_ex():
	global avg_points_by_draft_ex
	global avg_place_by_draft_ex

	return ( avg_points_by_draft_ex['avg_points'].tolist(), avg_points_by_draft_ex['pick'].tolist(), 
			avg_place_by_draft_ex['avg_place'].tolist(), avg_place_by_draft_ex['pick'].tolist() )

############################################################
#REGULAR SEASON WINNER & PLAYOFF CHAMPS
############################################################



# #############################
# if __name__ == "__main__":

# 	averages_EX()
#############################	