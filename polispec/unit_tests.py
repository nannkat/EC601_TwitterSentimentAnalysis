import unittest
from polispec import polispec, twitter, google_api



class TwitterTest(unittest.TestCase):
    def setUp(self):
        self.name = 'George Bush'
        self.params = '%20has%3Amedia'
        self.hours1 = 4
        self.hours2 = -2
    
    def test_querify_name(self):
        res = twitter.querify_name(self.name)
        assert res == 'George%20Bush%20'
    
    def test_create_url1(self):
        res = twitter.create_url(self.name)
        assert res == 'https://api.twitter.com/2/tweets/search/recent?query=George%20Bush%20lang%3Aen%20-is%3Aretweet%20-is%3Areply'

    def test_create_url2(self):
        res = twitter.create_url(self.name, self.params)
        assert res == 'https://api.twitter.com/2/tweets/search/recent?query=George%20Bush%20lang%3Aen%20-is%3Aretweet%20-is%3Areply%20has%3Amedia'
    
    #negative input for dates
    def test_get_dates(self):
        res = twitter.get_dates(self.hours2)
        assert res == 'Hour count cant be negative or 0'



class GoogleTest(unittest.TestCase):
    
    def setUp(self):
        self.score_neg = -0.5
        self.score_pos = 0.8
        self.score_neut = 0.3

    def test_sentiment_neg(self):
        result = google_api.get_sentiment(self.score_neg)
        assert result == 'negative'

    def test_sentiment_pos(self):
        result = google_api.get_sentiment(self.score_pos)
        assert result == 'positive'

    def test_sentiment_neut(self):
        result = google_api.get_sentiment(self.score_neut)
        assert result == 'neutral'

        
class PoliTest(unittest.TestCase):

    def setUp(self):
        self.politician = polispec.Politician('Nancy Pelosi')
        self.politician._Politician__start_time = '2021-12-06T20:21:04.000Z'
        self.politician._Politician__end_time = '2021-12-06T20:22:04.000Z'
        self.neat_start = '20:21-06-12-2021'
        self.neat_end = '20:22-06-12-2021'

    def test_start_time(self):
        res = self.politician.get_start_time()
        assert res == self.neat_start

    def test_end_time(self):
        res = self.politician.get_end_time()
        assert res == self.neat_end


if __name__ == 'main':
    unittest.main()