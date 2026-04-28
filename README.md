# 🍲 Food History AI Shorts Generator & Uploader

Welcome to the **Food History AI Shorts** automation project! This repository contains a fully automated pipeline that generates engaging, short-form video content about the fascinating history and origins of Indian food, and then directly uploads it to YouTube Shorts.

## 🚀 How It Works

The project is divided into three main components:

1. **AI Video Generator (`ai-video-generator/`)**
   - **Script Generation**: Uses an AI model via Pollinations.ai to generate a catchy, viral Hindi script about a unique food history topic.
   - **Audio Generation**: Converts the generated Hindi script into a voiceover using AI TTS (Text-to-Speech).
   - **Image Generation**: Creates stunning, cinematic old-India aesthetic visuals for every scene based on English prompts.
   - **Video Assembly**: Stitches the audio, images, and background music together, adding subtle zoom effects to create a dynamic, engaging short video using `moviepy`.

2. **AI Video Uploader (`ai-video-uploader/`)**
   - Handles OAuth2 authentication with the YouTube Data API v3.
   - Automatically takes the generated video and script metadata (Title, Description) and publishes it directly to a connected YouTube channel as a Short.
   - Cleans up the workspace by deleting uploaded files after a successful run.

3. **Orchestrator (`orchestrator.py`)**
   - Coordinates the entire workflow. First triggers the video generator, then once successful, triggers the YouTube uploader. 
   - Sends real-time Telegram notifications about the pipeline's status.

## 🛠️ Setup & Installation

### 1. Prerequisites
- Python 3.10+
- `ffmpeg` installed on your system and added to PATH (required by `moviepy` for video rendering).

### 2. Install Dependencies
Install the required Python packages for both the generator and the uploader:
```bash
pip install -r requirements.txt
pip install -r ai-video-generator/requirements.txt
pip install -r ai-video-uploader/requirements.txt
```

### 3. Environment Variables
Create a `.env` file in the root directory and add the following secrets:
```env
POLLINATIONS_API_KEY=your_pollinations_api_key
TELEGRAM_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_telegram_chat_id
```

### 4. YouTube API Authentication
- Place your `client_secret.json` from the Google Cloud Console inside the `ai-video-uploader/src/` folder.
- Run the `auth.py` script locally once to grant permissions. This will generate a `token.json` file which is needed for headless, automated uploads.

## 🤖 Automation (GitHub Actions)

This project includes a `.github/workflows/cron.yml` workflow that automatically runs the pipeline at scheduled intervals (e.g., 6:00, 12:00, and 18:00 UTC). 

Ensure you have configured the following **Repository Secrets** in your GitHub repository:
- `YOUTUBE_TOKEN` (Content of your local `token.json`)
- `YOUTUBE_CLIENT_SECRET` (Content of your `client_secret.json`)
- `POLLINATIONS_API_KEY`
- `TELEGRAM_TOKEN`
- `TELEGRAM_CHAT_ID`

## 📁 Directory Structure
```text
Food History YT/
├── .github/workflows/   # CI/CD pipelines
├── ai-video-generator/  # Scripts for generating audio, video, images, and scripts
├── ai-video-uploader/   # YouTube upload automation and authentication
├── logs/                # Automation execution logs
├── orchestrator.py      # Main pipeline script
├── README.MD            # Project documentation
└── requirements.txt     # Python dependencies
```