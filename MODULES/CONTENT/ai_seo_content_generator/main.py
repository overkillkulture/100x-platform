#!/usr/bin/env python3
"""
AI SEO Content Generator - Module #25
Automated keyword research, SEO-optimized articles, meta tags, schema generation
Complete SEO content pipeline powered by Claude AI
"""

import os
import json
import re
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict, field
from enum import Enum
import anthropic
import random


class ContentType(Enum):
    """Types of SEO content"""
    BLOG_POST = "blog_post"
    PRODUCT_PAGE = "product_page"
    LANDING_PAGE = "landing_page"
    CATEGORY_PAGE = "category_page"
    FAQ_PAGE = "faq_page"
    PILLAR_CONTENT = "pillar_content"
    LISTICLE = "listicle"
    HOW_TO_GUIDE = "how_to_guide"
    COMPARISON = "comparison"
    REVIEW = "review"


@dataclass
class Keyword:
    """Keyword data structure"""
    keyword: str
    search_volume: int
    difficulty: int  # 0-100
    cpc: float  # Cost per click
    intent: str  # informational, commercial, transactional, navigational
    related_keywords: List[str] = field(default_factory=list)


@dataclass
class SEOMetadata:
    """SEO metadata for content"""
    title_tag: str  # max 60 chars
    meta_description: str  # max 160 chars
    focus_keyword: str
    secondary_keywords: List[str]
    canonical_url: Optional[str] = None
    og_title: Optional[str] = None  # Open Graph
    og_description: Optional[str] = None
    og_image: Optional[str] = None
    twitter_title: Optional[str] = None
    twitter_description: Optional[str] = None


@dataclass
class SchemaMarkup:
    """Structured data schema"""
    schema_type: str  # Article, Product, FAQ, HowTo, etc.
    schema_json: str  # JSON-LD format


@dataclass
class SEOContent:
    """Complete SEO-optimized content"""
    content_id: str
    content_type: ContentType
    title: str
    content_html: str
    content_markdown: str
    seo_metadata: SEOMetadata
    schema_markup: SchemaMarkup
    word_count: int
    reading_time: int  # minutes
    internal_links: List[str] = field(default_factory=list)
    external_links: List[str] = field(default_factory=list)
    images: List[Dict[str, str]] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class SEOScore:
    """SEO quality score"""
    overall_score: int  # 0-100
    keyword_optimization: int
    readability: int
    meta_tags: int
    content_structure: int
    recommendations: List[str]


class KeywordResearcher:
    """AI-powered keyword research"""

    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = "claude-3-5-sonnet-20241022"

    def research_keywords(
        self,
        topic: str,
        count: int = 20,
        intent: Optional[str] = None
    ) -> List[Keyword]:
        """Research keywords for a topic using AI"""

        prompt = f"""You are an SEO keyword research expert. Research {count} high-value keywords for the topic: "{topic}"

{f"Focus on {intent} intent keywords." if intent else ""}

For each keyword provide:
- Keyword phrase
- Estimated monthly search volume
- SEO difficulty (0-100)
- Estimated CPC
- Search intent (informational/commercial/transactional/navigational)
- 3-5 related keywords

Return as JSON array:
[
  {{
    "keyword": "keyword phrase",
    "search_volume": 5000,
    "difficulty": 45,
    "cpc": 2.50,
    "intent": "informational",
    "related_keywords": ["related1", "related2", "related3"]
  }},
  ...
]

Focus on keywords with good search volume and reasonable difficulty."""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                messages=[{"role": "user", "content": prompt}]
            )

            content = response.content[0].text
            json_match = re.search(r'\[.*\]', content, re.DOTALL)

            if json_match:
                keywords_data = json.loads(json_match.group())
                return [
                    Keyword(
                        keyword=kw['keyword'],
                        search_volume=kw['search_volume'],
                        difficulty=kw['difficulty'],
                        cpc=kw['cpc'],
                        intent=kw['intent'],
                        related_keywords=kw.get('related_keywords', [])
                    )
                    for kw in keywords_data
                ]
            else:
                return []

        except Exception as e:
            print(f"Error researching keywords: {e}")
            return []

    def analyze_competitor_keywords(
        self,
        competitor_content: str
    ) -> List[str]:
        """Extract keywords from competitor content"""

        prompt = f"""Analyze this competitor content and extract the main SEO keywords they are targeting:

CONTENT:
{competitor_content[:2000]}

Return as JSON array: ["keyword1", "keyword2", ...]
Focus on phrases that appear multiple times and seem intentional for SEO."""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}]
            )

            content = response.content[0].text
            json_match = re.search(r'\[.*\]', content, re.DOTALL)

            if json_match:
                return json.loads(json_match.group())
            else:
                return []

        except Exception as e:
            print(f"Error analyzing competitor: {e}")
            return []


