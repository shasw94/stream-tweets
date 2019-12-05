from flask import Flask, render_template
app = Flask(__name__)

app.config['SECRET_KEY'] = '04c45ebc6159ed5d60be3fbf273a4b37'

from main import routes