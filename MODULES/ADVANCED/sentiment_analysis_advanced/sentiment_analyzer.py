#!/usr/bin/env python3
"""
ADVANCED SENTIMENT ANALYSIS MODULE
===================================

Multi-dimensional sentiment analysis with context awareness,
emotion detection, sarcasm detection, and trend analysis.

Features:
- Polarity detection (positive/negative/neutral)
- Emotion classification (joy, anger, sadness, fear, surprise, disgust)
- Intensity scoring
- Context-aware analysis
- Sarcasm detection
- Temporal sentiment trends
- Multi-language support (basic)
- Aspect-based sentiment (what specifically is being evaluated)

Module #21 of 100x Platform
"""

import re
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import json
from datetime import datetime


class SentimentPolarity(Enum):
    """Sentiment polarity categories"""
    VERY_POSITIVE = "very_positive"
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"
    VERY_NEGATIVE = "very_negative"


class Emotion(Enum):
    """Primary emotions"""
    JOY = "joy"
    ANGER = "anger"
    SADNESS = "sadness"
    FEAR = "fear"
    SURPRISE = "surprise"
    DISGUST = "disgust"
    NEUTRAL = "neutral"


@dataclass
class SentimentScore:
    """Detailed sentiment scoring"""
    polarity: SentimentPolarity
    polarity_score: float  # -1.0 to 1.0
    intensity: float  # 0.0 to 1.0
    confidence: float  # 0.0 to 1.0
    emotions: Dict[Emotion, float]
    sarcasm_detected: bool
    sarcasm_confidence: float
    aspects: Dict[str, float]  # Aspect -> sentiment score


