from flask import render_template
from main import app

@app.route("/")
def hello():
    return render_template("wordcloud.html")