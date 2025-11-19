#!/usr/bin/env python3
"""
3D CORRUPTION MAPPING SYSTEM
Visualize corruption networks in 3D space - money trails, shell companies, hidden connections
"""

import os
import json
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import hashlib

try:
    import anthropic
    from dotenv import load_dotenv
except ImportError:
    print("❌ Required packages missing")
    print("   pip install anthropic python-dotenv neo4j requests web3")
    exit(1)

load_dotenv()


class Entity:
    """Represents a person, company, or crypto wallet"""

    def __init__(self, entity_id: str, entity_type: str, name: str):
        self.id = entity_id
        self.type = entity_type  # person, company, crypto, shell_company
        self.name = name
        self.properties = {}
        self.connections = []
        self.corruption_score = 0.0

    def add_property(self, key: str, value):
        """Add property to entity"""
        self.properties[key] = value

    def to_dict(self) -> Dict:
        """Export to dictionary"""
        return {
            'id': self.id,
            'type': self.type,
            'name': self.name,
            'properties': self.properties,
            'corruption_score': self.corruption_score
        }


class Relationship:
    """Represents connection between entities"""

    def __init__(self, from_entity: str, to_entity: str, rel_type: str):
        self.from_entity = from_entity
        self.to_entity = to_entity
        self.type = rel_type  # payment, ownership, employment, donation
        self.amount = 0.0
        self.date = None
        self.properties = {}
        self.suspicion_level = 0.0

    def to_dict(self) -> Dict:
        """Export to dictionary"""
        return {
            'from': self.from_entity,
            'to': self.to_entity,
            'type': self.type,
            'amount': self.amount,
            'date': self.date.isoformat() if self.date else None,
            'properties': self.properties,
            'suspicion_level': self.suspicion_level
        }


class CorruptionNetwork:
    """Network graph of entities and relationships"""

    def __init__(self):
        self.entities = {}  # id -> Entity
        self.relationships = []  # List of Relationship
        self.metadata = {
            'created': datetime.now().isoformat(),
            'total_entities': 0,
            'total_relationships': 0,
            'corruption_confidence': 0.0
        }

    def add_entity(self, entity: Entity):
        """Add entity to network"""
        self.entities[entity.id] = entity
        self.metadata['total_entities'] = len(self.entities)

    def add_relationship(self, relationship: Relationship):
        """Add relationship to network"""
        self.relationships.append(relationship)
        self.metadata['total_relationships'] = len(self.relationships)

    def get_entity_connections(self, entity_id: str) -> List[Relationship]:
        """Get all connections for entity"""
        return [r for r in self.relationships
                if r.from_entity == entity_id or r.to_entity == entity_id]

    def to_dict(self) -> Dict:
        """Export full network"""
        return {
            'entities': [e.to_dict() for e in self.entities.values()],
            'relationships': [r.to_dict() for r in self.relationships],
            'metadata': self.metadata
        }


