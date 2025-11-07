# AI Voice Assistant

**Module #28 - ADVANCED Category**

Voice-activated platform control with speech-to-text, text-to-speech, multi-language support, and custom wake words powered by Claude AI and advanced speech processing.

## Overview

The AI Voice Assistant enables hands-free platform interaction through natural voice commands. It supports 12+ languages, custom wake words, personalized voice profiles, and seamless integration with all platform modules.

### Key Features

- **Voice Commands**: Control entire platform with natural language
- **Speech-to-Text**: High-accuracy transcription in 12+ languages
- **Text-to-Speech**: Natural-sounding voice responses
- **Multi-Language Support**: English, Spanish, French, German, Chinese, Japanese, and more
- **Custom Wake Words**: Personalize with your own activation phrase
- **Intent Recognition**: AI-powered command understanding
- **Voice Profiles**: Personalized settings per user
- **Continuous Conversation**: Context-aware multi-turn dialogues
- **Command Customization**: Create custom voice shortcuts

## Installation

```bash
cd /home/user/100x-platform/MODULES/ADVANCED/ai_voice_assistant
pip install -r requirements.txt
```

### Additional Setup

Install system dependencies:

```bash
# macOS
brew install portaudio ffmpeg

# Ubuntu/Debian
sudo apt-get install portaudio19-dev ffmpeg

# Windows
# Download and install from official websites
```

## Configuration

Set your API keys:

```bash
# Anthropic (required)
export ANTHROPIC_API_KEY="your-api-key-here"

# Google Cloud (optional - for enhanced STT/TTS)
export GOOGLE_APPLICATION_CREDENTIALS="path/to/credentials.json"

# Azure Speech Services (optional)
export AZURE_SPEECH_KEY="your-azure-key"
export AZURE_SPEECH_REGION="your-region"

# OpenAI (optional - for Whisper)
export OPENAI_API_KEY="your-openai-key"
```

## Quick Start

```python
from main import AIVoiceAssistant, Language, VoiceGender
import asyncio

# Initialize assistant
assistant = AIVoiceAssistant()

# Create user profile
profile = assistant.create_profile(
    user_id="user_001",
    preferred_language=Language.ENGLISH,
    wake_word="hey assistant"
)

async def main():
    # Start session
    session = await assistant.start_session("user_001")

    # Process voice command (from audio file or microphone)
    audio_data = load_audio_file("command.wav")
    output = await assistant.process_voice_command(audio_data, session.session_id)

    print(f"Response: {output.text}")
    # Play audio_output.audio_data through speakers

asyncio.run(main())
```

## Supported Languages

1. **English** (en-US) - Default
2. **Spanish** (es-ES)
3. **French** (fr-FR)
4. **German** (de-DE)
5. **Italian** (it-IT)
6. **Portuguese** (pt-BR)
7. **Japanese** (ja-JP)
8. **Chinese** (zh-CN)
9. **Korean** (ko-KR)
10. **Russian** (ru-RU)
11. **Arabic** (ar-SA)
12. **Hindi** (hi-IN)

## Voice Commands

### Navigation Commands
```
"Navigate to dashboard"
"Go to projects"
"Show me analytics"
"Open settings"
```

### Creation Commands
```
"Create a new project called Mobile App"
"Add a task for the design phase"
"Schedule a meeting for tomorrow"
"Start a new document"
```

### Search Commands
```
"Search for legal documents"
"Find emails from last week"
"Look up customer data"
"Show me pending tasks"
```

### Query Commands
```
"What is the status of project Alpha?"
"How many tasks are completed?"
"What's my schedule today?"
"Show me the latest analytics"
```

### Update Commands
```
"Mark task 123 as completed"
"Change project status to active"
"Update meeting time to 3 PM"
"Set priority to high"
```

### Control Commands
```
"Pause recording"
"Resume playback"
"Increase volume"
"Switch to Spanish"
```

## Voice Profiles

Each user has a customizable profile:

```python
profile = VoiceProfile(
    user_id="user_001",
    preferred_language=Language.ENGLISH,
    preferred_voice=VoiceGender.FEMALE,
    wake_word="hey assistant",
    speech_rate=1.0,  # 0.5 to 2.0
    volume=0.8,       # 0.0 to 1.0
    custom_commands={
        "show the money": "open_revenue_dashboard",
        "team status": "display_team_workload"
    }
)
```

