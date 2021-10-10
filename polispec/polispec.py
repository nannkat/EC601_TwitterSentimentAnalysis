from ipywidgets.widgets.widget_box import VBox
import pandas as pd
import twitter
from twitter import Tweet
import google_api
from prettytable import PrettyTable
import ipywidgets as widgets

class Politician:

    __POS = 'Positive'
    __NEG = 'Negative'
    __NEUT = 'Neutral'

    def __init__(self, name):
        """Takes as input argument string with name of politician and generates Politician object for analysis"""
        self.name = name
        self.__analyzed_tweet_count = 0
        self.__positive_tweet_count = 0
        self.__negative_tweet_count = 0
        self.__neutral_tweet_count = 0
        self.__hours = 0
        self.__start_time = None
        self.__end_time = None
        self.examples = None

    def __str__(self):
        return '{}, tweets: {}, positive:{}, negative: {}, neutral: {}'.format(self.name, self.get_tweet_count(), self.get_pos_tweet_count(), self.get_neg_tweet_count(), self.get_neut_tweet_count())

    def reset(self):
        self.__analyzed_tweet_count = 0
        self.__positive_tweet_count = 0
        self.__negative_tweet_count = 0
        self.__neutral_tweet_count = 0
        self.__hours = 0
        self.__start_time = None
        self.__end_time = None
        self.examples = None

    def get_tweet_count(self):
        return self.__analyzed_tweet_count

    def get_pos_tweet_count(self):
        return self.__positive_tweet_count
    
    def get_neg_tweet_count(self):
        return self.__negative_tweet_count
    
    def get_neut_tweet_count(self):
        return self.__neutral_tweet_count

    def get_start_time(self):
        neat_start = self.__start_time[11:16] + '-' + self.__start_time[8:10]+ '-'+ self.__start_time[5:7] + '-'+self.__start_time[0:4]
        return neat_start

    def get_end_time(self):
        neat_end = self.__end_time[11:16] + '-' + self.__end_time[8:10]+ '-'+ self.__end_time[5:7] + '-'+self.__end_time[0:4]
        return neat_end
    
    def display_statistics(self):
        ppos = str(round((self.__positive_tweet_count/self.__analyzed_tweet_count)*100, 2)) + '%'
        pneg = str(round((self.__negative_tweet_count/self.__analyzed_tweet_count)*100, 2)) + '%'
        pneut = str(round((self.__neutral_tweet_count/self.__analyzed_tweet_count)*100, 2)) + '%'

        table = PrettyTable()
        table.title = 'Statistic of sentiment for ' + self.name
        table.field_names = ['Sentiment', 'Count', 'Percentage']
        table.add_row(['Positive', self.__positive_tweet_count, ppos])
        table.add_row(['Negaitve', self.__negative_tweet_count, pneg])
        table.add_row(['Neutral', self.__neutral_tweet_count, pneut])

        print('-------------------------------------')
        print('RESULTS')
        print(table)
        print()
        print("Of {} total tweets in the last {} hours, {} were positive, {} were negative, {} were neutral".format(str(self.__analyzed_tweet_count), str(self.__hours), ppos, pneg, pneut))


    def __create_twitter_query(self, hours):

        headers = twitter.create_headers()
        url = twitter.create_url(self.name)
        self.__end_time, self.__start_time = twitter.get_dates(hours)
        parameters = twitter.create_params(max_results=100, start_time=self.__start_time, end_time=self.__end_time)
        print("Query for twitter api: {}".format(url))

        return (url, headers, parameters)
    
    def __get_tweet_batch(self, url, headers, parameters, next_token={}):

        tweet_batch = twitter.connect_to_endpoint_twitter(url, headers, parameters, next_token=next_token)
        self.__analyzed_tweet_count += len(tweet_batch['data'])
        try:
             next = tweet_batch['meta']['next_token']
        except KeyError:
            next = None
        return (tweet_batch, next)


    def analyze_tweets(self, hour_count = 1, display = True):
        if hour_count > 24:
            print("Max 1 day!")
            return
        else:
            #prepare
            self.__hours = hour_count
            google_client = google_api.get_google_client()
            print("Google api client connection established...\n")

            url, headers, parameters = self.__create_twitter_query(hour_count)

            print("\nAnalyzing....\n")
            tweet_dict = {'sentiment':[], 'text':[], 'score':[], 'like_count':[], 'date':[]}
            next = 'start'
            max = 150
            loop = 0
            #loop
            while next != None:
                loop += 1
                print('loop {}'.format(loop))
                tweet_batch, next = self.__get_tweet_batch(url, headers, parameters)

                #analyze sentiment of batch
                for response in tweet_batch['data']:
                    try:
                        tweet = Tweet(response)
                        tweet.clean_tweet()
                        tweet_dict['date'].append(tweet.get_date())
                        tweet_dict['like_count'].append(tweet.get_likes())
                        
                        text, feeling, score = google_api.analyze_tweet(tweet.text, google_client)
                        tweet_dict['text'].append(text)
                        tweet_dict['score'].append(round(float(score),2))

                        if feeling == 'positive':
                            tweet_dict['sentiment'].append(self.__POS)
                            self.__positive_tweet_count += 1
                        elif feeling == 'negative':
                            tweet_dict['sentiment'].append(self.__NEG)
                            self.__negative_tweet_count += 1
                        else:
                            tweet_dict['sentiment'].append(self.__NEUT)
                            self.__neutral_tweet_count +=1
                    except Exception as e:
                        print(e)

                #go to next batch at beginning of loop
                if self.get_tweet_count() > max:
                    break
                print("Tweets processed: {}".format(self.__analyzed_tweet_count))
    
        self.examples = pd.DataFrame(data=tweet_dict)
        self.examples = self.examples.sort_values(by='like_count', ascending=False).reset_index(drop=True)

        if display:
            self.display_statistics()

    def summary(self):
        pos = self.examples_positive()
        neg = self.examples_negative()
        neut = self.examples_neutral()
        self.display_statistics()
        print('-------------------------------------')
        print('EXAMPLE TWEETS')
        print()
        print('POSITIVE')
        pos.next(header=False)
        print('-------------------------------------')
        print('NEGATIVE')
        neg.next(header=False)
        print('-------------------------------------')
        print('NEUTRAL')
        neut.next(header=False)


    def examples_all(self, page_size = 3):
        return Example(self.examples, page_size = page_size)

    def examples_positive(self, page_size = 3):
        positive = self.examples[self.examples['sentiment'] == self.__POS].reset_index(drop=True)
        return Example(positive, page_size = page_size, sentiment='Positive')

    def examples_negative(self, page_size = 3):
        negative = self.examples[self.examples['sentiment'] == self.__NEG].reset_index(drop=True)
        return Example(negative, page_size = page_size, sentiment='Negative')

    def examples_neutral(self, page_size = 3):
        neutral = self.examples[self.examples['sentiment'] == self.__NEUT].reset_index(drop=True)
        return Example(neutral, page_size = page_size, sentiment='Neutral')