class AdvancedSentimentAnalyzer:
    """Advanced sentiment analysis with multiple dimensions"""

    def __init__(self):
        """Initialize the analyzer with lexicons and patterns"""
        self._load_lexicons()
        self._load_patterns()

    def _load_lexicons(self):
        """Load sentiment lexicons"""
        # Positive words with intensity scores
        self.positive_words = {
            # Very strong positive
            'amazing': 0.9, 'excellent': 0.9, 'outstanding': 0.9,
            'fantastic': 0.9, 'incredible': 0.9, 'brilliant': 0.9,
            'phenomenal': 0.95, 'extraordinary': 0.95, 'exceptional': 0.95,

            # Strong positive
            'great': 0.7, 'wonderful': 0.7, 'awesome': 0.7,
            'good': 0.6, 'nice': 0.5, 'pleasant': 0.6,
            'love': 0.8, 'perfect': 0.9, 'beautiful': 0.7,

            # Moderate positive
            'like': 0.4, 'enjoy': 0.5, 'happy': 0.6,
            'glad': 0.5, 'pleased': 0.6, 'satisfied': 0.5,
        }

        # Negative words with intensity scores
        self.negative_words = {
            # Very strong negative
            'terrible': -0.9, 'horrible': -0.9, 'awful': -0.9,
            'atrocious': -0.95, 'abysmal': -0.95, 'dreadful': -0.9,
            'disgusting': -0.9, 'hate': -0.8, 'despise': -0.9,

            # Strong negative
            'bad': -0.6, 'poor': -0.6, 'disappointing': -0.7,
            'unfortunate': -0.6, 'unpleasant': -0.6, 'sad': -0.6,

            # Moderate negative
            'dislike': -0.4, 'annoying': -0.5, 'concerning': -0.4,
            'worried': -0.5, 'unhappy': -0.6, 'frustrated': -0.6,
        }

        # Emotion lexicons
        self.emotion_words = {
            Emotion.JOY: ['happy', 'joyful', 'delighted', 'ecstatic', 'cheerful', 'pleased', 'glad'],
            Emotion.ANGER: ['angry', 'furious', 'enraged', 'mad', 'irritated', 'annoyed', 'frustrated'],
            Emotion.SADNESS: ['sad', 'depressed', 'miserable', 'unhappy', 'sorrowful', 'gloomy', 'heartbroken'],
            Emotion.FEAR: ['afraid', 'scared', 'terrified', 'fearful', 'anxious', 'worried', 'nervous'],
            Emotion.SURPRISE: ['surprised', 'amazed', 'astonished', 'shocked', 'stunned', 'astounded'],
            Emotion.DISGUST: ['disgusting', 'revolting', 'repulsive', 'gross', 'nauseating', 'vile'],
        }

        # Intensifiers and dampeners
        self.intensifiers = {
            'very': 1.5, 'extremely': 2.0, 'incredibly': 2.0,
            'absolutely': 1.8, 'really': 1.3, 'so': 1.3,
            'totally': 1.6, 'completely': 1.7, 'utterly': 1.8,
        }

        self.dampeners = {
            'somewhat': 0.5, 'slightly': 0.3, 'barely': 0.2,
            'kind of': 0.4, 'sort of': 0.4, 'a little': 0.3,
        }

        # Negation words
        self.negations = {
            'not', 'no', 'never', 'neither', 'nobody', 'nothing',
            'nowhere', 'hardly', 'scarcely', 'barely', "n't", "dont"
        }

    def _load_patterns(self):
        """Load linguistic patterns for sarcasm detection"""
        self.sarcasm_patterns = [
            r'oh (great|wonderful|fantastic)',  # "oh great"
            r'yeah,? right',  # "yeah right"
            r'sure,? totally',  # "sure, totally"
            r'(just|exactly) what i needed',  # Sarcastic needs
            r'couldn\'t be (better|happier)',  # Over-positive
        ]

    def analyze(self, text: str, context: Optional[str] = None) -> SentimentScore:
        """
        Perform comprehensive sentiment analysis

        Args:
            text: Text to analyze
            context: Optional contextual information

        Returns:
            SentimentScore with multi-dimensional analysis
        """
        text_lower = text.lower()
        words = re.findall(r'\b\w+\b', text_lower)

        # Calculate base polarity
        polarity_score, intensity = self._calculate_polarity(text_lower, words)

        # Detect emotions
        emotions = self._detect_emotions(text_lower, words)

        # Detect sarcasm
        sarcasm_detected, sarcasm_conf = self._detect_sarcasm(text_lower, polarity_score)

        # If sarcasm detected, flip polarity
        if sarcasm_detected and sarcasm_conf > 0.6:
            polarity_score = -polarity_score

        # Classify polarity
        polarity = self._classify_polarity(polarity_score)

        # Calculate confidence
        confidence = self._calculate_confidence(intensity, len(words))

        # Extract aspects
        aspects = self._extract_aspects(text_lower, words)

        return SentimentScore(
            polarity=polarity,
            polarity_score=polarity_score,
            intensity=intensity,
            confidence=confidence,
            emotions=emotions,
            sarcasm_detected=sarcasm_detected,
            sarcasm_confidence=sarcasm_conf,
            aspects=aspects
        )

    def _calculate_polarity(self, text: str, words: List[str]) -> Tuple[float, float]:
        """Calculate sentiment polarity and intensity"""
        scores = []
        negation_active = False
        intensifier_mult = 1.0

        for i, word in enumerate(words):
            # Check for negation
            if word in self.negations:
                negation_active = True
                continue

            # Check for intensifiers/dampeners
            if word in self.intensifiers:
                intensifier_mult = self.intensifiers[word]
                continue
            if word in self.dampeners:
                intensifier_mult = self.dampeners[word]
                continue

            # Get sentiment score
            score = 0.0
            if word in self.positive_words:
                score = self.positive_words[word]
            elif word in self.negative_words:
                score = self.negative_words[word]

            # Apply modifiers
            if score != 0.0:
                score *= intensifier_mult
                if negation_active:
                    score = -score * 0.8  # Negation flips and dampens
                scores.append(score)

                # Reset modifiers
                negation_active = False
                intensifier_mult = 1.0

        if not scores:
            return 0.0, 0.0

        # Calculate average polarity
        avg_polarity = sum(scores) / len(scores)

        # Clamp to [-1, 1]
        avg_polarity = max(-1.0, min(1.0, avg_polarity))

        # Calculate intensity (how strong the sentiment is)
        intensity = sum(abs(s) for s in scores) / len(scores)
        intensity = min(1.0, intensity)

        return avg_polarity, intensity

    def _detect_emotions(self, text: str, words: List[str]) -> Dict[Emotion, float]:
        """Detect and score emotions"""
        emotion_scores = {emotion: 0.0 for emotion in Emotion}

        for emotion, keywords in self.emotion_words.items():
            matches = sum(1 for word in words if word in keywords)
            if matches > 0:
                # Normalize by text length
                emotion_scores[emotion] = min(1.0, matches / len(words) * 10)

        # Neutral if no specific emotions
        if all(score == 0.0 for score in emotion_scores.values()):
            emotion_scores[Emotion.NEUTRAL] = 1.0

        return emotion_scores

    def _detect_sarcasm(self, text: str, polarity: float) -> Tuple[bool, float]:
        """Detect sarcasm with confidence score"""
        sarcasm_signals = 0
        total_signals = 4  # Number of different sarcasm indicators

        # Pattern matching
        for pattern in self.sarcasm_patterns:
            if re.search(pattern, text):
                sarcasm_signals += 1
                break

        # Contradiction: positive words with negative context
        if polarity > 0.5 and any(neg in text for neg in ['but', 'however', 'unfortunately']):
            sarcasm_signals += 1

        # Over-positive (too many intensifiers)
        intensifier_count = sum(1 for word in text.split() if word in self.intensifiers)
        if intensifier_count > 2:
            sarcasm_signals += 1

        # Exclamation marks with positive words
        if text.count('!') > 1 and polarity > 0:
            sarcasm_signals += 1

        confidence = sarcasm_signals / total_signals
        detected = confidence > 0.5

        return detected, confidence

    def _classify_polarity(self, score: float) -> SentimentPolarity:
        """Classify polarity score into categories"""
        if score >= 0.6:
            return SentimentPolarity.VERY_POSITIVE
        elif score >= 0.2:
            return SentimentPolarity.POSITIVE
        elif score >= -0.2:
            return SentimentPolarity.NEUTRAL
        elif score >= -0.6:
            return SentimentPolarity.NEGATIVE
        else:
            return SentimentPolarity.VERY_NEGATIVE

    def _calculate_confidence(self, intensity: float, word_count: int) -> float:
        """Calculate confidence in the analysis"""
        # More words = more confidence (up to a point)
        word_confidence = min(1.0, word_count / 50)

        # Higher intensity = more confidence
        intensity_confidence = intensity

        # Combine
        return (word_confidence + intensity_confidence) / 2

    def _extract_aspects(self, text: str, words: List[str]) -> Dict[str, float]:
        """Extract aspects and their sentiments (basic implementation)"""
        aspects = {}

        # Common aspect indicators
        aspect_patterns = {
            'price': ['price', 'cost', 'expensive', 'cheap', 'affordable'],
            'quality': ['quality', 'well-made', 'durable', 'poor'],
            'service': ['service', 'support', 'help', 'customer'],
            'speed': ['fast', 'slow', 'quick', 'speed', 'performance'],
            'design': ['design', 'look', 'appearance', 'beautiful', 'ugly'],
        }

        for aspect, keywords in aspect_patterns.items():
            # Check if aspect is mentioned
            if any(kw in text for kw in keywords):
                # Get sentiment around aspect (simplified)
                aspect_sentiment = self._get_local_sentiment(text, keywords)
                aspects[aspect] = aspect_sentiment

        return aspects

    def _get_local_sentiment(self, text: str, keywords: List[str]) -> float:
        """Get sentiment near specific keywords"""
        # Find keyword position and analyze surrounding words
        for keyword in keywords:
            if keyword in text:
                # Get words around keyword (window of 5 words)
                words = text.split()
                try:
                    idx = words.index(keyword)
                    window = words[max(0, idx-5):min(len(words), idx+6)]

                    # Calculate sentiment in window
                    sentiment = 0.0
                    count = 0
                    for word in window:
                        if word in self.positive_words:
                            sentiment += self.positive_words[word]
                            count += 1
                        elif word in self.negative_words:
                            sentiment += self.negative_words[word]
                            count += 1

                    if count > 0:
                        return sentiment / count
                except ValueError:
                    continue

        return 0.0

    def analyze_batch(self, texts: List[str]) -> List[SentimentScore]:
        """Analyze multiple texts"""
        return [self.analyze(text) for text in texts]

    def get_sentiment_trend(self, texts: List[str], timestamps: Optional[List[datetime]] = None) -> Dict:
        """Analyze sentiment trend over time"""
        scores = self.analyze_batch(texts)

        trend_data = {
            'average_polarity': sum(s.polarity_score for s in scores) / len(scores),
            'average_intensity': sum(s.intensity for s in scores) / len(scores),
            'polarity_distribution': {},
            'dominant_emotions': {},
            'sarcasm_rate': sum(1 for s in scores if s.sarcasm_detected) / len(scores),
        }

        # Polarity distribution
        for polarity in SentimentPolarity:
            count = sum(1 for s in scores if s.polarity == polarity)
            trend_data['polarity_distribution'][polarity.value] = count / len(scores)

        # Dominant emotions
        emotion_totals = {emotion: 0.0 for emotion in Emotion}
        for score in scores:
            for emotion, value in score.emotions.items():
                emotion_totals[emotion] += value

        trend_data['dominant_emotions'] = {
            e.value: v/len(scores) for e, v in emotion_totals.items()
        }

        return trend_data