### Profile Customization

```python
# Change language
profile.preferred_language = Language.SPANISH

# Adjust speech rate (slower or faster)
profile.speech_rate = 1.2  # 20% faster

# Change voice gender
profile.preferred_voice = VoiceGender.MALE

# Set custom wake word
assistant.wake_word_detector.set_wake_word("user_001", "computer")
```

## Custom Wake Words

Activate the assistant with your personalized phrase:

```python
# Default wake words
"hey assistant"
"ok assistant"
"assistant"

# Custom wake words
profile.wake_word = "jarvis"
profile.wake_word = "computer"
profile.wake_word = "hey buddy"
```

## Custom Commands

Create voice shortcuts:

```python
# Register custom command
assistant.register_custom_command(
    user_id="user_001",
    trigger_phrase="morning briefing",
    action="display_daily_summary"
)

# Now you can say: "Hey assistant, morning briefing"
```

## Intent Recognition

The AI automatically understands command intent:

```python
# User says: "Create a new project called Mobile App"

intent = CommandIntent(
    command_type=VoiceCommand.CREATE,
    action="create_project",
    parameters={"name": "Mobile App"},
    confidence=0.92,
    entities=["project"]
)
```

### Supported Intent Types

1. **NAVIGATE**: Go to different sections
2. **SEARCH**: Find information
3. **CREATE**: Make new items
4. **UPDATE**: Modify existing items
5. **DELETE**: Remove items
6. **QUERY**: Ask questions
7. **CONTROL**: Control settings
8. **HELP**: Get assistance
9. **CUSTOM**: User-defined commands

## Multi-Language Support

### Language Detection

Automatically detect spoken language:

```python
detected_language = assistant.stt.detect_language(audio_data)
# Returns: Language.SPANISH
```

### Translation

Translate responses on-the-fly:

```python
spanish_response = await assistant.translate_response(
    text="Your project has been created",
    source_language=Language.ENGLISH,
    target_language=Language.SPANISH
)
# Returns: "Su proyecto ha sido creado"
```

### Language-Specific Commands

```python
# English
"Create a new project"

# Spanish
"Crear un nuevo proyecto"

# French
"Créer un nouveau projet"

# All automatically understood!
```

## Speech Processing Pipeline

### Complete Pipeline

1. **Wake Word Detection** → Listen for activation phrase
2. **Speech-to-Text** → Transcribe audio to text
3. **Intent Parsing** → Understand command meaning
4. **Command Execution** → Perform action
5. **Response Generation** → Create natural response
6. **Text-to-Speech** → Synthesize audio
7. **Audio Playback** → Speak response

### Processing Example

```python
# User speaks: "Create a project called Mobile App"

# 1. Wake word detected: ✓
# 2. Transcription: "Create a project called Mobile App"
# 3. Intent: CREATE, action=create_project, params={name: "Mobile App"}
# 4. Execution: Project created with ID proj_12345
# 5. Response: "I've created a new project called Mobile App for you"
# 6. Synthesis: Audio generated
# 7. Playback: Voice speaks response
```

## Voice Session Management

### Session Lifecycle

```python
# Start session
session = await assistant.start_session("user_001")

# Process multiple commands in conversation
output1 = await assistant.process_voice_command(audio1, session.session_id)
output2 = await assistant.process_voice_command(audio2, session.session_id)

# Context is maintained across commands
# Session automatically tracks conversation history
```

### Session Context

The assistant remembers previous commands:

```
User: "Create a project called Mobile App"
Assistant: "Project created"

User: "Add a design task to it"  ← "it" refers to Mobile App
Assistant: "Added design task to Mobile App project"
```

## Integration with Speech Services

### Google Cloud Speech

```python
# Best for: High accuracy, many languages
# Cost: $0.006 per 15 seconds

from google.cloud import speech

client = speech.SpeechClient()
# Integrate with assistant.stt
```

### Azure Speech Services

```python
# Best for: Enterprise features, neural voices
# Cost: $1 per hour (STT), $16 per 1M chars (TTS)

import azure.cognitiveservices.speech as speechsdk

speech_config = speechsdk.SpeechConfig(
    subscription=os.environ.get('AZURE_SPEECH_KEY'),
    region=os.environ.get('AZURE_SPEECH_REGION')
)
```

### OpenAI Whisper

