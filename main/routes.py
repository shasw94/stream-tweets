from flask import render_template, Response, url_for, flash, redirect
from main import app, connect
from pykafka import KafkaClient
from main.forms import UserIdSearchForm, HastagSearchForm


def get_kafka_client():
    '''
    Gets the client for communicating with kafka.
    :return: KafkaClient
    '''
    return KafkaClient(hosts='127.0.0.1:9092')


@app.route("/", methods=['GET', 'POST'])
def home():
    formHastag = HastagSearchForm()
    if formHastag.validate_on_submit():
        flash(f'Validated search string {formHastag.hashtag.data}', 'success')
        connect.main(hashtag=formHastag.hashtag.data)
        return redirect(url_for('stream'))
    formUser = UserIdSearchForm()

    if formUser.validate_on_submit():
        flash(f'Validated search string {formUser.user_id.data}', 'success')
        connect.main(user_id=formUser.user_id.data)
        return redirect(url_for('user'))
    return render_template("wordcloud.html", title='Stream Tweets', hash_form=formHastag, user_form=formUser)


@app.route("/stream")
def stream():
    return render_template("stream.html")


@app.route("/user")
def user():
    return render_template("user.html")


@app.route("/tweets/<topicname>")
def get_tweets(topicname):
    '''
    yields events from kafka topic
    :param: topicname: name of the relevant topic in kafka
    :return: parsed string of message from kafka.
    '''
    client = get_kafka_client()

    def events():
        for i in client.topics[topicname].get_simple_consumer():
            yield 'data: {0}\n\n'.format(i.value.decode())

    return (Response(events(), mimetype="text/event-stream"))
