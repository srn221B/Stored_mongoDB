import datetime
import json
import pymongo
import requests_oauthlib
import tqdm

# API key
consumer_key = ''
consumer_secret = ''
access_token_key = ''
access_token_secret = ''

# Twitter Streaming API
twitter = requests_oauthlib.OAuth1Session(
	consumer_key, consumer_secret, access_token_key, access_token_secret)
uri = 'http://stream.twitter.com/1.1/statuses/sample.json'
r = twitter.get(uri, stream=True)
r.raise_for_status()

# Stored in mongoDB
mongo = pymongo.MongoClient()
for line in tqdm.tqdm(r.iter_lines(), unit='tweets', mininterval=1):
	if line:
		tweet = json.loads(line)
		tweet['_timestamp'] = datetime.datetime.utcnow().isoformat()
		mongo.twitter.sample.insert_one(tweet)
