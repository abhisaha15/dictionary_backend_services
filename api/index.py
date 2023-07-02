from flask import Flask
from dictionary_scraper import process_word

app=Flask(__name__)



@app.route('/')
@app.route('/<string:word>')


def home(word=" "):
    output = process_word(word)
    return output.get_output()



if __name__== "__main__":
    app.run(debug=True)