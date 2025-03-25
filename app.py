from flask import Flask, render_template, request, jsonify
import json
import test_scraper  # Import your existing scraper script

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/fetch_news', methods=['POST'])
def fetch_news():
    data = request.json
    topic = data.get('topic')

    if not topic:
        return jsonify({"error": "Please enter a topic!"}), 400

    articles = test_scraper.fetch_news(topic)
    test_scraper.save_news_data(articles)
    test_scraper.text_to_speech(articles)  # Generate audio summary

    return jsonify({"articles": articles, "audio": "news_audio.mp3"})

if __name__ == '__main__':
    app.run(debug=True)