class AIContentGenerator:
    """AI-powered SEO content generation"""

    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = "claude-3-5-sonnet-20241022"

    def generate_seo_content(
        self,
        content_type: ContentType,
        focus_keyword: str,
        secondary_keywords: List[str],
        title: str,
        outline: Optional[List[str]] = None,
        word_count: int = 1500,
        tone: str = "professional"
    ) -> Dict[str, str]:
        """Generate SEO-optimized content"""

        outline_text = ""
        if outline:
            outline_text = f"\n\nOUTLINE:\n" + "\n".join(f"- {point}" for point in outline)

        prompt = f"""You are an expert SEO content writer. Write a {content_type.value} optimized for search engines.

TITLE: {title}
FOCUS KEYWORD: {focus_keyword}
SECONDARY KEYWORDS: {', '.join(secondary_keywords)}
TARGET WORD COUNT: {word_count}
TONE: {tone}
{outline_text}

Requirements:
1. Include focus keyword in first paragraph
2. Use focus keyword 3-5 times naturally throughout
3. Include secondary keywords 1-2 times each
4. Use proper heading structure (H2, H3)
5. Write compelling introduction and conclusion
6. Include actionable takeaways
7. Make it engaging and valuable for readers
8. Optimize for featured snippets where possible

Return as JSON:
{{
  "content_html": "Full HTML content with proper heading tags",
  "content_markdown": "Same content in Markdown format",
  "excerpt": "150-character excerpt for previews"
}}

Make it high-quality, informative, and SEO-optimized."""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                messages=[{"role": "user", "content": prompt}]
            )

            content = response.content[0].text
            json_match = re.search(r'\{.*\}', content, re.DOTALL)

            if json_match:
                return json.loads(json_match.group())
            else:
                return {
                    "content_html": content,
                    "content_markdown": content,
                    "excerpt": content[:150]
                }

        except Exception as e:
            print(f"Error generating content: {e}")
            raise

    def generate_meta_tags(
        self,
        title: str,
        content: str,
        focus_keyword: str
    ) -> SEOMetadata:
        """Generate optimized meta tags"""

        prompt = f"""Create SEO-optimized meta tags for this content:

TITLE: {title}
FOCUS KEYWORD: {focus_keyword}
CONTENT PREVIEW: {content[:500]}

Generate:
1. Title tag (max 60 chars, includes focus keyword)
2. Meta description (max 160 chars, compelling, includes keyword)
3. Open Graph title (can be slightly different)
4. Open Graph description
5. Twitter title
6. Twitter description

Return as JSON:
{{
  "title_tag": "...",
  "meta_description": "...",
  "og_title": "...",
  "og_description": "...",
  "twitter_title": "...",
  "twitter_description": "..."
}}

Make them compelling and click-worthy while including the keyword naturally."""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}]
            )

            content = response.content[0].text
            json_match = re.search(r'\{.*\}', content, re.DOTALL)

            if json_match:
                meta_data = json.loads(json_match.group())
                return SEOMetadata(
                    title_tag=meta_data['title_tag'],
                    meta_description=meta_data['meta_description'],
                    focus_keyword=focus_keyword,
                    secondary_keywords=[],
                    og_title=meta_data.get('og_title'),
                    og_description=meta_data.get('og_description'),
                    twitter_title=meta_data.get('twitter_title'),
                    twitter_description=meta_data.get('twitter_description')
                )
            else:
                raise ValueError("Could not parse meta tags")

        except Exception as e:
            print(f"Error generating meta tags: {e}")
            # Return basic meta tags
            return SEOMetadata(
                title_tag=title[:60],
                meta_description=content[:160],
                focus_keyword=focus_keyword,
                secondary_keywords=[]
            )

    def generate_schema_markup(
        self,
        content_type: ContentType,
        title: str,
        content: str,
        author: str = "Your Company",
        date_published: Optional[str] = None
    ) -> SchemaMarkup:
        """Generate structured data schema"""

        date_published = date_published or datetime.now().isoformat()

        # Map content types to schema types
        schema_type_map = {
            ContentType.BLOG_POST: "Article",
            ContentType.HOW_TO_GUIDE: "HowTo",
            ContentType.FAQ_PAGE: "FAQPage",
            ContentType.PRODUCT_PAGE: "Product",
            ContentType.REVIEW: "Review"
        }

        schema_type = schema_type_map.get(content_type, "Article")

        if schema_type == "Article":
            schema_json = json.dumps({
                "@context": "https://schema.org",
                "@type": "Article",
                "headline": title,
                "author": {
                    "@type": "Organization",
                    "name": author
                },
                "datePublished": date_published,
                "description": content[:200]
            }, indent=2)

        elif schema_type == "HowTo":
            schema_json = json.dumps({
                "@context": "https://schema.org",
                "@type": "HowTo",
                "name": title,
                "description": content[:200],
                "step": [
                    {
                        "@type": "HowToStep",
                        "text": "Step details here"
                    }
                ]
            }, indent=2)

        else:
            schema_json = json.dumps({
                "@context": "https://schema.org",
                "@type": schema_type,
                "name": title,
                "description": content[:200]
            }, indent=2)

        return SchemaMarkup(
            schema_type=schema_type,
            schema_json=schema_json
        )


