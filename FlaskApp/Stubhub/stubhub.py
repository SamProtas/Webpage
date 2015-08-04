import urllib, urllib2, json, base64, pandas as pd, sqlite3, os
from datetime import datetime
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

userid= '6C21FFC12D823BC0E04400144FB7AAA6'
url = 'https://api.stubhub.com/accountmanagement/sales/v1/seller/' + userid 
# Authorization: Bearer {userToken}

key = 'Bearer 716be510a6ae1cf6d93e3d568c7493'
req = urllib2.Request(url)
req.add_header('Authorization', key)
req.add_header('Content-Type', "application/x-www-form-urlencoded")
req.add_header('Accept', 'application/json')

response = urllib2.urlopen(req)
data = json.load(response) 
data = data['sales']['sale']
length = len(data)
table = 'wild_sales'


for i in range(length):
	listingId=data[i]['listingId']
	eventId=data[i]['eventId']
	event=data[i]['eventDescription']
	eventdate=data[i]['eventDate']
	eventdate=datetime.strptime(eventdate, '%Y-%m-%dT%H:%M:%S')
	opponent=(data[i]['eventDescription'])#.find('at')
	saleId=data[i]['saleId']
	saledate=data[i]['saleDate']
	saledate=datetime.strptime(saledate, '%Y-%m-%dT%H:%M:%S')
	sellersees=data[i]['pricePerTicket']['amount']
	quantity=data[i]['quantity']
	payout=data[i]['payoutPerTicket']['amount']
	row=data[i]['row']
	seat=data[i]['seats']
	section=data[i]['section']
	city = data[i]['city']
	state = data[i]['state']

	c.execute("INSERT OR REPLACE INTO  {} (listingId,eventId,event,eventdate,opponent,saleId,saledate,sellersees,quantity,payout,row,seat,section,city,state)\
	            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);".format(table), (listingId,eventId,event,eventdate,opponent,saleId,saledate,\
	            	sellersees,quantity,payout,row,seat,section,city,state))
	
	conn.commit()


