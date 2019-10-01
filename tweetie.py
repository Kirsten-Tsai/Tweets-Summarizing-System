import sys
import tweepy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from tfidf import *


def loadkeys(filename):
    """"
    load twitter api keys/tokens from CSV file with form
    consumer_key, consumer_secret, access_token, access_token_secret
    """
    with open(filename) as f:
        items = f.readline().strip().split(', ')
        return items


def authenticate(twitter_auth_filename):
    """
    Given a file name containing the Twitter keys and tokens,
    create and return a tweepy API object.
    """
    key = loadkeys(twitter_auth_filename)
    # print((key))
    auth = tweepy.OAuthHandler(key[0], key[1])
    auth.set_access_token(key[2], key[3])
    api = tweepy.API(auth)

    return api

# post["created"] = str(tweet.created_at).split(" ")[0]


date_since = "2019-09-23"
def fetch_tweets(api, ppl, numOfPost, periods):
    trump = {}
    cnt = 0 #check if it already numOfPost
    docNo = 0
    post = []
    for tweet in tweepy.Cursor(api.user_timeline, id=ppl, tweet_mode='extended').items(numOfPost * periods):
        if cnt >= numOfPost:
            # trump[docNo] = post
            # trump[docNo] = post
            trump[str(tweet.created_at).split(" ")[0]] = post
            post = []
            cnt = 0
            docNo += 1
        cnt += 1
        post.append(tweet.full_text)

    return trump


def account_tweet(user) -> dict: 
    """
    build the dict with {"period: [tweet, tweet]"}
    remove urls in the tweets
    """

    for period, tweets in user.items():
        noUrlPostS = []
        for tweet in tweets:
            content = tweet.replace("\n", " ")
            content = content.replace("\t", " ")
            content = content.split(" ")
            new = [word for word in content if word[:8]!="https://"]
            noUrlPost = " ".join(new)
            noUrlPostS.append(noUrlPost)
        user[period] = noUrlPostS
    return user

# def loadCorpus():

### important ###

if __name__ == "__main__":
    api = authenticate("twitter.csv")
    nameList = getTop100()
    tweetsDict = account_tweet(fetch_tweets(api, nameList))
    # print(tweetsDict)
    tfidf, postList = compute_tfidf(tweetsDict) #postList : Dict with values -- all post into a list
    ans = summarize(tfidf, postList, nameList, 10)
    print(ans)
