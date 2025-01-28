import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer, SnowballStemmer

# Ensure necessary NLTK data is downloaded
nltk.download('punkt')
nltk.download('stopwords')

class TextProcessor:
    def __init__(self, language='english'):
        """
        Initialize the TextProcessor with the specified language.
        Supported languages: 'english', 'french'.
        """
        self.language = language
        self.stop_words = set(stopwords.words(language))
        if language == 'french':
            self.stemmer = SnowballStemmer('french')
        else:
            self.stemmer = PorterStemmer()

    def preprocess_text(self, text):
        """
        Cleans and preprocesses the input text by:
        - Lowercasing
        - Removing special characters and numbers
        - Tokenizing
        - Removing stopwords
        - Applying stemming

        Parameters:
        text (str): The input text.

        Returns:
        str: The cleaned and processed text.
        """
        # Convert text to lowercase
        text = text.lower()
        # Remove special characters and numbers
        text = re.sub(r'[^a-zA-Zàâçéèêëîïôûùüÿñæœ\s]', '', text)
        # Tokenize text
        tokens = word_tokenize(text)
        # Remove stopwords and apply stemming
        filtered_tokens = [
            self.stemmer.stem(word) for word in tokens if word not in self.stop_words
        ]
        # Rejoin tokens into a single string
        return ' '.join(filtered_tokens)

    def extract_keywords(self, text, top_n=10):
        """
        Extracts the top N keywords from the text based on term frequency.

        Parameters:
        text (str): The input text.
        top_n (int): Number of top keywords to extract.

        Returns:
        list: A list of tuples containing keywords and their frequencies.
        """
        processed_text = self.preprocess_text(text)
        word_freq = nltk.FreqDist(processed_text.split())
        return word_freq.most_common(top_n)

    def compute_word_frequencies(self, text):
        """
        Computes the frequency of each word in the input text.

        Parameters:
        text (str): The input text.

        Returns:
        dict: A dictionary of word frequencies.
        """
        processed_text = self.preprocess_text(text)
        word_freq = nltk.FreqDist(processed_text.split())
        return dict(word_freq)

    def compare_texts(self, text1, text2):
        """
        Compares two texts by computing their overlapping keywords.
        Returns a list of common words and their frequencies.

        Parameters:
        text1 (str): The first input text.
        text2 (str): The second input text.

        Returns:
        dict: A dictionary of common words with their frequencies in both texts.
        """
        freq1 = self.compute_word_frequencies(text1)
        freq2 = self.compute_word_frequencies(text2)
        common_words = set(freq1.keys()) & set(freq2.keys())

        return {
            word: (freq1[word], freq2[word])
            for word in common_words
        }
