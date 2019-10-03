import sys

import nltk
from nltk.stem.porter import *
from sklearn.feature_extraction import stop_words
import xml.etree.cElementTree as ET
from collections import Counter
import string
from sklearn.feature_extraction.text import TfidfVectorizer
import zipfile
import os



def gettext(xmltext):
    xmltext = xmltext.encode('ascii', 'ignore') # ensure there are no weird char
    tree = ET.fromstring(xmltext)
    root = ET.ElementTree(tree)

    word = ""
    for _ in root.iterfind("title"):
        word += _.text
    word += " "
    for _ in root.iterfind(".//text/*"):
        word += _.text
        word += " "
    return word

def tokenize(text):
    regex = re.compile('[' + re.escape(string.punctuation) + '0-9\\r\\t\\n]')
    nopunct = regex.sub(" ", text)  # delete stuff but leave at least a space to avoid clumping together
    words = ' '.join(nopunct.split(" "))
    words = nltk.word_tokenize(words)
    words = [w for w in words if len(w) > 2]  # ignore a, an, to, at, be, ...
    words = [w.lower() for w in words]
    words = [i for i in words if i not in list(stop_words.ENGLISH_STOP_WORDS)]

    return words


def stemwords(words):
    ps = PorterStemmer()
    stem = [ps.stem(w) for w in words]
    return stem

def tokenizer(text):
    return stemwords(tokenize(text))
    # return stemwords(tokenize(text))

def compute_tfidf(tweetsDict):
    tfidf = TfidfVectorizer(input='content',
                        analyzer='word',
                        tokenizer=tokenizer,
                        stop_words='english',
                        decode_error = 'ignore')
    
    newDict = {}
    for account, tweets in tweetsDict.items():
        newDict[account] = " ".join(tweetsDict[account])
    corpusList = list(newDict.values())

    tfidf.fit(corpusList)
    return tfidf

def summarize(tfidf, postList, nameList, n):
    ans = [[] for i in range(len(nameList))] 

    for i_name in range(len(nameList)):
        text = postList[nameList[i_name]]
        matrix = tfidf.transform([text])
        names = tfidf.get_feature_names()
        non0 = matrix.nonzero()
        for i in non0[1]:
            if matrix[0, i] < 0.09:
                continue
            ans[i_name].append((names[i], float("{:.{}f}".format( matrix[0,i], 3 ))))
            ans[i_name] = sorted(ans[i_name], key = lambda x:x[1], reverse = True)
        ans[i_name] = ans[i_name][:n]
    return ans


if __name__ == "__main__":
    tweetsDict = {'BarackObama': ['On National Voter Registration Day, it’s up to us as citizens to make sure everyone we know can make their voices heard at the ballot box. Check and update your registration at — and tell your friends, too.', 'One challenge will define the future for today’s young generation more dramatically than any other: Climate change. The millions of young people worldwide who’ve organized and joined today’s #ClimateStrike demand action to protect our planet, and they deserve it.', 'Just 16, @GretaThunberg is already one of our planet’s greatest advocates. Recognizing that her generation will bear the brunt of climate change, she’s unafraid to push for real action. She embodies our vision at the @ObamaFoundation: A future shaped by young leaders like her.', 'That’s what Americans do when others are in need – we help. We give. We inspire. Want to make a difference? There are a number of ways you can help right here:', 'Jermaine Bell is just six years old, but when he saw people in need, he took the money he’d been saving for a trip to Disney World and spent it on food and water for South Carolina evacuees.'], 'katyperry': ['Omg woke up to this adorable thread and need to add one that my niece did a few months ago for my sister. It makes my heart burst every time I hear it 😩', 'A @BraggLiveFoods 🍎 (cider vinegar) a day keeps a throat tickle away, but health and wellness close by 🤗 #FBF #ExpoEast', 'Ironic that our smartphones are making us dumbhumans 🙃', 'My characters in FINAL FANTASY BRAVE EXVIUS are #NeverReallyOver, so you can play them #365, but you have to check it out before September 30th! #FFBEWW', 'Fall boot but make it PSL 🍂🍁 (Or maybe you’re more of a unicorn latte 🌈) We gotchu. #ShoesdayTuesday @kpcollections'], 'justinbieber': ['RT @SchmidtsNatural: Here+Now is here, for good! Co-created with @justinbieber, Here+Now combines spicy citrus, warm florals, and deep wood…', '@flakmengo Go again', 'That’s a lot of retweets', 'Retweet this tweet to see this tweet on your twitter when you tweet.', 'You like me?']}
    nameList = ['BarackObama', 'katyperry', 'justinbieber']

    tfidf, postList = compute_tfidf(tweetsDict) #postList : Dict with values -- all post into a list
    ans = summarize(tfidf, postList, nameList, 10)
    print(ans)
