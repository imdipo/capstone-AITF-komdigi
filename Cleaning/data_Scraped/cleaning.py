import json
import os
import re
import unicodedata

from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from tqdm import tqdm

trash_keywords = ['zodiak', 'jadwal', 'imsak', 'akhir', "pertandingan", "bursa"]

folder_jsonl = Path("Scraping/Scraping_ArtikelBerita/data")  

def bersihin_invisibleChar(teks):
    if not isinstance(teks, str):
        return ""

    baris_data = unicodedata.normalize("NFKC", teks)
    baris_data = baris_data.replace("\xa0", " ")
    baris_data = re.sub(r'[\u200b\u200c\u200d\ufeff\u200e\u200f]', '', baris_data)
    baris_data = baris_data.replace('\u201c', '"').replace('\u201d', '"')
    baris_data = baris_data.replace('\u2018', "'").replace('\u2019', "'")
    return baris_data.strip()

base_folder = os.path.dirname(os.path.abspath(__file__))
folder_data = os.path.join(base_folder, "data_gabungan")
os.makedirs(folder_data, exist_ok=True)

file_output = os.path.join(folder_data, "berita_gabungan.jsonl")

with open(file_output, 'w', encoding="utf-8") as output_file:
    for file_json in folder_jsonl.glob("*.jsonl"):
        print(file_json)

        with open(file_json, 'r', encoding="utf-8") as file_input:
            for barisJson in file_input:
                data = json.loads(barisJson)
                
                judul = data.get('title', '').lower()
                if any(kata in judul for kata in trash_keywords):
                    continue

                data["title"] = bersihin_invisibleChar(data.get('title', ''))
                data["text"] = bersihin_invisibleChar(data.get('text', ''))

                output_file.write(json.dumps(data, ensure_ascii=False) + '\n')
            
