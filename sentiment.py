
# Demonstrates connecting to the twitter API and accessing the twitter stream
# Author: Michael Fahy
# Email: fahy@chapman.edu
# Course: CPSC 353
# Assignment: PA01 Sentiment Analysis
# Version 1.2
# Date: February 15, 2016

# Takes in two search terms from the user
# Identifies which of the search terms has a higher positive sentiment score
# Edited by: Kathleen Gendotti
# Email: gendo102@mail.chapman.edu
# Date: October 8, 2018


# Demonstrates connecting to the twitter API and accessing the twitter stream

import twitter

print 'Establishing Authentication Credentials'
CONSUMER_KEY = 'xW4plMsMfGwsZS59Yv1efNBQk'
CONSUMER_SECRET = '4ci6vkYAvYqhzyIAeRF3Q9NIq4wnGW0krbt0bW0rnn3QDhAFgN'
OAUTH_TOKEN = '1045483764271308800-zEF2TO4rDfogUWHhd9VruXg5tcJdHI'
OAUTH_TOKEN_SECRET = 'mIAnfqMPOkX5iLK6ILAHu84BtsUaOwyDR3SlQsuLME3kH'
auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                           CONSUMER_KEY, CONSUMER_SECRET)

# making twitter_api a defined variable
twitter_api = twitter.Twitter(auth=auth)

# prompts user for search terms
print
term1 = raw_input('Please enter your first search term: ')
term2 = raw_input('Please enter your second search term: ')

print
print "Calculating sentiment scores..."

# sets count to 1000 to be used to search twitter stream for the first 1000
# tweets containing each search term
count = 1000

# searches the twitter stream for the first 1000 tweets
# containing the first search term
search_results_1 = twitter_api.search.tweets(q=term1, count=count)
statuses_1 = search_results_1['statuses']

# searches the twitter stream for the first 1000 tweets
# containing the second search term
search_results_2 = twitter_api.search.tweets(q=term2, count=count)
statuses_2 = search_results_2['statuses']

# Iterate through 5 more batches of results by following the cursor
for _ in range(5):
    try:
        next_results_1 = search_results_1['search_metadata']['next_results']
        next_results_2 = search_results_2['search_metadata']['next_results']
    except KeyError, e:  # No more results when next_results doesn't exist
        break

    # Create a dictionary from next_results, which has the following form:
    # ?max_id=313519052523986943&q=NCAA&include_entities=1
    kwargs_1 = dict([kv.split('=') for kv in next_results_1[1:].split("&")])
    kwargs_2 = dict([kv.split('=') for kv in next_results_2[1:].split("&")])

    # gets the first search term results and
    # adds up the statuses of the results
    search_results_1 = twitter_api.search.tweets(**kwargs_1)
    statuses_1 += search_results_1['statuses']

    # gets the second search term results and
    # adds up the statuses of the results
    search_results_2 = twitter_api.search.tweets(**kwargs_2)
    statuses_2 += search_results_2['statuses']

status_texts_1 = [status['text'] for status in statuses_1]

status_texts_2 = [status['text'] for status in statuses_2]

# Compute a collection of all words from all tweets
words_1 = [w for t in status_texts_1 for w in t.split()]

words_2 = [w for t in status_texts_2 for w in t.split()]

sent_file = open('AFINN-111.txt')

scores = {}  # initialize an empty dictionary
for line in sent_file:
    term, score = line.split("\t")
    # The file is tab-delimited.
    # "\t" means "tab character"
    scores[term] = int(score)  # Convert the score to an integer.

# initializes the search terms scores
term1_score = 0
term2_score = 0

# iterates through the words for the first search term to
# calculate the sentiment score
for word in words_1:
    uword = word.encode('utf-8')
    if uword in scores.keys():
        term1_score = term1_score + scores[word]

# iterates through the words for the second search term to
# calculate the sentiment score
for word in words_2:
    uword = word.encode('utf-8')
    if uword in scores.keys():
        term2_score = term2_score + scores[word]

# Prints the sentiment scores of each term to the user
print
print 'Sentiment score for ' + term1 + ': ' + str(float(term1_score))
print 'Sentiment score for ' + term2 + ': ' + str(float(term2_score))
print

# Statments used to identify
# which search term has a higher positive sentiment score

# If the first search term's sentiment score is large, it tells the user
if(float(term1_score) > float(term2_score)):
    print term1 + ' has a more postive sentiment score than ' + term2
# If the second search term's sentiment score is large, it tells the user
elif(float(term1_score) < float(term2_score)):
    print term2 + ' has a more postive sentiment score than ' + term1
# If the search terms sentiment scores are equal, it tells the user
else:
    print term1 + ' and ' + term2 + ' have an equal sentiment scores'
