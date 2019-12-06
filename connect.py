from tweepy.streaming import StreamListener
from tweepy import OAuthHandler, Stream
import credentials
from pykafka import KafkaClient
import json

def get_kafka_client():
    return KafkaClient(hosts='127.0.0.1:9092')


class MyStreamListener(StreamListener):
    def on_data(self, data):
        print(data)
        message = json.loads(data)
        if message['text'] is not None:
            client = get_kafka_client()
            topic = client.topics['twitterstreamdata']
            producer = topic.get_sync_producer()
            producer.produce(data.encode('ascii'))
        return True

    def on_error(self, status_code):
        print(status_code)
        return False


if __name__ == "__main__":
    auth = OAuthHandler(credentials.CONSUMER_KEY, credentials.CONSUMER_SECRET_KEY)
    auth.set_access_token(credentials.ACCESS_TOKEN, credentials.ACCESS_TOKEN_SECRET)
    listener = MyStreamListener()
    stream = Stream(auth=auth, listener=listener)
    stream.filter(track=['Drivezy'])

