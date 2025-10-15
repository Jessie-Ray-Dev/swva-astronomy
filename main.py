from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/articles')
def articles():
    return "This is where articles go"

@app.route('/about')
def about():
    return render_template("about.html")