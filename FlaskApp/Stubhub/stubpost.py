import urllib, urllib2, json, requests, ast, sqlite3, os
from datetime import datetime
from stubconnect import *
######################
#  DATABASE CONNECTION
######################
PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__)) #makes the folder this file is stored in the root folder
DATABASE_SCOREBOARD = os.path.join(PROJECT_ROOT, 'data', 'stubhub.db') 
conn = sqlite3.connect(DATABASE_SCOREBOARD) #connect to database scoreboard lcoated in data folder
c = conn.cursor()
######################
# END DATABASE 
######################

# TEST CONNECTION
consumer_key = 'Dlh8271RPXmMX6Wyh2l6ZT_Rd2Ua'
consumer_secret = 'RzZ7hv3QerH5IZ1MxLP4RvFiyxUa'

connection = testaccess(consumer_key, consumer_secret)
if connection:
	pass
else:
	updateaccesskeys()


def findevents(team='wild'):
	try:
		f=open('passwords.txt', 'r')
	except:
		f = createfile()

	text = f.read()
	d = ast.literal_eval(text)
	url = 'https://api.stubhub.com/search/catolog/events/v2'

	key = 'Bearer ' + d['access_token']
	req = urllib2.Request(url)
	req.add_header('Authorization', key)
	req.add_header('Content-Type', "application/x-www-form-urlencoded")
	req.add_header('Accept', 'application/json')

	try:
		response = urllib2.urlopen(req)
		print "connected to listings information"
	except:
		print "connection failed", "trying to refresh tokens"
		updateaccesskeys()

	data = json.load(response)	
	title = minnesota wild - parking	
	pass

def posttickets(team='wild'):
	try:
		f=open('passwords.txt', 'r')
	except:
		f = createfile()

	text = f.read()
	d = ast.literal_eval(text)
	url = 'https://api.stubhub.com/inventory/listings/v1/'

	key = 'Bearer ' + d['access_token']
	req = urllib2.Request(url)
	req.add_header('Authorization', key)
	req.add_header('Content-Type', "application/x-www-form-urlencoded")
	req.add_header('Accept', 'application/json')

	try:
		response = urllib2.urlopen(req)
		print "connected to listings information"
	except:
		print "connection failed", "trying to refresh tokens"
		updateaccesskeys()	

	

def updatetickets(team='wild'):
	try:
		f=open('passwords.txt', 'r')
	except:
		f = createfile()

	listingid = findevents('wild')

	text = f.read()
	d = ast.literal_eval(text)
	url = 'https://api.stubhub.com/inventory/listings/v1/' + listingid

	key = 'Bearer ' + d['access_token']
	req = urllib2.Request(url)
	req.add_header('Authorization', key)
	req.add_header('Content-Type', "application/x-www-form-urlencoded")
	req.add_header('Accept', 'application/json')

	try:
		response = urllib2.urlopen(req)
		print "connected to listings information"
	except:
		print "connection failed", "trying to refresh tokens"
		updateaccesskeys()	


def newfunction():
	pass