class SEOContentGenerator:
    """Main SEO content generation system"""

    def __init__(self, api_key: Optional[str] = None):
        """Initialize SEO content generator"""
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY is required")

        self.keyword_researcher = KeywordResearcher(self.api_key)
        self.content_generator = AIContentGenerator(self.api_key)

        # Storage
        self.contents: Dict[str, SEOContent] = {}
        self.keywords_cache: Dict[str, List[Keyword]] = {}

    def create_seo_content(
        self,
        topic: str,
        content_type: ContentType = ContentType.BLOG_POST,
        target_word_count: int = 1500,
        tone: str = "professional"
    ) -> SEOContent:
        """Complete SEO content generation pipeline"""

        print(f"\n🔍 Step 1: Keyword Research for '{topic}'...")

        # Research keywords
        keywords = self.keyword_researcher.research_keywords(
            topic=topic,
            count=10
        )

        if not keywords:
            raise ValueError("No keywords found")

        # Select best keyword
        focus_keyword = keywords[0].keyword
        secondary_keywords = [kw.keyword for kw in keywords[1:6]]

        print(f"✓ Focus Keyword: {focus_keyword}")
        print(f"✓ Secondary Keywords: {', '.join(secondary_keywords[:3])}...")

        # Generate title
        title = f"{topic} - Complete Guide"

        print(f"\n✍️  Step 2: Generating SEO-optimized content...")

        # Generate content
        content_data = self.content_generator.generate_seo_content(
            content_type=content_type,
            focus_keyword=focus_keyword,
            secondary_keywords=secondary_keywords,
            title=title,
            word_count=target_word_count,
            tone=tone
        )

        print(f"✓ Content generated ({len(content_data['content_html'])} chars)")

        print(f"\n🏷️  Step 3: Creating meta tags...")

        # Generate meta tags
        seo_metadata = self.content_generator.generate_meta_tags(
            title=title,
            content=content_data['content_markdown'],
            focus_keyword=focus_keyword
        )
        seo_metadata.secondary_keywords = secondary_keywords

        print(f"✓ Title: {seo_metadata.title_tag}")
        print(f"✓ Description: {seo_metadata.meta_description[:50]}...")

        print(f"\n🔧 Step 4: Generating schema markup...")

        # Generate schema
        schema_markup = self.content_generator.generate_schema_markup(
            content_type=content_type,
            title=title,
            content=content_data['content_markdown']
        )

        print(f"✓ Schema type: {schema_markup.schema_type}")

        # Calculate metrics
        word_count = len(content_data['content_markdown'].split())
        reading_time = max(1, word_count // 200)  # 200 words per minute

        # Create SEO content object
        content_id = f"seo_{int(datetime.now().timestamp())}"

        seo_content = SEOContent(
            content_id=content_id,
            content_type=content_type,
            title=title,
            content_html=content_data['content_html'],
            content_markdown=content_data['content_markdown'],
            seo_metadata=seo_metadata,
            schema_markup=schema_markup,
            word_count=word_count,
            reading_time=reading_time
        )

        self.contents[content_id] = seo_content

        print(f"\n✅ SEO content created: {content_id}")
        print(f"   Word count: {word_count}")
        print(f"   Reading time: {reading_time} min")

        return seo_content

    def analyze_seo_score(self, content: SEOContent) -> SEOScore:
        """Analyze SEO quality of content"""

        recommendations = []
        scores = {}

        # Keyword optimization (0-100)
        keyword_count = content.content_markdown.lower().count(
            content.seo_metadata.focus_keyword.lower()
        )
        if keyword_count < 2:
            scores['keyword_optimization'] = 40
            recommendations.append(f"Use focus keyword '{content.seo_metadata.focus_keyword}' more (current: {keyword_count})")
        elif keyword_count > 10:
            scores['keyword_optimization'] = 60
            recommendations.append("Focus keyword appears too often - reduce for natural flow")
        else:
            scores['keyword_optimization'] = 95

        # Meta tags (0-100)
        meta_score = 100
        if len(content.seo_metadata.title_tag) > 60:
            meta_score -= 20
            recommendations.append("Title tag too long (max 60 chars)")
        if len(content.seo_metadata.meta_description) > 160:
            meta_score -= 20
            recommendations.append("Meta description too long (max 160 chars)")
        if content.seo_metadata.focus_keyword.lower() not in content.seo_metadata.title_tag.lower():
            meta_score -= 30
            recommendations.append("Include focus keyword in title tag")
        scores['meta_tags'] = max(0, meta_score)

        # Readability (0-100)
        avg_sentence_length = len(content.content_markdown.split()) / max(1, content.content_markdown.count('.'))
        if avg_sentence_length > 25:
            scores['readability'] = 60
            recommendations.append("Use shorter sentences for better readability")
        else:
            scores['readability'] = 90

        # Content structure (0-100)
        structure_score = 100
        if '<h2>' not in content.content_html.lower() and '##' not in content.content_markdown:
            structure_score -= 40
            recommendations.append("Add H2 headings for better structure")
        if content.word_count < 300:
            structure_score -= 30
            recommendations.append(f"Content too short ({content.word_count} words) - aim for 1000+")
        scores['content_structure'] = max(0, structure_score)

        # Overall score
        overall_score = sum(scores.values()) // len(scores)

        return SEOScore(
            overall_score=overall_score,
            keyword_optimization=scores['keyword_optimization'],
            readability=scores['readability'],
            meta_tags=scores['meta_tags'],
            content_structure=scores['content_structure'],
            recommendations=recommendations
        )

    def export_wordpress(self, content_id: str) -> Dict[str, Any]:
        """Export content in WordPress-ready format"""

        if content_id not in self.contents:
            raise ValueError(f"Content {content_id} not found")

        content = self.contents[content_id]

        return {
            "title": content.title,
            "content": content.content_html,
            "excerpt": content.seo_metadata.meta_description,
            "status": "draft",
            "meta": {
                "yoast_title": content.seo_metadata.title_tag,
                "yoast_description": content.seo_metadata.meta_description,
                "yoast_focus_keyword": content.seo_metadata.focus_keyword,
                "schema": content.schema_markup.schema_json
            }
        }

    def get_analytics(self) -> Dict[str, Any]:
        """Get content generation analytics"""

        total_content = len(self.contents)
        total_words = sum(c.word_count for c in self.contents.values())
        avg_word_count = total_words // total_content if total_content > 0 else 0

        # Calculate average SEO score
        seo_scores = [
            self.analyze_seo_score(content).overall_score
            for content in self.contents.values()
        ]
        avg_seo_score = sum(seo_scores) // len(seo_scores) if seo_scores else 0

        return {
            "total_content_pieces": total_content,
            "total_words_generated": total_words,
            "average_word_count": avg_word_count,
            "average_seo_score": avg_seo_score,
            "content_types": {
                ct.value: len([c for c in self.contents.values() if c.content_type == ct])
                for ct in ContentType
            }
        }


def demo_seo_content_generator():
    """Demo function showing SEO content generation"""
    print("=" * 70)
    print("AI SEO Content Generator - Demo")
    print("=" * 70)

    try:
        generator = SEOContentGenerator()
    except ValueError as e:
        print(f"\nError: {e}")
        print("Please set ANTHROPIC_API_KEY environment variable")
        return

    # Generate SEO-optimized content
    print("\n🚀 Generating SEO-optimized blog post...")

    content = generator.create_seo_content(
        topic="How to Improve Website Speed",
        content_type=ContentType.HOW_TO_GUIDE,
        target_word_count=1500,
        tone="educational"
    )

    # Analyze SEO score
    print("\n" + "=" * 70)
    print("SEO Analysis")
    print("=" * 70)

    seo_score = generator.analyze_seo_score(content)

    print(f"\n📊 Overall SEO Score: {seo_score.overall_score}/100")
    print(f"   Keyword Optimization: {seo_score.keyword_optimization}/100")
    print(f"   Readability: {seo_score.readability}/100")
    print(f"   Meta Tags: {seo_score.meta_tags}/100")
    print(f"   Content Structure: {seo_score.content_structure}/100")

    if seo_score.recommendations:
        print("\n💡 Recommendations:")
        for rec in seo_score.recommendations:
            print(f"   • {rec}")

    # Show content preview
    print("\n" + "=" * 70)
    print("Content Preview")
    print("=" * 70)
    print(f"\nTitle: {content.title}")
    print(f"Word Count: {content.word_count}")
    print(f"Reading Time: {content.reading_time} minutes")
    print(f"\nMeta Title: {content.seo_metadata.title_tag}")
    print(f"Meta Description: {content.seo_metadata.meta_description}")
    print(f"\nContent Preview:")
    print(content.content_markdown[:300] + "...")

    # Analytics
    print("\n" + "=" * 70)
    print("Analytics")
    print("=" * 70)
    analytics = generator.get_analytics()
    print(json.dumps(analytics, indent=2))

    print("\n✅ Demo completed!")


if __name__ == "__main__":
    demo_seo_content_generator()
