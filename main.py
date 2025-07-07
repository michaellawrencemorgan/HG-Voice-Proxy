from flask import Flask, request, jsonify, send_from_directory
import requests
import os

app = Flask(__name__, static_folder=".")

# 🔐 Hardcoded API key and voice ID (for testing only)
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
            "stability": 0.75,
            "similarity_boost": 0.75
        }
    }

    tts_url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    response = requests.post(tts_url, json=payload, headers=headers)

    if response.status_code == 200:
        return response.content, 200, {
            "Content-Type": "audio/mpeg",
            "Content-Disposition": "inline; filename=voice.mp3"
        }
    else:
        print("❌ ElevenLabs API Error:", response.status_code, response.text)
        return jsonify({
            "error": "Failed to call ElevenLabs",
            "details": response.text
        }), 500

# ✅ Serve privacy.html from root directory
@app.route("/privacy.html")
def serve_privacy():
    return send_from_directory(".", "privacy.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

