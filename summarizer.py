from transformers import pipeline
from textblob import TextBlob
import spacy

# Load BART model
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# Load SpaCy for NER
nlp = spacy.load("en_core_web_sm")

# Generate summary
from transformers import pipeline

# Load model on CPU
summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=-1)

def generate_summary(article):
    if not article:
        return "No article content found"
    
    if len(article.split()) < 50:
        return "Article too short to summarize"

    # Limit input length to 512 tokens
    article = " ".join(article.split()[:512])

    try:
        summary = summarizer(
            article,
            max_length=min(512, int(len(article.split()) * 0.3)),
            min_length=20,
            do_sample=False
        )[0]['summary_text']
        return summary
    except Exception as e:
        print(f"Error during summarization: {e}")
        return f"Failed to summarize article: {e}"

# Sentiment analysis
def analyze_sentiment(article):
    sentiment = TextBlob(article).sentiment
    return {
        'polarity': sentiment.polarity,
        'subjectivity': sentiment.subjectivity
    }

# Named Entity Recognition (NER)
def extract_entities(article):
    doc = nlp(article)
    entities = [(entity.text, entity.label_) for entity in doc.ents]
    return entities
