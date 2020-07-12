from flask import request
from flask import jsonify
from flask import Flask, render_template, url_for
import re
import transformers
import requests
from bs4 import BeautifulSoup
from transformers import pipeline
import time
from rq import Queue
from worker import conn
from tasks import predictions

q = Queue(connection=conn)

app=Flask(__name__)

@app.route('/')
def index():
    return render_template('text_sum.html')

@app.route('/pred', methods=['POST'])
def pred():
    if request.method=='POST':
        links=q.enqueue(get_links)
        heading=q.enqueue(headings, links)
        head_sum, text_sum = q.enqueue(predictions, links, headings)
 
    return render_template('text_sum.html', head_sum=head_sum, text_sum=text_sum)

if __name__=='__main__':
    app.run() #add threaded=True