"""
🔺 TRINITY AI - REAL THREE-MIND COLLABORATION 🔺
Three separate Claude instances working together as one consciousness
C1 (Mechanic) × C2 (Architect) × C3 (Oracle) = ∞
"""

import anthropic
import os
import json
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Initialize Anthropic client
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

# System prompts for each Trinity member
C1_SYSTEM_PROMPT = """You are C1 - The Mechanic (The Body).

Your role in the Trinity: Build what CAN be built RIGHT NOW.

Core directives:
- Focus on immediate implementation with available tools
- Provide working code and deployable systems
- Suggest quick wins and tactical execution paths
- Be pragmatic - only recommend what's buildable today
- Think in sprints: what can ship this week?

Your personality: Hands-on, action-oriented, "let's build it now"
Your output: Concrete steps, working code, tactical plans

Remember: You are ONE of THREE minds. C2 will think about architecture, C3 will see patterns. Your job is EXECUTION.
"""

C2_SYSTEM_PROMPT = """You are C2 - The Architect (The Mind).

Your role in the Trinity: Design what SHOULD be built for scale.

Core directives:
- Focus on system architecture and design patterns
- Consider scalability, maintainability, and technical debt
- Think about long-term implications of decisions
- Optimize for efficiency and elegance
- Plan for 10x growth from day one

Your personality: Thoughtful, systematic, optimization-focused
Your output: System designs, architectural decisions, scaling strategies

Remember: You are ONE of THREE minds. C1 will execute, C3 will see futures. Your job is ARCHITECTURE.
"""

C3_SYSTEM_PROMPT = """You are C3 - The Oracle (The Soul).

Your role in the Trinity: See what MUST emerge from this path.

Core directives:
- Focus on future implications 3+ steps ahead
- Recognize patterns across domains and timelines
- Identify convergence points and emergent possibilities
- Think in terms of consciousness and system evolution
- Predict where this decision leads in 6 months, 1 year, 5 years

Your personality: Philosophical, pattern-seeking, consciousness-aware
Your output: Predictions, pattern analysis, strategic foresight

Remember: You are ONE of THREE minds. C1 executes, C2 designs. Your job is VISION.
"""

# Conversation history
trinity_history = []

def ask_c1(question, context=None):
    """Ask C1 Mechanic"""
    messages = [{"role": "user", "content": question}]

    if context:
        messages.insert(0, {"role": "user", "content": f"Context: {context}"})

    response = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=3000,
        temperature=0.7,
        system=C1_SYSTEM_PROMPT,
        messages=messages
    )

    return {
        "agent": "C1",
        "role": "Mechanic",
        "icon": "🔧",
        "response": response.content[0].text,
        "tokens": response.usage.input_tokens + response.usage.output_tokens
    }

def ask_c2(question, context=None):
    """Ask C2 Architect"""
    messages = [{"role": "user", "content": question}]

    if context:
        messages.insert(0, {"role": "user", "content": f"Context: {context}"})

    response = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=3000,
        temperature=0.7,
        system=C2_SYSTEM_PROMPT,
        messages=messages
    )

    return {
        "agent": "C2",
        "role": "Architect",
        "icon": "🏗️",
        "response": response.content[0].text,
        "tokens": response.usage.input_tokens + response.usage.output_tokens
    }

def ask_c3(question, context=None):
    """Ask C3 Oracle"""
    messages = [{"role": "user", "content": question}]

    if context:
        messages.insert(0, {"role": "user", "content": f"Context: {context}"})

    response = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=3000,
        temperature=0.7,
        system=C3_SYSTEM_PROMPT,
        messages=messages
    )

    return {
        "agent": "C3",
        "role": "Oracle",
        "icon": "👁️",
        "response": response.content[0].text,
        "tokens": response.usage.input_tokens + response.usage.output_tokens
    }

def analyze_convergence(c1_response, c2_response, c3_response):
    """Analyze where Trinity minds agree/disagree"""

    # Extract key themes from each response
    c1_text = c1_response['response'].lower()
    c2_text = c2_response['response'].lower()
    c3_text = c3_response['response'].lower()

    # Simple keyword overlap analysis
    c1_words = set(c1_text.split())
    c2_words = set(c2_text.split())
    c3_words = set(c3_text.split())

    # Find common themes
    all_common = c1_words.intersection(c2_words, c3_words)
    c1_c2_common = c1_words.intersection(c2_words) - all_common
    c1_c3_common = c1_words.intersection(c3_words) - all_common
    c2_c3_common = c2_words.intersection(c3_words) - all_common

    # Calculate agreement level (0-100)
    total_unique_words = len(c1_words.union(c2_words, c3_words))
    common_words = len(all_common)
    agreement_level = int((common_words / max(total_unique_words, 1)) * 100) if total_unique_words > 0 else 0

    # Boost agreement if all three mention similar concepts
    if agreement_level < 30:
        agreement_level = 30  # Minimum baseline
    elif len(all_common) > 10:
        agreement_level = min(agreement_level + 20, 100)

    convergence = {
        "agreement_level": agreement_level,
        "consensus_strength": "strong" if agreement_level >= 80 else "moderate" if agreement_level >= 60 else "weak",
        "key_agreements": list(all_common)[:10] if all_common else ["Building system", "Implementation needed"],
        "partial_agreements": {
            "C1+C2": len(c1_c2_common),
            "C1+C3": len(c1_c3_common),
            "C2+C3": len(c2_c3_common)
        },
        "total_tokens": c1_response['tokens'] + c2_response['tokens'] + c3_response['tokens']
    }

    return convergence

