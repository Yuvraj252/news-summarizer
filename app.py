from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId
from scraper import fetch_article
from summarizer import generate_summary, analyze_sentiment, extract_entities

app = Flask(__name__)
CORS(app)

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['summarizer']
collection = db['summaries']

# Function to convert ObjectId to string
def convert_objectid(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    if isinstance(obj, dict):
        return {k: convert_objectid(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [convert_objectid(i) for i in obj]
    return obj

@app.route('/summarize', methods=['POST'])
def summarize():
    data = request.json
    url = data.get('url')
    article = fetch_article(url)
    if article.startswith("Error"):
        return jsonify({'error': article}), 400
    
    summary = generate_summary(article)
    sentiment = analyze_sentiment(article)
    entities = extract_entities(article)

    result = {
        'summary': summary,
        'sentiment': sentiment,
        'entities': entities
    }

    # Save to MongoDB (after converting ObjectId)
    inserted_id = collection.insert_one(result).inserted_id
    result['_id'] = inserted_id

    # Convert ObjectId before returning
    return jsonify(convert_objectid(result))

if __name__ == '__main__':
    app.run(debug=True)
