from flask import Flask, request, jsonify
import requests
import os
import io
import uuid
import firebase_admin
from firebase_admin import credentials, storage

app = Flask(__name__)

# 🔐 Load Firebase Admin SDK credentials
cred = credentials.Certificate("firebase-adminsdk.json")  # Make sure this file is in the same folder
firebase_admin.initialize_app(cred, {
    "storageBucket": "hg-voice.appspot.com"  # Replace with your actual bucket name
})

# 🔊 ElevenLabs voice settings
ELEVENLABS_API_KEY = "your-elevenlabs-api-key"  # Replace with your actual ElevenLabs API key
VOICE_ID = "TIFcRUNcZnleeEhIlso8"  # Ileydrian Deacon voice

@app.route("/")
def home():
    return jsonify({"message": "🕊️ Holy Ghost Voice Proxy is running!"})

# 📤 Upload mp3 bytes to Firebase and return a public URL
def upload_mp3_to_firebase(mp3_bytes, filename):
    bucket = storage.bucket()
    blob = bucket.blob(f"voices/{filename}")
    blob.upload_from_string(mp3_bytes, content_type="audio/mpeg")
    blob.make_public()
    return blob.public_url

# 🎙️ /speak route to convert text to speech and upload to Firebase
@app.route("/speak", methods=["POST"])
def speak():
    data = request.json
    text = data.get("text", "").strip()

    if not text:
        return jsonify({"error": "Missing 'text' in request body"}), 400

    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "text": text,
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    response = requests.post(url, headers=headers, json=payload)

    if response.status_code != 200:
        return jsonify({
            "error": "Failed to generate audio",
            "details": response.text
        }), 500

    audio_bytes = response.content
    filename = f"{uuid.uuid4()}.mp3"
    public_url = upload_mp3_to_firebase(audio_bytes, filename)

    return jsonify({
        "message": "🎧 Voice generated!",
        "audio_url": public_url
    })

# 🚀 Required for Render deployment and local dev
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