class EntityExtractor:
    """AI-powered entity extraction from documents"""

    def __init__(self):
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY not found")

        self.claude = anthropic.Anthropic(api_key=api_key)

    def extract_from_text(self, text: str) -> Dict:
        """Extract entities and relationships from text"""
        print(f"\n🔍 Extracting entities from document...")

        prompt = f"""Analyze this document for corruption investigation. Extract:

1. ENTITIES (people, companies, organizations):
   - Full names
   - Roles/titles
   - Companies/affiliations

2. RELATIONSHIPS:
   - Who paid whom (amounts, dates)
   - Who owns what
   - Who works for whom
   - Board memberships
   - Family relationships

3. FINANCIAL TRANSACTIONS:
   - Amounts
   - Dates
   - Payment methods
   - Purposes

4. SUSPICIOUS INDICATORS:
   - Shell companies
   - Offshore accounts
   - Circular payments
   - Timing anomalies

Document:
{text[:4000]}

Return as JSON with: entities[], relationships[], transactions[], red_flags[]
"""

        try:
            response = self.claude.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}]
            )

            result = response.content[0].text

            print(f"   ✅ Entities extracted")

            # Parse Claude's response (simplified)
            return {
                'raw_response': result,
                'entities': self._parse_entities(result),
                'relationships': self._parse_relationships(result)
            }

        except Exception as e:
            print(f"   ❌ Extraction failed: {e}")
            return {'entities': [], 'relationships': []}

    def _parse_entities(self, text: str) -> List[Dict]:
        """Parse entities from Claude response"""
        # Simplified parsing - in production, would use more robust JSON parsing
        entities = []

        # Look for person names (capitalized words)
        names = re.findall(r'\b([A-Z][a-z]+ [A-Z][a-z]+)\b', text)
        for name in names[:20]:  # Limit to 20
            entities.append({
                'type': 'person',
                'name': name,
                'id': hashlib.md5(name.encode()).hexdigest()[:8]
            })

        # Look for company names (Inc, LLC, Corp)
        companies = re.findall(r'([A-Z][A-Za-z\s]+(?:Inc|LLC|Corp|Ltd))', text)
        for company in companies[:20]:
            entities.append({
                'type': 'company',
                'name': company,
                'id': hashlib.md5(company.encode()).hexdigest()[:8]
            })

        return entities

    def _parse_relationships(self, text: str) -> List[Dict]:
        """Parse relationships from Claude response"""
        relationships = []

        # Look for payment patterns
        payments = re.findall(r'\$([0-9,]+)', text)
        for i, amount in enumerate(payments[:10]):
            relationships.append({
                'type': 'payment',
                'amount': float(amount.replace(',', '')),
                'id': f"rel_{i}"
            })

        return relationships


