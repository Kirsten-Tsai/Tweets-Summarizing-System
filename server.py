# Launch with
#
# gunicorn -D --threads 4 -b 0.0.0.0:5000 --access-logfile server.log --timeout 60 server:app glove.6B.300d.txt bbc

# gunicorn -D --threads 1 -b 0.0.0.0:5000 --access-logfile server.log --timeout 60 server:app /Users/kirsten/Documents/USF/2019Fall/DataAcquisition/SelfRepo/recommendation/recommender-Kirsten-Tsai/Data/glove.6B/glove.6B.50d.txt /Users/kirsten/Documents/USF/2019Fall/DataAcquisition/SelfRepo/recommendation/recommender-Kirsten-Tsai/Data/bbcTest

from flask import Flask, render_template
import sys
from tweetie import *

app = Flask(__name__)

@app.route("/")
def articles():
    table = []
    for i in range(len(dateList)):
        item = dict(account = dateList[i], symbol = terms[i])
        table.append(item)
    names = dateList
    return render_template('articles.html', people = zip(names, terms), table = table, account = ppl)


############
numOfPost = 200 #how many post in a corpus
numOfWords = 10 # how many symbolic words you wanna know
numOfPeriods = 10

api = authenticate("twitter.csv")
ppl = "realDonaldTrump"

tweetsDict = account_tweet(fetch_tweets(api, ppl, numOfPost, numOfPeriods))
# print(tweetsDict)
tfidf, postList = compute_tfidf(tweetsDict) #postList : Dict with values -- all post into a list
dateList = list(tweetsDict.keys())
ans = summarize(tfidf, postList, dateList, numOfWords)
terms = [" ".join([word[0] for word in ppl])for ppl in ans]
# print(ans)