# Scribe v1 model speech-to-text Service

A Python application that leverages ElevenLabs' Scribe model for speech-to-text transcription with webhook functionality to process and format transcription results.

## Project Overview

This project provides an end-to-end solution for audio transcription using ElevenLabs' Scribe v1 model. It includes:

- A client script that submits audio for transcription  
- A webhook server that receives and processes transcription results  
- Automatic conversion of transcription data to multiple formats (JSON, TXT, SRT)  

## Features

- Audio transcription using ElevenLabs' advanced Scribe v1 model  
- Webhook integration for asynchronous processing of transcription results  
- Conversion of transcription data to SRT subtitle format with timestamp formatting  
- Support for remote audio files via URL  
- Automatic ngrok tunnel setup for webhook access  

## Components

### 1. Transcription Client (`main.py`)

Handles the submission of audio files to the ElevenLabs API for transcription:

- Loads environment variables for API authentication  
- Downloads audio from a specified URL  
- Submits audio for transcription with webhook configuration  
- Triggers the transcription process  

### 2. Webhook Server (`webhook.py`)

Receives and processes transcription results:

- Creates a public-facing endpoint using ngrok  
- Receives JSON data from ElevenLabs when transcription is complete  
- Extracts and saves the transcription in multiple formats  
- Generates SRT subtitle files with proper timestamp formatting  

## Setup and Installation

### Prerequisites

- Python 3.8+  
- Flask  
- pyngrok  
- ElevenLabs Python SDK  
- python-dotenv  
- requests  

### Installation

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd scribe-v1-model
   ```

2. Install required packages:
   ```bash
   pip install flask pyngrok elevenlabs python-dotenv requests
   ```

3. Create a `.env` file in the project root with your ElevenLabs API key:
   ```env
   ELEVENLABS_API_KEY=your_api_key_here
   ```

4. (Optional) Update the ngrok authentication token in `webhook.py` if needed.

## Usage

### Step 1: Start the Webhook Server

Run the webhook server to receive transcription callbacks:

```bash
python webhook.py
```

This will start a Flask server and establish an ngrok tunnel.  
Note the public URL displayed in the console – you'll need this for configuring webhooks in production.

### Step 2: Run the Transcription Client

With the webhook server running, submit an audio file for transcription:

```bash
python main.py
```

By default, this will download and transcribe the sample audio file from the URL specified in the script.  
To transcribe a different file, modify the `audio_url` variable in `main.py`.

### Step 3: View Results

After transcription is complete, the following files will be generated:

- `webhook_transcription.json`: Raw JSON response from ElevenLabs  
- `webhook_transcription.txt`: Plain text transcription  
- `transcription.srt`: Formatted subtitle file with timestamps  

## Customization

### Changing the Audio Source

Modify the `audio_url` variable in `main.py` to point to your audio file:

```python
audio_url = "https://your-audio-file-url.mp3"
```

### Adjusting SRT Formatting

The `save_srt` function in `webhook.py` can be customized to change how timestamps and words are grouped into subtitle segments. Example:

```python
save_srt(words, filename="transcription.srt")
```

## Security Notes

- Never commit your `.env` file containing API keys to version control  
- The ngrok authentication token in `webhook.py` should also be kept secure  
- For production use, replace the webhook setup with a proper reverse proxy  

## License

[Specify your license here]

## Acknowledgements

- This project uses the [ElevenLabs](https://elevenlabs.io/) Scribe v1 API for speech-to-text transcription  
- [ngrok](https://ngrok.com/) for creating secure tunnels to localhost  