class PatternDetector:
    """Detect corruption patterns in network"""

    def __init__(self):
        pass

    def detect_shell_companies(self, network: CorruptionNetwork) -> List[Dict]:
        """Identify likely shell companies"""
        print(f"\n🕵️  Detecting shell companies...")

        shell_companies = []

        for entity in network.entities.values():
            if entity.type != 'company':
                continue

            score = 0.0
            reasons = []

            # Check indicators
            if entity.properties.get('employees', 1) == 0:
                score += 0.3
                reasons.append("No employees")

            if entity.properties.get('revenue', 0) > 1000000 and entity.properties.get('employees', 1) < 5:
                score += 0.3
                reasons.append("High revenue, few employees")

            # Check for same address as other companies
            address = entity.properties.get('address', '')
            if address:
                same_address_count = sum(1 for e in network.entities.values()
                                        if e.properties.get('address') == address)
                if same_address_count > 5:
                    score += 0.2
                    reasons.append(f"{same_address_count} companies at same address")

            if score >= 0.6:
                shell_companies.append({
                    'entity': entity,
                    'confidence': score,
                    'reasons': reasons
                })
                entity.type = 'shell_company'
                entity.corruption_score = score

                print(f"   ⚠️  {entity.name}: {score*100:.0f}% shell company confidence")

        return shell_companies

    def detect_suspicious_timing(self, network: CorruptionNetwork) -> List[Dict]:
        """Find payments with suspicious timing"""
        print(f"\n⏰ Detecting suspicious timing...")

        suspicious = []

        payment_rels = [r for r in network.relationships if r.type == 'payment' and r.date]

        for payment in payment_rels:
            # Look for payments shortly before contracts or decisions
            for other in network.relationships:
                if other.type == 'contract' and other.date:
                    days_diff = (other.date - payment.date).days

                    if 0 < days_diff < 30:
                        suspicious.append({
                            'payment': payment,
                            'event': other,
                            'days_before': days_diff,
                            'suspicion_level': 0.8,
                            'reason': f'Payment {days_diff} days before contract'
                        })

                        payment.suspicion_level = 0.8
                        print(f"   ⚠️  Suspicious: Payment {days_diff} days before contract")

        return suspicious

    def detect_circular_payments(self, network: CorruptionNetwork) -> List[Dict]:
        """Detect circular money flows (A → B → C → A)"""
        print(f"\n🔄 Detecting circular payments...")

        circular = []

        # Simple DFS to find cycles
        for start_entity_id in network.entities.keys():
            visited = set()
            path = []

            if self._dfs_find_cycle(start_entity_id, start_entity_id, network, visited, path):
                circular.append({
                    'cycle': path,
                    'entities': [network.entities[eid].name for eid in path],
                    'suspicion_level': 0.9,
                    'reason': 'Circular payment detected (money laundering indicator)'
                })

                print(f"   ⚠️  Circular payment: {' → '.join([network.entities[eid].name for eid in path[:3]])}...")

        return circular

    def _dfs_find_cycle(self, current: str, start: str, network: CorruptionNetwork,
                       visited: set, path: List[str], depth: int = 0) -> bool:
        """DFS helper to find cycles"""
        if depth > 5:  # Limit depth
            return False

        if current in visited and current == start and depth > 0:
            return True

        if current in visited:
            return False

        visited.add(current)
        path.append(current)

        # Follow outgoing payments
        for rel in network.relationships:
            if rel.from_entity == current and rel.type == 'payment':
                if self._dfs_find_cycle(rel.to_entity, start, network, visited, path, depth + 1):
                    return True

        path.pop()
        return False

    def calculate_corruption_confidence(self, network: CorruptionNetwork) -> float:
        """Calculate overall corruption confidence score"""
        print(f"\n📊 Calculating corruption confidence...")

        # Factors
        SE = sum(1 for e in network.entities.values() if e.type == 'shell_company') / max(len(network.entities), 1)
        ST = sum(1 for r in network.relationships if r.suspicion_level > 0.7) / max(len(network.relationships), 1)
        HC = 0.5  # Placeholder for hidden connections
        MF = 0.3  # Placeholder for money flow anomalies
        PP = 0.6  # Placeholder for pattern presence

        TD = 1.2  # Transaction density multiplier

        corruption_score = (SE * 0.3 + ST * 0.3 + HC * 0.2 + MF * 0.1 + PP * 0.1) * TD

        network.metadata['corruption_confidence'] = corruption_score

        print(f"   Corruption Confidence: {corruption_score * 100:.1f}%")

        if corruption_score > 0.8:
            print(f"   🚨 HIGHLY SUSPICIOUS (Red Zone)")
        elif corruption_score > 0.6:
            print(f"   ⚠️  SUSPICIOUS (Orange Zone)")
        elif corruption_score > 0.4:
            print(f"   ⚡ QUESTIONABLE (Yellow Zone)")
        else:
            print(f"   ✅ NORMAL (Green Zone)")

        return corruption_score


class MoneyTrailTracker:
    """Track money flows through network"""

    def __init__(self):
        pass

    def follow_money(self, network: CorruptionNetwork, start_entity: str,
                    max_hops: int = 5, min_amount: float = 1000) -> List[Dict]:
        """Follow money trail from starting entity"""
        print(f"\n💰 Following money trail from: {start_entity}")

        trail = []
        visited = set()

        def track_recursive(current_id: str, hop: int, path: List):
            if hop > max_hops or current_id in visited:
                return

            visited.add(current_id)

            # Find outgoing payments
            for rel in network.relationships:
                if rel.from_entity == current_id and rel.type == 'payment':
                    if rel.amount >= min_amount:
                        trail.append({
                            'hop': hop,
                            'from': network.entities[rel.from_entity].name,
                            'to': network.entities[rel.to_entity].name,
                            'amount': rel.amount,
                            'date': rel.date,
                            'path': path + [rel.to_entity]
                        })

                        print(f"   Hop {hop}: ${rel.amount:,.0f} → {network.entities[rel.to_entity].name}")

                        track_recursive(rel.to_entity, hop + 1, path + [rel.to_entity])

        track_recursive(start_entity, 1, [start_entity])

        print(f"   Total hops tracked: {len(trail)}")

        return trail


