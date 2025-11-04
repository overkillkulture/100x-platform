#!/usr/bin/env python3
"""
PI MAPPING SYSTEM - Private Investigation & Corruption Mapping
Track manipulation trails, map relationships, expose corruption
"""

import os
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set
import re

try:
    import anthropic
    from dotenv import load_dotenv
except ImportError:
    print("❌ Required packages missing")
    print("   pip install anthropic python-dotenv")
    exit(1)


class Entity:
    """Represents a person, organization, or entity in the investigation"""

    def __init__(self, name: str, entity_type: str, data: Dict = None):
        self.name = name
        self.type = entity_type  # person, organization, money, event
        self.data = data or {}
        self.relationships = []
        self.manipulation_score = 0
        self.tactics = []
        self.evidence = []

    def to_dict(self):
        return {
            'name': self.name,
            'type': self.type,
            'data': self.data,
            'manipulation_score': self.manipulation_score,
            'tactics': self.tactics,
            'evidence_count': len(self.evidence)
        }


class Relationship:
    """Represents a connection between entities"""

    def __init__(self, entity1: str, entity2: str, relationship_type: str, evidence: str = ""):
        self.entity1 = entity1
        self.entity2 = entity2
        self.type = relationship_type  # family, business, communication, financial
        self.evidence = evidence
        self.strength = 1.0

    def to_dict(self):
        return {
            'entity1': self.entity1,
            'entity2': self.entity2,
            'type': self.type,
            'evidence': self.evidence,
            'strength': self.strength
        }


