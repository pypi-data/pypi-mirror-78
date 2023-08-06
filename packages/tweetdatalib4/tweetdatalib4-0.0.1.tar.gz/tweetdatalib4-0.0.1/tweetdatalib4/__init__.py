
"""
INPUTS:
    consumer_key, consumer_secret, access_token, access_token_secret: codes 
    telling twitter that we are authorized to access this data
    hashtag_phrase: the combination of hashtags to search for
OUTPUTS:
    none, simply save the tweet info to a spreadsheet
"""

def tweetsearch_for_hashtags(hashtag_phrase):
    consumer_key ="30GAxNeTfZuPL5SfNhFBodmRF"
    consumer_secret ="C6O64nP0XjtwaAnXYL9zCcDZKEIP2iL1yVdlsNJtwLiZ5AEEBs"
    access_token ="1246523558563471360-WrbCqO8phqjIzx393mrfOSKvDFPmey"
    access_token_secret ="u7B6yX6ZyTa5ph7xkCFnbzyuD9jbuHHJNL0Y4S7mdZb1J"
    hashtag_phrase =input('Hashtag Phrase ')
    #create authentication for accessing Twitter
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    #initialize Tweepy API
    api = tweepy.API(auth)
    
    #get the name of the spreadsheet we will write to
    fname = '_'.join(re.findall(r"#(\w+)", hashtag_phrase))

    #open the spreadsheet we will write to
    with open('%s.csv' % (fname), 'w',encoding='utf-8') as file:
       # lines = [x.decode('utf8').strip() for x in file.readlines()]

        w = csv.writer(file)

        #write header row to spreadsheet
        w.writerow(['timestamp', 'tweet_text', 'username', 'all_hashtags', 'followers_count'])

        #for each tweet matching our hashtags, write relevant info to the spreadsheet
        for tweet in tweepy.Cursor(api.search, q=hashtag_phrase+' -filter:retweets',                                    lang="en", tweet_mode='extended').items(100):
            w.writerow([tweet.created_at, tweet.full_text.replace('\n',' ').encode('utf-8'), tweet.user.screen_name.encode('utf-8'), [e['text'] for e in tweet._json['entities']['hashtags']], tweet.user.followers_count])


#tweetsearch_for_hashtags(hashtag_phrase)

