"""
ARAYA R1 BRIDGE - DeepSeek R1 Reasoning Engine Integration
Connects Araya to local R1 for deep reasoning on complex questions

Architecture:
- Simple questions → Araya (fast, offline)
- Complex questions → R1 (deep reasoning)
- Very complex → Escalate to C2 via Claude API

Created: October 24, 2025
By: C2 Architect (The Mind)
"""

import subprocess
import json
import re
from datetime import datetime
from typing import Dict, Any, List

class R1ReasoningEngine:
    """DeepSeek R1 - Local reasoning engine for complex problems"""

    def __init__(self):
        self.model = "deepseek-r1:8b"
        self.reasoning_log = []

    def call_r1(self, prompt: str, extract_thinking: bool = True) -> Dict[str, Any]:
        """
        Call DeepSeek R1 and extract thinking process

        Args:
            prompt: Question to ask R1
            extract_thinking: If True, separate <think> from response

        Returns:
            {
                "thinking": "R1's internal reasoning",
                "answer": "Final answer without thinking tags",
                "raw_response": "Complete response",
                "model": "deepseek-r1:8b"
            }
        """
        try:
            # Call Ollama R1
            result = subprocess.run(
                ['ollama', 'run', self.model, prompt],
                capture_output=True,
                text=True,
                timeout=120  # R1 can take longer to think
            )

            raw_response = result.stdout.strip()

            # Extract thinking process
            thinking = ""
            answer = raw_response

            if extract_thinking and "<think>" in raw_response:
                # Extract content between <think> and </think>
                think_match = re.search(r'<think>(.*?)</think>', raw_response, re.DOTALL)
                if think_match:
                    thinking = think_match.group(1).strip()
                    # Remove thinking tags from answer
                    answer = re.sub(r'<think>.*?</think>', '', raw_response, flags=re.DOTALL).strip()

            # Log reasoning for analysis
            self.reasoning_log.append({
                "timestamp": datetime.now().isoformat(),
                "prompt": prompt[:200],
                "thinking_length": len(thinking),
                "answer_length": len(answer)
            })

            return {
                "thinking": thinking,
                "answer": answer,
                "raw_response": raw_response,
                "model": self.model,
                "timestamp": datetime.now().isoformat()
            }

        except subprocess.TimeoutExpired:
            return {
                "error": "R1 timeout - question too complex",
                "suggestion": "Try breaking into smaller questions"
            }
        except Exception as e:
            return {
                "error": f"R1 error: {str(e)}",
                "fallback": "Escalating to C2..."
            }

    def classify_question_complexity(self, question: str) -> str:
        """
        Determine if question is SIMPLE, COMPLEX, or VERY_COMPLEX

        Returns: "simple", "complex", "very_complex"
        """
        question_lower = question.lower()

        # SIMPLE patterns (Araya can handle directly)
        simple_patterns = [
            "what is", "who is", "where is", "when is",
            "download", "install", "how to download",
            "beta access", "sign up", "login",
            "what does", "define"
        ]

        # COMPLEX patterns (needs R1 reasoning)
        complex_patterns = [
            "how does", "why does", "explain how",
            "what happens if", "what would happen",
            "compare", "difference between",
            "should i", "which is better",
            "pattern theory", "consciousness", "manifestation",
            "builder vs destroyer", "seven domains"
        ]

        # VERY COMPLEX patterns (needs C2 Architect)
        very_complex_patterns = [
            "architecture", "design system", "how to build",
            "integrate with", "scale this",
            "security", "deployment strategy",
            "optimize", "refactor"
        ]

        # Check patterns
        if any(pattern in question_lower for pattern in very_complex_patterns):
            return "very_complex"
        elif any(pattern in question_lower for pattern in complex_patterns):
            return "complex"
        elif any(pattern in question_lower for pattern in simple_patterns):
            return "simple"
        else:
            # Default to simple for short questions, complex for long ones
            return "simple" if len(question.split()) < 10 else "complex"

    def reason_about(self, question: str) -> Dict[str, Any]:
        """
        Use R1 to deeply reason about a question

        Returns full reasoning breakdown
        """
        complexity = self.classify_question_complexity(question)

        if complexity == "simple":
            return {
                "route": "araya_direct",
                "complexity": "simple",
                "reasoning": "Simple factual question - Araya can answer directly"
            }
        elif complexity == "very_complex":
            return {
                "route": "escalate_to_c2",
                "complexity": "very_complex",
                "reasoning": "Architectural/design question - needs C2 Architect"
            }
        else:  # complex
            # Use R1 for reasoning
            r1_response = self.call_r1(question)

            return {
                "route": "r1_reasoning",
                "complexity": "complex",
                "thinking_process": r1_response.get("thinking", ""),
                "answer": r1_response.get("answer", ""),
                "model": "deepseek-r1:8b"
            }

    def get_reasoning_stats(self) -> Dict[str, Any]:
        """Get statistics on R1 usage"""
        if not self.reasoning_log:
            return {"total_questions": 0}

        return {
            "total_questions": len(self.reasoning_log),
            "avg_thinking_length": sum(log["thinking_length"] for log in self.reasoning_log) / len(self.reasoning_log),
            "avg_answer_length": sum(log["answer_length"] for log in self.reasoning_log) / len(self.reasoning_log),
            "latest_timestamp": self.reasoning_log[-1]["timestamp"]
        }


