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

years_lm = (pd.read_sql("SELECT year FROM leagues_curweek WHERE type='LM' AND curweek>15 ORDER BY year DESC", conn)['year']).tolist()
years_ex = (pd.read_sql("SELECT year FROM leagues_curweek WHERE type='EX' AND curweek>15 ORDER BY year DESC", conn)['year']).tolist()

managers_lm = (pd.read_sql("SELECT DISTINCT manager_name FROM standings", conn)['manager_name']).tolist()
managers_ex = (pd.read_sql("SELECT DISTINCT manager_name FROM standings_ex", conn)['manager_name']).tolist()
weekly_winners = (pd.read_sql("SELECT manager, earnings, week, year, type FROM weekly_winners", conn))
yearly_winners = (pd.read_sql("SELECT manager, earnings, type FROM yearly_winners", conn))
regseason_winners = (pd.read_sql("SELECT manager, earnings, type FROM yearly_winners_regseason", conn))
mostpoints_winners = pd.read_sql("SELECT manager, earnings, type FROM mostpoints_winners", conn)
yearly_buyin = pd.read_sql("SELECT manager, buyin, type FROM yearly_buyin", conn)


########################################################################################################################
####		START QUERIES
########################################################################################################################
data_of_champions_lm=[]; data_of_regseason_lm=[]
for i in years_lm:
	c.execute("SELECT manager_name, manager_team, wins, losses, year FROM standings WHERE year = %s AND place=1" %i)
	row = c.fetchone()
	data_of_champions_lm.append(row)
	c.execute("SELECT manager_name, manager_team, wins, losses, year FROM standings WHERE year = %s ORDER BY wins DESC, points_for DESC LIMIT 1" %i)
	row2 = c.fetchone()
	data_of_regseason_lm.append(row2)

df_of_champions_lm = pd.DataFrame(data_of_champions_lm, columns = ['manager_name', 'manager_team', 'wins', 'losses', 'year'])	
df_of_regseason_lm = pd.DataFrame(data_of_regseason_lm, columns = ['manager_name', 'manager_team', 'wins', 'losses', 'year'])	

########################################################################################################################
data_of_champions_ex=[]; data_of_regseason_ex=[]
for i in years_ex:
	c.execute("SELECT manager_name, manager_team, wins, losses, year FROM standings_ex WHERE year = %s AND place=1" %i)
	row = c.fetchone()
	data_of_champions_ex.append(row)
	c.execute("SELECT manager_name, manager_team, wins, losses, year FROM standings_ex WHERE year = %s ORDER BY wins DESC, points_for DESC LIMIT 1" %i)
	row2 = c.fetchone()
	data_of_regseason_ex.append(row2)

df_of_champions_ex = pd.DataFrame(data_of_champions_ex, columns = ['manager_name', 'manager_team', 'wins', 'losses', 'year'])	
df_of_regseason_ex = pd.DataFrame(data_of_regseason_ex, columns = ['manager_name', 'manager_team', 'wins', 'losses', 'year'])	
########################################################################################################################



########################################################################################################################
####		END QUERIES
########################################################################################################################

#Build table with all managers for LM FOR EACH YEAR  SELECT DISTINCT MANAGERS, JOIN ON YEAR
#OR FOR EACH MANAGER HAVE A SCRIPT THAT CHECKS WHETHER THEY WON IN A YEAR, CAME IN 2nd, WON each week...etc
#and continually add/subtract money values...then build dictionary of these managers

def earnings_ex():
	
	managers=[];buyin=[];weekly=[];yearly=[];mostpoints=[];regseason=[]
	
	for i in managers_ex:
		managers.append(i)
		buyin.append( sum(yearly_buyin[(yearly_buyin.manager==i) & (yearly_buyin.type=='EX')]['buyin']) )
		weekly.append( sum(weekly_winners[(weekly_winners.manager==i) & (weekly_winners.type=='EX')]['earnings']) )
		yearly.append( sum(yearly_winners[(yearly_winners.manager==i) & (yearly_winners.type=='EX')]['earnings']) )
		mostpoints.append( sum(mostpoints_winners[(mostpoints_winners.manager==i) & (mostpoints_winners.type=='EX')]['earnings']) )
		regseason.append (sum(regseason_winners[(regseason_winners.manager==i) & (regseason_winners.type=='EX')]['earnings']))


	earnings = {
	    'manager': managers,
	    'buyin': buyin,
	    'weekly': weekly,
	    'yearly': yearly,
	    'regseason': regseason,
	    'mostpoints': mostpoints
	}

	return earnings

def earnings_lm():
	
	managers=[];buyin=[];weekly=[];yearly=[];mostpoints=[];regseason=[]
	
	for i in managers_lm:
		managers.append(i)
		buyin.append( sum(yearly_buyin[(yearly_buyin.manager==i) & (yearly_buyin.type=='LM')]['buyin']) )
		weekly.append( sum(weekly_winners[(weekly_winners.manager==i) & (weekly_winners.type=='LM')]['earnings']) )
		yearly.append( sum(yearly_winners[(yearly_winners.manager==i) & (yearly_winners.type=='LM')]['earnings']) )
		mostpoints.append( sum(mostpoints_winners[(mostpoints_winners.manager==i) & (mostpoints_winners.type=='LM')]['earnings']) )
		regseason.append (sum(regseason_winners[(regseason_winners.manager==i) & (regseason_winners.type=='LM')]['earnings']))

	earnings = {
	    'manager': managers,
	    'buyin': buyin,
	    'weekly': weekly,
	    'yearly': yearly,
	    'regseason': regseason,
	    'mostpoints': mostpoints
	}

	
	return earnings

############################################################
#REGULAR SEASON WINNER & PLAYOFF CHAMPS
############################################################

def champions_lm():
	global df_of_champions_lm
	global df_of_regseason_lm
	print df_of_champions_lm
	return df_of_champions_lm, df_of_regseason_lm

def champions_ex():	
	global df_of_champions_ex
	global df_of_regseason_ex
	return df_of_champions_ex,df_of_regseason_ex
	

#############################
if __name__ == "__main__":

	earnings_ex()
#############################	