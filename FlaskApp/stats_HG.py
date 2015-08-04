import urllib2
import json
import unicodedata
import datetime
import pandas as pd
from pandas.stats.api import ols
import numpy as np
import sqlite3
import os


def Followers_per_hour():
	#connect and retreive information from databases
	PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
	DATABASE = os.path.join(PROJECT_ROOT, 'data', 'HG.db')
	conn = sqlite3.connect(DATABASE)
	c = conn.cursor()
	data= pd.read_sql('SELECT * FROM stats ORDER BY id ASC', conn) 
	data2=pd.read_sql('SELECT * FROM allmedia',conn)

	#create the column of difference in followers per row
	Followers_per_hour = (data['Followers']-data['Followers'].shift(2)).tolist()
	length = len(Followers_per_hour)

	Followers = data['Followers'].tolist()

	Positive_Followers = len([i for i in Followers_per_hour if i>0])
	Nuetral_Followers = len([i for i in Followers_per_hour if i==0])
	Negative_Followers = len([i for i in Followers_per_hour if i<0])
	Positive_vs_Negative = (Positive_Followers, Nuetral_Followers, Negative_Followers)
	
	post_occurs = (data['Posts']-data['Posts'].shift(1)).tolist()

	Time_of_Post = (data2['Time_of_Post']).tolist()
	Likes = (data2['Likes']).tolist()
	yaxis=max(Likes)
	length_likes = len(Likes)

	conn.close()
	return Followers_per_hour, length, Followers, Positive_vs_Negative, Time_of_Post, Likes, length_likes, yaxis

def date_predict(prediction):
	#connect and retreive information from databases
	PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
	DATABASE = os.path.join(PROJECT_ROOT, 'data', 'HG.db')
	conn = sqlite3.connect(DATABASE)
	c = conn.cursor()
	data= pd.read_sql('SELECT * FROM stats', conn) 

	df_for_regression = data
	df_for_regression['index1']=df_for_regression.index
	res = ols(y=df_for_regression['Followers'], x=df_for_regression['index1'])
	r2 = res.r2
	slope = res.beta[0]
	intercept = res.beta[1]
	startdate = "11/15/2014"
	days = (prediction - intercept)/(slope*48)
	days = round( days ,2)
	enddate = pd.to_datetime(startdate) + pd.DateOffset(days=days)
	enddate = enddate.strftime('%b-%d-%Y')
	return enddate, r2


#def New_Post():
#	cols = ['Followers', 'Posts', 'Month', 'Day', 'Year', 'Time']
#	data = pd.read_csv('/users/jmc856/Desktop/HG_data_new.csv', sep=',', header=None, names=cols)

def total_added():

	#connect and retreive information from databases
	PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
	DATABASE = os.path.join(PROJECT_ROOT, 'data', 'HG.db')
	conn = sqlite3.connect(DATABASE)
	c = conn.cursor()
	data= pd.read_sql('SELECT * FROM stats', conn) 
	data2=pd.read_sql('SELECT * FROM allmedia',conn)
	


	followers_added_per_day = []
	day = []
	length=len(data['Followers'])-1
	i=0
	while i<(1000):
		x = data['Followers'][length-i] - data['Followers'][length-i-48]
		followers_added_per_day.append(x)
		y="{0}-{1}".format(data['Day'][length-i-48], data['Mon'][length-i-48])
		day.append(y)
		i=i+48
	length = len(followers_added_per_day)
	return followers_added_per_day, day, length
	

	followers_past_day = data['Followers'][length] - data['Followers'][length-48]
	followers_past_week = data['Followers'][length] - data['Followers'][length-48*7]
	followers_past_month = data['Followers'][length] - data['Followers'][length-48*30]
	return followers_past_day, followers_past_week, followers_past_month
	
def added_by_dayofweek():
	pass
	#PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
	#DATABASE = os.path.join(PROJECT_ROOT, 'data', 'HG.db')
	#conn = sqlite3.connect(DATABASE)
	#c = conn.cursor()
	#data= pd.read_sql('SELECT * FROM stats', conn) 

	#Followers_per_hour = (data['Followers'].sub(data['Followers'].shift(1), fill_value=0)

