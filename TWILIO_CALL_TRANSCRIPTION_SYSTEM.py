"""
TWILIO CALL TRANSCRIPTION SYSTEM
Automatically transcribes EVERY phone call
Stores in database + searchable archive
Integrates with Trinity for analysis
"""

import os
import json
from datetime import datetime
from pathlib import Path
from flask import Flask, request, jsonify
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse, Gather

# Configuration
TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.environ.get('TWILIO_PHONE_NUMBER')  # Your Twilio number
YOUR_REAL_NUMBER = os.environ.get('YOUR_REAL_NUMBER')  # Your actual phone

# Storage
CALL_LOG_DIR = Path("C:/Users/dwrek/.consciousness/call_logs/")
CALL_LOG_DIR.mkdir(parents=True, exist_ok=True)

# Initialize
app = Flask(__name__)
twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


class CallTranscriptionSystem:
    """
    Automatically transcribes all incoming and outgoing calls
    """

    def __init__(self):
        self.call_count = 0

    def log_call_metadata(self, call_sid, from_number, to_number, direction):
        """Log call metadata immediately"""
        metadata = {
            "call_sid": call_sid,
            "from": from_number,
            "to": to_number,
            "direction": direction,
            "timestamp": datetime.now().isoformat(),
            "status": "in_progress"
        }

        metadata_file = CALL_LOG_DIR / f"{call_sid}_metadata.json"
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)

        return metadata

    def save_transcription(self, call_sid, transcription_text):
        """Save call transcription"""
        transcript_file = CALL_LOG_DIR / f"{call_sid}_transcript.txt"
        with open(transcript_file, 'w') as f:
            f.write(transcription_text)

        # Update metadata
        metadata_file = CALL_LOG_DIR / f"{call_sid}_metadata.json"
        if metadata_file.exists():
            with open(metadata_file, 'r') as f:
                metadata = json.load(f)

            metadata["transcription_complete"] = True
            metadata["transcription_file"] = str(transcript_file)
            metadata["transcript_length"] = len(transcription_text)
            metadata["completed_at"] = datetime.now().isoformat()

            with open(metadata_file, 'w') as f:
                json.dump(metadata, f, indent=2)

    def get_all_calls(self):
        """Get all call logs"""
        calls = []
        for metadata_file in CALL_LOG_DIR.glob("*_metadata.json"):
            with open(metadata_file, 'r') as f:
                calls.append(json.load(f))

        # Sort by timestamp (newest first)
        calls.sort(key=lambda x: x['timestamp'], reverse=True)
        return calls

    def search_transcripts(self, query):
        """Search all transcripts for keyword"""
        results = []
        for transcript_file in CALL_LOG_DIR.glob("*_transcript.txt"):
            with open(transcript_file, 'r') as f:
                content = f.read()

            if query.lower() in content.lower():
                call_sid = transcript_file.stem.replace('_transcript', '')
                metadata_file = CALL_LOG_DIR / f"{call_sid}_metadata.json"

                if metadata_file.exists():
                    with open(metadata_file, 'r') as f:
                        metadata = json.load(f)

                    results.append({
                        "call_sid": call_sid,
                        "metadata": metadata,
                        "excerpt": self._get_excerpt(content, query)
                    })

        return results

    def _get_excerpt(self, text, query, context_chars=100):
        """Get excerpt around query match"""
        index = text.lower().find(query.lower())
        if index == -1:
            return text[:200]

        start = max(0, index - context_chars)
        end = min(len(text), index + len(query) + context_chars)

        excerpt = text[start:end]
        if start > 0:
            excerpt = "..." + excerpt
        if end < len(text):
            excerpt = excerpt + "..."

        return excerpt


# Initialize system
transcription_system = CallTranscriptionSystem()


@app.route('/voice/incoming', methods=['POST'])
def handle_incoming_call():
    """Handle incoming call - record and transcribe"""

    from_number = request.form.get('From')
    to_number = request.form.get('To')
    call_sid = request.form.get('CallSid')

    # Log call metadata
    transcription_system.log_call_metadata(
        call_sid,
        from_number,
        to_number,
        "incoming"
    )

    # Create TwiML response
    response = VoiceResponse()

    # Say greeting
    response.say("Call is being recorded and transcribed.", voice='alice')

    # Start recording with transcription
    response.record(
        transcribe=True,
        transcribe_callback=f'/voice/transcription/{call_sid}',
        play_beep=True,
        max_length=3600,  # 1 hour max
        timeout=5
    )

    # Forward to your real number
    response.dial(YOUR_REAL_NUMBER)

    return str(response)


