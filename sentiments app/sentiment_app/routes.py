from sentiment_app import app
from flask import render_template
from sentiment_app.forms import TextForm
from textblob import TextBlob

@app.route("/",methods=['POST','GET'])
def index():
    sentiment = None
    form = TextForm()
    if form.validate_on_submit():
        text = form.text.data
        analysize = TextBlob(text)
        polarity = analysize.sentiment.polarity

        if polarity > 0:
            sentiment = "Positive \U0001f600"
        elif polarity < 0:
            sentiment = "Negative \U0001F641"
        else:
            sentiment = "Neutral \U0001F610"
    return render_template('index.html',form = form, sentiment = sentiment)