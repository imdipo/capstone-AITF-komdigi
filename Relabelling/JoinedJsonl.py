from pathlib import Path
import json

"""
buat gabungin jsonl file yang udah di labellin
"""

pathData = Path("Relabelling\data")
jsonlGabungan = pathData / "jsonlGabungan.jsonl"
filter = "labeled"

def filterFile(jsonl):
    file_labeled = []
    for jsonl in pathData.glob("*.jsonl"):
        path = str(jsonl)
        labeled = path.split("_")
        lolos = filter in labeled

        if lolos:
            file_labeled.append(path)

    return file_labeled

seen = set()

with open(jsonlGabungan, 'w', encoding="utf-8") as outputFile:
    x = filterFile(pathData)
    for filenya in x:
        with open(filenya, "r", encoding="utf-8") as inputFile:
            for barisData in inputFile:
                data = json.loads(barisData)
                judul = data.get("title")
                if judul not in seen:
                    seen.add(judul)

                    outputFile.write(json.dumps(data, ensure_ascii=False) + "\n")

            