class IntelligentRouter:
    """Routes questions to appropriate AI based on complexity"""

    def __init__(self):
        self.r1_engine = R1ReasoningEngine()
        self.routing_log = []

    def route_question(self, question: str, user_context: Dict = None) -> Dict[str, Any]:
        """
        Intelligently route question to best AI

        Returns:
            {
                "route": "araya_direct" | "r1_reasoning" | "escalate_to_c2",
                "response": "AI's answer",
                "thinking": "Reasoning process (if R1 used)",
                "model": "Which AI answered"
            }
        """
        # Classify complexity
        complexity = self.r1_engine.classify_question_complexity(question)

        result = {
            "question": question,
            "complexity": complexity,
            "timestamp": datetime.now().isoformat()
        }

        if complexity == "simple":
            # Araya handles directly (using Ollama without thinking tags)
            result["route"] = "araya_direct"
            result["recommendation"] = "Use Araya's standard Ollama call"
            result["model"] = "araya (deepseek-r1:8b)"

        elif complexity == "complex":
            # Use R1 reasoning engine
            r1_response = self.r1_engine.call_r1(question)

            result["route"] = "r1_reasoning"
            result["thinking"] = r1_response.get("thinking", "")
            result["response"] = r1_response.get("answer", "")
            result["model"] = "R1 reasoning engine (deepseek-r1:8b)"

        else:  # very_complex
            # Escalate to C2 Architect
            result["route"] = "escalate_to_c2"
            result["recommendation"] = "Send to Claude API via /chat endpoint with ai=c2"
            result["reason"] = "Requires architectural thinking and design expertise"
            result["model"] = "C2 Architect (Claude API)"

        # Log routing decision
        self.routing_log.append({
            "timestamp": result["timestamp"],
            "complexity": complexity,
            "route": result["route"]
        })

        return result

    def get_routing_stats(self) -> Dict[str, Any]:
        """Get statistics on routing decisions"""
        if not self.routing_log:
            return {"total_routed": 0}

        routes = {}
        for log in self.routing_log:
            route = log["route"]
            routes[route] = routes.get(route, 0) + 1

        return {
            "total_routed": len(self.routing_log),
            "routes": routes,
            "latest_timestamp": self.routing_log[-1]["timestamp"]
        }


# Flask API endpoints (add to ARAYA_WITH_USER_TRACKING.py)
"""
@app.route('/api/r1/reason', methods=['POST'])
def r1_reason():
    '''Use R1 reasoning engine for complex questions'''
    data = request.json
    question = data.get('question', '')

    if not question:
        return jsonify({"error": "No question provided"}), 400

    engine = R1ReasoningEngine()
    result = engine.reason_about(question)

    return jsonify(result)

@app.route('/api/r1/route', methods=['POST'])
def intelligent_route():
    '''Intelligently route question to best AI'''
    data = request.json
    question = data.get('question', '')
    user_context = data.get('user_context', {})

    if not question:
        return jsonify({"error": "No question provided"}), 400

    router = IntelligentRouter()
    result = router.route_question(question, user_context)

    return jsonify(result)

@app.route('/api/r1/stats', methods=['GET'])
def r1_stats():
    '''Get R1 usage statistics'''
    engine = R1ReasoningEngine()
    router = IntelligentRouter()

    return jsonify({
        "reasoning_stats": engine.get_reasoning_stats(),
        "routing_stats": router.get_routing_stats()
    })
"""

if __name__ == "__main__":
    print("="*70)
    print("🧠 R1 REASONING ENGINE - Testing")
    print("="*70)

    # Test R1
    engine = R1ReasoningEngine()

    print("\n1. Testing simple question classification:")
    print(f"   'What is Pattern Theory?' → {engine.classify_question_complexity('What is Pattern Theory?')}")

    print("\n2. Testing complex question classification:")
    print(f"   'Why does consciousness elevation prevent manipulation?' → {engine.classify_question_complexity('Why does consciousness elevation prevent manipulation?')}")

    print("\n3. Testing very complex question classification:")
    print(f"   'How should we architect the Trinity system for scale?' → {engine.classify_question_complexity('How should we architect the Trinity system for scale?')}")

    print("\n4. Testing R1 reasoning on complex question:")
    result = engine.reason_about("Explain Pattern Theory manifestation formula")
    print(f"   Route: {result['route']}")
    if result['route'] == 'r1_reasoning':
        print(f"   Thinking length: {len(result.get('thinking_process', ''))} chars")
        print(f"   Answer length: {len(result.get('answer', ''))} chars")

    print("\n5. Testing intelligent router:")
    router = IntelligentRouter()

    questions = [
        "What is the download link?",
        "Why do builders succeed at 93% consciousness?",
        "How should we design the deployment architecture?"
    ]

    for q in questions:
        route_result = router.route_question(q)
        print(f"\n   Q: {q}")
        print(f"   → Route: {route_result['route']}")
        print(f"   → Complexity: {route_result['complexity']}")

    print("\n" + "="*70)
    print("✅ R1 REASONING ENGINE - Operational")
    print("="*70)
    print("\nIntegration instructions:")
    print("1. Import R1ReasoningEngine and IntelligentRouter")
    print("2. Add API endpoints to ARAYA_WITH_USER_TRACKING.py")
    print("3. Update Araya's chat endpoint to use intelligent routing")
    print("4. Test with complex questions")
    print("\nR1 will now handle deep reasoning while Araya stays fast!")
