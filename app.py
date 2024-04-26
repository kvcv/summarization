from flask import Flask, render_template, request
from transformers import pipeline
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def summarize_text(text, model_name="t5-small"):
    summarization_pipeline = pipeline("summarization", model=model_name)
    summarized_text = summarization_pipeline(text, max_length=150, min_length=30, do_sample=False)[0]['summary_text']
    return summarized_text

def fetch_article(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    article_text = ' '.join([p.text.strip() for p in soup.find_all('p')])
    return article_text

@app.route('/')
def inputs():
    return render_template('inputs.html')

@app.route('/summary', methods=['POST'])
def summary():
    if request.method == 'POST':
        url = request.form.get("url")
        text = fetch_article(url)
        summary = summarize_text(text)
        return render_template("inputs.html", news=text, summary=summary)
    return render_template("inputs.html")

if __name__ == "__main__":
    app.run(debug=True)