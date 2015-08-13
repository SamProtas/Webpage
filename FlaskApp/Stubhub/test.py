import urllib, urllib2, json, requests, base64, ast, sqlite3, os


def createfile(openclose='read'):

 	f=open('passwords.txt', 'w') 
	f.write("{'consumer_key': 'Dlh8271RPXmMX6Wyh2l6ZT_Rd2Ua', 'consumer_secret': 'RzZ7hv3QerH5IZ1MxLP4RvFiyxUa', \
		      'userid': '6C21FFC12D823BC0E04400144FB7AAA6', 'access_token': '716be510a6ae1cf6d93e3d568c7493', \
		     'refresh_token': 'bb010be84467c1d476c29bc2dd9804a', 'Authorization': 'Basic RGxoODI3MVJQWG1NWDZXeWgybDZaVF9SZDJVYTpSelo3aHYzUWVySDVJWjFNeExQNFJ2Rml5eFVh'}")
	
	if openclose == 'read':
		return open('passwords.txt', 'r')

	else:
		f.close()	

def rewritefile(access_token, refresh_token):
	d = {'consumer_key': 'Dlh8271RPXmMX6Wyh2l6ZT_Rd2Ua', 'consumer_secret': 'RzZ7hv3QerH5IZ1MxLP4RvFiyxUa', \
			       'userid': '6C21FFC12D823BC0E04400144FB7AAA6', 'access_token': access_token, \
			        'refresh_token': refresh_token, 'Authorization': 'Basic RGxoODI3MVJQWG1NWDZXeWgybDZaVF9SZDJVYTpSelo3aHYzUWVySDVJWjFNeExQNFJ2Rml5eFVh'}
	d=json.dumps(d)
	f=open('passwords.txt', 'w')
	f.write(d)
	print "txt file written to directory"
	f.close()


def originalaccess():
	# DECLARE APPLICATION LOGIN PASSWORDS & CONCATENATE
	consumer_key = 'Dlh8271RPXmMX6Wyh2l6ZT_Rd2Ua'
	consumer_secret = 'RzZ7hv3QerH5IZ1MxLP4RvFiyxUa'
	concat = consumer_key + ":" + consumer_secret
	encoded = base64.b64encode(concat)  # CREATE AUTHORIZATION W/ BASE64
	auth = 'Basic ' + encoded

	login='https://api.stubhub.com/login'
	headers = {'Content-Type': "application/x-www-form-urlencoded",
				'Authorization': auth}
	payload = { 'grant_type': 'password', 
			'username': 'sharkstix2013@gmail.com',
			'password': 'trIbe19t',
			'scope': 'PRODUCTION'}
	
	r=requests.post(login, data=payload, headers=headers)
	if r.status_code == requests.codes.ok:
		print "connection made"
		
		response= json.loads(r.text)
		access_token = response['access_token']
		refresh_token = response['refresh_token']
		rewritefile(access_token, refresh_token) #store access_token, refresh_token
	else:
		print "can not connect because ", sys.exc_info()[0]
	
def updateaccesskeys():
	try:
		f=open('passwords.txt', 'r')
	except:
		f= createfile()

	text = f.read()
	d = ast.literal_eval(text)

	login='https://api.stubhub.com/login'
	headers = {'Content-Type': "application/x-www-form-urlencoded", 'Authorization': d['Authorization']}
	payload = { 'grant_type': 'password','username': 'sharkstix2013@gmail.com',
			'password': 'trIbe19t', 'scope': 'PRODUCTION'}
	#test connection		
	r=requests.post(login, data=payload, headers=headers)
	if r.status_code == requests.codes.ok:
		print "connection made, no refresh necessary for access token"
	#if connection is bad due to expiration, refresh tokens and rewrite txt file
	else: 
		print "attempting to refresh access token"
		headers = {'Content-Type': "application/x-www-form-urlencoded", 'Authorization': d['Authorization']}
		payload = { 'grant_type': 'refresh_token','refresh_token': d['refresh_token'],
				   'password': 'trIbe19t', 'scope': 'PRODUCTION'}
		r=requests.post(login, data=payload, headers=headers)
		if r.status_code == requests.codes.ok:
			response= json.loads(r.text)
			access_token = response['access_token']
			refresh_token = response['refresh_token']
			print "connection made, rewriting text files for new access & refresh keys"
			rewritefile(access_token, refresh_token)

		else:
			
			print "failed to refresh access token using headers:  " + headers + "and payload:  " + payload 
			print "attempting to get access via POST " 
			originalaccess()
			#original code to get access tokens


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
	response = urllib2.urlopen(req)
	data = json.load(response) 
	data = data['sales']['sale']
	length = len(data)
	table = 'wild_sales'





if __name__ == "__main__":

	updateaccesskeys()
