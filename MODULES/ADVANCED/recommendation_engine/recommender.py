"""
MODULE #28: RECOMMENDATION ENGINE
Instance 3: Module Developer
Built: 2025-11-08

Intelligent content recommendations using collaborative filtering and content-based methods.
"""

import numpy as np
from typing import List, Dict, Tuple, Set
from dataclasses import dataclass
from collections import defaultdict


@dataclass
class Recommendation:
    """A recommendation with score"""
    item_id: str
    score: float
    reason: str


class RecommendationEngine:
    """
    Hybrid recommendation system combining collaborative and content-based filtering

    Methods:
    - Collaborative filtering (user-user similarity)
    - Content-based filtering (item features)
    - Hybrid approach
    """

    def __init__(self):
        self.user_item_matrix = {}  # {user_id: {item_id: rating}}
        self.item_features = {}     # {item_id: {feature: value}}
        self.user_profiles = {}     # {user_id: {feature: weight}}

    def add_rating(self, user_id: str, item_id: str, rating: float):
        """Add user rating for item"""
        if user_id not in self.user_item_matrix:
            self.user_item_matrix[user_id] = {}
        self.user_item_matrix[user_id][item_id] = rating

    def add_item_features(self, item_id: str, features: Dict[str, float]):
        """Add features for item"""
        self.item_features[item_id] = features

    def cosine_similarity(self, vec1: Dict[str, float], vec2: Dict[str, float]) -> float:
        """Calculate cosine similarity between two feature vectors"""

        # Get common keys
        common = set(vec1.keys()) & set(vec2.keys())

        if not common:
            return 0.0

        # Calculate dot product and magnitudes
        dot_product = sum(vec1[k] * vec2[k] for k in common)
        mag1 = np.sqrt(sum(v**2 for v in vec1.values()))
        mag2 = np.sqrt(sum(v**2 for v in vec2.values()))

        if mag1 == 0 or mag2 == 0:
            return 0.0

        return dot_product / (mag1 * mag2)

    def find_similar_users(self, user_id: str, top_k: int = 5) -> List[Tuple[str, float]]:
        """Find users similar to given user based on ratings"""

        if user_id not in self.user_item_matrix:
            return []

        user_ratings = self.user_item_matrix[user_id]
        similarities = []

        for other_id, other_ratings in self.user_item_matrix.items():
            if other_id == user_id:
                continue

            sim = self.cosine_similarity(user_ratings, other_ratings)
            if sim > 0:
                similarities.append((other_id, sim))

        # Sort by similarity
        similarities.sort(key=lambda x: x[1], reverse=True)

        return similarities[:top_k]

    def collaborative_filtering(self, user_id: str, top_n: int = 10) -> List[Recommendation]:
        """Recommend items based on similar users (collaborative filtering)"""

        if user_id not in self.user_item_matrix:
            return []

        # Find similar users
        similar_users = self.find_similar_users(user_id, top_k=10)

        if not similar_users:
            return []

        # Get items rated by similar users
        user_items = set(self.user_item_matrix[user_id].keys())
        candidate_scores = defaultdict(float)
        candidate_weights = defaultdict(float)

        for similar_id, similarity in similar_users:
            similar_ratings = self.user_item_matrix[similar_id]

            for item_id, rating in similar_ratings.items():
                if item_id not in user_items:  # Not already rated
                    candidate_scores[item_id] += rating * similarity
                    candidate_weights[item_id] += similarity

        # Calculate weighted average scores
        recommendations = []
        for item_id, weighted_score in candidate_scores.items():
            score = weighted_score / candidate_weights[item_id] if candidate_weights[item_id] > 0 else 0
            recommendations.append(Recommendation(
                item_id=item_id,
                score=score,
                reason="collaborative"
            ))

        # Sort by score
        recommendations.sort(key=lambda x: x.score, reverse=True)

        return recommendations[:top_n]

    def build_user_profile(self, user_id: str):
        """Build user profile from rated items"""

        if user_id not in self.user_item_matrix:
            return

        profile = defaultdict(float)
        total_weight = 0

        for item_id, rating in self.user_item_matrix[user_id].items():
            if item_id in self.item_features:
                weight = rating  # Weight by rating
                for feature, value in self.item_features[item_id].items():
                    profile[feature] += value * weight
                total_weight += weight

        # Normalize
        if total_weight > 0:
            profile = {k: v / total_weight for k, v in profile.items()}

        self.user_profiles[user_id] = dict(profile)

    def content_based_filtering(self, user_id: str, top_n: int = 10) -> List[Recommendation]:
        """Recommend items based on user preferences (content-based filtering)"""

        # Build/update user profile
        self.build_user_profile(user_id)

        if user_id not in self.user_profiles:
            return []

        user_profile = self.user_profiles[user_id]
        user_items = set(self.user_item_matrix.get(user_id, {}).keys())

        # Score all items not yet rated
        recommendations = []
        for item_id, features in self.item_features.items():
            if item_id not in user_items:
                score = self.cosine_similarity(user_profile, features)
                recommendations.append(Recommendation(
                    item_id=item_id,
                    score=score,
                    reason="content_based"
                ))

        # Sort by score
        recommendations.sort(key=lambda x: x.score, reverse=True)

        return recommendations[:top_n]

    def hybrid_recommend(self, user_id: str, top_n: int = 10,
                         collab_weight: float = 0.5) -> List[Recommendation]:
        """Hybrid recommendation combining both methods"""

        # Get recommendations from both methods
        collab_recs = self.collaborative_filtering(user_id, top_n=20)
        content_recs = self.content_based_filtering(user_id, top_n=20)

        # Combine scores
        combined = {}

        for rec in collab_recs:
            combined[rec.item_id] = rec.score * collab_weight

        for rec in content_recs:
            if rec.item_id in combined:
                combined[rec.item_id] += rec.score * (1 - collab_weight)
            else:
                combined[rec.item_id] = rec.score * (1 - collab_weight)

        # Create final recommendations
        recommendations = [
            Recommendation(item_id=item_id, score=score, reason="hybrid")
            for item_id, score in combined.items()
        ]

        recommendations.sort(key=lambda x: x.score, reverse=True)

        return recommendations[:top_n]

    def get_popular_items(self, top_n: int = 10) -> List[Recommendation]:
        """Get most popular items (fallback for cold start)"""

        item_ratings = defaultdict(list)

        for user_ratings in self.user_item_matrix.values():
            for item_id, rating in user_ratings.items():
                item_ratings[item_id].append(rating)

        # Calculate average rating
        popular = []
        for item_id, ratings in item_ratings.items():
            avg_rating = np.mean(ratings)
            count = len(ratings)
            # Weighted score (rating * log(count))
            score = avg_rating * np.log1p(count)
            popular.append(Recommendation(
                item_id=item_id,
                score=score,
                reason="popular"
            ))

        popular.sort(key=lambda x: x.score, reverse=True)

        return popular[:top_n]


