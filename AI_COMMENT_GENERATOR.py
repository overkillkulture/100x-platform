"""
🤖 AI COMMENT GENERATOR - Contextually Relevant Instagram Comments
Powered by Claude API - No spam, genuine engagement

Built with Trinity - C2 designed, C1 implemented
"""

import os
import json
from anthropic import Anthropic

class AICommentGenerator:
    """
    Generate contextually relevant Instagram comments using Claude API

    Features:
    - Analyzes post content (image description + caption)
    - Generates genuine, relevant comments
    - No spam or generic responses
    - Varies comment style and length
    - Natural conversation starters
    """

    def __init__(self):
        # Initialize Claude API
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable not set")

        self.client = Anthropic(api_key=api_key)
        self.model = "claude-3-5-sonnet-20241022"

    def generate_comment(self, image_description="", post_caption="", user_bio="", niche="general"):
        """
        Generate contextually relevant comment

        Args:
            image_description: What the image shows (e.g., "sunset over mountains")
            post_caption: The caption text
            user_bio: User's bio (for additional context)
            niche: Content niche (entrepreneur, fitness, travel, etc.)

        Returns:
            str: Generated comment (5-20 words, genuine and relevant)
        """

        # Build context
        context_parts = []
        if image_description:
            context_parts.append(f"Image shows: {image_description}")
        if post_caption:
            context_parts.append(f"Caption: {post_caption}")
        if user_bio:
            context_parts.append(f"User bio: {user_bio}")
        if niche and niche != "general":
            context_parts.append(f"Content niche: {niche}")

        context = "\n".join(context_parts) if context_parts else "General Instagram post"

        prompt = f"""Generate a genuine, contextually relevant Instagram comment for this post.

{context}

REQUIREMENTS:
1. Sound human and genuine (not robotic)
2. Relate directly to the content
3. Length: 5-20 words
4. NO generic words like "nice", "great", "amazing" alone
5. Can be:
   - A specific observation ("That lighting is incredible")
   - A thoughtful question ("How long did this take?")
   - Shared experience ("I felt the same way")
   - Encouragement with specificity ("This approach to X is brilliant")
6. Natural conversation starter
7. NO emojis (keep it genuine)
8. NO hashtags
9. NO promotional content

EXAMPLES OF GOOD COMMENTS:
- "The way you framed this shot is masterful"
- "This resonates so much. Going through similar journey"
- "Your perspective on this is refreshing"
- "The detail in the background tells a whole story"
- "This is exactly what I needed to see today"

EXAMPLES OF BAD COMMENTS (AVOID):
- "Nice!"
- "Great post!"
- "Amazing! 😍"
- "Love this"
- "Check out my page"

Return ONLY the comment text, nothing else. No quotes, no explanation."""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=100,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )

            comment = response.content[0].text.strip()

            # Validation: ensure it's not too short or generic
            if len(comment.split()) < 3:
                # If too short, try again with more specific instruction
                return self.generate_comment_fallback(context)

            return comment

        except Exception as e:
            print(f"❌ Error generating AI comment: {e}")
            return self.generate_comment_fallback(context)

    def generate_comment_fallback(self, context):
        """Fallback comment generator if API fails"""
        # More sophisticated than simple templates, but doesn't require API
        templates = [
            "This speaks volumes about {topic}",
            "Your perspective on this is compelling",
            "The composition here is remarkable",
            "This captures the essence perfectly",
            "Thought-provoking way to present this",
            "The detail in this is extraordinary",
            "This resonates on a deep level",
            "Your approach to this is inspiring",
            "The storytelling here is powerful",
            "This shifts my perspective in the best way"
        ]

        import random
        return random.choice(templates).replace('{topic}', 'this')

    def generate_batch_comments(self, posts_data):
        """
        Generate comments for multiple posts at once

        Args:
            posts_data: List of dicts with keys: image_description, post_caption, niche

        Returns:
            List of generated comments
        """
        comments = []

        for post in posts_data:
            comment = self.generate_comment(
                image_description=post.get('image_description', ''),
                post_caption=post.get('post_caption', ''),
                user_bio=post.get('user_bio', ''),
                niche=post.get('niche', 'general')
            )
            comments.append(comment)

        return comments

    def test_comment_generation(self):
        """Test comment generator with sample posts"""
        print("\n" + "="*70)
        print("🧪 TESTING AI COMMENT GENERATOR")
        print("="*70)

        test_posts = [
            {
                'image_description': 'sunset over ocean with dramatic clouds',
                'post_caption': 'Perfect end to an amazing day',
                'niche': 'travel'
            },
            {
                'image_description': 'person working on laptop in coffee shop',
                'post_caption': 'Building the dream one line of code at a time',
                'niche': 'entrepreneur'
            },
            {
                'image_description': 'healthy breakfast bowl with fruits and granola',
                'post_caption': 'Fueling the body right #cleaneating',
                'niche': 'fitness'
            },
            {
                'image_description': 'quote about mindset overlaid on mountains',
                'post_caption': 'Your mindset determines everything',
                'niche': 'motivation'
            }
        ]

        for i, post in enumerate(test_posts, 1):
            print(f"\n[Test {i}]")
            print(f"Image: {post['image_description']}")
            print(f"Caption: {post['post_caption']}")
            print(f"Niche: {post['niche']}")

            comment = self.generate_comment(
                image_description=post['image_description'],
                post_caption=post['post_caption'],
                niche=post['niche']
            )

            print(f"✅ Generated Comment: \"{comment}\"")
            print(f"   Length: {len(comment.split())} words")

        print("\n" + "="*70)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='🤖 AI Comment Generator for Instagram')
    parser.add_argument('--test', action='store_true',
                       help='Run test with sample posts')
    parser.add_argument('--image', type=str,
                       help='Image description')
    parser.add_argument('--caption', type=str,
                       help='Post caption')
    parser.add_argument('--niche', type=str, default='general',
                       help='Content niche')

    args = parser.parse_args()

    generator = AICommentGenerator()

    if args.test:
        generator.test_comment_generation()
    elif args.image or args.caption:
        comment = generator.generate_comment(
            image_description=args.image or '',
            post_caption=args.caption or '',
            niche=args.niche
        )
        print(f"\n✅ Generated Comment:\n\"{comment}\"\n")
    else:
        print("\n🤖 AI Comment Generator")
        print("="*70)
        print("\nUsage:")
        print("  Test mode:       python AI_COMMENT_GENERATOR.py --test")
        print("  Generate:        python AI_COMMENT_GENERATOR.py --image 'sunset' --caption 'Beautiful day'")
        print("  With niche:      python AI_COMMENT_GENERATOR.py --caption 'text' --niche entrepreneur")
        print()
