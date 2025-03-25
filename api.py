from flask import Flask, request, jsonify
from utils import fetch_news, analyze_sentiment, generate_tts  # Import utility functions

app = Flask(__name__)

@app.route('/fetch_news', methods=['GET'])
def fetch_news_api():
    """Fetches news articles related to the given company"""
    company = request.args.get('company')
    if not company:
        return jsonify({"error": "Company name is required"}), 400

    articles = fetch_news(company)  # Call function from utils.py
    response = {
        "company": company,
        "articles": articles
    }
    return jsonify(response)

@app.route('/analyze_sentiment', methods=['POST'])
def analyze_sentiment_api():
    """Analyzes sentiment of the given articles"""
    data = request.json
    if not data or "articles" not in data:
        return jsonify({"error": "Invalid input"}), 400

    sentiment_results = analyze_sentiment(data["articles"])
    response = {
        "company": data.get("company", "Unknown"),
        "sentiment_distribution": sentiment_results
    }
    return jsonify(response)

@app.route('/generate_tts', methods=['POST'])
def generate_tts_api():
    """Generates Hindi text-to-speech output for given text"""
    data = request.json
    if not data or "text" not in data:
        return jsonify({"error": "Text input is required"}), 400

    audio_path = generate_tts(data["text"])
    response = {"audio_url": audio_path}
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
