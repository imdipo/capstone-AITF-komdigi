import json
from pathlib import Path

"""
kalau mati terus beberapa berita udah dilabel, dari pada diulang
kita pisahin dulu berita yang udah dilabel dari file utama 
"""

def filter_jsonl_by_title(source_file, reference_file, output_file):
    title_set = set()

    # load reference
    with open(reference_file, 'r', encoding='utf-8') as f:
        for line in f:
            data = json.loads(line)
            title_set.add(data.get("title", "").strip().lower())

    count_total = 0
    count_match = 0
    count_written = 0

    with open(source_file, 'r', encoding='utf-8') as src, \
         open(output_file, 'w', encoding='utf-8') as out:

        for line in src:
            count_total += 1
            data = json.loads(line)
            title = data.get("title", "").strip().lower()

            if title in title_set:
                count_match += 1


            if title not in title_set:
                out.write(json.dumps(data, ensure_ascii=False) + '\n')
                count_written += 1

    print("Total source:", count_total)
    print("Match (ada di reference):", count_match)
    print("Written (tidak ada di reference):", count_written)

BASE_DIR = Path(__file__).resolve().parent
folder_data = BASE_DIR / "data"

filter_jsonl_by_title(
    f"{folder_data}/belumlabel2.jsonl",
    f"{folder_data}/jsonlGabungan.jsonl",
    f"{folder_data}/belumlabel3.jsonl"
)