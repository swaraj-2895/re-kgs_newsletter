from flask import request
from flask import jsonify
from flask import Flask, render_template, url_for
import transformers
import requests
from bs4 import BeautifulSoup
from transformers import pipeline
import time


def get_links():
    links=[]
    source_link='https://www.retaildive.com'
    htmlfile=requests.get(source_link).text
    soup=BeautifulSoup(htmlfile,'lxml')
    article_others=soup.find_all('div', class_='medium-8 columns')
    for article in article_others[:5]:    
       links.append(source_link+article.a['href'])
    return links



def headings(links):
  head_sum=[]
  for link in links:
      htmlfile_source=requests.get(link).text
      soup=BeautifulSoup(htmlfile_source,'lxml')
      article_head=soup.find('h1', class_='display-heading-04').text.strip()
      head_sum.append(article_head) 
  return (head_sum)
  

    
def predictions(links, head_sum):
    text_sum=[]
    summarizer=pipeline("summarization")
    for link in links:
          try:  
                htmlfile=requests.get(link).text
                soup=BeautifulSoup(htmlfile,'lxml')
                article_body=soup.find('div', class_='article-large-10 columns article-wrapper')
                article_head=soup.find('h1', class_='display-heading-04')
                articles=article_body.find_all('p')
                sentences=[]
                articles_to_sum=""
                final_article=[]
                for art in articles[:10]:
                    articles_to_sum=articles_to_sum+" "+art.text
                text=summarizer(articles_to_sum, max_len=120, min_len=30)
                for i in text:
                    for key, value in i.items():
                        text_sum.append(value)
                
          except:  
                print("Connection refused by the server..")
                print("Let me sleep for 5 seconds")
                print("ZZzzzz...")
                print("Was a nice sleep, now let me continue...")
                continue
    return (head_sum, text_sum)