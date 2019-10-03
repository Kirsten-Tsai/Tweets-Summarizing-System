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
    for i in range(len(datePeriod)):
        item = dict(account = datePeriod[i], symbol = dateMsg[i])
        table.append(item)
    names = dateList
    return render_template('articles.html', table = table, account = ppl)


numOfPost = 100 #how many post in a corpus
numOfWords = 10 # how many symbolic words you wanna know
numOfPeriods = 40

api = authenticate("twitter.csv")
ppl = "realDonaldTrump"

tweetsDict = account_tweet(fetch_tweets(api, ppl, numOfPost, numOfPeriods))
dates = list(tweetsDict.keys())

tfidf = compute_tfidf(tweetsDict) #postList : Dict with values -- all post into a list
dateList = list(tweetsDict.keys())

def toPostList(tweetsDict):
    newDict = {}
    for account, tweets in tweetsDict.items():
        newDict[account] = " ".join(tweetsDict[account])
    return newDict

postList = toPostList(tweetsDict)

ans = summarize(tfidf, postList, dateList, numOfWords)
keywordDict = []

for i in range(len(ans)):
	tmp = {}
	for tup in ans[i]:
		tmp[tup[0]] = tup[1]
	keywordDict.append(tmp)

maxIndex = []
for i in range(len(dates)):
	msg = tweetsDict[dates[i]]
	score = 0
	maxScore = 0
	maxInd = 0
	for j in range(len(msg)):
		txt = tokenize(msg[j])
		score = 0
		for word in txt:
			try:
				score += keywordDict[i][word]
			except:
				pass
		if score > maxScore:
			maxScore = score
			maxInd = j
	maxIndex.append(maxInd)

kingMsg = {}
for index, i in enumerate(maxIndex, 0):
	kingMsg[dates[index]] = tweetsDict[dates[index]][i]

datePeriod = list(kingMsg.keys())
dateMsg = list(kingMsg.values())
