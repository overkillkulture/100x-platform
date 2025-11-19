#!/usr/bin/env python3
"""
JARVIS - Just A Rather Very Intelligent System
Your Personal AI Assistant

Voice-controlled AI assistant that runs locally on your computer
"""

import os
import sys
import json
import time
from datetime import datetime
from pathlib import Path

# Check for required packages
try:
    import speech_recognition as sr
    import pyttsx3
    import anthropic
    from dotenv import load_dotenv
except ImportError as e:
    print(f"❌ Missing required package: {e}")
    print("\n📦 Please install requirements:")
    print("   pip install speechrecognition pyaudio pyttsx3 anthropic python-dotenv")
    sys.exit(1)

# Try to import winsound (Windows only, but graceful fallback)
try:
    import winsound
    WINSOUND_AVAILABLE = True
except ImportError:
    WINSOUND_AVAILABLE = False


class JARVIS:
    """Just A Rather Very Intelligent System"""

    def __init__(self):
        print("=" * 60)
        print("🤖 JARVIS - Your Personal AI Assistant")
        print("=" * 60)
        print("")

        # Load environment variables
        env_path = Path.home() / "JARVIS" / ".env"
        if not env_path.exists():
            env_path = Path(".env")

        load_dotenv(env_path)

        # Initialize speech recognition
        print("🎤 Initializing microphone...")
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = 300
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8

        self.microphone = sr.Microphone()

        # Initialize text-to-speech
        print("🔊 Initializing voice...")
        self.tts_engine = pyttsx3.init()
        self.tts_engine.setProperty('rate', 160)
        self.tts_engine.setProperty('volume', 1.0)

        # Initialize Claude API
        print("🧠 Connecting to Claude AI...")
        api_key = os.getenv("ANTHROPIC_API_KEY")

        if not api_key or api_key == "your_api_key_here":
            print("")
            print("❌ ANTHROPIC_API_KEY not configured!")
            print("")
            print("📋 To fix this:")
            print("   1. Get API key from: https://console.anthropic.com")
            print("   2. Edit file: " + str(env_path))
            print("   3. Replace 'your_api_key_here' with your key")
            print("")
            sys.exit(1)

        self.claude = anthropic.Anthropic(api_key=api_key)

        # Session tracking
        self.session_id = f"jarvis_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.conversation_history = []
        self.listening = True

        print("")
        print("✅ JARVIS is online and ready!")
        print("")
        print("=" * 60)
        print("")
        self.speak("JARVIS online. How can I assist you?")

    def beep(self, frequency=800, duration=150):
        """Play audio feedback beep"""
        if WINSOUND_AVAILABLE:
            try:
                winsound.Beep(frequency, duration)
            except:
                pass
        else:
            # Non-Windows fallback (print notification)
            print("🔔")

    def speak(self, text):
        """Convert text to speech"""
        print(f"🤖 JARVIS: {text}")
        try:
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
        except Exception as e:
            print(f"⚠️  Speech error: {e}")

    def listen(self):
        """Listen for voice input"""
        with self.microphone as source:
            print("🎧 Listening...")
            self.beep(600, 100)  # Low beep = listening

            try:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                self.beep(800, 100)  # High beep = processing

                print("🧠 Processing...")
                text = self.recognizer.recognize_google(audio)
                print(f"👤 You said: {text}")
                return text

            except sr.WaitTimeoutError:
                return None
            except sr.UnknownValueError:
                print("❓ Couldn't understand that")
                return None
            except sr.RequestError as e:
                print(f"❌ Speech recognition error: {e}")
                return None

    def process_command(self, command):
        """Send command to Claude and get response"""
        if not command:
            return None

        # Add to conversation history
        self.conversation_history.append({
            "role": "user",
            "content": command
        })

        # Build context for Claude
        system_prompt = """You are JARVIS (Just A Rather Very Intelligent System),
a voice-controlled AI assistant running on the user's personal computer.

You should:
- Be helpful, efficient, and direct
- Give concise responses (1-3 sentences for voice)
- Sound professional but friendly
- If asked to do tasks beyond your capabilities, acknowledge limitations

You can:
- Answer questions
- Provide information
- Have conversations
- Give advice and suggestions

Keep responses SHORT for voice - user is listening, not reading."""

        try:
            # Call Claude API
            response = self.claude.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=500,
                system=system_prompt,
                messages=self.conversation_history
            )

            assistant_message = response.content[0].text

            # Add to history
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message
            })

            # Keep history reasonable length (last 10 exchanges)
            if len(self.conversation_history) > 20:
                self.conversation_history = self.conversation_history[-20:]

            return assistant_message

        except Exception as e:
            error_msg = f"Error communicating with Claude: {e}"
            print(f"❌ {error_msg}")
            return "I'm having trouble connecting to my neural network. Please check your API key and internet connection."

    def run(self):
        """Main JARVIS loop"""
        print("🎤 Say 'Hey JARVIS' or 'JARVIS' to get my attention")
        print("   (Or just start talking, I'll listen!)")
        print("")
        print("💡 Try: 'JARVIS, what time is it?'")
        print("        'JARVIS, tell me a joke'")
        print("        'JARVIS, what can you do?'")
        print("")
        print("🛑 Say 'JARVIS goodbye' or press Ctrl+C to exit")
        print("")
        print("-" * 60)
        print("")

        while self.listening:
            try:
                # Listen for input
                command = self.listen()

                if not command:
                    continue

                # Check for wake word (case insensitive)
                command_lower = command.lower()

                # Check for exit commands
                if any(phrase in command_lower for phrase in ["jarvis goodbye", "goodbye jarvis", "exit", "quit"]):
                    self.speak("Goodbye! JARVIS going offline.")
                    break

                # Check for wake word or just process everything
                if "jarvis" in command_lower or "hey jarvis" in command_lower:
                    # Remove wake word from command
                    for wake in ["hey jarvis", "jarvis"]:
                        command = command_lower.replace(wake, "").strip()

                    if not command:
                        self.speak("Yes?")
                        continue

                # Process the command
                response = self.process_command(command)

                if response:
                    self.speak(response)

                print("")  # Blank line for readability

            except KeyboardInterrupt:
                print("\n\n🛑 Interrupt received...")
                self.speak("JARVIS shutting down.")
                break

            except Exception as e:
                print(f"\n❌ Error: {e}")
                self.speak("I encountered an error. Please try again.")

        print("")
        print("=" * 60)
        print("👋 JARVIS offline. Session ended.")
        print("=" * 60)


def main():
    """Main entry point"""
    try:
        jarvis = JARVIS()
        jarvis.run()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        print("\n📧 If this persists, contact: jarvis-support@conciousnessrevolution.io")
        sys.exit(1)


if __name__ == "__main__":
    main()
