
import os
from google.cloud import language_v1

CRED_PATH = "/Users/Nanna/Desktop/EC601/google_keys/sentiment-analysis-test-327412-c89ef3ef857c.json"

def get_google_client():
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = CRED_PATH
    client = language_v1.LanguageServiceClient()
    return client

def get_sentiment(score):
    '''Anything close to 0 is neutral -> positive >= 0.5, negative <= -0.5, neutral: -0.5 < score < 0.5.
    Question of how strict to be....'''
    s = float(score)
    if s > 0.3:
        return "positive"
    elif s < -0.3:
        return "negative"
    else:
        return "neutral"

def analyze_tweet(tweet_text, client):
    
    doc = language_v1.Document(content = tweet_text, type_= language_v1.Document.Type.PLAIN_TEXT)
    sentiment_analysis = client.analyze_sentiment(request ={'document': doc})
    score = sentiment_analysis.document_sentiment.score
    sentiment = get_sentiment(score)

    return(tweet_text, sentiment, score)