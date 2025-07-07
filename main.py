from flask import Flask, request, jsonify, send_file
import requests
import os
import uuid

app = Flask(__name__, static_folder=".")

# 🔐 Hardcoded API key and voice ID (for testing only — move to env vars in production)
ELEVENLABS_API_KEY = "sk_15e22f0a744a31ed96339c9f5bd2cc2c3e864afa088d7f92"
VOICE_ID = "TIFcRUNcZnleeEhIlso8"  # Ileydrian Deacon

@app.route("/")
def home():
    return jsonify({"message": "🕊️ HG ElevenLabs Proxy is running!"})

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
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.4,
            "similarity_boost": 0.75
        }
    }

    response = requests.post(
        f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}",
        headers=headers,
        json=payload
    )

    if response.status_code != 200:
        return jsonify({"error": "Failed to generate speech"}), 500

    # Save the audio to static/audio/<uuid>.mp3
    audio_id = str(uuid.uuid4())
    audio_folder = "./static/audio"
    os.makedirs(audio_folder, exist_ok=True)
    file_path = os.path.join(audio_folder, f"{audio_id}.mp3")

    with open(file_path, "wb") as f:
        f.write(response.content)

    return jsonify({
        "audio_url": f"https://hg-voice-proxy.onrender.com/playback/{audio_id}"
    })

@app.route("/playback/<audio_id>", methods=["GET"])
def playback(audio_id):
    file_path = f"./static/audio/{audio_id}.mp3"
    if os.path.exists(file_path):
        return send_file(file_path, mimetype="audio/mpeg")
    else:
        return jsonify({"error": "Audio not found"}), 404