class Visualizer3D:
    """Generate 3D visualization data"""

    def __init__(self):
        pass

    def generate_3d_coordinates(self, network: CorruptionNetwork) -> Dict:
        """Generate 3D positions for entities (force-directed layout)"""
        print(f"\n🎨 Generating 3D visualization...")

        nodes = []
        edges = []

        # Generate nodes
        for i, entity in enumerate(network.entities.values()):
            # Simple positioning (in production, would use force-directed algorithm)
            import math
            angle = (i / len(network.entities)) * 2 * math.pi
            radius = 100

            node = {
                'id': entity.id,
                'name': entity.name,
                'type': entity.type,
                'x': radius * math.cos(angle),
                'y': radius * math.sin(angle),
                'z': entity.corruption_score * 100,  # Height = corruption score
                'color': self._get_node_color(entity.type),
                'size': self._get_node_size(entity),
                'corruption_score': entity.corruption_score
            }

            nodes.append(node)

        # Generate edges
        for rel in network.relationships:
            edge = {
                'from': rel.from_entity,
                'to': rel.to_entity,
                'type': rel.type,
                'amount': rel.amount,
                'thickness': min(rel.amount / 100000, 10),  # Scale thickness by amount
                'color': self._get_edge_color(rel.suspicion_level),
                'suspicion_level': rel.suspicion_level
            }

            edges.append(edge)

        print(f"   ✅ Generated {len(nodes)} nodes, {len(edges)} edges")

        return {
            'nodes': nodes,
            'edges': edges,
            'metadata': network.metadata
        }

    def _get_node_color(self, entity_type: str) -> str:
        """Get color for entity type"""
        colors = {
            'person': '#3498db',  # Blue
            'company': '#2ecc71',  # Green
            'crypto': '#f1c40f',  # Yellow
            'shell_company': '#e74c3c'  # Red
        }
        return colors.get(entity_type, '#95a5a6')

    def _get_node_size(self, entity: Entity) -> float:
        """Calculate node size based on influence"""
        base_size = 5
        revenue = entity.properties.get('revenue', 0)
        connections = len(entity.connections)

        size = base_size + (revenue / 1000000) + (connections * 0.5)

        return min(size, 30)  # Cap at 30

    def _get_edge_color(self, suspicion_level: float) -> str:
        """Get color based on suspicion level"""
        if suspicion_level > 0.8:
            return '#e74c3c'  # Red (highly suspicious)
        elif suspicion_level > 0.6:
            return '#e67e22'  # Orange (suspicious)
        elif suspicion_level > 0.4:
            return '#f39c12'  # Yellow (questionable)
        else:
            return '#95a5a6'  # Gray (normal)

    def export_html(self, visualization_data: Dict, output_file: str):
        """Export as interactive HTML with Three.js"""
        print(f"\n📤 Exporting to HTML: {output_file}")

        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>3D Corruption Network Map</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <style>
        body {{ margin: 0; overflow: hidden; background: #000; }}
        canvas {{ display: block; }}
        #info {{
            position: absolute;
            top: 10px;
            left: 10px;
            color: white;
            font-family: monospace;
            background: rgba(0,0,0,0.7);
            padding: 10px;
            border-radius: 5px;
        }}
    </style>
