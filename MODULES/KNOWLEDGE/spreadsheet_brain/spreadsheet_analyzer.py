#!/usr/bin/env python3
"""
SPREADSHEET BRAIN - AI-Powered Spreadsheet Analysis
Adds consciousness to your spreadsheets using Claude AI
"""

import os
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import pandas as pd

try:
    import anthropic
    from dotenv import load_dotenv
except ImportError:
    print("❌ Required packages missing")
    print("   pip install anthropic python-dotenv pandas openpyxl")
    exit(1)


class SpreadsheetBrain:
    """AI-powered spreadsheet analysis engine"""

    def __init__(self):
        load_dotenv()

        # Initialize Claude
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment")

        self.claude = anthropic.Anthropic(api_key=api_key)

        # Storage
        self.analysis_dir = Path.home() / ".spreadsheet_brain"
        self.analysis_dir.mkdir(exist_ok=True)

        self.current_data = None
        self.current_filename = None
        self.analysis_cache = {}

    def load_spreadsheet(self, file_path: str) -> bool:
        """Load spreadsheet from various formats"""
        file_path = Path(file_path)

        if not file_path.exists():
            print(f"❌ File not found: {file_path}")
            return False

        print(f"\n📊 Loading: {file_path.name}")

        try:
            # Detect file type and load
            if file_path.suffix in ['.xlsx', '.xls']:
                self.current_data = pd.read_excel(file_path)
            elif file_path.suffix == '.csv':
                self.current_data = pd.read_csv(file_path)
            else:
                print(f"❌ Unsupported format: {file_path.suffix}")
                return False

            self.current_filename = file_path.name

            print(f"   ✅ Loaded {len(self.current_data)} rows × {len(self.current_data.columns)} columns")
            print(f"   📋 Columns: {', '.join(self.current_data.columns.tolist())}")

            # Auto-generate initial insights
            print("\n🧠 Generating initial insights...")
            self.auto_insights()

            return True

        except Exception as e:
            print(f"❌ Failed to load: {e}")
            return False

    def auto_insights(self) -> Dict:
        """Automatically generate insights about the data"""
        if self.current_data is None:
            return {"error": "No data loaded"}

        # Prepare data summary for Claude
        data_summary = self._get_data_summary()

        prompt = f"""Analyze this spreadsheet and provide key insights.

Spreadsheet: {self.current_filename}
Rows: {len(self.current_data)}
Columns: {len(self.current_data.columns)}

Data Summary:
{data_summary}

First few rows:
{self.current_data.head(10).to_string()}

Provide:
1. **Key Trends** - What patterns do you see?
2. **Top Performers** - What's doing well?
3. **Areas of Concern** - What needs attention?
4. **Quick Wins** - What easy improvements can be made?
5. **Anomalies** - Any outliers or unusual data points?

Format as clear, actionable insights."""

        try:
            response = self.claude.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1500,
                messages=[{"role": "user", "content": prompt}]
            )

            insights = response.content[0].text

            # Cache insights
            self.analysis_cache['auto_insights'] = {
                'insights': insights,
                'generated': datetime.now().isoformat()
            }

            print("\n💡 AUTO-INSIGHTS:")
            print("=" * 60)
            print(insights)
            print("=" * 60)

            return self.analysis_cache['auto_insights']

        except Exception as e:
            print(f"⚠️ Auto-insights failed: {e}")
            return {"error": str(e)}

    def query(self, question: str) -> str:
        """Ask natural language questions about the data"""
        if self.current_data is None:
            return "No spreadsheet loaded. Load a file first."

        print(f"\n❓ Question: {question}")

        # Prepare context
        data_summary = self._get_data_summary()
        sample_data = self.current_data.head(20).to_string()

        prompt = f"""Answer this question about the spreadsheet data.

Spreadsheet: {self.current_filename}
Question: {question}

Data Summary:
{data_summary}

Sample Data (first 20 rows):
{sample_data}

Provide:
1. Direct answer to the question
2. Supporting data/evidence
3. Confidence level (High/Medium/Low)
4. Recommendations based on the answer

Be specific with numbers, percentages, and data points."""

        try:
            response = self.claude.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1000,
                messages=[{"role": "user", "content": prompt}]
            )

            answer = response.content[0].text

            print("\n💡 ANSWER:")
            print("=" * 60)
            print(answer)
            print("=" * 60)

            # Cache query result
            if 'queries' not in self.analysis_cache:
                self.analysis_cache['queries'] = []

            self.analysis_cache['queries'].append({
                'question': question,
                'answer': answer,
                'timestamp': datetime.now().isoformat()
            })

            return answer

        except Exception as e:
            error_msg = f"Query failed: {e}"
            print(f"❌ {error_msg}")
            return error_msg

    def detect_manipulation(self) -> Dict:
        """Use Pattern Theory to detect data manipulation"""
        if self.current_data is None:
            return {"error": "No data loaded"}

        print("\n🔍 Running Pattern Theory manipulation detection...")

        data_summary = self._get_data_summary()

        prompt = f"""Use Pattern Theory to detect potential data manipulation in this spreadsheet.

Pattern Theory Formula: M = (FE × CB × SR × CD × PE) × DC

Look for:
- **Frequency Escalation (FE):** Are there unusual spikes or patterns?
- **Confusion Building (CB):** Are there inconsistencies or conflicting data?
- **Stress Response (SR):** Are there data points that don't make sense?
- **Complexity/Dependency (CD):** Is the data unnecessarily complex?
- **Pattern Escaping (PE):** Are there attempts to hide patterns?
- **Dependency Creation (DC):** Is there suspicious data clustering?

Data Summary:
{data_summary}

Sample Data:
{self.current_data.head(50).to_string()}

Provide:
1. **Manipulation Score (0-100):** Overall manipulation likelihood
2. **Suspicious Patterns:** List specific anomalies
3. **Red Flags:** What to investigate further
4. **Clean Data:** What looks legitimate
5. **Recommendations:** What to do next"""

        try:
            response = self.claude.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1500,
                messages=[{"role": "user", "content": prompt}]
            )

            analysis = response.content[0].text

            print("\n🎯 MANIPULATION DETECTION:")
            print("=" * 60)
            print(analysis)
            print("=" * 60)

            return {
                'analysis': analysis,
                'timestamp': datetime.now().isoformat()
            }

        except Exception as e:
            print(f"❌ Detection failed: {e}")
            return {"error": str(e)}

    def get_recommendations(self) -> List[str]:
        """Get AI-powered recommendations"""
        if self.current_data is None:
            return ["Load a spreadsheet first"]

        print("\n💡 Generating recommendations...")

        data_summary = self._get_data_summary()

        prompt = f"""Provide actionable recommendations based on this data.

Data Summary:
{data_summary}

Sample Data:
{self.current_data.head(20).to_string()}

Provide 5-10 specific, actionable recommendations like:
- "Raise prices on Product X (inelastic demand, 45% margin opportunity)"
- "Contact Customer Y (high value, declining orders)"
- "Cut Marketing Channel Z (negative ROI, $5K/month waste)"

Each recommendation should:
1. Be specific and actionable
2. Include data backing
3. Show expected impact
4. Have a confidence score"""

        try:
            response = self.claude.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1000,
                messages=[{"role": "user", "content": prompt}]
            )

            recommendations = response.content[0].text

            print("\n🎯 RECOMMENDATIONS:")
            print("=" * 60)
            print(recommendations)
            print("=" * 60)

            return recommendations.split('\n')

        except Exception as e:
            print(f"❌ Recommendations failed: {e}")
            return [f"Error: {e}"]

    def _get_data_summary(self) -> str:
        """Generate statistical summary of current data"""
        if self.current_data is None:
            return "No data loaded"

        summary = []
        summary.append(f"Total rows: {len(self.current_data)}")
        summary.append(f"Total columns: {len(self.current_data.columns)}")
        summary.append(f"\nColumns: {', '.join(self.current_data.columns.tolist())}")

        # Numeric columns statistics
        numeric_cols = self.current_data.select_dtypes(include=['number']).columns
        if len(numeric_cols) > 0:
            summary.append(f"\nNumeric columns: {', '.join(numeric_cols.tolist())}")
            summary.append("\nStatistics:")
            summary.append(self.current_data[numeric_cols].describe().to_string())

        # Non-numeric columns
        text_cols = self.current_data.select_dtypes(include=['object']).columns
        if len(text_cols) > 0:
            summary.append(f"\nText columns: {', '.join(text_cols.tolist())}")
            for col in text_cols:
                unique_count = self.current_data[col].nunique()
                summary.append(f"  {col}: {unique_count} unique values")

        return '\n'.join(summary)

    def export_analysis(self, output_path: Optional[str] = None) -> str:
        """Export all analysis to JSON file"""
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = self.analysis_dir / f"analysis_{timestamp}.json"

        analysis_export = {
            'filename': self.current_filename,
            'analyzed': datetime.now().isoformat(),
            'data_shape': {
                'rows': len(self.current_data) if self.current_data is not None else 0,
                'columns': len(self.current_data.columns) if self.current_data is not None else 0
            },
            'cache': self.analysis_cache
        }

        with open(output_path, 'w') as f:
            json.dump(analysis_export, f, indent=2)

        print(f"\n💾 Analysis exported to: {output_path}")
        return str(output_path)


