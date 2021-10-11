# Twitter Sentiment Analysis Project
## By Nanna Katrín Hannesdóttir
## Milestone 2(b) - Political Spectrum Speculator 'polispec' Library 
### Mission
My project was to build a library that analyses sentiment of tweets about prominent politicians and gives statistics on number of positive vs. negative tweets about them. The mission is to create an easy way to get informed about how popular certain politicians are and also perhaps get a reality check regarding 'the other side', the politicians you don't agree with. Trump might seem really unpopular in someone's circle, but how many people are tweeting about him with positive sentiment? Is Biden becomin increasingly unpopular? The library should also have functions to get actual text examples of what people are saying in their tweets. That way it can give both numerical and conceptual insight simultaniously.

### Implementation
The resulting library can be found under the folder /polispec in this repository. The implementation went overall well with the mvp goal reached and some of the other user stories as well (defined under milestone 2a). I organized the modular design so that the user would only have to use simple commands to get statistics and/or examples. Two modules, 'twitter.py' and 'google_api.py' are background modules that organize communication with the twitter and google APIs, handling authentication and requests. The user does not interact with those. The main module is the 'polispec.py' that utilises the other two modules and which contains the classes and functions needed for analysis. This is the module the user imports from and interacts with.

### How to test/run
In the /polispec folder there is also a jupyter notebook with a short demo of the library, 'polispec_demo.ipynb! It should be easy to run, only requiring some change of variables for authentication.<br>

<b>Authentication</b><br>
What you need to do to get the authentication correct:
- Inside 'twitter.py' modify the path at the top to contain with your own credential.yaml file containing the bearer token. For safety and convenience I used .yaml files for the twitter tokens. The format and variable names for the .yaml file are specified in 'twitter.py'
- Inside 'google_api.py' change the path to the path to your google credentials .json file

After this you should be all set with authentication

<b>Libraries</b><br>
Please make sure you have the following libraries installed:
- language_V1 from google.cloud
- ipywidgets
- prettytable
- pandas
- requests
- yaml
- json
- re
- datetime

With this in place, running the demo should be straight forward.

### Conclusion
This was a fun project and I feel lucky to get the chance to explore these APIs. It gave me good insights into modular design and organization and building queries and requests. It also gave me some insight into the status of natural language processing. As my library included in part displaying text examples of tweets, I got a look at how well the google api sentiment analysis was doing from time to time. The biggest problem seemed to be that the API can't detect sarcasm. On twitter many people use sarcasm to express themselves and this resulted in some pretty drastic misclassifications. Tweets about politicians were often said to be positive when in reality the person was clearly using positive words in a sarcastic manner. It will be interesting to see how engineers try to tackle this problem in the future. Can computers be sarcastic?

# Older Milestones
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

## Milestone 2(a) - Product Definition

<b>The product, "Political Spectrum Speculator"</b><br>
My project will be to build a library that analyses sentiment of tweets about prominent politicians and gives statistics on number of positive vs. negative tweets about them. The mission is to create an easy way to get informed about how popular certain politicians are and also perhaps get a reality check regarding 'the other side', the politicians you don't agree with. Trump might seem really unpopular in someone's circle, but how many people are tweeting about him with positive sentiment? Is Biden becomin increasingly unpopular? The library should also have functions to get actual text examples of what people are saying in their tweets. That way it can give both numerical and conceptual insight simultaniously.

<b>Who is the user?</b><br>
Some main users are:
- The general public. People who are curious to get a glimpse at how popular their favorite (or least favorite) politician is on a larger scale
- Reporters. Who need a quick way to get statistics and analysis for an informative article. 
- Political strategist. Wanting to check the popularity of politician X declining rapidly in the last few days after event Y. Getting insight into popularity on the other side of the political spectrum and on the views there.

<b>Potential user stories</b>
- I want to be able to enter/select a name of a politician and get the count of positive and negative tweets about them for the last 7 days <i>(mvp)</i>
- I want to be able to choose from when and over how long the positive/negative tweets used in analysis are
- I want to see the trend of positivity and negativity over time
- I want to be able to enter two or more politicians names and get results to show how they compare 
- I want to be able to get text examples of tweets from the positive and negative side <i>(mvp)</i>
- I want to be able to flip through multiple text examples with some sort of 'next' button and/or get batches
- I want to get the results organized by location so I can compare differences between states/countries
- I want to get the results in a clear and compact form that is easy to interpret <i>(mvp)</i>
- I want to be able to get the results displayed as a graph
- Instead of getting examples of whole tweets, I just want some top keywords that might indicate patterns in positive/negative tweets

<b>The MVP (Minimum Valued Product)</b><br>
Based on the user stories above, I picked the ones that I felt were most essential to my mission (user stories marked with mvp). The minimum value product will thus be a library where you can enter/select a name of a politician and get the count of positive and negative tweets about them for the last 7 days, get text examples from each side and have the results displayed clearly in a compact fashion. 


