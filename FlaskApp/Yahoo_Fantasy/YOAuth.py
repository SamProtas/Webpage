import yql, os, datetime, pandas as pd, numpy as np  #import authentification libraries and dataframe libraries
from yql.storage import FileTokenStore

def OAuth():

	consumer_key = ('dj0yJmk9SGRrbkt5SHFSd2hVJmQ9WVdrOVJqUTRiMVZLTXpRbWNHbzlNQS0tJnM9Y29uc3VtZXJzZWNyZXQmeD1iNQ--')
	consumer_secret = ('3deb9f91d5086dec9c9dfe1ac8925eecb5741070')

	y3 = yql.ThreeLegged(consumer_key, consumer_secret)
	_cache_dir = os.path.expanduser('~/Desktop/FlaskApp/FlaskApp/Yahoo_Fantasy')

	if not os.access(_cache_dir,os.R_OK):
		os.mkdir(_cache_dir)
	token_store = FileTokenStore(_cache_dir, secret=consumer_secret)

	stored_token = token_store.get('foo')

	if not stored_token:
		#get access token, visit website and grant yourself access to league information
		request_token, auth_url = y3.get_token_and_auth_url()
		print "Visit url %s and get a verifier string" % auth_url
		verifier = raw_input("Enter the code: ") 
		token = y3.get_access_token(request_token, verifier)
		token_store.set('foo', token)

	else:
		# Check access_token is within 1hour-old and if not refresh it and stash it
		token = y3.check_token(stored_token)
		if token != stored_token:
			token_store.set('foo', token)




if __name__== "__main__":
	OAuth()


