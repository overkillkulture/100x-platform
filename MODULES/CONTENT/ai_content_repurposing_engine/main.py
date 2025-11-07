#!/usr/bin/env python3
"""
AI Content Repurposing Engine - Module #23
Transform one piece of content into 15+ formats across all platforms
Blog → Twitter threads, LinkedIn posts, Instagram captions, and more
"""

import os
import json
import re
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict, field
from enum import Enum
import anthropic


class ContentFormat(Enum):
    """Supported content formats"""
    BLOG_POST = "blog_post"
    TWITTER_THREAD = "twitter_thread"
    LINKEDIN_POST = "linkedin_post"
    INSTAGRAM_CAPTION = "instagram_caption"
    FACEBOOK_POST = "facebook_post"
    YOUTUBE_SCRIPT = "youtube_script"
    PODCAST_SCRIPT = "podcast_script"
    EMAIL_NEWSLETTER = "email_newsletter"
    TIKTOK_SCRIPT = "tiktok_script"
    PINTEREST_PIN = "pinterest_pin"
    REDDIT_POST = "reddit_post"
    MEDIUM_ARTICLE = "medium_article"
    SHORT_VIDEO = "short_video_script"
    INFOGRAPHIC_TEXT = "infographic_text"
    CAROUSEL_POST = "carousel_post"


class ContentTone(Enum):
    """Content tone/voice options"""
    PROFESSIONAL = "professional"
    CASUAL = "casual"
    HUMOROUS = "humorous"
    INSPIRATIONAL = "inspirational"
    EDUCATIONAL = "educational"
    STORYTELLING = "storytelling"


@dataclass
class SourceContent:
    """Original content to be repurposed"""
    content_id: str
    title: str
    body: str
    format: ContentFormat
    url: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class RepurposedContent:
    """Repurposed content output"""
    output_id: str
    source_id: str
    format: ContentFormat
    title: str
    content: str
    hashtags: List[str] = field(default_factory=list)
    call_to_action: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)


