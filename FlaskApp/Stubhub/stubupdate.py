import urllib, urllib2, json, requests, base64, ast, sqlite3, os
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


def stubhubsales():
	
	try:
		f=open('passwords.txt', 'r')
	except:
		f = createfile()

	text = f.read()
	d = ast.literal_eval(text)

	url = 'https://api.stubhub.com/accountmanagement/sales/v1/seller/' + d['userid'] 
	key = 'Bearer ' + d['access_token']
	req = urllib2.Request(url)
	req.add_header('Authorization', key)
	req.add_header('Content-Type', "application/x-www-form-urlencoded")
	req.add_header('Accept', 'application/json')
	
	try:
		response = urllib2.urlopen(req)
		print "connected to sales information"
	except:
		print "connection failed", "trying to refresh tokens"
		updateaccesskeys()

	data = json.load(response) 
	data = data['sales']['sale']
	length = len(data)

	table = 'tickets'

	for i in range(length):
		listingId=data[i]['listingId']
		eventId=data[i]['eventId']
		event=data[i]['eventDescription']
		eventdate=data[i]['eventDate']
		eventdate=datetime.strptime(eventdate, '%Y-%m-%dT%H:%M:%S')
		#parse event text to find opponent
		char = event.find(' at ')
		if char == -1:
			opponent = event
		else:
			opponent=event[0:char]
		saleId=data[i]['saleId']
		saledate=data[i]['saleDate']
		saledate=datetime.strptime(saledate, '%Y-%m-%dT%H:%M:%S')
		sellersees=data[i]['pricePerTicket']['amount']
		quantity=data[i]['quantity']
		payout=2*(data[i]['payoutPerTicket']['amount'])
		row=data[i]['row']
		seat=data[i]['seats']
		section=data[i]['section']
		city = data[i]['city']
		state = data[i]['state']
		status = data[i]['status']


		c.execute("INSERT OR REPLACE INTO  {} (listingId,eventId,event,eventdate,opponent,saleId,saledate,sellersees,quantity,payout,row,seat,section,city,state, status)\
	            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);".format(table), (listingId,eventId,event,eventdate,opponent,saleId,saledate,\
	            	sellersees,quantity,payout,row,seat,section,city,state, status))
	
		conn.commit()
		


def stubhubselling():
	try:
		f=open('passwords.txt', 'r')
	except:
		f = createfile()

	text = f.read()
	d = ast.literal_eval(text)

	url = 'https://api.stubhub.com/accountmanagement/listings/v1/seller/' + d['userid'] 
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
	data = data['listings']['listing']
	length = len(data)

	table = 'tickets'

	for i in range(length):
		listingId=data[i]['id']
		eventId=data[i]['eventId']
		event=data[i]['eventDescription']
		eventdate=data[i]['eventDate']
		d=datetime.strptime(eventdate, '%Y-%m-%dT%H:%M:%S-%f')
		d = d.strftime('%Y-%m-%d %H:%M:%S')
		eventdate=datetime.strptime(d, '%Y-%m-%d %H:%M:%S')
		#parse event text to locate opponent
		char = event.find(' at ')
		if char == -1:
			opponent = event
		else:
			opponent=event[0:char]		

		sellersees=data[i]['pricePerTicket']['amount']
		buyersees = data[i]['displayPricePerTicket']['amount']
		quantity=data[i]['quantity']
		payout=2*(data[i]['payoutPerTicket']['amount'])
		row=data[i]['rows']
		seat=data[i]['seats']
		section=data[i]['section']
		city = data[i]['city']
		status = data[i]['status']
		

		c.execute("INSERT OR REPLACE INTO  {} (listingId,eventId,event,eventdate,opponent,sellersees,buyersees,quantity,payout,row,seat,section,city, status)\
	            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?, ?);".format(table), (listingId,eventId,event,eventdate,opponent,\
	            	sellersees,buyersees,quantity,payout,row,seat,section,city, status))

		conn.commit()
		
def findwildevent():
	
	pass

def posttickets(team):

	if team == 'wild':
		pass

	pass

def updatetickets(team):
#this is a test
	pass
		
if __name__ == "__main__":

	stubhubsales()
	stubhubselling()


