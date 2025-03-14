import requests
from bs4 import BeautifulSoup

def fetch_article(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        paragraphs = soup.find_all('p')
        article = ' '.join([para.get_text() for para in paragraphs])
        return article
    except Exception as e:
        return f"Error: {e}"
