__email__ = ["shayan@cs.ucla.edu"]
__credit__ = ["ER Lab - UCLA"]

from TwitterSearch import *
from typing import List, Iterable, Any
from datetime import date, timedelta
from wordcloud import WordCloud
import matplotlib
import pandas
import os

matplotlib.use('Agg')


class CoatTwitterAgent:
    """
    The :class:`CoatTwitterAgent` is responsible for querying the information that
    the user requires from the twitter website. The calls are made using the API calls and to
    do so you need to create and register your request via the twitter website.
    """

    def __init__(self, consumer_key: str, consumer_secret: str, access_token_key: str, access_token_secret: str):
        """
        The constructor of the :class:`CoatTwitterAgent`.
        
        Parameters
        ----------
        consumer_key: `str`, required
            token for the API access to twitter

        consumer_secret:  `str`, required
            token for the API access to twitter

        access_token_key:  `str`, required
            token for the API access to twitter

        access_token_secret:  `str`, required
            token for the API access to twitter
        """
        # it's about time to create a TwitterSearch object with our secret tokens
        self.ts = TwitterSearch(
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            access_token=access_token_key,
            access_token_secret=access_token_secret
        )

    def get_tweet_stream(self,
                         search_keywords: List[str] = ['covid19'],
                         include_entities: bool = False,
                         language: str = 'en') -> Iterable[str]:
        """
        The :meth:`get_tweet_stream` allows the researcher to obtain the stream of queried tweets to analyze.
        
        Parameters
        ----------
        search_keywords: `List[str]`, optional (default=`['#covid19']`)
            The search keywords

        include_entities: `bool`, optional (default=False)
            Whether or not entities should be included in the results.

        language: `str`, optional (default='en')
            The language of the queried tweets, which helps in clustering the output results.

        Returns
        ----------
        The output is of type `Iterable[str]`.
        """
        tso = TwitterSearchOrder()  # create a TwitterSearchOrder object
        tso.set_keywords(search_keywords)  # let's define all words we would like to have a look for
        tso.set_language(language)  # we want to see German tweets only
        tso.set_include_entities(include_entities)  # and don't give us all those entity information
        tso.set_since(date=(date.today() - timedelta(days=1)))
        return self.ts.search_tweets_iterable(tso)

    def save_tweets_dataframe(self, stream: Any, output_path: str,
                              tweet_count: int = 1000) -> None:
        """
        Getting the tweets using :meth:`save_tweets_dataframe`.
        
        Parameters
        ----------
        stream: `TwitterSearch.TwitterSearch.TwitterSearch`, required
            The tweet stream for this method to work with.

        output_path: `str`, required
            The path to the output csv file

        tweet_count: `int`, optional (default=1000)
            The maximum number of tweets to fetch
        """
        tweets = []
        for i in range(tweet_count):
            try:
                tweets.append(next(stream))
            except:
                break
        retweet_counts = [e['retweet_count'] for e in tweets]
        favorite_counts = [e['favorite_count'] for e in tweets]
        usernames = [e['user']['screen_name'] for e in tweets]
        names = [e['user']['name'] for e in tweets]
        locations = [e['user']['location'] for e in tweets]
        texts = [e['text'] for e in tweets]
        dates = [e['created_at'] for e in tweets]
        ids = [e['id'] for e in tweets]
        df = pandas.DataFrame(
            {
                'Retweeted by': retweet_counts,
                'Favorited by': favorite_counts,
                'Username': usernames,
                'Location': locations,
                'Tweet': texts,
                'Created at': dates,
                'ID': ids,
                'Name': names
            })

        df.to_csv(os.path.abspath(output_path))

    @staticmethod
    def get_tweets_dataframe(stream: Any,
                             tweet_count: int = 1000) -> pandas.DataFrame:
        """
        Getting the tweets using :meth:`get_tweets_dataframe`.

        Parameters
        ----------
        stream: `TwitterSearch.TwitterSearch.TwitterSearch`, required
            The tweet stream for this method to work with.

        output_path: `str`, required
            The path to the output csv file

        tweet_count: `int`, optional (default=1000)
            The maximum number of tweets to fetch
        """
        tweets = []
        for i in range(tweet_count):
            try:
                tweets.append(next(stream))
            except:
                break

        def get_date_from_raw(x: str):
            month = x.strip().split(' ')[1].lower()
            day = str(int(x.split(' ')[2]))
            year = str(int(x.split(' ')[-1]))

            if month.startswith('jan'):
                month = 'January'
            elif month.startswith('feb'):
                month = 'February'
            elif month.startswith('mar'):
                month = 'March'
            elif month.startswith('apr'):
                month = 'April'
            elif month.startswith('may'):
                month = 'May'
            elif month.startswith('jun'):
                month = 'June'
            elif month.startswith('jul'):
                month = 'July'
            elif month.startswith('aug'):
                month = 'August'
            elif month.startswith('sep'):
                month = 'September'
            elif month.startswith('oct'):
                month = 'October'
            elif month.startswith('nov'):
                month = 'November'
            elif month.startswith('dec'):
                month = 'December'

            return "{} {}, {}".format(month, day, year)


        retweet_counts = [e['retweet_count'] for e in tweets]
        favorite_counts = [e['favorite_count'] for e in tweets]
        usernames = [e['user']['screen_name'] for e in tweets]
        names = [e['user']['name'] for e in tweets]
        locations = [e['user']['location'] for e in tweets]
        texts = [e['text'] for e in tweets]
        dates = [get_date_from_raw(e['created_at']) for e in tweets]
        ids = [e['id'] for e in tweets]

        df = pandas.DataFrame(
            {
                'Retweeted by': retweet_counts,
                'Favorited by': favorite_counts,
                'Username': usernames,
                'Location': locations,
                'Tweet': texts,
                'Created at': dates,
                'ID': ids,
                'Name': names
            })

        return df

    @staticmethod
    def save_tweets_wordcloud(df: pandas.DataFrame, output_path: str):
        """
        The method to save the tweets word cloud

        Parameters
        ----------
        df: `pandas.DataFrame`, required
            The tweets dataframe

        output_path: `str`, required
            The path to the output image
        """
        texts = df['Tweet'].tolist()
        full_text = ' '.join(texts)
        wordcloud = WordCloud(width=1600, height=800, max_font_size=100, max_words=10000,
                              background_color="lightblue").generate(full_text)
        wordcloud.to_file(os.path.abspath(output_path))
