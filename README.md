# Twitter Sentiment Analysis Project
## By Nanna Katrín Hannesdóttir
## Milestone 1(a) - Experimenting with the Twitter API

Full experiment under:
- examperiments/experiments_TwitterAPI.ipynb

After getting access to the API I experimented with some requests to some endpoints from my visual studio code environment.

For help with interacting with the API via Python I found this tutorial helpful: https://towardsdatascience.com/an-extensive-guide-to-collecting-tweets-from-twitter-api-v2-for-academic-research-using-python-3-518fcb71df2a
. As well as the [requests](https://docs.python-requests.org/en/latest/) library in python.

The results of my experimentation are stored in a jupyter notebook under the examples folder. I first started with the basics, exploring a user data endpoint. For that I used my own old twitter account. I tried expanding the information fields to get metadata, setting different time boundaries,
and changing the default result count. Moving on to the search endpoint I tried querying by topics and time. I tried querying for tweets on the Icelandic government elections going on this evening along with all tweets on cats and dogs in english within the last hour that included pictures.

It was very fun and I look forward to working with the API. 

## Milestone 1(b) - Experimenting with the Google API
Full experiment under:
- experiments/experiments_GoogleAPI.ipynb 

And additional files from using google console under:
- experiments/Google_API_ConsoleCommands.txt 
- experiments/basic_request.json
- experiments/basic_request2.json
- experiments/basic_requestIcelandic.json

For these tests I started out by playing around on the console offered on the Google API dashboard page to get a feeling for the basic format of the requests. I practiced with the format for the data of the request: a .json file of certain structure and made requests to the API via the terminal where results also got printed out. I learned about the scale of the sentiment analysis -1;1 where -1 is most negative and 1 is most positive. I tried entering sentences like "Boston is a great city to live" or mixed ones with both positive and negative and got appropriate results. The API did not like the usage of Icelandic my native language however, and did not recognize it. I wanted to try just for fun but will stick to English for the main project.

After my tests online I wanted to test how to connect to the API with python as I will be using python for the project. Using the google documentation I was able to utilise the [google.cloud language v1 library](https://cloud.google.com/natural-language/docs/reference/rpc/google.cloud.language.v1) and easily send basic requests from Visual Studio to the API. To take it further I loosely based on the [Twitter API documentation](https://developer.twitter.com/en/docs/tutorials/how-to-analyze-the-sentiment-of-your-own-tweets) to connect it with my experiments on the twitter API and was able to successfully characterize sentiment of 10 tweets from a query using Trump as keyword.
