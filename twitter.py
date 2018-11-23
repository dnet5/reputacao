import tweepy
import json
import io


class AcessoTwitter(object):

    def __init__(self):
        self.api = self.api_login()

    def quick_start(self, query):
        print('Inicio da coleta de tweets referentes ao termo %s,'
              ' com o limite de resultados até 10 dias retroativos e 1500 tweets.' % query)
        tweet_obj_list = self.quick_query(query)
        tweet_dict_list = self.struct_tweet_list(tweet_obj_list)
        self.save_tweets(tweet_dict_list, query)
        print('Fim da coleta de %d tweet, referente ao termo %s' % (len(tweet_dict_list), query))
        return tweet_dict_list

    def quick_query(self, query, limit=1499):
        tweet_obj_list = list()
        for idx, tweet in enumerate(tweepy.Cursor(self.api.search, q=query, rpp=100).items()):
            print('Coletando tweet de número %d' % (idx + 1))
            tweet_obj_list.append(tweet)
            if idx >= limit:
                break
        return tweet_obj_list

    @staticmethod
    def struct_tweet_list(tweet_list):
        structured_list = list()
        for tweet in tweet_list:
            structured_tweet = dict()
            structured_tweet['id'] = tweet.id
            structured_tweet['text'] = tweet.text
            structured_tweet['author'] = tweet.author.screen_name
            structured_tweet['date'] = tweet.created_at.strftime("%d/%m/%Y %H:%M:%S")
            structured_tweet['link'] = 'twitter.com/%s/status/%s' % (structured_tweet['author'], structured_tweet['id'])
            structured_tweet['share_count'] = tweet.retweet_count
            structured_tweet['likes_count'] = tweet.favorite_count
            structured_tweet['repercussion_count'] = structured_tweet['share_count'] + structured_tweet['likes_count']
            structured_list.append(structured_tweet)
        return structured_list

    def save_tweets(self, tweet_list, query=''):
        twitter_dict = {'tweet_list': tweet_list}
        self.write_json(twitter_dict, 'twitter_query_%s' % query)

    @staticmethod
    def api_login(auth_dict=None):
        if auth_dict is None:
            auth_dict = {
                'consumer_key': '',
                'consumer_secret': '',
                'access_key': '',
                'access_secret': ''
            }
        auth = tweepy.OAuthHandler(auth_dict['consumer_key'], auth_dict['consumer_secret'])
        auth.set_access_token(auth_dict['access_key'], auth_dict['access_secret'])
        return tweepy.API(auth)

    @staticmethod
    def write_json(dictionary, start_name):
        with io.open(start_name + '.json', 'w', encoding='utf8') as json_file:
            json.dump(dictionary, json_file, ensure_ascii=False, indent=4)