def compare(politician1, politician2):

        ppos1 = str(round((politician1.get_pos_tweet_count()/politician1.get_tweet_count())*100, 2)) + '%'
        pneg1 = str(round((politician1.get_neg_tweet_count()/politician1.get_tweet_count())*100, 2)) + '%'
        pneut1 = str(round((politician1.get_neut_tweet_count()/politician1.get_tweet_count())*100, 2)) + '%'

        ppos2 = str(round((politician2.get_pos_tweet_count()/politician2.get_tweet_count())*100, 2)) + '%'
        pneg2 = str(round((politician2.get_neg_tweet_count()/politician2.get_tweet_count())*100, 2)) + '%'
        pneut2 = str(round((politician2.get_neut_tweet_count()/politician2.get_tweet_count())*100, 2)) + '%'

        table = PrettyTable()
        table.title = 'Statistic of sentiment for ' + politician1.name + ' vs. ' + politician2.name
        table.field_names = ['Sentiment', 'Percentage ' + politician1.name, 'Percentage ' + politician2.name ]
        table.add_row(['Positive', ppos1, ppos2])
        table.add_row(['Negaitve', pneg1, pneg2])
        table.add_row(['Neutral', pneut1, pneut2])


        print('-------------------------------------')
        print('RESULTS')
        print(table)
        print()
        print("Of {} tweets on {} from {} to {}, {} were positive, {} were negative, {} were neutral".format(str(politician1.get_tweet_count()), politician1.name,str(politician1.get_start_time()), str(politician1.get_end_time()), ppos1, pneg1, pneut1))
        print("Of {} tweets on {} from {} to {}, {} were positive, {} were negative, {} were neutral".format(str(politician2.get_tweet_count()), politician2.name, str(politician2.get_start_time()), str(politician2.get_end_time()), ppos2, pneg2, pneut2))

class Example:

    def __init__(self, data, page_size, sentiment = ''):
        self.__example = data
        self.__current_index = 0
        self.__sentiment = sentiment
        self.__page_size = page_size
        self.__example_viewer = widgets.Output(layout={'border': '1px solid black'})

    def clear(self):
       self.__example_viewer = widgets.Output(layout={'border': '1px solid black'})
       self.__current_index = 0

    def next(self, header = True):
        if header:
            self.__example_viewer.append_display_data(widgets.HTML('<b>Example ' + self.__sentiment + ' Tweets</b>'))

        for i in range(self.__current_index, self.__current_index + self.__page_size):
            try:
                tweet = widgets.HTML(" <i>'{}'</i><br>".format(self.__example.at[i,'text']))
                tweet_feel = self.__example.at[i,'sentiment']
                sentiment = widgets.HTML("<b>{}</b> ({}) | ".format(tweet_feel, str(self.__example.at[i,'score'])))
                likes = widgets.HTML('{} likes | '.format(str(self.__example.at[i,'like_count'])))
                date = widgets.HTML('{}'.format(self.__example.at[i,'date']))
                metrics = widgets.HBox([sentiment, likes, date])
                info = VBox([tweet, metrics])
                self.__example_viewer.append_display_data(info)
            except KeyError:
                break

        self.__current_index += self.__page_size



   