def post_by_long_lat():
	PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
	DATABASE = os.path.join(PROJECT_ROOT, 'data', 'HG.db')
	conn = sqlite3.connect(DATABASE)
	c = conn.cursor()
	data2=pd.read_sql('SELECT * FROM allmedia',conn)

	nyclikes=[]; philalikes=[]; dclikes=[]; calilikes=[]; otherlikes=[]; nonelikes=[]
	nyccomments=[]; philacomments=[]; dccomments=[]; calicomments=[]; othercomments=[]; nonecomments=[]
	nyc = 0; phila = 0; dc=0; cali=0; other=0;none=0

	for i in range(len(data2)):
		try:
			if 40.3 > float(data2['Latitudes'][i]) > 39.5 and -75.0 > float(data2['Longitudes'][i]) > -75.5:
				phila+=1; philalikes.append(data2['Likes'][i]); philacomments.append(data2['Comments'][i])
			elif 41.0 > float(data2['Latitudes'][i]) > 40.3 and -73.2 > float(data2['Longitudes'][i]) > -74.2:
				nyc+=1; nyclikes.append(data2['Likes'][i]); nyccomments.append(data2['Comments'][i])
			elif 40.1 > float(data2['Latitudes'][i]) > 38.2 and -76.0 > float(data2['Longitudes'][i]) > -77.7:
				dc+=1; dclikes.append(data2['Likes'][i]); dccomments.append(data2['Comments'][i])
			elif 39.0 > float(data2['Latitudes'][i]) > 36.0 and -118.0 > float(data2['Longitudes'][i]) > -125.0:
				cali+=1; calilikes.append(data2['Likes'][i]); calicomments.append(data2['Comments'][i]) 
			else:
				other+=1; otherlikes.append(data2['Likes'][i]); othercomments.append(data2['Comments'][i])
		except:
			none+=1; nonelikes.append(data2['Likes'][i]); nonecomments.append(data2['Comments'][i])	 	

	# data3=pd.read_sql('SELECT * FROM allmedia where Time_of_post >"2014,02-1,15,09,48"',conn)
	# nyc2 = 0; phila2 = 0; dc2=0; cali2=0; other2=0;none2=0
	# for i in range(len(data3)):
	# 	try:
	# 		if 40.3 > float(data2['Latitudes'][i]) > 39.5 and -75.0 > float(data2['Longitudes'][i]) > -75.5:
	# 			phila2+=1; philalikes.append(data2['Likes'][i])
	# 		elif 41.0 > float(data2['Latitudes'][i]) > 40.3 and -73.2 > float(data2['Longitudes'][i]) > -74.2:
	# 			nyc2+=1; nyclikes.append(data2['Likes'][i])
	# 		elif 40.1 > float(data2['Latitudes'][i]) > 38.2 and -76.0 > float(data2['Longitudes'][i]) > -77.7:
	# 			dc2+=1; dclikes.append(data2['Likes'][i])
	# 		elif 39.0 > float(data2['Latitudes'][i]) > 36.0 and -118.0 > float(data2['Longitudes'][i]) > -125.0:
	# 			cali2+=1 ; calilikes.append(data2['Likes'][i])
	# 		else:
	# 			other2+=1 ; otherlikes.append(data2['Likes'][i])
	# 	except:
	# 		none2+=1 ; nonelikes.append(data2['Likes'][i])

	
	
	

	###############   LIKE STATS PER CITY  ######################
	total_nyc=sum(nyclikes); nyc_lpp = sum(nyclikes)/nyc; max_nyc=max(nyclikes); min_nyc = min(nyclikes)
	total_phila=sum(philalikes); phila_lpp = sum(philalikes)/phila; max_phila=max(philalikes); min_phila=min(philalikes)
	total_dc=sum(dclikes); dc_lpp = sum(dclikes)/dc; max_dc= max(dclikes); min_dc=min(dclikes)
	total_cali = sum(calilikes); cali_lpp = sum(calilikes)/cali; max_cali=max(calilikes); min_cali=min(calilikes)
	total_other=sum(otherlikes); other_lpp = sum(otherlikes)/other; max_other = max(otherlikes); min_other = min(otherlikes)
	total_none=sum(nonelikes); none_lpp = sum(nonelikes)/none; max_none = max(nonelikes); min_none = min(nonelikes)

	###############   COMMENT STATS PER CITY  ######################
	total_nyc_com=sum(nyccomments); nyc_cpp = sum(nyccomments)/nyc; max_nyc_com=max(nyccomments); min_nyc_com = min(nyccomments)
	total_phila_com=sum(philacomments); phila_cpp = sum(philacomments)/phila; max_phila_com=max(philacomments); min_phila_com=min(philacomments)
	total_dc_com=sum(dccomments); dc_cpp = sum(dccomments)/dc; max_dc_com= max(dccomments); min_dc_com=min(dccomments)
	total_cali_com = sum(calicomments); cali_cpp = sum(calicomments)/cali; max_cali_com=max(calicomments); min_cali_com=min(calicomments)
	total_other_com=sum(othercomments); other_cpp = sum(othercomments)/other; max_other_com = max(othercomments); min_other_com = min(othercomments)
	total_none_com=sum(nonecomments); none_cpp = sum(nonecomments)/none; max_none_com = max(nonecomments); min_none_com = min(nonecomments)

	print nyc_lpp; print phila_lpp; print dc_lpp; print cali_lpp; print other_lpp; print none_lpp
	cities=('New York', 'Philadelphia', 'Washington DC', 'California', 'Other', 'Unknown', 'Totals')

	total_posts=(nyc,phila,dc,cali,other,none)
	total_likes=(total_nyc, total_phila, total_dc, total_cali, total_other, total_none, (total_nyc+total_phila+total_dc+total_cali+total_other+total_none))
	
	lpp = (nyc_lpp, phila_lpp, dc_lpp, cali_lpp, other_lpp, none_lpp)
	lpp_total=np.mean(lpp)
	lpp = (nyc_lpp, phila_lpp, dc_lpp, cali_lpp, other_lpp, none_lpp, lpp_total)
	
	max_likes = [max_nyc, max_phila, max_dc, max_cali, max_other, max_none]
	max_total = max(max_likes)
	max_likes = [max_nyc, max_phila, max_dc, max_cali, max_other, max_none, max_total]

	min_likes = (min_nyc, min_phila, min_dc, min_cali, min_other, min_none)
	min_total = min(min_likes)
	min_likes = (min_nyc, min_phila, min_dc, min_cali, min_other, min_none, min_total)

	
	total_com=(total_nyc_com, total_phila_com, total_dc_com, total_cali_com, total_other_com, total_none_com, (total_nyc_com+total_phila_com+total_dc_com+total_cali_com+total_other_com+total_none_com))

	cpp = (nyc_cpp, phila_cpp, dc_cpp, cali_cpp, other_cpp, none_cpp)
	cpp_total=np.mean(cpp)
	cpp = (nyc_cpp, phila_cpp, dc_cpp, cali_cpp, other_cpp, none_cpp, cpp_total)

	max_com = [max_nyc_com, max_phila_com, max_dc_com, max_cali_com, max_other_com, max_none_com]
	max_total_com = max(max_com)
	max_com = [max_nyc_com, max_phila_com, max_dc_com, max_cali_com, max_other_com, max_none_com, max_total_com]

	min_com = (min_nyc_com, min_phila_com, min_dc_com, min_cali_com, min_other_com, min_none_com)
	min_total_com = min(min_com)
	min_com = (min_nyc_com, min_phila_com, min_dc_com, min_cali_com, min_other_com, min_none_com, min_total_com)


	data=[cities, total_posts, total_likes, lpp, max_likes, min_likes, total_com, cpp, max_com, min_com]
	df=pd.DataFrame(data)
	df= df.transpose()
	df.columns=['Cities','Total_Posts','Total_Likes', 'Likes_Post', 'Max_Likes', 'Min_Likes','Total_Comments', 'Comments_Post', 'Max_Comments', 'Min_Comments' ]
	print df
	return df




def get_day_of_week(day):
	return str(day).strftime()


	example = data2.reset_index().values
	#if in single array format

	example1=[example[1][2], example[1][3], example[1][4]]
	example2 = (str(w) for w in example1)
	example2= ' '.join(example2)
	example3=datetime.datetime.strptime(example2, "%b %d %Y")
	example3.strftime("%A")  #this outputs the DAY in string format!!
	

if __name__ == "__main__":
	post_by_long_lat()
	


	
