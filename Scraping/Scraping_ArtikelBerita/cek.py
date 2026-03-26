"""
ngecek nbsp 
"""

with open("data/indozone.jsonl", "r", encoding="utf-8") as f:
    for i, line in enumerate(f):
        if i < 5:  
            print(repr(line))