from flask import render_template, Response, url_for
from main import app
from pykafka import KafkaClient
import json

def get_kafka_client():
    return KafkaClient(hosts='127.0.0.1:9092')

@app.route("/")
def hello():
    return render_template("wordcloud.html")


@app.route("/stream")
def stream():
    return render_template("stream.html")

@app.route("/tweets")
def get_tweets():
    client = get_kafka_client()
    def events():
        for i in client.topics['twitterstreamdata'].get_simple_consumer():
            yield 'data: {0}\n\n'.format(i.value.decode())
    return (Response(events(), mimetype="text/event-stream"))