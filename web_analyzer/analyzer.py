import requests
from bs4 import BeautifulSoup
import re
import spacy
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

nlp = spacy.load("en_core_web_md")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/123.0.0.0 Safari/537.36"
}

def extract_entities(text):
    doc = nlp(text)
    return {
        "persons": list({ent.text for ent in doc.ents if ent.label_ == "PERSON"}),
        "organizations": list({ent.text for ent in doc.ents if ent.label_ == "ORG"}),
        "locations": list({ent.text for ent in doc.ents if ent.label_ in ("GPE", "LOC")})
    }

def summarize_text(text, sentence_count=5):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summary = LsaSummarizer()(parser.document, sentence_count)
    return " ".join(str(sentence) for sentence in summary)

def extract_from_url(url):
    try:
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code != 200:
            return None

        soup = BeautifulSoup(res.text, 'html.parser')
        text = re.sub(r'[^a-zA-Z0-9 .,]', '', soup.get_text(separator=' ', strip=True))
        return {
            "url": url,
            "entities": extract_entities(text),
            "topics": [],
            "summary": summarize_text(text)
        }
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None