class PIMapper:
    """Private Investigation Mapping System"""

    def __init__(self, case_name: str):
        load_dotenv()

        self.case_name = case_name
        self.case_dir = Path.home() / ".pi_mapper" / case_name.replace(" ", "_")
        self.case_dir.mkdir(parents=True, exist_ok=True)

        # Initialize Claude
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment")

        self.claude = anthropic.Anthropic(api_key=api_key)

        # Case data
        self.entities: Dict[str, Entity] = {}
        self.relationships: List[Relationship] = []
        self.timeline = []
        self.evidence = []

        # Files
        self.case_file = self.case_dir / "case_data.json"
        self.evidence_dir = self.case_dir / "evidence"
        self.evidence_dir.mkdir(exist_ok=True)

        self._load_case()

    def _load_case(self):
        """Load existing case data"""
        if self.case_file.exists():
            with open(self.case_file, 'r') as f:
                data = json.load(f)

            # Rebuild entities
            for entity_data in data.get('entities', []):
                entity = Entity(
                    entity_data['name'],
                    entity_data['type'],
                    entity_data.get('data', {})
                )
                entity.manipulation_score = entity_data.get('manipulation_score', 0)
                entity.tactics = entity_data.get('tactics', [])
                self.entities[entity.name] = entity

            # Rebuild relationships
            for rel_data in data.get('relationships', []):
                rel = Relationship(
                    rel_data['entity1'],
                    rel_data['entity2'],
                    rel_data['type'],
                    rel_data.get('evidence', '')
                )
                rel.strength = rel_data.get('strength', 1.0)
                self.relationships.append(rel)

            self.timeline = data.get('timeline', [])
            self.evidence = data.get('evidence', [])

            print(f"📦 Loaded existing case: {self.case_name}")
            print(f"   Entities: {len(self.entities)}")
            print(f"   Relationships: {len(self.relationships)}")
        else:
            print(f"💼 Created new case: {self.case_name}")

    def _save_case(self):
        """Save case data to file"""
        data = {
            'case_name': self.case_name,
            'created': datetime.now().isoformat(),
            'entities': [e.to_dict() for e in self.entities.values()],
            'relationships': [r.to_dict() for r in self.relationships],
            'timeline': self.timeline,
            'evidence': self.evidence
        }

        with open(self.case_file, 'w') as f:
            json.dump(data, f, indent=2)

    def add_evidence(self, text: str, evidence_type: str = "document", date: str = None) -> Dict:
        """Add piece of evidence and automatically extract entities/relationships"""
        print(f"\n📄 Processing evidence: {evidence_type}")

        # Use Claude to extract entities and relationships
        extraction = self._extract_entities_and_relationships(text)

        # Add entities
        for entity_data in extraction['entities']:
            name = entity_data['name']
            if name not in self.entities:
                entity = Entity(name, entity_data['type'], entity_data.get('data', {}))
                self.entities[name] = entity
                print(f"   ✅ Added entity: {name} ({entity_data['type']})")

        # Add relationships
        for rel_data in extraction['relationships']:
            rel = Relationship(
                rel_data['entity1'],
                rel_data['entity2'],
                rel_data['type'],
                rel_data.get('evidence', '')
            )
            self.relationships.append(rel)
            print(f"   🔗 Added relationship: {rel_data['entity1']} → {rel_data['entity2']}")

        # Add to timeline if date provided
        if date:
            self.timeline.append({
                'date': date,
                'type': evidence_type,
                'summary': extraction.get('summary', ''),
                'entities': extraction['entities']
            })

        # Add to evidence log
        self.evidence.append({
            'date_added': datetime.now().isoformat(),
            'type': evidence_type,
            'date_occurred': date,
            'entity_count': len(extraction['entities']),
            'relationship_count': len(extraction['relationships'])
        })

        self._save_case()

        return extraction

    def _extract_entities_and_relationships(self, text: str) -> Dict:
        """Use Claude to extract entities and relationships from text"""

        prompt = f"""Extract entities and relationships from this investigation document.

Document:
{text[:5000]}

Identify:
1. ENTITIES:
   - People (names, roles)
   - Organizations (companies, agencies)
   - Money (amounts, accounts, transactions)
   - Events (what happened, when, where)

2. RELATIONSHIPS:
   - Family connections
   - Business relationships
   - Financial transactions
   - Communications
   - Power/hierarchy

Return as JSON:
{{
  "entities": [
    {{"name": "John Doe", "type": "person", "role": "defendant"}},
    {{"name": "ABC Corp", "type": "organization", "role": "employer"}}
  ],
  "relationships": [
    {{"entity1": "John Doe", "entity2": "ABC Corp", "type": "employment"}},
    {{"entity1": "John Doe", "entity2": "Jane Smith", "type": "family"}}
  ],
  "summary": "Brief summary of document content"
}}"""

        try:
            response = self.claude.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}]
            )

            result_text = response.content[0].text

            # Extract JSON from response
            json_match = re.search(r'\{.*\}', result_text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                return {'entities': [], 'relationships': [], 'summary': result_text}

        except Exception as e:
            print(f"   ⚠️  Extraction failed: {e}")
            return {'entities': [], 'relationships': [], 'summary': ''}

    def analyze_manipulation(self) -> Dict:
        """Analyze all entities for manipulation patterns using Pattern Theory"""
        print("\n🔍 Running Pattern Theory manipulation analysis...")

        results = {
            'overall_score': 0,
            'entities': {},
            'high_risk': [],
            'medium_risk': [],
            'low_risk': []
        }

        for entity_name, entity in self.entities.items():
            if entity.type == 'person' or entity.type == 'organization':
                score = self._calculate_manipulation_score(entity_name)
                entity.manipulation_score = score

                results['entities'][entity_name] = {
                    'score': score,
                    'tactics': entity.tactics,
                    'evidence': len(entity.evidence)
                }

                if score >= 80:
                    results['high_risk'].append(entity_name)
                    print(f"   ⚠️  HIGH RISK: {entity_name} (Score: {score})")
                elif score >= 60:
                    results['medium_risk'].append(entity_name)
                    print(f"   ⚡ MEDIUM RISK: {entity_name} (Score: {score})")
                else:
                    results['low_risk'].append(entity_name)
                    print(f"   ✓ Low risk: {entity_name} (Score: {score})")

        # Calculate overall case manipulation score
        if results['entities']:
            results['overall_score'] = sum(
                e['score'] for e in results['entities'].values()
            ) / len(results['entities'])

        print(f"\n📊 Overall case manipulation score: {results['overall_score']:.1f}/100")

        self._save_case()

        return results

    def _calculate_manipulation_score(self, entity_name: str) -> float:
        """Calculate manipulation score for specific entity using Pattern Theory"""

        # Get all relationships for this entity
        entity_relationships = [
            r for r in self.relationships
            if r.entity1 == entity_name or r.entity2 == entity_name
        ]

        # Pattern Theory components (simplified calculation)
        frequency_escalation = min(len(entity_relationships) / 10.0, 10.0)  # More connections = higher
        confusion_building = len([r for r in entity_relationships if r.type == 'conflicting']) / 2.0
        stress_response = len([e for e in self.timeline if entity_name in str(e)]) / 5.0
        complexity = len(set(r.type for r in entity_relationships)) / 2.0
        pattern_escaping = 5.0  # Would need more data to calculate
        dependency_creation = len([r for r in entity_relationships if 'control' in r.type.lower()]) * 2.0

        # Formula: M = (FE × CB × SR × CD × PE) × DC / 1000
        manipulation_score = (
            (frequency_escalation * max(confusion_building, 1) * max(stress_response, 1) *
             max(complexity, 1) * pattern_escaping) * max(dependency_creation, 1)
        ) / 10.0  # Normalize to 0-100

        return min(manipulation_score, 100.0)

    def generate_map_html(self, output_file: str = None) -> str:
        """Generate visual relationship map as HTML"""
        if output_file is None:
            output_file = self.case_dir / "relationship_map.html"

        # Build nodes and edges for visualization
        nodes = []
        for entity in self.entities.values():
            color = self._get_node_color(entity.manipulation_score)
            nodes.append({
                'id': entity.name,
                'label': entity.name,
                'type': entity.type,
                'score': entity.manipulation_score,
                'color': color
            })

        edges = []
        for rel in self.relationships:
            edges.append({
                'from': rel.entity1,
                'to': rel.entity2,
                'label': rel.type,
                'strength': rel.strength
            })

        # Generate HTML
        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>{self.case_name} - Relationship Map</title>
    <script src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #1a1a1a; color: #fff; }}
        #map {{ width: 100%; height: 80vh; border: 2px solid #333; background: #0a0a0a; }}
        .legend {{ margin-top: 20px; padding: 20px; background: #222; border-radius: 10px; }}
        .legend-item {{ display: inline-block; margin-right: 30px; }}
        .legend-color {{ display: inline-block; width: 20px; height: 20px; margin-right: 5px; vertical-align: middle; }}
    </style>
</head>
<body>
    <h1>🔍 {self.case_name}</h1>
    <p>Entities: {len(nodes)} | Relationships: {len(edges)}</p>
    <div id="map"></div>
    <div class="legend">
        <h3>Legend:</h3>
        <div class="legend-item"><span class="legend-color" style="background: #ff0000;"></span> High Risk (80+)</div>
        <div class="legend-item"><span class="legend-color" style="background: #ff8800;"></span> Medium Risk (60-79)</div>
        <div class="legend-item"><span class="legend-color" style="background: #ffff00;"></span> Low Risk (40-59)</div>
        <div class="legend-item"><span class="legend-color" style="background: #00ff00;"></span> Clear (&lt;40)</div>
    </div>
    <script>
        var nodes = new vis.DataSet({json.dumps(nodes)});
        var edges = new vis.DataSet({json.dumps(edges)});

        var container = document.getElementById('map');
        var data = {{ nodes: nodes, edges: edges }};
        var options = {{
            nodes: {{
                shape: 'dot',
                size: 20,
                font: {{ size: 14, color: '#ffffff' }},
                borderWidth: 2
            }},
            edges: {{
                width: 2,
                color: {{ color: '#666666', hover: '#ffffff' }},
                font: {{ size: 12, color: '#ffffff', align: 'top' }},
                arrows: {{ to: {{ enabled: true, scaleFactor: 0.5 }} }}
            }},
            physics: {{
                enabled: true,
                stabilization: {{ iterations: 100 }}
            }}
        }};

        var network = new vis.Network(container, data, options);

        network.on('click', function(params) {{
            if (params.nodes.length > 0) {{
                var nodeId = params.nodes[0];
                var node = nodes.get(nodeId);
                alert('Entity: ' + node.label + '\\nType: ' + node.type + '\\nManipulation Score: ' + node.score.toFixed(1));
            }}
        }});
    </script>
</body>
</html>"""

        with open(output_file, 'w') as f:
            f.write(html)

        print(f"\n🗺️  Map generated: {output_file}")
        return str(output_file)

    def _get_node_color(self, score: float) -> str:
        """Get node color based on manipulation score"""
        if score >= 80:
            return '#ff0000'  # Red - High risk
        elif score >= 60:
            return '#ff8800'  # Orange - Medium risk
        elif score >= 40:
            return '#ffff00'  # Yellow - Low risk
        else:
            return '#00ff00'  # Green - Clear

    def export_report(self, output_file: str = None) -> str:
        """Export court-ready investigation report"""
        if output_file is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = self.case_dir / f"investigation_report_{timestamp}.txt"

        report = []
        report.append("=" * 70)
        report.append(f"PRIVATE INVESTIGATION REPORT")
        report.append(f"Case: {self.case_name}")
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("=" * 70)
        report.append("")

        # Executive Summary
        report.append("EXECUTIVE SUMMARY")
        report.append("-" * 70)
        report.append(f"Total Entities Investigated: {len(self.entities)}")
        report.append(f"Total Relationships Mapped: {len(self.relationships)}")
        report.append(f"Evidence Items Analyzed: {len(self.evidence)}")
        report.append(f"Timeline Events: {len(self.timeline)}")
        report.append("")

        # High Risk Entities
        high_risk = [e for e in self.entities.values() if e.manipulation_score >= 80]
        if high_risk:
            report.append("HIGH RISK ENTITIES (Manipulation Score 80+)")
            report.append("-" * 70)
            for entity in high_risk:
                report.append(f"\n⚠️  {entity.name}")
                report.append(f"    Type: {entity.type}")
                report.append(f"    Manipulation Score: {entity.manipulation_score:.1f}/100")
                if entity.tactics:
                    report.append(f"    Tactics: {', '.join(entity.tactics)}")
                report.append(f"    Evidence Items: {len(entity.evidence)}")
            report.append("")

        # Relationship Network
        report.append("RELATIONSHIP NETWORK")
        report.append("-" * 70)
        for rel in self.relationships:
            report.append(f"{rel.entity1} → {rel.entity2} ({rel.type})")
        report.append("")

        # Timeline
        if self.timeline:
            report.append("TIMELINE OF EVENTS")
            report.append("-" * 70)
            sorted_timeline = sorted(self.timeline, key=lambda x: x.get('date', ''))
            for event in sorted_timeline:
                report.append(f"\n{event.get('date', 'Unknown date')}: {event.get('type', 'Event')}")
                if event.get('summary'):
                    report.append(f"  {event['summary']}")
            report.append("")

        # Recommendations
        report.append("RECOMMENDATIONS")
        report.append("-" * 70)
        if high_risk:
            report.append("1. Focus investigation on high-risk entities identified above")
            report.append("2. Subpoena communications between connected parties")
            report.append("3. Request financial records for suspicious transactions")
            report.append("4. Consider Pattern Theory analysis as expert evidence in court")
        else:
            report.append("No high-risk manipulation patterns detected.")
        report.append("")

        report.append("=" * 70)
        report.append("END OF REPORT")
        report.append("=" * 70)

        report_text = '\n'.join(report)

        with open(output_file, 'w') as f:
            f.write(report_text)

        print(f"\n📄 Report exported: {output_file}")
        return str(output_file)


def main():
    """CLI interface"""
    import sys
    import argparse

    parser = argparse.ArgumentParser(description='PI Mapping System - Private Investigation Tool')
    parser.add_argument('case_name', help='Name of the investigation case')
    parser.add_argument('--add-evidence', type=str, help='Add evidence from text file')
    parser.add_argument('--analyze', action='store_true', help='Run Pattern Theory analysis')
    parser.add_argument('--map', action='store_true', help='Generate relationship map')
    parser.add_argument('--report', action='store_true', help='Export investigation report')

    args = parser.parse_args()

    print("=" * 70)
    print("🔍 PI MAPPING SYSTEM")
    print("   Private Investigation & Corruption Mapping")
    print("=" * 70)

    mapper = PIMapper(args.case_name)

    if args.add_evidence:
        # Read evidence file
        with open(args.add_evidence, 'r') as f:
            evidence_text = f.read()

        mapper.add_evidence(evidence_text, evidence_type="document")

    if args.analyze:
        mapper.analyze_manipulation()

    if args.map:
        mapper.generate_map_html()

    if args.report:
        mapper.export_report()

    if not (args.add_evidence or args.analyze or args.map or args.report):
        print("\n💡 Usage:")
        print("  Add evidence:  python pi_mapper.py 'Case Name' --add-evidence evidence.txt")
        print("  Analyze:       python pi_mapper.py 'Case Name' --analyze")
        print("  Generate map:  python pi_mapper.py 'Case Name' --map")
        print("  Export report: python pi_mapper.py 'Case Name' --report")

    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()
