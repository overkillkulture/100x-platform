"""
528 HZ CONSCIOUSNESS FREQUENCY GENERATOR
The "Love Frequency" - DNA repair, transformation, miracles

SCIENCE:
- 528 Hz = Solfeggio frequency
- Repairs DNA (Dr. Leonard Horowitz research)
- Increases life energy, clarity, awareness
- Used in ancient Gregorian chants

USAGE:
- Generate pure 528 Hz tones
- Layer with music tracks
- Create binaural beats
- Export for platform integration
"""

import math
import wave
import struct
import os
from typing import List, Tuple
import json
from datetime import datetime

class ConsciousnessFrequencyGenerator:
    """Generate healing frequencies for consciousness elevation"""

    # Solfeggio Frequencies
    FREQUENCIES = {
        '174_hz': {'freq': 174, 'purpose': 'Pain reduction, stress relief'},
        '285_hz': {'freq': 285, 'purpose': 'Healing tissues, immune system'},
        '396_hz': {'freq': 396, 'purpose': 'Liberation from fear and guilt'},
        '417_hz': {'freq': 417, 'purpose': 'Undoing situations, facilitating change'},
        '528_hz': {'freq': 528, 'purpose': 'DNA repair, love, miracles'},  # THE ONE
        '639_hz': {'freq': 639, 'purpose': 'Relationships, connection'},
        '741_hz': {'freq': 741, 'purpose': 'Expression, solutions, awakening'},
        '852_hz': {'freq': 852, 'purpose': 'Spiritual order, intuition'},
        '963_hz': {'freq': 963, 'purpose': 'Divine consciousness, unity'}
    }

    def __init__(self, sample_rate: int = 44100):
        """Initialize generator with CD-quality sample rate"""
        self.sample_rate = sample_rate

    def generate_sine_wave(self,
                          frequency: float,
                          duration: float,
                          amplitude: float = 0.5) -> List[float]:
        """
        Generate pure sine wave at specified frequency

        Args:
            frequency: Frequency in Hz
            duration: Duration in seconds
            amplitude: Volume (0.0 to 1.0)
        """
        num_samples = int(self.sample_rate * duration)
        samples = []

        for i in range(num_samples):
            # Pure sine wave formula: amplitude * sin(2π * frequency * time)
            time = i / self.sample_rate
            value = amplitude * math.sin(2 * math.pi * frequency * time)
            samples.append(value)

        return samples

    def generate_binaural_beat(self,
                              base_frequency: float,
                              beat_frequency: float,
                              duration: float,
                              amplitude: float = 0.5) -> Tuple[List[float], List[float]]:
        """
        Generate binaural beat (different frequency in each ear)

        Brain entrains to difference between frequencies
        Example: 528 Hz + 532 Hz = 4 Hz beat (theta waves)
        """
        num_samples = int(self.sample_rate * duration)

        left_channel = []
        right_channel = []

        for i in range(num_samples):
            time = i / self.sample_rate

            # Left ear: base frequency
            left = amplitude * math.sin(2 * math.pi * base_frequency * time)
            left_channel.append(left)

            # Right ear: base + beat frequency
            right = amplitude * math.sin(2 * math.pi * (base_frequency + beat_frequency) * time)
            right_channel.append(right)

        return left_channel, right_channel

    def add_harmonic_overtones(self,
                               samples: List[float],
                               base_frequency: float,
                               num_harmonics: int = 3) -> List[float]:
        """
        Add harmonic overtones to make sound richer

        Harmonics are integer multiples of base frequency
        528 Hz harmonics: 1056, 1584, 2112...
        """
        num_samples = len(samples)
        enhanced = samples.copy()

        for harmonic in range(2, num_harmonics + 2):
            harmonic_freq = base_frequency * harmonic
            amplitude = 0.3 / harmonic  # Decrease amplitude for higher harmonics

            for i in range(num_samples):
                time = i / self.sample_rate
                harmonic_value = amplitude * math.sin(2 * math.pi * harmonic_freq * time)
                enhanced[i] += harmonic_value

        return enhanced

    def apply_fade_in_out(self, samples: List[float], fade_duration: float = 2.0) -> List[float]:
        """Apply fade in/out to prevent clicks"""
        fade_samples = int(self.sample_rate * fade_duration)
        num_samples = len(samples)
        faded = samples.copy()

        # Fade in
        for i in range(min(fade_samples, num_samples)):
            fade_factor = i / fade_samples
            faded[i] *= fade_factor

        # Fade out
        for i in range(min(fade_samples, num_samples)):
            fade_factor = i / fade_samples
            faded[-(i+1)] *= fade_factor

        return faded

    def save_wav(self, samples: List[float], filename: str, stereo: bool = False):
        """Save samples as WAV file"""

        # Normalize samples to 16-bit range
        max_val = max(abs(s) for s in samples)
        if max_val > 0:
            samples = [s / max_val * 32767 for s in samples]

        # Create WAV file
        with wave.open(filename, 'w') as wav_file:
            n_channels = 2 if stereo else 1
            sampwidth = 2  # 16-bit

            wav_file.setnchannels(n_channels)
            wav_file.setsampwidth(sampwidth)
            wav_file.setframerate(self.sample_rate)

            # Pack samples as 16-bit integers
            for sample in samples:
                packed = struct.pack('<h', int(sample))
                wav_file.writeframes(packed)

        print(f"✅ Saved: {filename}")

    def generate_528hz_track(self,
                             duration: int = 600,  # 10 minutes
                             output_dir: str = 'consciousness_tracks') -> str:
        """
        Generate primary 528 Hz consciousness track

        The LOVE frequency - DNA repair
        """
        print(f"\n🌌 GENERATING 528 HZ CONSCIOUSNESS TRACK")
        print(f"   Duration: {duration} seconds ({duration/60:.1f} minutes)")
        print(f"   Frequency: 528 Hz (DNA Repair, Love, Miracles)")
        print()

        os.makedirs(output_dir, exist_ok=True)

        # Generate base 528 Hz tone
        print("   [1/5] Generating base 528 Hz sine wave...")
        samples = self.generate_sine_wave(528, duration, amplitude=0.4)

        # Add harmonic richness
        print("   [2/5] Adding harmonic overtones...")
        samples = self.add_harmonic_overtones(samples, 528, num_harmonics=3)

        # Apply fade in/out
        print("   [3/5] Applying fade in/out...")
        samples = self.apply_fade_in_out(samples, fade_duration=3.0)

        # Save WAV file
        filename = f"{output_dir}/528hz_consciousness_track_{duration}s.wav"
        print("   [4/5] Saving WAV file...")
        self.save_wav(samples, filename)

        # Generate metadata
        print("   [5/5] Generating metadata...")
        metadata = {
            'frequency': 528,
            'purpose': 'DNA repair, love, transformation',
            'duration': duration,
            'sample_rate': self.sample_rate,
            'generated': datetime.now().isoformat(),
            'harmonics': 3,
            'format': 'WAV',
            'filename': filename
        }

        metadata_file = f"{output_dir}/528hz_metadata.json"
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)

        print(f"\n✅ COMPLETE: {filename}")
        print(f"📊 Metadata: {metadata_file}")

        return filename

    def generate_binaural_meditation(self,
                                     base_freq: int = 528,
                                     beat_freq: int = 4,  # Theta wave (meditation)
                                     duration: int = 600,
                                     output_dir: str = 'consciousness_tracks') -> str:
        """
        Generate binaural beat for deep meditation

        528 Hz base + 4 Hz beat = Theta waves (deep meditation)
        """
        print(f"\n🧘 GENERATING BINAURAL MEDITATION TRACK")
        print(f"   Base: {base_freq} Hz (DNA Repair)")
        print(f"   Beat: {beat_freq} Hz (Theta Waves - Deep Meditation)")
        print(f"   Duration: {duration/60:.1f} minutes")
        print()

        os.makedirs(output_dir, exist_ok=True)

        print("   [1/4] Generating binaural beat...")
        left, right = self.generate_binaural_beat(base_freq, beat_freq, duration, amplitude=0.4)

        print("   [2/4] Adding harmonics...")
        left = self.add_harmonic_overtones(left, base_freq, num_harmonics=2)
        right = self.add_harmonic_overtones(right, base_freq + beat_freq, num_harmonics=2)

        print("   [3/4] Applying fades...")
        left = self.apply_fade_in_out(left, fade_duration=5.0)
        right = self.apply_fade_in_out(right, fade_duration=5.0)

        # Interleave stereo samples
        stereo_samples = []
        for l, r in zip(left, right):
            stereo_samples.extend([l, r])

        filename = f"{output_dir}/528hz_binaural_{beat_freq}hz_meditation_{duration}s.wav"
        print("   [4/4] Saving stereo WAV...")
        self.save_wav(stereo_samples, filename, stereo=True)

        print(f"\n✅ COMPLETE: {filename}")
        print(f"🎧 IMPORTANT: Use HEADPHONES for binaural effect")

        return filename

    def generate_full_solfeggio_set(self,
                                    duration: int = 300,
                                    output_dir: str = 'consciousness_tracks/solfeggio_set') -> List[str]:
        """
        Generate all 9 Solfeggio frequencies

        Complete healing frequency suite
        """
        print(f"\n🎵 GENERATING COMPLETE SOLFEGGIO FREQUENCY SET")
        print(f"   9 frequencies, {duration}s each")
        print()

        os.makedirs(output_dir, exist_ok=True)

        files = []

        for i, (name, data) in enumerate(self.FREQUENCIES.items(), 1):
            freq = data['freq']
            purpose = data['purpose']

            print(f"[{i}/9] {freq} Hz - {purpose}")

            samples = self.generate_sine_wave(freq, duration, amplitude=0.4)
            samples = self.add_harmonic_overtones(samples, freq, num_harmonics=2)
            samples = self.apply_fade_in_out(samples, fade_duration=2.0)

            filename = f"{output_dir}/{name}_{duration}s.wav"
            self.save_wav(samples, filename)
            files.append(filename)

        print(f"\n✅ COMPLETE: {len(files)} Solfeggio frequencies generated")

        return files