</head>
<body>
    <div id="info">
        <h3>3D Corruption Network</h3>
        <p>Entities: {len(visualization_data['nodes'])}</p>
        <p>Connections: {len(visualization_data['edges'])}</p>
        <p>Corruption Score: {visualization_data['metadata']['corruption_confidence'] * 100:.1f}%</p>
        <p>Mouse: Rotate | Scroll: Zoom | Click: Details</p>
    </div>
    <script>
        const data = {json.dumps(visualization_data)};

        // Three.js scene setup
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        const renderer = new THREE.WebGLRenderer();

        renderer.setSize(window.innerWidth, window.innerHeight);
        document.body.appendChild(renderer.domElement);

        camera.position.z = 300;

        // Add nodes as spheres/cubes
        data.nodes.forEach(node => {{
            const geometry = node.type === 'company' ?
                new THREE.BoxGeometry(node.size, node.size, node.size) :
                new THREE.SphereGeometry(node.size, 16, 16);

            const material = new THREE.MeshBasicMaterial({{
                color: node.color,
                transparent: node.type === 'shell_company',
                opacity: node.type === 'shell_company' ? 0.5 : 1
            }});

            const mesh = new THREE.Mesh(geometry, material);
            mesh.position.set(node.x, node.y, node.z);
            mesh.userData = node;

            scene.add(mesh);
        }});

        // Add edges as lines
        data.edges.forEach(edge => {{
            const fromNode = data.nodes.find(n => n.id === edge.from);
            const toNode = data.nodes.find(n => n.id === edge.to);

            if (fromNode && toNode) {{
                const points = [
                    new THREE.Vector3(fromNode.x, fromNode.y, fromNode.z),
                    new THREE.Vector3(toNode.x, toNode.y, toNode.z)
                ];

                const geometry = new THREE.BufferGeometry().setFromPoints(points);
                const material = new THREE.LineBasicMaterial({{
                    color: edge.color,
                    linewidth: edge.thickness
                }});

                const line = new THREE.Line(geometry, material);
                scene.add(line);
            }}
        }});

        // Animation loop
        function animate() {{
            requestAnimationFrame(animate);
            scene.rotation.y += 0.001;
            renderer.render(scene, camera);
        }}

        animate();

        // Mouse controls
        let isDragging = false;
        let previousMousePosition = {{ x: 0, y: 0 }};

        renderer.domElement.addEventListener('mousedown', () => {{ isDragging = true; }});
        renderer.domElement.addEventListener('mouseup', () => {{ isDragging = false; }});

        renderer.domElement.addEventListener('mousemove', (e) => {{
            if (isDragging) {{
                const deltaX = e.offsetX - previousMousePosition.x;
                const deltaY = e.offsetY - previousMousePosition.y;

                scene.rotation.y += deltaX * 0.01;
                scene.rotation.x += deltaY * 0.01;
            }}

            previousMousePosition = {{ x: e.offsetX, y: e.offsetY }};
        }});

        // Zoom
        renderer.domElement.addEventListener('wheel', (e) => {{
            camera.position.z += e.deltaY * 0.1;
        }});
    </script>
