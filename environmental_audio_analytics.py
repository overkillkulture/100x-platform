#!/usr/bin/env python3
"""
Environmental Audio Analytics - Continuous Audio Monitoring
Measures decibels, frequency spectrum, patterns, anomalies
"""

import sounddevice as sd
import numpy as np
import json
import time
from datetime import datetime
from collections import deque

class EnvironmentalMonitor:
    def __init__(self, sample_rate=44100, block_duration=0.1):
        self.sample_rate = sample_rate
        self.block_duration = block_duration
        self.blocksize = int(sample_rate * block_duration)

        # Analytics storage
        self.decibel_history = deque(maxlen=600)  # Last 60 seconds at 10Hz
        self.frequency_peaks = deque(maxlen=100)
        self.log_file = f"C:/Users/dwrek/100X_DEPLOYMENT/environmental_audio_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jsonl"

        # Anomaly detection
        self.baseline_db = None
        self.anomaly_threshold = 10  # dB above baseline

        print("=" * 70)
        print("🔊 ENVIRONMENTAL AUDIO ANALYTICS")
        print("=" * 70)
        print(f"📊 Sample Rate: {sample_rate} Hz")
        print(f"⏱️  Block Duration: {block_duration}s")
        print(f"📝 Log: {self.log_file}\n")

    def calculate_decibels(self, audio_data):
        """Calculate RMS decibel level"""
        rms = np.sqrt(np.mean(audio_data**2))
        if rms > 0:
            db = 20 * np.log10(rms)
        else:
            db = -np.inf
        return db

    def analyze_frequency_spectrum(self, audio_data):
        """Analyze frequency content"""
        fft = np.fft.fft(audio_data)
        freqs = np.fft.fftfreq(len(audio_data), 1/self.sample_rate)

        # Get positive frequencies only
        positive_freqs = freqs[:len(freqs)//2]
        magnitude = np.abs(fft[:len(fft)//2])

        # Find dominant frequency
        if len(magnitude) > 0:
            dominant_idx = np.argmax(magnitude)
            dominant_freq = abs(positive_freqs[dominant_idx])
            dominant_magnitude = magnitude[dominant_idx]
        else:
            dominant_freq = 0
            dominant_magnitude = 0

        return {
            "dominant_frequency": float(dominant_freq),
            "dominant_magnitude": float(dominant_magnitude),
            "total_energy": float(np.sum(magnitude))
        }

    def detect_anomaly(self, current_db):
        """Detect anomalous sound levels"""
        if self.baseline_db is None:
            return False, None

        deviation = current_db - self.baseline_db

        if deviation > self.anomaly_threshold:
            return True, {
                "type": "loud_spike",
                "baseline_db": self.baseline_db,
                "current_db": current_db,
                "deviation": deviation
            }

        return False, None

    def classify_sound_type(self, db, freq_data):
        """Classify type of sound"""
        dominant_freq = freq_data["dominant_frequency"]

        if db < 40:
            return "quiet"
        elif 40 <= db < 60:
            if 100 < dominant_freq < 300:
                return "generator/motor"
            elif dominant_freq < 100:
                return "low_rumble"
            else:
                return "ambient"
        elif 60 <= db < 80:
            if 200 < dominant_freq < 1000:
                return "machinery"
            elif 1000 < dominant_freq < 4000:
                return "voice/speech"
            else:
                return "loud_noise"
        else:
            return "very_loud"

    def log_analytics(self, db, freq_data, sound_type, anomaly=None):
        """Log environmental analytics"""
        timestamp = datetime.now()

        entry = {
            "timestamp": timestamp.isoformat(),
            "unix_ms": int(timestamp.timestamp() * 1000),
            "decibels": float(db) if not np.isinf(db) else None,
            "frequency_analysis": freq_data,
            "sound_type": sound_type,
            "anomaly": anomaly
        }

        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(entry) + '\n')

        return entry

    def audio_callback(self, indata, frames, time_info, status):
        """Process audio in real-time"""
        if status:
            print(f"⚠️  {status}")

        # Convert to mono if stereo
        if len(indata.shape) > 1:
            audio_data = np.mean(indata, axis=1)
        else:
            audio_data = indata[:, 0]

        # Calculate decibels
        db = self.calculate_decibels(audio_data)

        if not np.isinf(db):
            self.decibel_history.append(db)

            # Establish baseline after 5 seconds
            if self.baseline_db is None and len(self.decibel_history) > 50:
                self.baseline_db = np.median(list(self.decibel_history))
                print(f"✅ Baseline established: {self.baseline_db:.1f} dB\n")

            # Frequency analysis
            freq_data = self.analyze_frequency_spectrum(audio_data)

            # Classify sound
            sound_type = self.classify_sound_type(db, freq_data)

            # Detect anomalies
            is_anomaly, anomaly_data = self.detect_anomaly(db)

            # Log every second (10 blocks)
            if len(self.decibel_history) % 10 == 0:
                self.log_analytics(db, freq_data, sound_type, anomaly_data if is_anomaly else None)

                # Console output
                time_str = datetime.now().strftime("%H:%M:%S")
                print(f"\r[{time_str}] {db:5.1f} dB | {sound_type:15s} | {freq_data['dominant_frequency']:6.0f} Hz", end='')

                if is_anomaly:
                    print(f" | 🚨 ANOMALY: +{anomaly_data['deviation']:.1f} dB")

    def start(self):
        """Start continuous monitoring"""
        print("🎧 Starting environmental audio monitoring...")
        print("📊 Listening for patterns, anomalies, and analytics...\n")
        print("Press Ctrl+C to stop\n")

        try:
            with sd.InputStream(
                callback=self.audio_callback,
                channels=1,
                samplerate=self.sample_rate,
                blocksize=self.blocksize
            ):
                while True:
                    time.sleep(0.1)

        except KeyboardInterrupt:
            print("\n\n⚠️  Monitoring stopped by user")
        except Exception as e:
            print(f"\n\n❌ Error: {e}")
            import traceback
            traceback.print_exc()
        finally:
            self.print_summary()

    def print_summary(self):
        """Print session summary"""
        print("\n")
        print("=" * 70)
        print("📊 SESSION SUMMARY")
        print("=" * 70)

        if len(self.decibel_history) > 0:
            avg_db = np.mean(list(self.decibel_history))
            min_db = np.min(list(self.decibel_history))
            max_db = np.max(list(self.decibel_history))

            print(f"Average Decibels: {avg_db:.1f} dB")
            print(f"Min Decibels: {min_db:.1f} dB")
            print(f"Max Decibels: {max_db:.1f} dB")
            print(f"Samples Collected: {len(self.decibel_history)}")

        print(f"\n📝 Full log: {self.log_file}")
        print()

def main():
    try:
        monitor = EnvironmentalMonitor()
        monitor.start()
    except KeyboardInterrupt:
        print("\n⚠️  Interrupted")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
