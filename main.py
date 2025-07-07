from flask import Flask, request, jsonify, send_from_directory
import requests
import os
import uuid

app = Flask(__name__, static_folder=".")

# 🔐 Hardcoded API key and voice ID (for testing only)
ELEVENLABS_API_KEY = "sk_15e22f0a744a31ed96339c9f5bd2cc2c3e864afa088d7f92"
VOICE_ID = "TIFcRUNcZnleeEhIlso8"  # Ileydrian Deacon


@app.route("/")
def home():
    return jsonify({"message": "🕊️ Holy Ghost Global ElevenLabs Proxy is running!"})


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
        return jsonify({"error": "Failed to generate audio", "details": response.text}), 500

    # Save audio to a file
    audio_id = str(uuid.uuid4())
    filename = f"{audio_id}.mp3"
    filepath = os.path.join("static", filename)

    os.makedirs("static", exist_ok=True)
    with open(filepath, "wb") as f:
        f.write(response.content)

    return jsonify({
        "message": "Audio generated successfully.",
        "audio_url": f"https://hg-voice-proxy.onrender.com/static/{filename}"
    })


# 🔥 CRITICAL for Render deployment: Bind to assigned port
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


