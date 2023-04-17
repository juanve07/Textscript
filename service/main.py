from fastapi import FastAPI
import dill
import os
import numpy as np
import uvicorn
from pydantic import BaseModel
import pandas as pd
import spacy 
from sentence_transformers import SentenceTransformer
import pickle 
import spacy
import re
from bs4 import BeautifulSoup
import bs4 as bs4
from urllib.parse import urlparse
import requests
from collections import Counter
import sqlite3


PKL_FILENAME = "website_classification.pkl"
MODELS_PATH = "./Models/"
MODEL_FILE_PATH = os.path.join(MODELS_PATH,PKL_FILENAME)
SENTENCE_BERT = SentenceTransformer('paraphrase-distilroberta-base-v1')
nlp = spacy.load('en_core_web_sm')


def load_model():
    with open(MODEL_FILE_PATH,'rb') as file:
        return dill.load(file)

LOADED_MODEL = load_model()

app = FastAPI(title="LinkScribe", description="Aplicación web que utiliza NLP para permitir a los usuarios crear listas de enlaces de forma fácil y eficiente")


class Data(BaseModel):
    text:str

class ScrapTool:
    def visit_url(self, website_url):
        '''
        Visit URL. Download the Content. Initialize the beautifulsoup object. Call parsing methods. Return Series object.
        '''
        #headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}
        content = requests.get(website_url,timeout=60).content
        
        #lxml is apparently faster than other settings.
        soup = BeautifulSoup(content, "lxml")
        result = {
            "website_url": website_url,
            "website_name": self.get_website_name(website_url),
            "website_text": self.get_html_title_tag(soup)+self.get_html_meta_tags(soup)+self.get_html_heading_tags(soup)+
                                                               self.get_text_content(soup)
        }
        
        #Convert to Series object and return
        return pd.Series(result)
    
    def get_website_name(self,website_url):
        '''
        Example: returns "google" from "www.google.com"
        '''
        return "".join(urlparse(website_url).netloc.split(".")[-2])
    
    def get_html_title_tag(self,soup):
        '''Return the text content of <title> tag from a webpage'''
        return '. '.join(soup.title.contents)
    
    def get_html_meta_tags(self,soup):
        '''Returns the text content of <meta> tags related to keywords and description from a webpage'''
        tags = soup.find_all(lambda tag: (tag.name=="meta") & (tag.has_attr('name') & (tag.has_attr('content'))))
        content = [str(tag["content"]) for tag in tags if tag["name"] in ['keywords','description']]
        return ' '.join(content)
    
    def get_html_heading_tags(self,soup):
        '''returns the text content of heading tags. The assumption is that headings might contain relatively important text.'''
        tags = soup.find_all(["h1","h2","h3","h4","h5","h6"])
        content = [" ".join(tag.stripped_strings) for tag in tags]
        return ' '.join(content)
    
    def get_text_content(self,soup):
        '''returns the text content of the whole page with some exception to tags. See tags_to_ignore.'''
        tags_to_ignore = ['style', 'script', 'head', 'title', 'meta', '[document]',"h1","h2","h3","h4","h5","h6","noscript"]
        tags = soup.find_all(text=True)
        result = []
        for tag in tags:
            stripped_tag = tag.strip()
            if tag.parent.name not in tags_to_ignore\
                and isinstance(tag, bs4.element.Comment)==False\
                and not stripped_tag.isnumeric()\
                and len(stripped_tag)>0:
                result.append(stripped_tag)
        return ' '.join(result)

@app.get("/")
def read_root():
    return {"message": "Welcome from the API"}

#@app.post("/predict")
def predict(url):
    prediction = LOADED_MODEL.predict([url])
    prediction_str = prediction[0]
    scrapTool = ScrapTool()
    web = dict(scrapTool.visit_url(url))
    url_web = web['website_url']
    name = web['website_name']
    text = web['website_text']
    return {
        "Url" : url_web,
        "Name" : name,
        "text" : text,
        "prediction": prediction_str,
    }
if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)