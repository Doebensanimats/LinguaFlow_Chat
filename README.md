# 🌐 LinguaFlow

> Real-time AI-powered translation platform — live chat, document translation, and audiobook generation across 6 languages.

---

## Overview

**LinguaFlow** is a cloud-native translation platform built on AWS and Firebase. It enables real-time two-way conversations between speakers of different languages, document translation with instant download, and text-to-speech audiobook generation — all from a clean, browser-based interface.

Built as a team project with a personalised extension by **Ebenezer Dokyi**, transitioning from Medical Laboratory Science into Cloud & AI/ML Engineering.

---

## Features

- 💬 **Live Chat Translation** — Two-way real-time conversation with voice input and audio playback
- 🎤 **Speech-to-Text** — Record your voice using Amazon Transcribe
- 🔊 **Text-to-Speech** — Neural Polly voices read back translations naturally
- 📄 **Document Translator** — Upload TXT, PDF, or DOCX and download the translated version
- 🎧 **Audiobook Generator** — Translate any text and generate a downloadable MP3
- 🔗 **Shareable Chat Rooms** — Create a room link and invite anyone instantly via Firebase
- ☁️ **Fully Serverless** — Powered by AWS Lambda-compatible services and Firebase Firestore

---

## Architecture

```
User (Streamlit UI)
        │
        ├──► Amazon Transcribe     (speech → text)
        ├──► AWS Translate         (text → translated text)
        ├──► Amazon Polly          (translated text → audio)
        │
        └──► Firebase Firestore    (real-time shared chat rooms)
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit (Python) |
| Speech-to-Text | Amazon Transcribe |
| Translation | AWS Translate |
| Text-to-Speech | Amazon Polly (Neural) |
| Real-time Database | Firebase Firestore |
| Audio Processing | pydub + ffmpeg |
| Infrastructure | AWS (cloud) · Streamlit Cloud (hosting) |
| Language | Python 3.11+ |

---

## Project Structure

```
linguaflow/
├── app.py                        # Home / landing page
├── pages/
│   ├── 1_Chat.py                 # Live chat (single & two-user modes)
│   ├── 2_Document_Translator.py  # Document upload & translate
│   └── 3_Audiobook.py            # Text to translated audio
├── components/
│   ├── navbar.py                 # Sidebar navigation + page headers
│   └── styles.py                 # Shared CSS theme
├── services/
│   ├── aws_service.py            # Translate + Polly API calls
│   ├── chat_service.py           # Chat pipeline logic
│   └── firebase_service.py      # Firestore room management
├── utils/
│   └── languages.py             # Language configuration
├── .env                          # AWS credentials (not committed)
├── firebase_key.json             # Firebase service account key (not committed)
└── requirements.txt
```

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Doebensanimats/linguaflow-translation-app.git
cd linguaflow-translation-app
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Install ffmpeg (required for audio processing)

```bash
# Windows
winget install ffmpeg

# macOS
brew install ffmpeg

# Linux
sudo apt install ffmpeg -y
```

### 4. Configure AWS credentials

```bash
aws configure
```

Or create a `.env` file in the project root:

```
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
```

### 5. Add Firebase credentials

- Download your Firebase service account key from the Firebase Console
- Rename it to `firebase_key.json`
- Place it in the project root

### 6. Run the app

```bash
streamlit run app.py
```

---

## Supported Languages

| Language | Translate | Transcribe | Polly Voice |
|---|---|---|---|
| English | `en` | `en-US` | Joanna |
| Spanish | `es` | `es-US` | Lupe |
| French | `fr` | `fr-FR` | Lea |
| German | `de` | `de-DE` | Vicki |
| Italian | `it` | `it-IT` | Bianca |
| Portuguese | `pt` | `pt-BR` | Camila |

---

## Security

`firebase_key.json` and `.env` are excluded via `.gitignore` and must never be committed.

For production deployment use [Streamlit Secrets](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/secrets-management) to store credentials securely.

---

## Roadmap

- [x] Real-time text translation (AWS Translate)
- [x] Voice input (Amazon Transcribe)
- [x] Text-to-speech playback (Amazon Polly)
- [x] Document translation (TXT, PDF, DOCX)
- [x] Audiobook generation with MP3 download
- [x] Shareable chat rooms (Firebase Firestore)
- [ ] User authentication (Firebase Auth)
- [ ] African language expansion (Swahili, Hausa, Yoruba, Amharic)
- [ ] WebSocket upgrade for lower-latency chat
- [ ] Subscription and usage tier system
- [ ] Mobile-optimised UI

---

## Author

**Ebenezer Dokyi**
Medical Laboratory Scientist → Cloud & AI/ML Engineer

- GitHub: [Doebensanimats](https://github.com/Doebensanimats)
- Project: [linguaflow-translation-app](https://github.com/Doebensanimats/linguaflow-translation-app)

---

*If you find this project useful, give it a ⭐ on GitHub.*