@app.route('/voice/outgoing', methods=['POST'])
def handle_outgoing_call():
    """Handle outgoing call - record and transcribe"""

    to_number = request.form.get('To')
    from_number = request.form.get('From')
    call_sid = request.form.get('CallSid')

    # Log call metadata
    transcription_system.log_call_metadata(
        call_sid,
        from_number,
        to_number,
        "outgoing"
    )

    # Create TwiML response
    response = VoiceResponse()

    # Start recording with transcription
    response.record(
        transcribe=True,
        transcribe_callback=f'/voice/transcription/{call_sid}',
        max_length=3600
    )

    # Connect call
    response.dial(to_number)

    return str(response)


@app.route('/voice/transcription/<call_sid>', methods=['POST'])
def receive_transcription(call_sid):
    """Receive transcription from Twilio"""

    transcription_text = request.form.get('TranscriptionText', '')
    transcription_status = request.form.get('TranscriptionStatus')

    if transcription_status == 'completed':
        # Save transcription
        transcription_system.save_transcription(call_sid, transcription_text)

        # Send to Trinity for analysis (optional)
        # analyze_call_with_trinity(call_sid, transcription_text)

    return jsonify({"status": "received"})


@app.route('/api/calls', methods=['GET'])
def get_calls():
    """Get all calls"""
    calls = transcription_system.get_all_calls()
    return jsonify({"calls": calls, "total": len(calls)})


@app.route('/api/calls/search', methods=['GET'])
def search_calls():
    """Search call transcripts"""
    query = request.args.get('q', '')

    if not query:
        return jsonify({"error": "Query parameter 'q' required"}), 400

    results = transcription_system.search_transcripts(query)
    return jsonify({"results": results, "total": len(results)})


@app.route('/api/calls/<call_sid>', methods=['GET'])
def get_call_details(call_sid):
    """Get specific call details"""
    metadata_file = CALL_LOG_DIR / f"{call_sid}_metadata.json"
    transcript_file = CALL_LOG_DIR / f"{call_sid}_transcript.txt"

    if not metadata_file.exists():
        return jsonify({"error": "Call not found"}), 404

    with open(metadata_file, 'r') as f:
        metadata = json.load(f)

    result = {"metadata": metadata}

    if transcript_file.exists():
        with open(transcript_file, 'r') as f:
            result["transcript"] = f.read()

    return jsonify(result)


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    call_count = len(list(CALL_LOG_DIR.glob("*_metadata.json")))

    return jsonify({
        "status": "healthy",
        "total_calls_logged": call_count,
        "storage_path": str(CALL_LOG_DIR)
    })


def setup_twilio_number():
    """
    Configure Twilio number webhooks
    Call this once to set up your number
    """

    # Get your Twilio number
    phone_numbers = twilio_client.incoming_phone_numbers.list()

    if not phone_numbers:
        print("No Twilio numbers found. Buy one first!")
        return

    phone_number = phone_numbers[0]

    # Update webhooks
    phone_number.update(
        voice_url='https://your-ngrok-url.ngrok.io/voice/incoming',
        voice_method='POST',
        status_callback='https://your-ngrok-url.ngrok.io/voice/status',
        status_callback_method='POST'
    )

    print(f"✅ Configured {phone_number.phone_number}")
    print(f"   Voice URL: {phone_number.voice_url}")
    print(f"\n🔥 All calls to this number will now be transcribed automatically!")


if __name__ == '__main__':
    print()
    print("=" * 70)
    print("📞 TWILIO CALL TRANSCRIPTION SYSTEM")
    print("=" * 70)
    print()
    print("Features:")
    print("  • Auto-transcribe EVERY call (incoming + outgoing)")
    print("  • Store transcripts locally")
    print("  • Search all transcripts")
    print("  • API for Trinity integration")
    print()
    print("Storage: " + str(CALL_LOG_DIR))
    print()
    print("API Endpoints:")
    print("  GET  /api/calls           - List all calls")
    print("  GET  /api/calls/search?q= - Search transcripts")
    print("  GET  /api/calls/<sid>     - Get call details")
    print("  GET  /health              - Health check")
    print()
    print("=" * 70)
    print()

    # Run Flask app
    app.run(host='0.0.0.0', port=5000, debug=True)
