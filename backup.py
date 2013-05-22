#!/usr/bin/python

import json
import pytumblr
from pymongo import MongoClient

with open("config.json") as f:
    config = json.load(f)

blog = config['blog']
consumer_key = config['consumer_key']
consumer_secret = config['consumer_secret']
oauth_token = config['oauth_token']
oauth_token_secret = config['oauth_token_secret']

tumblrclient = pytumblr.TumblrRestClient(consumer_key,consumer_secret,oauth_token,oauth_token_secret)
mongoclient = MongoClient()

db = mongoclient.tumblr
posts = db.posts

likes = db.likes
result = json.loads(tumblrclient.likes())
likelimit = result['response']['liked_count']
i = 0
post_ids = []
options = {}
while i <= likelimit:
    options["offset"] = i
    result = json.loads(tumblrclient.likes(i))
    tumblrlikes = result['response']['liked_posts']
    post_ids.append(likes.insert(tumblrlikes))
    i += 20
    if i > postlimit:
    	print "Imported %d of %d posts." % (postlimit,postlimit)
    else:
        print "Imported %d of %d posts." % (i,postlimit)

posts = db.posts
result = json.loads(tumblrclient.posts(blog))
postlimit = result['response']['total_posts']
i = 0
post_ids = []
options = {}
while i <= postlimit:
    options["offset"] = i
    result = json.loads(tumblrclient.posts(blog,**options))
    tumblrposts = result['response']['posts']
    post_ids.append(posts.insert(tumblrposts))
    i += 20
    if i > postlimit:
    	print "Imported %d of %d posts." % (postlimit,postlimit)
    else:
        print "Imported %d of %d posts." % (i,postlimit)
