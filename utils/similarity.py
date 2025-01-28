import os
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from collections import Counter
import textract
import re

class EnhancedSimilarity:
    def __init__(self):
        # Load stopwords and initialize the vectorizer and stemmer
        self.stop_words = set(stopwords.words('english'))
        self.vectorizer = TfidfVectorizer(max_features=5000)  # Limit features to the top 5000 terms
        self.stemmer = PorterStemmer()

    def preprocess_text(self, text):
        """
        Preprocesses the input text by:
        - Lowercasing
        - Removing special characters
        - Tokenizing
        - Removing stopwords
        - Applying stemming
        """
        # Convert text to lowercase
        text = text.lower()
        # Remove special characters and numbers
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        # Tokenize text
        tokens = word_tokenize(text)
        # Remove stopwords and apply stemming
        filtered_tokens = [self.stemmer.stem(word) for word in tokens if word not in self.stop_words]
        # Join tokens back into a string
        return ' '.join(filtered_tokens)

    def extract_text_from_file(self, file_path):
        """
        Extracts text content from a file, supporting TXT, PDF, and DOCX formats.
        """
        try:
            return textract.process(file_path).decode('utf-8')
        except Exception as e:
            print(f"Error extracting text from {file_path}: {e}")
            return ""

    def calculate_similarity(self, cv_texts, jd_text):
        """
        Calculates similarity scores between a list of CV texts and a single JD text using TF-IDF and cosine similarity.
        """
        # Preprocess the input texts
        jd_text = self.preprocess_text(jd_text)
        cv_texts = [self.preprocess_text(cv) for cv in cv_texts]

        # Combine texts for TF-IDF vectorization
        all_texts = cv_texts + [jd_text]
        tfidf_matrix = self.vectorizer.fit_transform(all_texts)

        # Separate CV vectors and JD vector
        cv_vectors = tfidf_matrix[:-1]  # All but the last one
        jd_vector = tfidf_matrix[-1]   # Only the last one

        # Calculate cosine similarity
        similarity_scores = cosine_similarity(cv_vectors, jd_vector)

        return similarity_scores.flatten()

    def get_top_matches(self, cv_texts, jd_text, top_n=5):
        """
        Returns the top N matching CVs with their scores, sorted in descending order of similarity.
        """
        scores = self.calculate_similarity(cv_texts, jd_text)
        ranked_indices = np.argsort(scores)[::-1]  # Sort indices by descending score
        top_matches = [(idx, scores[idx]) for idx in ranked_indices[:top_n]]
        return top_matches

    def calculate_file_similarity(self, cv_dir, jd_file):
        """
        Compares all CVs in a directory against a given JD file and returns their similarity scores.
        """
        # Extract JD content
        jd_text = self.extract_text_from_file(jd_file)

        # Extract CV content
        cv_texts = []
        cv_filenames = []
        for cv_file in os.listdir(cv_dir):
            file_path = os.path.join(cv_dir, cv_file)
            cv_text = self.extract_text_from_file(file_path)
            if cv_text:
                cv_texts.append(cv_text)
                cv_filenames.append(cv_file)

        # Calculate similarity scores
        scores = self.calculate_similarity(cv_texts, jd_text)

        # Pair filenames with scores
        return sorted(zip(cv_filenames, scores), key=lambda x: x[1], reverse=True)

    def extract_top_keywords(self, text, top_n=10):
        """
        Extracts the top N keywords based on term frequency.
        """
        text = self.preprocess_text(text)
        word_freq = Counter(text.split())
        return word_freq.most_common(top_n)

    def get_detailed_match_report(self, cv_dir, jd_file):
        """
        Generates a detailed matching report, including similarity scores and top keywords for each CV.
        """
        jd_text = self.extract_text_from_file(jd_file)
        jd_keywords = self.extract_top_keywords(jd_text)

        results = self.calculate_file_similarity(cv_dir, jd_file)
        report = []
        for cv_file, score in results:
            cv_text = self.extract_text_from_file(os.path.join(cv_dir, cv_file))
            cv_keywords = self.extract_top_keywords(cv_text)
            report.append({
                'cv_file': cv_file,
                'score': score,
                'jd_keywords': jd_keywords,
                'cv_keywords': cv_keywords
            })
        return report
