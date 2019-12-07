from tweepy import OAuthHandler, Stream, API
from tweepy.streaming import StreamListener
from main import credentials
from pykafka import KafkaClient
import json


def get_kafka_client():
    return KafkaClient(hosts='127.0.0.1:9092')


class TwitterHashtagListener(StreamListener):
    '''
    inherits StreamListener
    '''

    def on_data(self, data):
        '''
        passes data from statuses to this method
        :param data: data from statuses
        :return: bool
        '''
        print(data)
        message = json.loads(data)
        if message['text'] is not None:
            # Creating kafka client and its producers
            client = get_kafka_client()
            topic = client.topics['twitterstreamdata']
            producer = topic.get_sync_producer()
            producer.produce(data.encode('ascii'))
        return True

    def on_error(self, status_code):
        print(status_code)
        return False


class TwitterUserIdListener(StreamListener):
    '''
    inherists StreamListener
    '''

    def on_data(self, data):
        '''
        passes data from statuses to this method
        :param data: data from statuses
        :return: bool
        '''
        print(data)
        message = json.loads(data)
        if message['text'] is not None:
            # Creating kafka client and its producers
            client = get_kafka_client()
            topic = client.topics['userstreamdata']
            producer = topic.get_sync_producer()
            producer.produce(data.encode('ascii'))
        return True

    def on_error(self, status_code):
        print(status_code)
        return False


def main(hashtag=None, user_id=None):
    '''
    Stream data from twitter based on the given filter
    :return: None
    '''
    if hashtag is None and user_id is None:
        return

    # Authentication for twitter app
    auth = OAuthHandler(credentials.CONSUMER_KEY, credentials.CONSUMER_SECRET_KEY)
    auth.set_access_token(credentials.ACCESS_TOKEN, credentials.ACCESS_TOKEN_SECRET)

    if user_id is None:
        # Creating stream
        listener = TwitterHashtagListener()
        stream = Stream(auth=auth, listener=listener)

        # Applying filter on stream and starting stream in a new thread
        stream.filter(track=[hashtag], is_async=True)
    else:

        api = API(auth)

        user = api.get_user(user_id)
        if user:
            listener = TwitterUserIdListener()
            stream = Stream(auth=auth, listener=listener)

            # Applying filter on stream and starting stream in a new thread
            stream.filter(follow=[user.id_str], is_async=True)


if __name__ == "__main__":
    main(hashtag='Python')
