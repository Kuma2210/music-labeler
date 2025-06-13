import re

def parse_music_structure(text):
    pattern = r"(\d{2}:\d{2})\s*[-–—]\s*(\d{2}:\d{2})\s*[,:-]?\s*(intro|verse|chorus|instrumental|outro)"
    matches = re.findall(pattern, text, flags=re.IGNORECASE)

    structure = []
    for start, end, label in matches:
        structure.append({
            "start_time": start,
            "end_time": end,
            "label": label.lower()
        })
    return structure
