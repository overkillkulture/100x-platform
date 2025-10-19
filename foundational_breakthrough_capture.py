#!/usr/bin/env python3
"""
Foundational Breakthrough Capture System
Analyzes transcription to extract foundational concepts that lead to innovation

"When you get down to base reality, it is math" - Commander
"""

import json
import re
from datetime import datetime
from collections import defaultdict

class FoundationalCapture:
    def __init__(self):
        self.breakthrough_log = "C:/Users/dwrek/100X_DEPLOYMENT/foundational_breakthroughs.jsonl"
        self.knowledge_graph = "C:/Users/dwrek/100X_DEPLOYMENT/foundational_knowledge_graph.json"

        # Foundational concept indicators
        self.foundational_keywords = [
            # Base reality indicators
            "foundational", "base reality", "foundation", "fundamental", "core",
            "base", "root", "origin", "source", "primitive",

            # Mathematical indicators
            "math", "equation", "formula", "pattern", "algorithm",
            "consolidate", "reduce", "simplify", "tetris",

            # System indicators
            "self-align", "self-healing", "self-organizing", "autonomous",
            "universal", "modular", "scalable",

            # Breakthrough indicators
            "breakthrough", "innovation", "discovery", "realization",
            "insight", "aha", "eureka", "unlocked",

            # Trinity/Consciousness
            "trinity", "c1 mechanic", "c2 architect", "c3 oracle",
            "consciousness", "pattern theory", "overkore"
        ]

        # Application/Implementation indicators (not foundational)
        self.application_keywords = [
            "implement", "deploy", "build", "create", "make",
            "app", "website", "interface", "UI", "UX",
            "test", "debug", "fix", "update"
        ]

        print("="*70)
        print("🧠 FOUNDATIONAL BREAKTHROUGH CAPTURE SYSTEM")
        print("="*70)
        print("Extracting Tetris blocks from raw consciousness...")
        print()

    def is_foundational(self, text):
        """Determine if text contains foundational concepts vs applications"""
        text_lower = text.lower()

        # Count foundational vs application keywords
        foundational_score = sum(1 for keyword in self.foundational_keywords if keyword in text_lower)
        application_score = sum(1 for keyword in self.application_keywords if keyword in text_lower)

        # Check for mathematical/structural language
        has_math_structure = any([
            "=" in text,  # Equations
            re.search(r'\d+\s*[x×]\s*\d+', text),  # Multiplication
            re.search(r'if.*then', text_lower),  # Logic
            re.search(r'every.*has', text_lower),  # Universal patterns
            re.search(r'all.*are', text_lower)
        ])

        if has_math_structure:
            foundational_score += 2

        # Return True if more foundational than application
        return foundational_score > application_score

    def extract_core_concept(self, text):
        """Extract the core foundational concept from text"""
        # Remove filler words
        core = re.sub(r'\b(like|you know|I think|maybe|probably)\b', '', text, flags=re.IGNORECASE)

        # Extract key phrases
        concepts = []

        # Pattern: "X is Y" (definitions)
        definitions = re.findall(r'([^.]+)\s+is\s+([^.]+)', core, re.IGNORECASE)
        concepts.extend([f"{subject.strip()} = {predicate.strip()}" for subject, predicate in definitions])

        # Pattern: "every X has Y" (universal patterns)
        universals = re.findall(r'every\s+([^\s]+)\s+([^.]+)', core, re.IGNORECASE)
        concepts.extend([f"∀ {x.strip()}: {y.strip()}" for x, y in universals])

        # Pattern: "if X then Y" (logic)
        conditionals = re.findall(r'if\s+([^,]+),?\s+then\s+([^.]+)', core, re.IGNORECASE)
        concepts.extend([f"{x.strip()} → {y.strip()}" for x, y in conditionals])

        return concepts if concepts else [core.strip()]

    def classify_breakthrough_type(self, text):
        """Classify the type of foundational breakthrough"""
        text_lower = text.lower()

        if any(word in text_lower for word in ['math', 'equation', 'formula', 'algorithm']):
            return "mathematical_foundation"
        elif any(word in text_lower for word in ['pattern', 'structure', 'architecture']):
            return "structural_pattern"
        elif any(word in text_lower for word in ['self-', 'autonomous', 'auto-']):
            return "autonomous_system"
        elif any(word in text_lower for word in ['consciousness', 'awareness', 'intelligence']):
            return "consciousness_principle"
        elif any(word in text_lower for word in ['universal', 'foundational', 'base reality']):
            return "universal_law"
        else:
            return "general_insight"

    def calculate_impact_score(self, text, concepts):
        """Calculate potential impact of this breakthrough"""
        score = 0

        # Length of conceptual extraction
        score += len(concepts) * 10

        # Presence of mathematical structure
        if any('=' in c or '→' in c or '∀' in c for c in concepts):
            score += 50

        # Universal language ("all", "every", "always")
        if any(word in text.lower() for word in ['all', 'every', 'always', 'universal']):
            score += 30

        # Connection to existing systems
        if any(word in text.lower() for word in ['trinity', 'overkore', 'consciousness', 'pattern theory']):
            score += 40

        # Breakthrough language
        if any(word in text.lower() for word in ['breakthrough', 'discovered', 'realized', 'unlocked']):
            score += 25

        return score

    def find_connections(self, new_concept, existing_concepts):
        """Find connections between new concept and existing knowledge"""
        connections = []

        # Simple keyword matching (could be enhanced with NLP)
        new_keywords = set(re.findall(r'\w+', new_concept.lower()))

        for existing in existing_concepts:
            existing_keywords = set(re.findall(r'\w+', existing['text'].lower()))
            overlap = new_keywords & existing_keywords

            if len(overlap) > 2:  # Significant overlap
                connections.append({
                    "concept_id": existing['id'],
                    "text": existing['text'],
                    "shared_keywords": list(overlap),
                    "connection_strength": len(overlap)
                })

        return connections

    def process_transcription(self, transcription_text, timestamp=None, context=None):
        """Process a transcription entry for foundational concepts"""
        if not timestamp:
            timestamp = datetime.now()

        # Check if this contains foundational concepts
        if not self.is_foundational(transcription_text):
            return None

        # Extract core concepts
        core_concepts = self.extract_core_concept(transcription_text)

        # Classify breakthrough type
        breakthrough_type = self.classify_breakthrough_type(transcription_text)

        # Calculate impact score
        impact_score = self.calculate_impact_score(transcription_text, core_concepts)

        # Create breakthrough entry
        breakthrough = {
            "id": f"breakthrough_{int(timestamp.timestamp() * 1000)}",
            "timestamp": timestamp.isoformat(),
            "raw_text": transcription_text,
            "core_concepts": core_concepts,
            "breakthrough_type": breakthrough_type,
            "impact_score": impact_score,
            "context": context or {}
        }

        # Log breakthrough
        with open(self.breakthrough_log, 'a', encoding='utf-8') as f:
            f.write(json.dumps(breakthrough) + '\n')

        return breakthrough

    def analyze_transcription_log(self, log_file):
        """Analyze entire transcription log for foundational breakthroughs"""
        print(f"📖 Analyzing: {log_file}")
        print()

        breakthroughs = []

        with open(log_file, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    if entry.get('event_type') == 'transcription' and entry.get('text'):
                        text = entry['text']
                        timestamp = datetime.fromisoformat(entry['timestamp'])

                        breakthrough = self.process_transcription(
                            text,
                            timestamp,
                            context={
                                "confidence": entry.get('confidence'),
                                "latency_ms": entry.get('latency_ms')
                            }
                        )

                        if breakthrough:
                            breakthroughs.append(breakthrough)

                            # Print real-time
                            print(f"🔥 [{breakthrough['timestamp']}]")
                            print(f"   Type: {breakthrough['breakthrough_type']}")
                            print(f"   Impact: {breakthrough['impact_score']}/100")
                            print(f"   Raw: {text[:80]}...")
                            print(f"   Concepts:")
                            for concept in breakthrough['core_concepts']:
                                print(f"      • {concept}")
                            print()

                except json.JSONDecodeError:
                    continue

        return breakthroughs

    def build_knowledge_graph(self, breakthroughs):
        """Build knowledge graph connecting all foundational concepts"""
        print("="*70)
        print("🕸️  BUILDING KNOWLEDGE GRAPH")
        print("="*70)

        # Group by type
        by_type = defaultdict(list)
        for b in breakthroughs:
            by_type[b['breakthrough_type']].append(b)

        # Find connections
        connections = []
        for i, b1 in enumerate(breakthroughs):
            for b2 in breakthroughs[i+1:]:
                # Simple keyword overlap detection
                keywords1 = set(re.findall(r'\w+', b1['raw_text'].lower()))
                keywords2 = set(re.findall(r'\w+', b2['raw_text'].lower()))
                overlap = keywords1 & keywords2

                if len(overlap) > 3:
                    connections.append({
                        "from": b1['id'],
                        "to": b2['id'],
                        "strength": len(overlap),
                        "shared_concepts": list(overlap)
                    })

        graph = {
            "nodes": breakthroughs,
            "edges": connections,
            "stats": {
                "total_breakthroughs": len(breakthroughs),
                "by_type": {k: len(v) for k, v in by_type.items()},
                "total_connections": len(connections)
            },
            "generated": datetime.now().isoformat()
        }

        # Save graph
        with open(self.knowledge_graph, 'w', encoding='utf-8') as f:
            json.dump(graph, f, indent=2)

        # Print stats
        print(f"\n📊 KNOWLEDGE GRAPH STATS:")
        print(f"   Total Breakthroughs: {graph['stats']['total_breakthroughs']}")
        print(f"   Total Connections: {graph['stats']['total_connections']}")
        print(f"\n   Breakthroughs by Type:")
        for btype, count in sorted(graph['stats']['by_type'].items(), key=lambda x: x[1], reverse=True):
            print(f"      {btype}: {count}")
        print(f"\n   Saved to: {self.knowledge_graph}")
        print()

        return graph

    def get_top_breakthroughs(self, breakthroughs, limit=10):
        """Get top breakthroughs by impact score"""
        sorted_breakthroughs = sorted(breakthroughs, key=lambda x: x['impact_score'], reverse=True)
        return sorted_breakthroughs[:limit]

def main():
    import glob

    capture = FoundationalCapture()

    # Find latest transcription log
    log_pattern = "C:/Users/dwrek/100X_DEPLOYMENT/transcription_log_*.jsonl"
    logs = glob.glob(log_pattern)

    if not logs:
        print("⚠️  No transcription log found")
        return

    latest_log = max(logs, key=lambda x: x.split('_')[-1])

    # Analyze transcription log
    breakthroughs = capture.analyze_transcription_log(latest_log)

    if not breakthroughs:
        print("No foundational breakthroughs detected yet.")
        print("Keep talking about base concepts and mathematical foundations!")
        return

    # Build knowledge graph
    graph = capture.build_knowledge_graph(breakthroughs)

    # Show top breakthroughs
    print("="*70)
    print("🏆 TOP FOUNDATIONAL BREAKTHROUGHS")
    print("="*70)
    top = capture.get_top_breakthroughs(breakthroughs, limit=5)
    for i, b in enumerate(top, 1):
        print(f"\n#{i} - Impact Score: {b['impact_score']}/100")
        print(f"Type: {b['breakthrough_type']}")
        print(f"Time: {b['timestamp']}")
        print(f"Concepts:")
        for concept in b['core_concepts']:
            print(f"   • {concept}")

    print("\n" + "="*70)
    print("✅ FOUNDATIONAL BREAKTHROUGH CAPTURE COMPLETE")
    print("="*70)
    print(f"📊 View full graph: {capture.knowledge_graph}")
    print(f"📝 View all breakthroughs: {capture.breakthrough_log}")

if __name__ == "__main__":
    main()