class ContentRepurposingEngine:
    """Main engine for AI-powered content repurposing"""

    def __init__(self, api_key: Optional[str] = None):
        """Initialize repurposing engine"""
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY is required")

        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.model = "claude-3-5-sonnet-20241022"

        # Content storage
        self.source_contents: Dict[str, SourceContent] = {}
        self.repurposed_contents: Dict[str, List[RepurposedContent]] = {}

        # Platform constraints
        self.platform_limits = {
            ContentFormat.TWITTER_THREAD: {"max_tweet_length": 280, "max_tweets": 25},
            ContentFormat.INSTAGRAM_CAPTION: {"max_length": 2200},
            ContentFormat.LINKEDIN_POST: {"max_length": 3000},
            ContentFormat.FACEBOOK_POST: {"max_length": 63206},
            ContentFormat.TIKTOK_SCRIPT: {"duration": "60 seconds"},
            ContentFormat.YOUTUBE_SCRIPT: {"duration": "5-10 minutes"},
            ContentFormat.PINTEREST_PIN: {"max_length": 500},
        }

    def add_source_content(
        self,
        title: str,
        body: str,
        format: ContentFormat,
        url: Optional[str] = None,
        metadata: Optional[Dict] = None
    ) -> SourceContent:
        """Add source content to be repurposed"""

        content_id = f"src_{int(datetime.now().timestamp())}"

        source = SourceContent(
            content_id=content_id,
            title=title,
            body=body,
            format=format,
            url=url,
            metadata=metadata or {}
        )

        self.source_contents[content_id] = source
        self.repurposed_contents[content_id] = []

        return source

    def repurpose_to_format(
        self,
        source_id: str,
        target_format: ContentFormat,
        tone: ContentTone = ContentTone.PROFESSIONAL,
        custom_instructions: Optional[str] = None
    ) -> RepurposedContent:
        """Repurpose content to specific format"""

        if source_id not in self.source_contents:
            raise ValueError(f"Source content {source_id} not found")

        source = self.source_contents[source_id]

        # Build prompt based on target format
        prompt = self._build_repurposing_prompt(
            source, target_format, tone, custom_instructions
        )

        # Call Claude API
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )

            output_text = response.content[0].text

            # Parse output based on format
            parsed_content = self._parse_output(output_text, target_format)

            # Create repurposed content object
            output_id = f"out_{int(datetime.now().timestamp())}_{target_format.value}"

            repurposed = RepurposedContent(
                output_id=output_id,
                source_id=source_id,
                format=target_format,
                title=parsed_content.get("title", source.title),
                content=parsed_content.get("content", ""),
                hashtags=parsed_content.get("hashtags", []),
                call_to_action=parsed_content.get("cta"),
                metadata={
                    "tone": tone.value,
                    "source_format": source.format.value
                }
            )

            self.repurposed_contents[source_id].append(repurposed)
            return repurposed

        except Exception as e:
            print(f"Error repurposing content: {e}")
            raise

    def _build_repurposing_prompt(
        self,
        source: SourceContent,
        target_format: ContentFormat,
        tone: ContentTone,
        custom_instructions: Optional[str]
    ) -> str:
        """Build AI prompt for repurposing"""

        base_prompt = f"""You are an expert content strategist. Repurpose the following content into a {target_format.value} with a {tone.value} tone.

SOURCE CONTENT:
Title: {source.title}

Body:
{source.body}

"""

        # Add format-specific instructions
        format_instructions = {
            ContentFormat.TWITTER_THREAD: """
Create a Twitter thread (up to 10 tweets, 280 chars each):
- Start with a hook tweet
- Number each tweet (1/10, 2/10, etc.)
- End with a CTA
- Include 3-5 relevant hashtags
Format as JSON: {"tweets": ["tweet1", "tweet2", ...], "hashtags": ["hash1", "hash2"]}
""",
            ContentFormat.LINKEDIN_POST: """
Create a LinkedIn post (max 3000 chars):
- Professional tone
- Hook in first 2 lines
- Use line breaks for readability
- Include relevant hashtags (3-5)
- End with engagement question or CTA
Format as JSON: {"content": "post text", "hashtags": [...], "cta": "call to action"}
""",
            ContentFormat.INSTAGRAM_CAPTION: """
Create an Instagram caption (max 2200 chars):
- Engaging hook
- Story-driven
- Include line breaks and emojis
- 15-20 relevant hashtags
- Strong CTA
Format as JSON: {"content": "caption", "hashtags": [...], "cta": "..."}
""",
            ContentFormat.YOUTUBE_SCRIPT: """
Create a YouTube video script (5-7 minutes):
- Strong hook (first 15 seconds)
- Clear structure with sections
- Conversational tone
- Include B-roll suggestions [in brackets]
- End with CTA
Format as JSON: {"title": "video title", "script": "full script", "timestamps": {"00:00": "Intro", ...}}
""",
            ContentFormat.PODCAST_SCRIPT: """
Create a podcast episode script:
- Engaging intro with music cue
- Conversational storytelling
- Natural transitions
- Include sponsor read placeholder
- Strong outro with CTA
Format as JSON: {"title": "episode title", "script": "full script"}
""",
            ContentFormat.EMAIL_NEWSLETTER: """
Create an email newsletter:
- Compelling subject line
- Personal greeting
- Scannable content with headers
- Clear CTA buttons
- P.S. section
Format as JSON: {"subject": "...", "body": "...", "cta": "..."}
""",
            ContentFormat.TIKTOK_SCRIPT: """
Create a TikTok video script (60 seconds):
- Hook in first 3 seconds
- Fast-paced, energetic
- Include visual cues [in brackets]
- Trendy language
- Strong CTA
Format as JSON: {"script": "...", "visual_cues": [...], "hooks": [...]}
""",
            ContentFormat.CAROUSEL_POST: """
Create a carousel post (10 slides):
- Slide 1: Eye-catching title
- Slides 2-9: One key point per slide
- Slide 10: CTA
- Each slide: max 50 words
Format as JSON: {"slides": [{"title": "...", "content": "..."}, ...]}
""",
        }

        instruction = format_instructions.get(
            target_format,
            f"Repurpose into {target_format.value} format. Return as JSON with 'content' field."
        )

        base_prompt += instruction

        if custom_instructions:
            base_prompt += f"\n\nADDITIONAL INSTRUCTIONS:\n{custom_instructions}"

        base_prompt += "\n\nIMPORTANT: Return ONLY valid JSON, no additional text."

        return base_prompt

    def _parse_output(self, output_text: str, format: ContentFormat) -> Dict[str, Any]:
        """Parse Claude's output into structured format"""

        try:
            # Extract JSON from output
            json_match = re.search(r'\{.*\}', output_text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                # Fallback: treat entire output as content
                return {"content": output_text}
        except json.JSONDecodeError:
            return {"content": output_text}

    def repurpose_to_all_formats(
        self,
        source_id: str,
        tone: ContentTone = ContentTone.PROFESSIONAL
    ) -> Dict[ContentFormat, RepurposedContent]:
        """Repurpose content to all supported formats"""

        results = {}

        # Priority formats for comprehensive repurposing
        priority_formats = [
            ContentFormat.TWITTER_THREAD,
            ContentFormat.LINKEDIN_POST,
            ContentFormat.INSTAGRAM_CAPTION,
            ContentFormat.FACEBOOK_POST,
            ContentFormat.EMAIL_NEWSLETTER,
            ContentFormat.YOUTUBE_SCRIPT,
            ContentFormat.PODCAST_SCRIPT,
            ContentFormat.TIKTOK_SCRIPT,
            ContentFormat.CAROUSEL_POST,
            ContentFormat.PINTEREST_PIN,
            ContentFormat.REDDIT_POST,
            ContentFormat.MEDIUM_ARTICLE,
        ]

        for format in priority_formats:
            try:
                repurposed = self.repurpose_to_format(source_id, format, tone)
                results[format] = repurposed
                print(f"✓ Created {format.value}")
            except Exception as e:
                print(f"✗ Failed to create {format.value}: {e}")

        return results

    def get_repurposing_analytics(self, source_id: str) -> Dict[str, Any]:
        """Get analytics for repurposed content"""

        if source_id not in self.repurposed_contents:
            return {"error": "Source not found"}

        outputs = self.repurposed_contents[source_id]

        formats_created = [output.format.value for output in outputs]
        total_content_length = sum(len(output.content) for output in outputs)

        # Calculate potential reach (example multipliers)
        reach_multipliers = {
            ContentFormat.TWITTER_THREAD: 5000,
            ContentFormat.LINKEDIN_POST: 3000,
            ContentFormat.INSTAGRAM_CAPTION: 8000,
            ContentFormat.YOUTUBE_SCRIPT: 10000,
            ContentFormat.TIKTOK_SCRIPT: 15000,
        }

        estimated_reach = sum(
            reach_multipliers.get(output.format, 1000)
            for output in outputs
        )

        return {
            "source_id": source_id,
            "formats_created": len(outputs),
            "format_list": formats_created,
            "total_content_generated": total_content_length,
            "estimated_reach": estimated_reach,
            "time_saved_hours": len(outputs) * 2,  # Estimate 2 hours per format
            "created_at": outputs[0].created_at.isoformat() if outputs else None
        }

    def export_content_package(self, source_id: str, output_dir: str = ".") -> str:
        """Export all repurposed content as organized files"""

        if source_id not in self.repurposed_contents:
            raise ValueError(f"Source {source_id} not found")

        source = self.source_contents[source_id]
        outputs = self.repurposed_contents[source_id]

        # Create output directory
        package_dir = f"{output_dir}/content_package_{source_id}"
        os.makedirs(package_dir, exist_ok=True)

        # Save source
        with open(f"{package_dir}/00_SOURCE.txt", "w") as f:
            f.write(f"Title: {source.title}\n\n")
            f.write(source.body)

        # Save each repurposed format
        for i, output in enumerate(outputs, 1):
            filename = f"{i:02d}_{output.format.value}.txt"
            filepath = f"{package_dir}/{filename}"

            with open(filepath, "w") as f:
                f.write(f"Format: {output.format.value}\n")
                f.write(f"Title: {output.title}\n")
                if output.hashtags:
                    f.write(f"Hashtags: {' '.join(output.hashtags)}\n")
                if output.call_to_action:
                    f.write(f"CTA: {output.call_to_action}\n")
                f.write("\n" + "="*60 + "\n\n")
                f.write(output.content)

        # Create summary
        analytics = self.get_repurposing_analytics(source_id)
        with open(f"{package_dir}/SUMMARY.json", "w") as f:
            json.dump(analytics, f, indent=2)

        return package_dir


class ContentWorkflow:
    """Pre-built workflows for common repurposing scenarios"""

    def __init__(self, engine: ContentRepurposingEngine):
        self.engine = engine

    def blog_to_social_media_suite(self, blog_title: str, blog_body: str) -> Dict:
        """Convert blog post to complete social media suite"""

        # Add source
        source = self.engine.add_source_content(
            title=blog_title,
            body=blog_body,
            format=ContentFormat.BLOG_POST
        )

        # Repurpose to key social formats
        formats = [
            ContentFormat.TWITTER_THREAD,
            ContentFormat.LINKEDIN_POST,
            ContentFormat.INSTAGRAM_CAPTION,
            ContentFormat.FACEBOOK_POST,
            ContentFormat.PINTEREST_PIN,
        ]

        results = {}
        for format in formats:
            try:
                output = self.engine.repurpose_to_format(source.content_id, format)
                results[format.value] = {
                    "content": output.content,
                    "hashtags": output.hashtags,
                    "cta": output.call_to_action
                }
            except Exception as e:
                results[format.value] = {"error": str(e)}

        return {
            "source_id": source.content_id,
            "outputs": results
        }

    def video_to_multimedia_content(
        self,
        video_title: str,
        video_transcript: str
    ) -> Dict:
        """Convert video/transcript to multiple formats"""

        source = self.engine.add_source_content(
            title=video_title,
            body=video_transcript,
            format=ContentFormat.YOUTUBE_SCRIPT
        )

        formats = [
            ContentFormat.BLOG_POST,
            ContentFormat.PODCAST_SCRIPT,
            ContentFormat.TWITTER_THREAD,
            ContentFormat.LINKEDIN_POST,
            ContentFormat.EMAIL_NEWSLETTER,
            ContentFormat.TIKTOK_SCRIPT,
            ContentFormat.CAROUSEL_POST,
        ]

        results = {}
        for format in formats:
            try:
                output = self.engine.repurpose_to_format(source.content_id, format)
                results[format.value] = output.content
            except Exception as e:
                results[format.value] = f"Error: {e}"

        return {
            "source_id": source.content_id,
            "outputs": results
        }


def demo_content_repurposing():
    """Demo function showing content repurposing capabilities"""
    print("=" * 70)
    print("AI Content Repurposing Engine - Demo")
    print("=" * 70)

    try:
        # Initialize engine
        engine = ContentRepurposingEngine()
    except ValueError as e:
        print(f"\nError: {e}")
        print("Please set ANTHROPIC_API_KEY environment variable")
        return

    # Sample blog post
    blog_title = "10 Proven Strategies to 10x Your Productivity"
    blog_body = """
Are you struggling to get everything done? You're not alone. In today's fast-paced world,
productivity is more important than ever. After studying successful entrepreneurs and testing
dozens of techniques, I've discovered 10 strategies that actually work.

1. Time Blocking: Schedule your day in focused blocks
2. The Two-Minute Rule: If it takes less than 2 minutes, do it now
3. Deep Work Sessions: 90-minute focused work periods
4. Energy Management: Work with your natural rhythms
5. The 80/20 Rule: Focus on high-impact activities
6. Digital Minimalism: Reduce distractions
7. Morning Routines: Start your day with intention
8. Weekly Reviews: Reflect and plan
9. Automate Everything: Use tools to save time
10. Say No More Often: Protect your time

The key is consistency. Pick 2-3 strategies and master them before adding more.
Start small, build habits, and watch your productivity soar.

What's your favorite productivity hack? Share in the comments!
"""

    print("\n📝 Source Content:")
    print(f"Title: {blog_title}")
    print(f"Length: {len(blog_body)} characters")

    # Add source content
    source = engine.add_source_content(
        title=blog_title,
        body=blog_body,
        format=ContentFormat.BLOG_POST
    )

    print(f"\n✅ Source content added: {source.content_id}")

    # Repurpose to different formats
    print("\n🔄 Repurposing to different formats...")

    # Twitter Thread
    print("\n📱 Creating Twitter Thread...")
    twitter = engine.repurpose_to_format(
        source.content_id,
        ContentFormat.TWITTER_THREAD,
        tone=ContentTone.CASUAL
    )
    print(f"✓ Twitter thread created with {len(twitter.hashtags)} hashtags")
    print(f"Preview: {twitter.content[:150]}...")

    # LinkedIn Post
    print("\n💼 Creating LinkedIn Post...")
    linkedin = engine.repurpose_to_format(
        source.content_id,
        ContentFormat.LINKEDIN_POST,
        tone=ContentTone.PROFESSIONAL
    )
    print(f"✓ LinkedIn post created ({len(linkedin.content)} chars)")
    print(f"Preview: {linkedin.content[:150]}...")

    # Instagram Caption
    print("\n📸 Creating Instagram Caption...")
    instagram = engine.repurpose_to_format(
        source.content_id,
        ContentFormat.INSTAGRAM_CAPTION,
        tone=ContentTone.INSPIRATIONAL
    )
    print(f"✓ Instagram caption created with {len(instagram.hashtags)} hashtags")
    print(f"Preview: {instagram.content[:150]}...")

    # Analytics
    print("\n" + "=" * 70)
    print("Repurposing Analytics")
    print("=" * 70)

    analytics = engine.get_repurposing_analytics(source.content_id)
    print(f"\nFormats Created: {analytics['formats_created']}")
    print(f"Total Content Generated: {analytics['total_content_generated']:,} characters")
    print(f"Estimated Reach: {analytics['estimated_reach']:,} people")
    print(f"Time Saved: ~{analytics['time_saved_hours']} hours")

    print("\nFormat List:")
    for format_name in analytics['format_list']:
        print(f"  ✓ {format_name}")

    # Export package
    print("\n" + "=" * 70)
    print("Exporting Content Package")
    print("=" * 70)

    package_dir = engine.export_content_package(source.content_id, "/tmp")
    print(f"\n✅ Content package exported to: {package_dir}")
    print("\nPackage includes:")
    print("  • Original source content")
    print("  • All repurposed formats")
    print("  • Analytics summary")

    print("\n✅ Demo completed!")


if __name__ == "__main__":
    demo_content_repurposing()
