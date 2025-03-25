import requests
from newspaper import Article
from bs4 import BeautifulSoup
from utils import get_news_articles, analyze_sentiment  # Import functions
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
import json
from text_to_speech import text_to_speech, play_audio  # Import TTS functions

def save_to_json(data, filename="news_data.json"):
    """Save summarized news to a JSON file."""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"\n✅ Data saved to {filename}\n")

def summarize_text(text, num_sentences=3):
    """Summarizes text using LSA (Latent Semantic Analysis)."""
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, num_sentences)

    return " ".join(str(sentence) for sentence in summary)

def fetch_article_summary(url):
    """Fetch and summarize article content."""
    try:
        article = Article(url)
        article.download()
        article.parse()

        if len(article.text) > 500:
            return summarize_text(article.text)  # Use LSA summarization
        
        raise ValueError("Article too short")

    except:
        # Fallback using BeautifulSoup
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            paragraphs = soup.find_all("p")

            if paragraphs:
                text = " ".join(p.text for p in paragraphs[:5])
                return summarize_text(text)

    return "Could not fetch article content."

def main():
    company = "Tesla"  # Change this to any company name
    articles = get_news_articles(company)

    if not articles:
        print(f"No news articles found for {company}.")
        return

    news_data = []  # Store processed articles
    combined_summaries = ""  # Store all summaries for TTS

    print(f"\nNews articles for {company}:\n")
    for i, article in enumerate(articles, 1):
        title = article.get("title", "No Title Available")
        url = article.get("url", "#")
        summary = fetch_article_summary(url)
        sentiment = analyze_sentiment(summary)

        article_data = {
            "title": title,
            "summary": summary,
            "sentiment": sentiment,
            "url": url
        }
        news_data.append(article_data)

        combined_summaries += f"Article {i}: {title}. {summary}.\n\n"

        print("---------------------------------")
        print(f"Article {i}:")
        print(f"Title: {title}")
        print(f"Summary: {summary[:300]}...")  # Display first 300 characters
        print(f"Sentiment: {sentiment}")
        print(f"URL: {url}")
        print("---------------------------------\n")

    # ✅ Save summarized news to JSON
    save_to_json(news_data)

    # ✅ Convert summarized news to speech
    text_to_speech(combined_summaries)

    # ✅ Play the audio
    play_audio()

if __name__ == "__main__":
    main()
