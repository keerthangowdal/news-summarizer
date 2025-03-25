import requests
from bs4 import BeautifulSoup
from newspaper import Article
import time
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize
nltk.download('punkt')  # Ensure word_tokenizer data is available


# Download the VADER lexicon for sentiment analysis (only required once)
nltk.download("vader_lexicon")

# Initialize Sentiment Analyzer
sia = SentimentIntensityAnalyzer()

def get_news_articles(company_name):
    """Fetch news articles from Bing and Google News."""
    
    # Bing News
    bing_url = f"https://www.bing.com/news/search?q={company_name}"
    
    # Google News
    google_url = f"https://news.google.com/search?q={company_name}&hl=en-US&gl=US&ceid=US:en"

    headers = {"User-Agent": "Mozilla/5.0"}
    
    articles = []
    
    # Fetch from Bing News
    response = requests.get(bing_url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        for item in soup.select("a.title")[:5]:
            title = item.get_text().strip()
            news_url = item["href"]
            if title and news_url.startswith("http"):
                articles.append({"title": title, "url": news_url})

    # Fetch from Google News
    response = requests.get(google_url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        for item in soup.select("article h3 a")[:5]:  # Google News structure
            title = item.get_text().strip()
            news_url = "https://news.google.com" + item["href"][1:]  # Google uses relative URLs
            articles.append({"title": title, "url": news_url})

    return articles


def analyze_sentiment(text):
    """Analyzes sentiment using VADER, ensuring enough words for accuracy."""
    words = word_tokenize(text)

    if len(words) < 30:  # Require at least 30 words for accuracy
        return "Not enough data for sentiment analysis ❓"

    sentiment_score = sia.polarity_scores(text)["compound"]

    if sentiment_score >= 0.05:
        return "Positive 😀"
    elif sentiment_score <= -0.05:
        return "Negative 😠"
    else:
        return "Neutral 😐"