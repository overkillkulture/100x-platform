#!/usr/bin/env python3
"""
Continuous Transcription Service - Black Box Recorder
Captures ALL audio and transcribes in real-time with timestamps
"""

import speech_recognition as sr
from datetime import datetime
import json
import os
import threading
import time

class ContinuousTranscriber:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.is_running = False
        self.log_file = f"C:/Users/dwrek/100X_DEPLOYMENT/transcription_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jsonl"
        self.session_start = datetime.now()

        # Adjust for ambient noise
        print("🎤 Calibrating for ambient noise... (please be quiet for 2 seconds)")
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=2)
        print("✅ Calibration complete!")

    def log_transcription(self, text, confidence, latency_ms, raw_data=None):
        """Log transcription with full metadata"""
        timestamp = datetime.now()

        entry = {
            "timestamp": timestamp.isoformat(),
            "unix_ms": int(timestamp.timestamp() * 1000),
            "session_elapsed_ms": int((timestamp - self.session_start).total_seconds() * 1000),
            "text": text,
            "confidence": confidence,
            "latency_ms": latency_ms,
            "raw": raw_data
        }

        # Append to JSONL file (one JSON object per line)
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(entry) + '\n')

        # Print to console with color
        time_str = timestamp.strftime("%H:%M:%S.%f")[:-3]
        print(f"\033[92m[{time_str}]\033[0m \033[93m{latency_ms}ms\033[0m | {text}")

        return entry

    def start(self):
        """Start continuous listening"""
        self.is_running = True
        print(f"\n🎯 Continuous Transcription Service ACTIVE")
        print(f"📝 Logging to: {self.log_file}")
        print(f"🎤 Listening... (Ctrl+C to stop)\n")

        with self.microphone as source:
            while self.is_running:
                try:
                    # Listen for audio
                    print("\033[94m● LISTENING...\033[0m", end='\r')
                    audio = self.recognizer.listen(source, timeout=None, phrase_time_limit=10)

                    # Measure transcription time
                    start_time = time.time()

                    try:
                        # Transcribe using Google Speech Recognition
                        result = self.recognizer.recognize_google(audio, show_all=True)

                        end_time = time.time()
                        latency_ms = int((end_time - start_time) * 1000)

                        if result and 'alternative' in result:
                            # Get best transcription
                            best = result['alternative'][0]
                            text = best.get('transcript', '')
                            confidence = best.get('confidence', 0.0)

                            if text:
                                self.log_transcription(text, confidence, latency_ms, result)

                    except sr.UnknownValueError:
                        # Speech was unintelligible
                        pass
                    except sr.RequestError as e:
                        print(f"\n❌ API Error: {e}")
                        time.sleep(1)

                except KeyboardInterrupt:
                    break
                except Exception as e:
                    print(f"\n⚠️ Error: {e}")
                    time.sleep(0.5)

        print("\n\n✅ Transcription service stopped")
        print(f"📊 Log saved: {self.log_file}")

    def stop(self):
        """Stop listening"""
        self.is_running = False

def main():
    print("=" * 60)
    print("🎤 CONTINUOUS TRANSCRIPTION SERVICE - BLACK BOX RECORDER")
    print("=" * 60)
    print()

    transcriber = ContinuousTranscriber()

    try:
        transcriber.start()
    except KeyboardInterrupt:
        print("\n\n⚠️ Interrupted by user")
    finally:
        transcriber.stop()
        print("\n📊 Session complete. Check log file for full data.")

if __name__ == "__main__":
    main()