def main():
    """CLI interface"""
    import sys
    import argparse

    parser = argparse.ArgumentParser(description='Spreadsheet Brain - AI-Powered Spreadsheet Analysis')
    parser.add_argument('file', nargs='?', help='Spreadsheet file to analyze')
    parser.add_argument('--query', type=str, help='Ask a question about the data')
    parser.add_argument('--insights', action='store_true', help='Generate auto insights')
    parser.add_argument('--detect', action='store_true', help='Run manipulation detection')
    parser.add_argument('--recommend', action='store_true', help='Get recommendations')
    parser.add_argument('--export', type=str, help='Export analysis to JSON')

    args = parser.parse_args()

    print("=" * 60)
    print("📊 SPREADSHEET BRAIN")
    print("   AI-Powered Spreadsheet Analysis")
    print("=" * 60)

    brain = SpreadsheetBrain()

    if args.file:
        # Load spreadsheet
        if not brain.load_spreadsheet(args.file):
            return

        # Execute requested operation
        if args.query:
            brain.query(args.query)
        elif args.detect:
            brain.detect_manipulation()
        elif args.recommend:
            brain.get_recommendations()
        elif args.insights:
            brain.auto_insights()

        # Export if requested
        if args.export:
            brain.export_analysis(args.export)

    else:
        # Interactive mode
        print("\n💡 Usage:")
        print("  Analyze:     python spreadsheet_analyzer.py data.xlsx")
        print("  Query:       python spreadsheet_analyzer.py data.xlsx --query 'What is my revenue trend?'")
        print("  Detect:      python spreadsheet_analyzer.py data.xlsx --detect")
        print("  Recommend:   python spreadsheet_analyzer.py data.xlsx --recommend")
        print("  Export:      python spreadsheet_analyzer.py data.xlsx --export results.json")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