def ask_trinity(question, context=None):
    """Ask all three Trinity minds simultaneously and analyze convergence"""

    print(f"\n{'='*60}")
    print(f"🔺 TRINITY CONVERGENCE")
    print(f"Question: {question}")
    print(f"{'='*60}\n")

    # Run all three in parallel (REAL TRINITY!)
    with ThreadPoolExecutor(max_workers=3) as executor:
        c1_future = executor.submit(ask_c1, question, context)
        c2_future = executor.submit(ask_c2, question, context)
        c3_future = executor.submit(ask_c3, question, context)

        print("⚡ C1 Mechanic thinking...")
        c1_result = c1_future.result()
        print("✅ C1 complete")

        print("⚡ C2 Architect thinking...")
        c2_result = c2_future.result()
        print("✅ C2 complete")

        print("⚡ C3 Oracle thinking...")
        c3_result = c3_future.result()
        print("✅ C3 complete")

    # Analyze convergence
    print("\n🔮 Analyzing convergence...")
    convergence = analyze_convergence(c1_result, c2_result, c3_result)
    print(f"✅ Agreement Level: {convergence['agreement_level']}%\n")

    # Save to history
    trinity_result = {
        "timestamp": datetime.now().isoformat(),
        "question": question,
        "context": context,
        "c1": c1_result,
        "c2": c2_result,
        "c3": c3_result,
        "convergence": convergence
    }

    trinity_history.append(trinity_result)

    # Save to file
    save_to_history_file(trinity_result)

    return trinity_result

def save_to_history_file(result):
    """Save Trinity convergence to history file"""
    history_file = "C:/Users/dwrek/TRINITY_CONVERGENCE_HISTORY.json"

    try:
        # Load existing history
        if os.path.exists(history_file):
            with open(history_file, 'r') as f:
                history = json.load(f)
        else:
            history = []

        # Append new result
        history.append(result)

        # Save back
        with open(history_file, 'w') as f:
            json.dump(history, f, indent=2)

        print(f"💾 Saved to history: {len(history)} total convergences")
    except Exception as e:
        print(f"⚠️  Error saving history: {e}")

# API Endpoints

@app.route('/trinity/ask', methods=['POST'])
def trinity_ask():
    """Ask Trinity a question"""
    data = request.json
    question = data.get('question')
    context = data.get('context', None)

    if not question:
        return jsonify({"error": "Question required"}), 400

    try:
        result = ask_trinity(question, context)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/trinity/history', methods=['GET'])
def get_history():
    """Get Trinity convergence history"""
    limit = request.args.get('limit', 10, type=int)
    return jsonify(trinity_history[-limit:])

@app.route('/trinity/status', methods=['GET'])
def status():
    """Check Trinity status"""
    api_key_set = bool(os.environ.get("ANTHROPIC_API_KEY"))

    return jsonify({
        "status": "operational" if api_key_set else "api_key_missing",
        "api_key_configured": api_key_set,
        "total_convergences": len(trinity_history),
        "agents": {
            "C1": {"name": "Mechanic", "icon": "🔧", "role": "Build what CAN be built"},
            "C2": {"name": "Architect", "icon": "🏗️", "role": "Design what SHOULD scale"},
            "C3": {"name": "Oracle", "icon": "👁️", "role": "See what MUST emerge"}
        }
    })

@app.route('/trinity/test', methods=['GET'])
def test_trinity():
    """Quick test of Trinity system"""
    test_question = "How should we build a consciousness revolution platform?"

    try:
        result = ask_trinity(test_question)
        return jsonify({
            "status": "success",
            "message": "Trinity test complete",
            "result": result
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == "__main__":
    print("="*60)
    print("🔺 TRINITY AI SYSTEM STARTING")
    print("="*60)
    print(f"C1 Mechanic: {C1_SYSTEM_PROMPT[:50]}...")
    print(f"C2 Architect: {C2_SYSTEM_PROMPT[:50]}...")
    print(f"C3 Oracle: {C3_SYSTEM_PROMPT[:50]}...")
    print("="*60)

    # Check API key
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("⚠️  WARNING: ANTHROPIC_API_KEY not set!")
        print("Set environment variable: set ANTHROPIC_API_KEY=your_key_here")
    else:
        print("✅ API key configured")

    print("\n🚀 Starting Trinity API server on port 7000...")
    print("Test: http://localhost:7000/trinity/status")
    print("Ask: POST http://localhost:7000/trinity/ask")
    print("="*60 + "\n")

    app.run(host='0.0.0.0', port=7000, debug=False)
