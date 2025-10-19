#!/usr/bin/env python3
"""
Universal Transcription Service - Works Everywhere
Continuous audio transcription with multiple fallbacks
"""

import speech_recognition as sr
from datetime import datetime
import json
import os
import sys
import time

class UniversalTranscriber:
    def __init__(self):
        print("=" * 70)
        print("🎤 UNIVERSAL TRANSCRIPTION SERVICE - BLACK BOX RECORDER")
        print("=" * 70)
        print()

        self.recognizer = sr.Recognizer()
        self.session_start = datetime.now()
        self.log_file = f"C:/Users/dwrek/100X_DEPLOYMENT/transcription_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jsonl"
        self.event_count = 0

        # List available microphones
        print("📋 Available Microphones:")
        try:
            for index, name in enumerate(sr.Microphone.list_microphone_names()):
                print(f"   [{index}] {name}")
            print()
        except Exception as e:
            print(f"   ⚠️  Could not list microphones: {e}")
            print()

        # Try to initialize microphone
        print("🎤 Initializing microphone...")
        try:
            self.microphone = sr.Microphone()
            print("✅ Microphone initialized!")
        except Exception as e:
            print(f"❌ Microphone initialization failed: {e}")
            print("   Try running as administrator or check microphone permissions")
            sys.exit(1)

        # Calibrate for ambient noise
        print("🔊 Calibrating for ambient noise... (please be quiet for 2 seconds)")
        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=2)
                # Adjust sensitivity
                self.recognizer.energy_threshold = 4000
                self.recognizer.dynamic_energy_threshold = True
            print("✅ Calibration complete!")
            print(f"   Energy threshold: {self.recognizer.energy_threshold}")
        except Exception as e:
            print(f"⚠️  Calibration warning: {e}")

        print()
        print(f"📝 Log file: {self.log_file}")
        print()

    def log_event(self, text, confidence=None, latency_ms=None, event_type="transcription"):
        """Log any event with timestamp"""
        timestamp = datetime.now()

        entry = {
            "event_type": event_type,
            "timestamp": timestamp.isoformat(),
            "unix_ms": int(timestamp.timestamp() * 1000),
            "session_elapsed_ms": int((timestamp - self.session_start).total_seconds() * 1000),
            "text": text,
            "confidence": confidence,
            "latency_ms": latency_ms,
            "event_number": self.event_count
        }

        # Append to JSONL file
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(entry) + '\n')
        except Exception as e:
            print(f"⚠️  Log write error: {e}")

        self.event_count += 1

        # Console output with color
        time_str = timestamp.strftime("%H:%M:%S.%f")[:-3]
        if latency_ms:
            print(f"[{time_str}] \033[93m{latency_ms}ms\033[0m | \033[92m{text}\033[0m")
        else:
            print(f"[{time_str}] {text}")

        return entry

    def start(self):
        """Start continuous listening"""
        print("🎯 LISTENING CONTINUOUSLY... (Ctrl+C to stop)")
        print("=" * 70)
        print()

        self.log_event("Transcription service started", event_type="system")

        with self.microphone as source:
            while True:
                try:
                    # Show listening indicator
                    sys.stdout.write("\r\033[94m● LISTENING... (speak now)\033[0m")
                    sys.stdout.flush()

                    # Listen for audio (10 second phrases)
                    audio = self.recognizer.listen(source, timeout=None, phrase_time_limit=10)

                    # Clear the listening indicator
                    sys.stdout.write("\r" + " " * 50 + "\r")
                    sys.stdout.flush()

                    # Measure transcription time
                    start_time = time.time()

                    try:
                        # Try Google Speech Recognition (free, no API key needed)
                        result = self.recognizer.recognize_google(audio, show_all=True)

                        end_time = time.time()
                        latency_ms = int((end_time - start_time) * 1000)

                        if result and 'alternative' in result:
                            # Get best transcription
                            best = result['alternative'][0]
                            text = best.get('transcript', '')
                            confidence = best.get('confidence', None)

                            if text:
                                self.log_event(text, confidence, latency_ms)

                    except sr.UnknownValueError:
                        # Speech was unintelligible - don't spam console
                        pass

                    except sr.RequestError as e:
                        # API error
                        error_msg = f"API Error: {e}"
                        self.log_event(error_msg, event_type="error")
                        print(f"\n❌ {error_msg}")
                        print("   Waiting 5 seconds before retry...")
                        time.sleep(5)

                    except Exception as e:
                        error_msg = f"Recognition error: {e}"
                        self.log_event(error_msg, event_type="error")
                        print(f"\n⚠️  {error_msg}")

                except KeyboardInterrupt:
                    print("\n\n⚠️  Interrupted by user (Ctrl+C)")
                    break

                except Exception as e:
                    error_msg = f"Listening error: {e}"
                    self.log_event(error_msg, event_type="error")
                    print(f"\n⚠️  {error_msg}")
                    time.sleep(1)

        # Session complete
        print()
        print("=" * 70)
        self.log_event("Transcription service stopped", event_type="system")
        print(f"✅ Session complete. {self.event_count} events logged.")
        print(f"📊 Full log: {self.log_file}")
        print()

def main():
    try:
        transcriber = UniversalTranscriber()
        transcriber.start()
    except KeyboardInterrupt:
        print("\n\n⚠️  Service interrupted")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
