import re
import json
import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
import lxml
from flask import Flask
#from dictionary_scraper import process_word

app=Flask(__name__)

class process_word:

    def __init__(self, word):
        self.word = word
        self.url_1 = "https://www.yourdictionary.com/{}".format(word)
        self.url_2 = "https://thesaurus.yourdictionary.com/{}".format(word)
        self.url_3 = "https://sentence.yourdictionary.com/{}".format(word)
        self.meanings = []
        self.synonyms = []
        self.antonyms = []
        self.sentance = []

    def get_meanings(self):
        webpage = requests.get(self.url_1).text
        soup = bs(webpage, 'lxml')
        res = soup.find_all('div', class_="definition-cluster")
        for i in res:
            try:
                self.meanings.append((i.find('div', class_="text-base")).text.strip())
            except:
                break

    def get_synonyms_antonyms(self):
        webpage = requests.get(self.url_2).text
        soup = bs(webpage, 'lxml')

        res = soup.find_all('div', class_="mt-3")
        for i in res:
            for j in i.find_all('li'):
                self.synonyms.append(j.text.strip())

        res = soup.find_all('div', class_="mt-4")
        for i in res:
            for j in i.find_all('li'):
                self.antonyms.append(j.text.strip())

        self.synonyms = list(set(self.synonyms))  # removing duplicate values if any
        self.antonyms = list(set(self.antonyms))  # removing duplicate values if any

    def get_sentance_applications(self):
        webpage = requests.get(self.url_3).text
        soup = bs(webpage, 'lxml')
        res = soup.find_all('div', class_="sentence-item")
        sentance_max_count = 5  # taking maximun 5 examples
        for i in res:
            if sentance_max_count > 0:
                for j in i.find_all('p'):
                    self.sentance.append(j.text.strip())
            else:
                break
            sentance_max_count -= 1

    def execute(self):
        self.get_meanings()
        self.get_synonyms_antonyms()
        self.get_sentance_applications()

    def get_output(self):
        self.execute()
        return {
            "word": self.word,
            "meanings": self.meanings,
            "synonyms": self.synonyms,
            "antonyms": self.antonyms,
            "sentance_application": self.sentance
        }

@app.route('/')
@app.route('/<string:word>')


def home(word=" "):
    output = process_word(word)
    return output.get_output()



if __name__== "__main__":
    app.run(debug=True)

