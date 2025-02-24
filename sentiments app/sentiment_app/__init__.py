from flask import Flask

app = Flask(__name__)

app.config['SECRET_KEY'] = '3e10d17801e0e6449b1b978f731f5816'

from sentiment_app import routes