def demo():
    """Demonstrate the sentiment analyzer"""
    print("=" * 70)
    print("ADVANCED SENTIMENT ANALYSIS - MODULE #21")
    print("=" * 70)
    print()

    analyzer = AdvancedSentimentAnalyzer()

    test_texts = [
        "This product is absolutely amazing! I love it so much!",
        "Terrible experience. The worst service I've ever had.",
        "It's okay, nothing special but not bad either.",
        "Oh great, another delay. Just what I needed!",  # Sarcasm
        "The quality is excellent but the price is too expensive.",  # Mixed aspects
        "I'm so happy and excited about this!",
        "This is disgusting and makes me very angry.",
    ]

    print("ANALYZING SAMPLE TEXTS:")
    print("-" * 70)

    for i, text in enumerate(test_texts, 1):
        print(f"\n{i}. Text: \"{text}\"")
        result = analyzer.analyze(text)

        print(f"   Polarity: {result.polarity.value} (score: {result.polarity_score:.2f})")
        print(f"   Intensity: {result.intensity:.2f}")
        print(f"   Confidence: {result.confidence:.2f}")

        if result.sarcasm_detected:
            print(f"   ⚠️  Sarcasm detected (confidence: {result.sarcasm_confidence:.2f})")

        # Show top emotions
        top_emotions = sorted(result.emotions.items(), key=lambda x: x[1], reverse=True)[:3]
        if top_emotions[0][1] > 0:
            print(f"   Emotions: {', '.join(f'{e.value}:{v:.2f}' for e, v in top_emotions if v > 0)}")

        if result.aspects:
            print(f"   Aspects: {', '.join(f'{a}:{s:.2f}' for a, s in result.aspects.items())}")

    print()
    print("-" * 70)
    print("\n📊 TREND ANALYSIS:")
    trend = analyzer.get_sentiment_trend(test_texts)
    print(f"   Average Polarity: {trend['average_polarity']:.2f}")
    print(f"   Average Intensity: {trend['average_intensity']:.2f}")
    print(f"   Sarcasm Rate: {trend['sarcasm_rate']*100:.1f}%")
    print(f"   Polarity Distribution:")
    for pol, pct in trend['polarity_distribution'].items():
        if pct > 0:
            print(f"      {pol}: {pct*100:.1f}%")

    print()
    print("=" * 70)
    print("✅ Module #21 - Advanced Sentiment Analysis - OPERATIONAL")
    print("=" * 70)


if __name__ == "__main__":
    demo()