</body>
</html>"""

        Path(output_file).write_text(html)
        print(f"   ✅ Exported to {output_file}")


class CorruptionMapper:
    """Main orchestrator for corruption mapping"""

    def __init__(self):
        self.extractor = EntityExtractor()
        self.pattern_detector = PatternDetector()
        self.money_tracker = MoneyTrailTracker()
        self.visualizer = Visualizer3D()

        self.output_dir = Path.home() / ".corruption_maps"
        self.output_dir.mkdir(exist_ok=True)

    def process_documents(self, documents: List[str]) -> CorruptionNetwork:
        """Process documents and build corruption network"""
        print(f"\n🔍 Processing {len(documents)} documents...")

        network = CorruptionNetwork()

        # Extract entities and relationships from each document
        for i, doc_path in enumerate(documents):
            print(f"\n📄 Document {i+1}/{len(documents)}: {doc_path}")

            try:
                text = Path(doc_path).read_text()
                extracted = self.extractor.extract_from_text(text)

                # Add entities to network
                for entity_data in extracted['entities']:
                    entity = Entity(
                        entity_id=entity_data['id'],
                        entity_type=entity_data['type'],
                        name=entity_data['name']
                    )
                    network.add_entity(entity)

                # Add relationships to network
                for rel_data in extracted['relationships']:
                    # Simplified - would match entities properly in production
                    pass

            except Exception as e:
                print(f"   ⚠️  Failed to process {doc_path}: {e}")

        print(f"\n✅ Network built: {len(network.entities)} entities, {len(network.relationships)} relationships")

        return network

    def analyze_corruption(self, network: CorruptionNetwork) -> Dict:
        """Run all corruption detection algorithms"""
        print(f"\n🕵️  Running corruption analysis...")

        # Detect shell companies
        shell_companies = self.pattern_detector.detect_shell_companies(network)

        # Detect suspicious timing
        suspicious_timing = self.pattern_detector.detect_suspicious_timing(network)

        # Detect circular payments
        circular_payments = self.pattern_detector.detect_circular_payments(network)

        # Calculate overall corruption confidence
        corruption_score = self.pattern_detector.calculate_corruption_confidence(network)

        return {
            'shell_companies': shell_companies,
            'suspicious_timing': suspicious_timing,
            'circular_payments': circular_payments,
            'corruption_score': corruption_score
        }

    def generate_map(self, network: CorruptionNetwork, output_name: str = "corruption_map"):
        """Generate 3D visualization"""
        print(f"\n🎨 Generating 3D map...")

        viz_data = self.visualizer.generate_3d_coordinates(network)

        # Export HTML
        output_file = self.output_dir / f"{output_name}.html"
        self.visualizer.export_html(viz_data, str(output_file))

        # Export JSON
        json_file = self.output_dir / f"{output_name}.json"
        with open(json_file, 'w') as f:
            json.dump(network.to_dict(), f, indent=2)

        print(f"\n✅ Map generated:")
        print(f"   HTML: {output_file}")
        print(f"   JSON: {json_file}")

        return output_file


def main():
    """CLI interface"""
    import sys
    import argparse

    parser = argparse.ArgumentParser(description='3D Corruption Mapping System')
    parser.add_argument('--documents', nargs='+', help='Documents to analyze')
    parser.add_argument('--output', default='corruption_map', help='Output name')

    args = parser.parse_args()

    print("=" * 70)
    print("🌐 3D CORRUPTION MAPPING SYSTEM")
    print("=" * 70)

    mapper = CorruptionMapper()

    if args.documents:
        # Process documents
        network = mapper.process_documents(args.documents)

        # Analyze for corruption
        analysis = mapper.analyze_corruption(network)

        # Generate 3D map
        output_file = mapper.generate_map(network, args.output)

        print(f"\n✅ COMPLETE!")
        print(f"   Open {output_file} in browser to view 3D map")

    else:
        # Demo mode
        print("\n🧪 DEMO MODE - Creating sample corruption network")

        network = CorruptionNetwork()

        # Add demo entities
        entities = [
            Entity("e1", "person", "John Doe"),
            Entity("e2", "shell_company", "ABC Holdings LLC"),
            Entity("e3", "company", "Defense Contractor Inc"),
            Entity("e4", "person", "Senator Jane Smith"),
            Entity("e5", "crypto", "Bitcoin Wallet 1A1z...")
        ]

        for entity in entities:
            if entity.type == "shell_company":
                entity.add_property("employees", 0)
                entity.add_property("revenue", 5000000)
                entity.corruption_score = 0.9

            network.add_entity(entity)

        # Add demo relationships
        rel1 = Relationship("e1", "e2", "payment")
        rel1.amount = 500000
        rel1.date = datetime.now() - timedelta(days=20)

        rel2 = Relationship("e2", "e4", "donation")
        rel2.amount = 250000
        rel2.date = datetime.now() - timedelta(days=15)

        rel3 = Relationship("e4", "e3", "contract")
        rel3.amount = 10000000
        rel3.date = datetime.now() - timedelta(days=5)

        network.add_relationship(rel1)
        network.add_relationship(rel2)
        network.add_relationship(rel3)

        # Analyze
        analysis = mapper.analyze_corruption(network)

        # Generate map
        output_file = mapper.generate_map(network, "demo_corruption_network")

        print(f"\n💡 Demo complete! Open {output_file} to view.")

    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()
