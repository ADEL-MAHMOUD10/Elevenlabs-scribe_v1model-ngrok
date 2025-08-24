from flask import Flask, request
from pyngrok import ngrok, conf
import json

conf.get_default().auth_token = "your_api_token" # get it from ngrok auth 
app = Flask(__name__)

def format_time(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds - int(seconds)) * 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"

def save_srt(words, filename="transcription.srt", max_gap=0.5):
    srt_lines = []
    index = 1
    line_words = []
    line_start = None
    line_end = None

    for word in words:
        if word['type'] != 'word':
            continue
        start_sec = word['start']
        end_sec = word['end']
        text = word['text']

        if line_start is None:
            line_start = start_sec
            line_end = end_sec
            line_words.append(text)
        else:
            if start_sec - line_end <= max_gap:
                line_words.append(text)
                line_end = end_sec
            else:
                srt_lines.append(f"{index}\n{format_time(line_start)} --> {format_time(line_end)}\n{' '.join(line_words)}\n")
                index += 1
                line_words = [text]
                line_start = start_sec
                line_end = end_sec

    if line_words:
        srt_lines.append(f"{index}\n{format_time(line_start)} --> {format_time(line_end)}\n{' '.join(line_words)}\n")

    with open(filename, 'w', encoding='utf-8') as f:
        f.writelines(srt_lines)
    print(f"✅ SRT file created: {filename}")


@app.route("/webhook_endpoint", methods=["POST"])
def webhook():
    data = request.json
    print("✅ Webhook received:", data)

    with open("webhook_transcription.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    text = data.get("data", {}).get("transcription", {}).get("text")
    if text:
        with open("webhook_transcription.txt", "w", encoding="utf-8") as f:
            f.write(text)

    words = data.get("data", {}).get("transcription", {}).get("words", [])
    if words:
        save_srt(words)

    return "OK", 200

if __name__ == "__main__":
    public_url = ngrok.connect(80)
    print("🌍 Public URL:", public_url)

    app.run(port=80)
