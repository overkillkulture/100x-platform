#!/usr/bin/env python3
"""
MICROPHONE DIAGNOSTIC TOOL
Tests microphone access and lists available devices
"""

import speech_recognition as sr
import sys

print("=" * 60)
print("🎤 MICROPHONE DIAGNOSTIC TOOL")
print("=" * 60)
print()

# Step 1: List available microphones
print("1️⃣ AVAILABLE MICROPHONES:")
print("-" * 60)
try:
    mic_list = sr.Microphone.list_microphone_names()
    if not mic_list:
        print("❌ No microphones detected!")
        print("   Check if microphone is plugged in")
    else:
        for i, name in enumerate(mic_list):
            print(f"  [{i}] {name}")
            if i == 0:
                print(f"       ⭐ DEFAULT")
    print()
except Exception as e:
    print(f"❌ Error listing microphones: {e}")
    print()

# Step 2: Test microphone access
print("2️⃣ TESTING MICROPHONE ACCESS:")
print("-" * 60)
try:
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("✅ Microphone access GRANTED")
        print(f"   Device: {source.CHUNK} chunk size")
        print()

        # Test ambient noise adjustment
        print("3️⃣ TESTING AMBIENT NOISE ADJUSTMENT:")
        print("   Please wait, adjusting for ambient noise...")
        recognizer.adjust_for_ambient_noise(source, duration=2)
        print(f"✅ Ambient noise adjusted")
        print(f"   Energy threshold: {recognizer.energy_threshold}")
        print()

        # Test recording
        print("4️⃣ TESTING RECORDING (5 seconds):")
        print("   🎤 SAY SOMETHING NOW...")
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            print("✅ Audio captured successfully!")
            print(f"   Data size: {len(audio.get_raw_data())} bytes")
            print()

            # Test recognition
            print("5️⃣ TESTING SPEECH RECOGNITION:")
            print("   Sending to Google Speech API...")
            try:
                text = recognizer.recognize_google(audio)
                print(f"✅ RECOGNIZED TEXT: '{text}'")
                print()
                print("🎉 SUCCESS! Microphone is working perfectly!")
            except sr.UnknownValueError:
                print("⚠️ Could not understand speech (but mic is working)")
                print("   Try speaking louder or closer to microphone")
            except sr.RequestError as e:
                print(f"❌ Google API error: {e}")
                print("   Check internet connection")

        except sr.WaitTimeoutError:
            print("⏱️ No speech detected in 5 seconds")
            print("   But microphone access is working!")
            print("   Try speaking louder or check mic volume in Windows")

except OSError as e:
    print("❌ MICROPHONE ACCESS DENIED")
    print()
    print("SOLUTION:")
    print("1. Run: FIX_MICROPHONE_PERMISSIONS.bat")
    print("2. Enable 'Let desktop apps access your microphone'")
    print("3. Run this test again")
    print()
    print(f"Technical error: {e}")

except Exception as e:
    print(f"❌ Unexpected error: {e}")
    print()
    print("TROUBLESHOOTING:")
    print("1. Check microphone is plugged in")
    print("2. Check Windows Sound settings (microphone not muted)")
    print("3. Run: FIX_MICROPHONE_PERMISSIONS.bat")
    print("4. Restart computer if permissions just changed")

print()
print("=" * 60)
print("NEXT STEPS:")
print("-" * 60)
if 'text' in locals():
    print("✅ Everything working! Try the wake word listener:")
    print("   START_WAKE_WORD_LISTENER.bat")
else:
    print("⚠️ Issues detected. Follow solutions above.")
    print("   Then run this test again: CHECK_MICROPHONE.bat")
print("=" * 60)

input("\nPress Enter to close...")