```python
# Best for: Open source, offline capability
# Cost: Free (self-hosted) or API pricing

import whisper

model = whisper.load_model("base")
result = model.transcribe(audio_file)
```

## Real-Time Voice Interaction

### Continuous Listening

```python
import pyaudio
import asyncio

async def continuous_listen():
    audio_stream = pyaudio.PyAudio().open(
        format=pyaudio.paInt16,
        channels=1,
        rate=16000,
        input=True,
        frames_per_buffer=1024
    )

    while True:
        # Read audio chunk
        audio_chunk = audio_stream.read(1024)

        # Check for wake word
        if await assistant.wake_word_detector.detect_wake_word(audio_chunk):
            print("Wake word detected!")

            # Record command
            command_audio = record_until_silence(audio_stream)

            # Process
            output = await assistant.process_voice_command(
                command_audio,
                session.session_id
            )

            # Speak response
            play_audio(output.audio_data)

asyncio.run(continuous_listen())
```

## Voice Analytics

### Session Analytics

```python
analytics = assistant.get_session_analytics(session.session_id)

# Returns:
{
    "session_id": "sess_12345",
    "user_id": "user_001",
    "started_at": "2025-01-15T10:30:00",
    "duration_minutes": 15.5,
    "commands_executed": 12,
    "conversation_length": 24,  # messages
    "active": True,
    "language": "en-US"
}
```

### Overall Analytics

```python
analytics = assistant.get_analytics()

# Returns:
{
    "total_users": 150,
    "total_sessions": 1200,
    "active_sessions": 45,
    "total_commands": 8500,
    "language_distribution": {
        "en-US": 100,
        "es-ES": 30,
        "fr-FR": 20
    },
    "average_commands_per_user": 56.7
}
```

## Revenue Model

### Pricing Tiers

**Basic Plan - $29/month**
- 1,000 voice commands per month
- 2 languages
- Standard wake words
- Email support
- 5 custom commands

**Premium Plan - $99/month**
- Unlimited voice commands
- All 12 languages
- Custom wake words
- Priority support
- Unlimited custom commands
- Voice profiles for team
- Advanced analytics

**Business Plan - $299/month**
- Everything in Premium
- White-label option
- Custom voice training
- Dedicated support
- API access
- SSO integration
- SLA guarantee

**Enterprise Plan - Custom Pricing**
- On-premise deployment
- Custom speech models
- Multi-tenant support
- Advanced security
- 24/7 support
- Professional services

### Revenue Projections

- **Year 1**: $250K (400 customers @ avg $50/mo)
- **Year 2**: $800K (1,200 customers)
- **Year 3**: $2.0M (3,000 customers + enterprise)

### Target Markets

1. **Accessibility Users** (hands-free computing)
2. **Busy Professionals** (multitasking)
3. **Mobile Users** (on-the-go access)
4. **International Teams** (multi-language)
5. **Voice-First Applications** (IoT, smart home)

## Integration with Other Modules

### Module Integrations

