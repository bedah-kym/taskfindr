# blog/plagiarism_detection.py
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

nltk.download('punkt')
nltk.download('stopwords')

def calculate_similarity(text1, text2):
    # Tokenize and preprocess the text
    tokens1 = preprocess_text(text1)
    tokens2 = preprocess_text(text2)

    # Calculate Jaccard similarity
    jaccard_similarity = calculate_jaccard_similarity(tokens1, tokens2)

    return jaccard_similarity

def preprocess_text(text):
    # Tokenize the text
    tokens = word_tokenize(text)

    # Remove stopwords and punctuation
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word.lower() not in stop_words and word.isalnum()]

    # Stem words
    stemmer = PorterStemmer()
    tokens = [stemmer.stem(word) for word in tokens]

    return set(tokens)

def calculate_jaccard_similarity(tokens1, tokens2):
    intersection = len(tokens1.intersection(tokens2))
    union = len(tokens1.union(tokens2))
    similarity = intersection / union if union != 0 else 0
    return similarity
