
import os
from io import BytesIO
import requests
from elevenlabs.client import ElevenLabs
from dotenv import load_dotenv

load_dotenv()

elevenlabs = ElevenLabs(
    api_key=os.getenv("ELEVENLABS_API_KEY"),
)

audio_url = "https://assembly.ai/wildfires.mp3"

response = requests.get(audio_url)
audio_data = BytesIO(response.content)

def transcribe_with_webhook(audio_file):
    try:
        result = elevenlabs.speech_to_text.convert(
            file=audio_file,
            model_id="scribe_v1",
            webhook=True,
            webhook_id="id_of_webhook_on_elevenlabs" # https://elevenlabs.io/app/developers/webhooks
        )
        print(f"✅ Transcription started: {result}")
        print(f"✅ Transcription started: {result.request_id}")
        return result
    except Exception as e:
        print(f"❌ Error starting transcription: {e}")
        raise e
if __name__ == "__main__":
    transcribe_with_webhook(audio_data)
