# HG-Voice-Proxy
Voice Proxy for HG 

# ElevenLabs Voice Proxy for ChatGPT Tools

This is a lightweight Flask-based proxy server that enables custom GPTs to generate spoken responses using the ElevenLabs Text-to-Speech API.

## 🔧 Features

- Converts text to high-quality voice audio using ElevenLabs
- Streams `audio/mpeg` responses for GPT integration
- Deployable to HTTPS (Render, Fly.io, etc.)
- Ready for use as an OpenAPI tool in ChatGPT's GPT Builder

## 📡 Use Case

Designed to allow custom GPTs to vocalize specific outputs using a chosen ElevenLabs voice, especially when OpenAI's native voices are insufficient or unavailable for tooling.

## 📁 Files

- `main.py` – Flask app that handles `/speak` POST requests
- `requirements.txt` – Python dependencies
- `render.yaml` – Render.com deployment config
- `privacy.html` – Optional privacy policy for GPT tool compliance

## 🔐 Environment Variables

Set these in your hosting environment:

| Variable              | Description                    |
|-----------------------|--------------------------------|
| `ELEVENLABS_API_KEY`  | Your ElevenLabs API key        |
| `VOICE_ID`            | The voice ID for ElevenLabs    |

## 🔄 API Endpoint

### `POST /speak`

**Request Body**:
```json
{
  "text": "Your message here"
}
