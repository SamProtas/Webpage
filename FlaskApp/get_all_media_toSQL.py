import urllib2
import json
import pandas as pd
import numpy as np
import datetime
import sqlite3
import os

#PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
#DATABASE_HG = os.path.join(PROJECT_ROOT, 'data', 'HG.db')

conn = sqlite3.connect('/var/www/FlaskApp/FlaskApp/data/HG.db')
c = conn.cursor()

client_id = 'e089f481b19f44f3b9a195a2e5ba7bc0'

#empty lists to append gathered information to
time_of_posts = []
captions = []
locations = []
likes = []
comments = []
latitudes = []
longitudes = []
next_max_id = ''

def followers(id, count, iters):
	global data
	global next_max_id	
	global time_of_posts
	global captions
	global locations
	global likes
	global comments
	global latitudes
	global longitudes
	
	while True:
	
		url = 'https://api.instagram.com/v1/users/' + id + '/media/recent?client_id=' + client_id + '&count=' + count + '&max_id=' + next_max_id	
		d = json.load(urllib2.urlopen(url))
		
		try:
			next_max_id = d['pagination']['next_max_id']
		except:
			break
			
		for i in range(iters):
		
			info=d['data'][i]    #digs into the main dictionary with all desired information
		
		
			#get unix timestamp of post and convert it to date/time
			try:
				time = info['caption']['created_time']
				date_time = (datetime.datetime.fromtimestamp(int(time)).strftime('%Y,%m-1,%d,%H,%M'))
				time_of_posts.append(date_time)
			
				#get caption
				try:
					caption = info['caption']['text']
					caption = caption.encode('ascii', 'ignore')
				except TypeError:
					caption = 'None'
				captions.append(caption)
				
				#get location, latitude, and longitude of post
				try:
					location = info['location']['name']
					location = location.encode('ascii', 'ignore')
				except KeyError:
					location = 'None'
				except TypeError:
					location = 'None'
				locations.append(location)

				#get amount of likes
				like = info['likes']['count']
				likes.append(like)

				#get amount of comments
				comment = info['comments']['count']
				comments.append(comment)

				try:
					latitude = info['location']['latitude']
					longitude = info['location']['longitude']
				except:
					latitude = 'None'
					longitude = 'None'
				latitudes.append(latitude)
				longitudes.append(longitude)
			
			except:
				None
	dict = {
			
			'Time_of_Post': time_of_posts,
			'Caption': captions,
			'Location': locations,
			'Likes': likes,
			'Comments': comments,
			'Latitudes': latitudes,
			'Longitudes': longitudes		
				}
	
	data = pd.DataFrame(dict, columns=['Time_of_Post', 'Caption', 'Location', 'Likes', 'Comments', 'Latitudes', 'Longitudes'])	

	pd.DataFrame.to_sql(data, 'allmedia', conn, if_exists='replace', index=None)	
							
	conn.commit()

												
if __name__ == "__main__":

	followers('54500086', '33', 33)
	
