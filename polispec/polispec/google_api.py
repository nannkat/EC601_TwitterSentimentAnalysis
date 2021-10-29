
import os
from google.cloud import language_v1

"""Functions related to connecting to and requesting from the Google API"""

CRED_PATH = "/Users/Nanna/Desktop/EC601/twitter_sentiment_analysis/google_keys/sentiment-analysis-test-327412-c89ef3ef857c.json"
"""Please replace the path to the google api credentials json file with your own."""
 

def get_google_client():
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = CRED_PATH
    client = language_v1.LanguageServiceClient()
    return client

def get_sentiment(score):
    '''Anything close to 0 is neutral -> positive > 0.3, negative < -0.3, neutral: -0.3 < score < 0.3.
    Strictness of metrics can be easily adjusted'''
    s = float(score)
    if s > 0.3:
        return "positive"
    elif s < -0.3:
        return "negative"
    else:
        return "neutral"

def analyze_tweet(tweet_text, client):
    """Recieves as input the text of a tweet (already preprocessed) and a google api client. 
    Connects to the endpoint and returns a tuple with the original tweet text, it's sentiment and score"""
    doc = language_v1.Document(content = tweet_text, type_= language_v1.Document.Type.PLAIN_TEXT)
    sentiment_analysis = client.analyze_sentiment(request ={'document': doc})
    score = sentiment_analysis.document_sentiment.score
    sentiment = get_sentiment(score)

    return(tweet_text, sentiment, score)