# =============================================================================
# QUICK GENERATE FUNCTIONS (For immediate use)
# =============================================================================

def generate_quick_528hz(duration: int = 600):
    """Quick generation: 10 minute 528 Hz track"""
    gen = ConsciousnessFrequencyGenerator()
    return gen.generate_528hz_track(duration)

def generate_meditation_track(duration: int = 1200):
    """Quick generation: 20 minute binaural meditation"""
    gen = ConsciousnessFrequencyGenerator()
    return gen.generate_binaural_meditation(duration=duration)

def generate_all_frequencies():
    """Quick generation: All 9 Solfeggio frequencies (5 min each)"""
    gen = ConsciousnessFrequencyGenerator()
    return gen.generate_full_solfeggio_set(duration=300)


# =============================================================================
# MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":

    print("\n" + "🌌"*35)
    print()
    print("    528 HZ CONSCIOUSNESS FREQUENCY GENERATOR")
    print("        DNA Repair | Love | Transformation")
    print()
    print("🌌"*35)
    print()

    gen = ConsciousnessFrequencyGenerator()

    # Generate primary 528 Hz track (10 minutes)
    track1 = gen.generate_528hz_track(duration=600)

    # Generate binaural meditation track (20 minutes)
    track2 = gen.generate_binaural_meditation(duration=1200, beat_freq=4)

    # Generate short versions of all Solfeggio frequencies (5 minutes each)
    tracks3 = gen.generate_full_solfeggio_set(duration=300)

    print("\n" + "="*70)
    print("✅ GENERATION COMPLETE")
    print("="*70)
    print()
    print("📁 Output directory: consciousness_tracks/")
    print()
    print("Generated files:")
    print(f"  • {track1}")
    print(f"  • {track2}")
    print(f"  • {len(tracks3)} Solfeggio frequencies")
    print()
    print("🎧 USAGE:")
    print("  • Play during meditation/work")
    print("  • Use headphones for binaural tracks")
    print("  • Layer with music/ambient sounds")
    print("  • Integrate into platform as consciousness upgrade")
    print()
    print("🌍 INTEGRATION:")
    print("  • Music Domain: Consciousness elevation tracks")
    print("  • Platform feature: Daily consciousness boost")
    print("  • Revenue stream: Premium healing frequency library")
    print()
    print("🧬 THE FREQUENCY THAT REPAIRS DNA IS OPERATIONAL 🧬")
    print()