1. **AI Project Manager (#27)**
   - "What's the status of my projects?"
   - "Create a new task for project Alpha"
   - "Assign this task to Alice"

2. **AI Legal Document Generator (#26)**
   - "Generate an NDA for Acme Corp"
   - "What documents need signatures?"
   - "Send contract to client"

3. **AI Data Analytics (#30)**
   - "Show me this month's revenue"
   - "What are the top performing products?"
   - "Create a sales report"

4. **Automated Bookkeeping (#25)**
   - "Record an expense for $500"
   - "What's my account balance?"
   - "Generate invoice for client"

5. **Content Creation Suite (#21)**
   - "Write a blog post about AI"
   - "Create social media content"
   - "Generate newsletter"

6. **AI Customer Service (#24)**
   - "Any new support tickets?"
   - "Respond to customer inquiry"
   - "Escalate ticket to human agent"

## API Reference

### REST API

```python
# Endpoints
POST   /api/v1/voice/profiles
GET    /api/v1/voice/profiles/{user_id}
PUT    /api/v1/voice/profiles/{user_id}

POST   /api/v1/voice/sessions
GET    /api/v1/voice/sessions/{session_id}
DELETE /api/v1/voice/sessions/{session_id}

POST   /api/v1/voice/process
POST   /api/v1/voice/transcribe
POST   /api/v1/voice/synthesize

GET    /api/v1/voice/analytics
```

### WebSocket API

```python
# Real-time voice streaming
ws://api.platform.com/v1/voice/stream

# Messages
{
    "type": "audio_chunk",
    "data": "<base64-encoded-audio>",
    "session_id": "sess_12345"
}
```

## Advanced Features

### Voice Biometrics

Identify users by voice:

```python
from pyannote.audio import Model

# Speaker recognition
speaker_id = identify_speaker(audio_data)
# Returns: "user_001"
```

### Emotion Detection

Detect emotion in voice:

```python
emotion = detect_emotion(audio_data)
# Returns: {"emotion": "happy", "confidence": 0.85}
```

### Noise Reduction

Clean audio before processing:

```python
import noisereduce as nr

# Remove background noise
clean_audio = nr.reduce_noise(
    y=audio_data,
    sr=16000
)
```

### Voice Activity Detection

Detect when someone is speaking:

```python
import webrtcvad

vad = webrtcvad.Vad()
is_speech = vad.is_speech(audio_chunk, sample_rate=16000)
```

## Best Practices

1. **Clear Speech**: Speak clearly and at normal pace
2. **Quiet Environment**: Minimize background noise
3. **Wake Word**: Pause briefly after wake word
4. **Natural Language**: Use conversational phrases
5. **Feedback**: Provide visual feedback during processing
6. **Error Handling**: Gracefully handle misunderstandings
7. **Privacy**: Clearly indicate when listening/recording
8. **Testing**: Test with diverse accents and speech patterns

## Security & Privacy

### Data Protection

- **No Storage**: Audio not stored by default
- **Encryption**: All data encrypted in transit (TLS)
- **Opt-In Recording**: Users control recording
- **Data Deletion**: Easy profile and history deletion
- **GDPR Compliant**: EU privacy regulations
- **CCPA Compliant**: California privacy law

### Privacy Controls

```python
# Disable voice recording
profile.settings["store_audio"] = False

# Delete command history
profile.command_history = []

# Delete profile
del assistant.profiles[user_id]
```

## Troubleshooting

### Common Issues

**Issue**: Wake word not detected
**Solution**: Check microphone permissions and background noise

**Issue**: Poor transcription accuracy
**Solution**: Speak more clearly, reduce background noise, check language setting

**Issue**: Slow response time
**Solution**: Use faster STT service (Whisper local), optimize network

**Issue**: Wrong language detected
**Solution**: Set preferred language in profile explicitly

## Performance Optimization

- **Local Processing**: Use Whisper locally to reduce latency
- **Streaming**: Stream audio for faster processing
- **Caching**: Cache common responses
- **Parallel Processing**: Process audio chunks in parallel

## Testing

```bash
# Run demo
python main.py

# Run tests
pytest tests/

# Test with audio file
python -c "from main import test_audio_file; test_audio_file('sample.wav')"
```

## Browser Integration

```javascript
// Web Speech API integration
const recognition = new webkitSpeechRecognition();

recognition.onresult = async (event) => {
    const transcript = event.results[0][0].transcript;

    // Send to AI Voice Assistant API
    const response = await fetch('/api/v1/voice/process', {
        method: 'POST',
        body: JSON.stringify({ text: transcript })
    });

    const result = await response.json();
    speakResponse(result.text);
};

recognition.start();
```

## Roadmap

### Q1 2025
- [ ] Enhanced wake word accuracy
- [ ] More languages (20+ total)
- [ ] Voice cloning for personalized responses

### Q2 2025
- [ ] Offline mode (fully local processing)
- [ ] Voice commands for mobile apps
- [ ] Integration with smart home devices

### Q3 2025
- [ ] Real-time translation during conversations
- [ ] Voice-based authentication
- [ ] Custom voice models per company

### Q4 2025
- [ ] Neural voice synthesis
- [ ] Emotion-aware responses
- [ ] Multi-speaker conversations

## License

Proprietary - Part of 100x Platform Ecosystem

## Credits

- **AI Engine**: Anthropic Claude 3.5 Sonnet
- **Speech Services**: Google, Azure, OpenAI Whisper
- **Wake Word**: Picovoice Porcupine
- **Audio Processing**: PyAudio, SoundFile

---

**Built with ❤️ for the 100x Platform Ecosystem**

*Empowering hands-free productivity through voice.*
