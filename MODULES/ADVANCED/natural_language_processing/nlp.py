"""
MODULE #29: NATURAL LANGUAGE PROCESSING
Instance 3: Module Developer
Built: 2025-11-08

Text analysis, sentiment detection, entity extraction, text generation.
"""

import re
import json
from typing import List, Dict, Tuple, Set
from dataclasses import dataclass
from collections import Counter, defaultdict
import numpy as np


@dataclass
class Token:
    """A tokenized word"""
    text: str
    pos: str  # part of speech
    lemma: str


@dataclass
class Entity:
    """Named entity"""
    text: str
    type: str
    start: int
    end: int


class NLPProcessor:
    """
    Natural Language Processing toolkit

    Features:
    - Tokenization
    - Sentiment analysis
    - Entity extraction
    - Text similarity
    - Keyword extraction
    """

    def __init__(self):
        self.stopwords = self._load_stopwords()
        self.sentiment_lexicon = self._load_sentiment_lexicon()

    def _load_stopwords(self) -> Set[str]:
        """Load common stopwords"""
        return {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'been',
            'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
            'could', 'should', 'may', 'might', 'must', 'can', 'this', 'that',
            'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they'
        }

    def _load_sentiment_lexicon(self) -> Dict[str, float]:
        """Load sentiment words with scores"""
        return {
            # Positive
            'good': 1.0, 'great': 1.5, 'excellent': 2.0, 'amazing': 2.0,
            'wonderful': 1.5, 'fantastic': 2.0, 'love': 1.5, 'best': 2.0,
            'awesome': 1.5, 'beautiful': 1.0, 'perfect': 2.0, 'happy': 1.0,
            # Negative
            'bad': -1.0, 'terrible': -2.0, 'awful': -2.0, 'horrible': -2.0,
            'worst': -2.0, 'hate': -1.5, 'poor': -1.0, 'sad': -1.0,
            'angry': -1.5, 'disappointing': -1.0, 'useless': -1.5,
        }

    def tokenize(self, text: str) -> List[str]:
        """Simple tokenization"""
        text = text.lower()
        text = re.sub(r'[^\w\s]', ' ', text)
        tokens = text.split()
        return [t for t in tokens if t]

    def remove_stopwords(self, tokens: List[str]) -> List[str]:
        """Remove common stopwords"""
        return [t for t in tokens if t not in self.stopwords]

    def sentiment_analysis(self, text: str) -> Dict[str, float]:
        """
        Analyze sentiment of text

        Returns:
            Score (-1 to 1), magnitude, classification
        """

        tokens = self.tokenize(text)

        # Calculate sentiment score
        scores = [self.sentiment_lexicon.get(t, 0) for t in tokens]

        if not scores:
            return {'score': 0.0, 'magnitude': 0.0, 'label': 'neutral'}

        # Average score
        score = np.mean(scores)

        # Magnitude (strength)
        magnitude = np.mean(np.abs(scores))

        # Classification
        if score > 0.3:
            label = 'positive'
        elif score < -0.3:
            label = 'negative'
        else:
            label = 'neutral'

        return {
            'score': float(score),
            'magnitude': float(magnitude),
            'label': label
        }

    def extract_entities(self, text: str) -> List[Entity]:
        """
        Extract named entities (simplified)

        Real implementation would use NER model
        """

        entities = []

        # Capitalized words (potential names/places)
        words = text.split()
        for i, word in enumerate(words):
            if word and word[0].isupper() and len(word) > 1:
                # Check if not start of sentence
                if i > 0:
                    entities.append(Entity(
                        text=word,
                        type='ENTITY',
                        start=sum(len(w) + 1 for w in words[:i]),
                        end=sum(len(w) + 1 for w in words[:i]) + len(word)
                    ))

        # Dates (simple pattern)
        date_pattern = r'\b\d{4}-\d{2}-\d{2}\b'
        for match in re.finditer(date_pattern, text):
            entities.append(Entity(
                text=match.group(),
                type='DATE',
                start=match.start(),
                end=match.end()
            ))

        return entities

    def extract_keywords(self, text: str, top_n: int = 5) -> List[Tuple[str, float]]:
        """Extract important keywords using TF-IDF-like approach"""

        tokens = self.tokenize(text)
        tokens = self.remove_stopwords(tokens)

        # Count term frequency
        tf = Counter(tokens)

        # Filter short words
        tf = {k: v for k, v in tf.items() if len(k) > 3}

        # Get top N
        keywords = tf.most_common(top_n)

        # Normalize scores
        if keywords:
            max_count = keywords[0][1]
            keywords = [(word, count / max_count) for word, count in keywords]

        return keywords

    def cosine_similarity(self, text1: str, text2: str) -> float:
        """Calculate cosine similarity between two texts"""

        # Tokenize
        tokens1 = self.tokenize(text1)
        tokens2 = self.tokenize(text2)

        # Create vocabulary
        vocab = set(tokens1 + tokens2)

        # Create vectors
        vec1 = [tokens1.count(w) for w in vocab]
        vec2 = [tokens2.count(w) for w in vocab]

        # Calculate cosine similarity
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        mag1 = np.sqrt(sum(a**2 for a in vec1))
        mag2 = np.sqrt(sum(b**2 for b in vec2))

        if mag1 == 0 or mag2 == 0:
            return 0.0

        return dot_product / (mag1 * mag2)

    def word_frequency(self, text: str, top_n: int = 10) -> List[Tuple[str, int]]:
        """Get most frequent words"""

        tokens = self.tokenize(text)
        tokens = self.remove_stopwords(tokens)

        freq = Counter(tokens)

        return freq.most_common(top_n)

    def extract_ngrams(self, text: str, n: int = 2, top_k: int = 5) -> List[Tuple[str, int]]:
        """Extract n-grams (phrases)"""

        tokens = self.tokenize(text)

        # Generate n-grams
        ngrams = []
        for i in range(len(tokens) - n + 1):
            ngram = ' '.join(tokens[i:i+n])
            ngrams.append(ngram)

        # Count frequency
        freq = Counter(ngrams)

        return freq.most_common(top_k)


