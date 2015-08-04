import urllib2
import json
from datetime import datetime
import time
import pandas as pd
import numpy as np


client_id = 'e089f481b19f44f3b9a195a2e5ba7bc0'
url = 'https://api.instagram.com/v1/users/'

total_followers = []
total_posts = []
day_of_posts = []
month_of_posts = []
year_of_posts=[]
time_of_posts=[]

def followers(id, iters, pause):
	for i in range(iters):
		global total_followers
		global total_posts
		global day_of_posts
		global month_of_posts
		global year_of_posts
		global time_of_posts
		
		url = 'https://api.instagram.com/v1/users/' + id + '/?client_id=' + client_id
		data = json.load(urllib2.urlopen(url))
		data2 = data['data']
		counts = data2['counts']
		followers = counts['followed_by']
		posts = counts['media']
		total_followers.append(followers)
		total_posts.append(posts)
		day_of_posts.append(datetime.now().strftime('%d'))
		month_of_posts.append(datetime.now().strftime('%b'))
		year_of_posts.append(datetime.now().strftime('%Y'))
		time_of_posts.append(datetime.now().strftime('%H:%M:%S'))
		time.sleep(pause)
		
	
	dict = {
			'followers': total_followers, 'posts': total_posts, 'month': month_of_posts, 
			'day': day_of_posts, 'year': year_of_posts, 'time': time_of_posts
			}

	data = pd.DataFrame(dict, columns=['followers', 'posts', 'month', 'day', 'year', 'time'])
	
	csv_file = '/var/www/FlaskApp/FlaskApp/data/HG_data1.csv'
	data.to_csv(csv_file, mode='a', header=False)
	
	#clear all lists
	total_followers = []
	total_posts = []
	day_of_posts = []
	month_of_posts = []
	year_of_posts=[]
	time_of_posts=[]

if __name__ == "__main__":
	
	while True:
		followers('54500086', 1, 1800)

#id is the twitter handle ID
#pause variable is amt of time between pulling the data
#iter is how many loops to run before appending the data to the spreadsheet






	

	
