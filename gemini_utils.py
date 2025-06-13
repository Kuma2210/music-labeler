import base64
import requests
from requests.adapters import HTTPAdapter, Retry
from pathlib import Path
import os

API_KEY = "YOUR_API_KEY"
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key={API_KEY}"
MODEL_NAME = "models/gemini-2.5-pro"


PROMPT = """
Recognise the structure of this music and annotate it into 5 labels (intro, verse, chorus, instrumental, outro). 
The output includes start time, end time and period label. Time format should be MM:SS, no decimal points. 
Return a clean list only, like this:

00:00 - 00:20, intro
00:20 - 00:38, outro
...
"""

HEADERS = {
    "Content-Type": "application/json"
}


def encode_audio_to_base64(file_path: str, duration_sec: int = 60) -> str:
    """从文件中提取前 N 秒音频并编码为 Base64"""
    import librosa
    import soundfile as sf
    import io

    y, sr = librosa.load(file_path, sr=None, mono=True, duration=duration_sec)
    buffer = io.BytesIO()
    sf.write(buffer, y, sr, format="WAV")
    buffer.seek(0)
    return base64.b64encode(buffer.read()).decode("utf-8")


def transcribe_music_structure(file_path: str) -> str | None:
    print(f"[🔍] 正在处理: {file_path}")

    audio_base64 = encode_audio_to_base64(file_path)
    prompt = PROMPT_TEMPLATE.format(audio_base64=audio_base64)

    request_body = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ]
    }

    # 设置重试策略
    session = requests.Session()
    retries = Retry(
        total=5,
        backoff_factor=2,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["POST"]
    )
    adapter = HTTPAdapter(max_retries=retries)
    session.mount("https://", adapter)

    try:
        response = session.post(API_URL, json=request_body, headers=HEADERS, timeout=60, proxies={})
        response.raise_for_status()
        return response.json()["candidates"][0]["content"]["parts"][0]["text"]
    except requests.exceptions.RequestException as e:
        print(f"[❌] 请求失败: {file_path} -> {e}")
        return None
