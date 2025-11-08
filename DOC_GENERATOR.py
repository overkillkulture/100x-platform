"""
DOCUMENTATION GENERATOR
Auto-generate documentation from code
"""

import os
import ast
from typing import List, Dict

class DocGenerator:
    def __init__(self):
        self.docs = []

    def parse_file(self, filepath: str) -> Dict:
        """Parse Python file and extract documentation"""
        with open(filepath, 'r') as f:
            content = f.read()

        try:
            tree = ast.parse(content)
        except:
            return {}

        doc = {
            'filepath': filepath,
            'classes': [],
            'functions': [],
            'docstring': ast.get_docstring(tree)
        }

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                doc['classes'].append({
                    'name': node.name,
                    'docstring': ast.get_docstring(node),
                    'methods': [m.name for m in node.body if isinstance(m, ast.FunctionDef)]
                })
            elif isinstance(node, ast.FunctionDef) and node.col_offset == 0:
                doc['functions'].append({
                    'name': node.name,
                    'docstring': ast.get_docstring(node),
                    'args': [arg.arg for arg in node.args.args]
                })

        return doc

    def generate_module_docs(self, module_path: str) -> str:
        """Generate markdown documentation for module"""
        docs = []

        # Find all Python files
        for root, dirs, files in os.walk(module_path):
            for file in files:
                if file.endswith('.py') and not file.startswith('__'):
                    filepath = os.path.join(root, file)
                    doc = self.parse_file(filepath)

                    if doc:
                        docs.append(self._format_doc(doc))

        return "\n\n".join(docs)

    def _format_doc(self, doc: Dict) -> str:
        """Format documentation as markdown"""
        md = f"## {os.path.basename(doc['filepath'])}\n\n"

        if doc.get('docstring'):
            md += f"{doc['docstring']}\n\n"

        if doc.get('classes'):
            md += "### Classes\n\n"
            for cls in doc['classes']:
                md += f"**{cls['name']}**\n"
                if cls['docstring']:
                    md += f"{cls['docstring']}\n"
                md += f"Methods: {', '.join(cls['methods'])}\n\n"

        if doc.get('functions'):
            md += "### Functions\n\n"
            for func in doc['functions']:
                md += f"**{func['name']}**({', '.join(func['args'])})\n"
                if func['docstring']:
                    md += f"{func['docstring']}\n"
                md += "\n"

        return md


if __name__ == "__main__":
    generator = DocGenerator()

    print("Generating documentation for pattern_recognition module...")
    docs = generator.generate_module_docs("MODULES/ADVANCED/pattern_recognition_engine")

    print(docs[:500])
    print("\n✅ Documentation generated!")