def demo():
    """Demonstrate NLP capabilities"""

    print("=" * 60)
    print("NATURAL LANGUAGE PROCESSING DEMO")
    print("=" * 60)
    print()

    nlp = NLPProcessor()

    # Test text
    text1 = "This is an excellent product! I love it. The quality is amazing and the price is great."
    text2 = "Terrible experience. The worst purchase I've ever made. Very disappointing."
    text3 = "The product arrived on 2025-11-08. John Smith from New York was very helpful."

    # Sentiment analysis
    print("SENTIMENT ANALYSIS:")
    print()
    print(f"Text: {text1}")
    sentiment = nlp.sentiment_analysis(text1)
    print(f"Score: {sentiment['score']:.2f}, Label: {sentiment['label']}")
    print()

    print(f"Text: {text2}")
    sentiment = nlp.sentiment_analysis(text2)
    print(f"Score: {sentiment['score']:.2f}, Label: {sentiment['label']}")
    print()

    # Entity extraction
    print("ENTITY EXTRACTION:")
    print()
    print(f"Text: {text3}")
    entities = nlp.extract_entities(text3)
    for ent in entities:
        print(f"  {ent.text} ({ent.type})")
    print()

    # Keyword extraction
    print("KEYWORD EXTRACTION:")
    print()
    long_text = "Machine learning and artificial intelligence are transforming technology. Deep learning models can learn patterns from data automatically."
    keywords = nlp.extract_keywords(long_text, top_n=3)
    print(f"Text: {long_text}")
    print(f"Keywords: {', '.join([k for k, s in keywords])}")
    print()

    # Text similarity
    print("TEXT SIMILARITY:")
    print()
    text_a = "I love machine learning and AI"
    text_b = "Artificial intelligence and ML are amazing"
    text_c = "I enjoy cooking and baking"
    sim_ab = nlp.cosine_similarity(text_a, text_b)
    sim_ac = nlp.cosine_similarity(text_a, text_c)
    print(f"Text A: {text_a}")
    print(f"Text B: {text_b}")
    print(f"Similarity: {sim_ab:.3f}")
    print()
    print(f"Text A: {text_a}")
    print(f"Text C: {text_c}")
    print(f"Similarity: {sim_ac:.3f}")
    print()

    print("=" * 60)
    print("NLP DEMO COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    demo()