def demo():
    """Demonstrate recommendation engine"""

    print("=" * 60)
    print("RECOMMENDATION ENGINE DEMO")
    print("=" * 60)
    print()

    engine = RecommendationEngine()

    # Add ratings (user, item, rating 0-5)
    ratings = [
        ("user1", "python", 5), ("user1", "javascript", 3), ("user1", "ml", 5),
        ("user2", "python", 5), ("user2", "ml", 5), ("user2", "quantum", 4),
        ("user3", "javascript", 4), ("user3", "react", 5), ("user3", "node", 4),
        ("user4", "python", 5), ("user4", "ml", 4), ("user4", "neural", 5),
    ]

    for user, item, rating in ratings:
        engine.add_rating(user, item, rating)

    # Add item features
    features = {
        "python": {"programming": 1.0, "backend": 0.8, "data": 0.9},
        "javascript": {"programming": 1.0, "frontend": 0.9, "web": 1.0},
        "ml": {"programming": 0.7, "data": 1.0, "ai": 1.0},
        "quantum": {"programming": 0.5, "data": 0.6, "ai": 0.9, "advanced": 1.0},
        "react": {"programming": 0.9, "frontend": 1.0, "web": 1.0},
        "node": {"programming": 1.0, "backend": 1.0, "web": 0.8},
        "neural": {"programming": 0.6, "data": 0.8, "ai": 1.0, "advanced": 0.9},
    }

    for item, feats in features.items():
        engine.add_item_features(item, feats)

    # Test recommendations
    print("Recommendations for user1 (likes: python, ml):")
    print()

    print("Collaborative Filtering:")
    recs = engine.collaborative_filtering("user1", top_n=3)
    for rec in recs:
        print(f"  {rec.item_id}: score={rec.score:.3f}")
    print()

    print("Content-Based Filtering:")
    recs = engine.content_based_filtering("user1", top_n=3)
    for rec in recs:
        print(f"  {rec.item_id}: score={rec.score:.3f}")
    print()

    print("Hybrid (best of both):")
    recs = engine.hybrid_recommend("user1", top_n=3)
    for rec in recs:
        print(f"  {rec.item_id}: score={rec.score:.3f}")
    print()

    print("=" * 60)
    print("DEMO COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    demo()
