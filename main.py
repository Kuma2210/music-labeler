import os
import json
from gemini_utils import transcribe_music_structure
from parse_utils import parse_music_structure

AUDIO_FOLDER = "audio_samples"
OUTPUT_FOLDER = "output"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

for filename in os.listdir(AUDIO_FOLDER):
    if not filename.lower().endswith((".mp3", ".wav")):
        continue
    file_path = os.path.join(AUDIO_FOLDER, filename)
    print(f"Processing {filename}...")

    response_text = transcribe_music_structure(file_path)
    print("Gemini 原始响应:\n", response_text)

    structure = parse_music_structure(response_text)
    json_path = os.path.join(OUTPUT_FOLDER, filename.rsplit(".", 1)[0] + ".json")

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(structure, f, indent=4, ensure_ascii=False)

    print(f"Saved: {json_path}")
