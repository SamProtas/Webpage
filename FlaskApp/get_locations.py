import urllib2
import json
import datetime
import pandas as pd
import numpy as np

client_id = 'e089f481b19f44f3b9a195a2e5ba7bc0'

#empty lists to append gathered information to
time_of_posts = []
captions = []
locations = []
latitudes = []
longitudes = []
likes = []
comments = []
next_max_id = ''


def get_locations(id, count, iters):
	global next_max_id	
	global time_of_posts
	global captions
	global locations
	global latitudes
	global longitudes
	global likes
	global comments
	
	
	for i in range(4):
	
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
				date_time = (datetime.datetime.fromtimestamp(int(time)).strftime('%Y-%m-%d %H:%M:%S'))
			except:
				date_time = 'None'
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
			
			try:
				latitude = info['location']['latitude']
				longitude = info['location']['longitude']
			except:
				latitude = 'None'
				longitude = 'None'
			latitudes.append(latitude)
			longitudes.append(longitude)

			#get amount of likes
			like = info['likes']['count']
			likes.append(like)

			#get amount of comments
			comment = info['comments']['count']
			comments.append(comment)
		
	dict = {
				 
				'Time_of_Post': time_of_posts,
				'Caption': captions,
				'Location': locations,
				'Latitude': latitudes,
				'Longitude': longitudes,
				'Likes': likes,
				'Comments': comments
			
				}

	return dict

def likes_locations():
	
	pass			
			
if __name__ == "__main__":

	get_locations('54500086', '20', 20)
	
