import urllib2
import json
from datetime import datetime
import time
import sqlite3
import os

conn = sqlite3.connect('/var/www/FlaskApp/FlaskApp/data/HG.db')
c = conn.cursor()
client_id = 'e089f481b19f44f3b9a195a2e5ba7bc0'
url = 'https://api.instagram.com/v1/users/'


def followers(id, iters, pause):
	for i in range(iters):
		
		url = 'https://api.instagram.com/v1/users/' + id + '/?client_id=' + client_id
		data = json.load(urllib2.urlopen(url))
		data2 = data['data']
		counts = data2['counts']

		followers = counts['followed_by']
		posts = counts['media']
		day_of_posts = (datetime.now().strftime('%d'))
		month_of_posts = (datetime.now().strftime('%b'))
		year_of_posts = (datetime.now().strftime('%Y'))
		time_of_posts = (datetime.now().strftime('%H:%M:%S'))
	
		
		c.execute('INSERT INTO stats (Followers, Posts, Mon, Day, Year, Time) VALUES (?, ?, ?, ?, ?, ?)', [followers, posts, month_of_posts, day_of_posts, year_of_posts, time_of_posts ])
		conn.commit()
	

if __name__ == "__main__":
	
		followers('54500086', 1, 1800)

#id is the twitter handle ID
#pause variable is amt of time between pulling the data
#iter is how many loops to run before appending the data to the spreadsheet







	

	
