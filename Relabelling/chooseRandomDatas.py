import os
import json
import random
from pathlib import Path

"""
sampling n data dari data gabungan
"""

base_folder = os.path.dirname(os.path.abspath(__file__))
folder_data = os.path.join(base_folder, "data")
os.makedirs(folder_data, exist_ok=True)
output_jsonl = os.path.join(folder_data, "9000_sampling.jsonl")


path_jsonl = Path("data\\belumlabel2.jsonl")  

def sampling(jsonl_input, jsonl_output, total_sampling = 9000):
    with open(jsonl_output, 'w', encoding="utf-8") as output:
        with open(jsonl_input, 'r', encoding="utf-8") as jsonl_path:
            total_data = sum(1 for _ in jsonl_path)
            angka_random = set(random.sample(range(total_data), min(total_sampling, total_data)))

            jsonl_path.seek(0)
            
            for i, file in enumerate(jsonl_path):
                if i in angka_random:
                    output.write(file)
            
            print("done")


sampling(path_jsonl, output_jsonl)


# f = ["c","c","c","c","c","c","c","c","c",]

# total = 0

# for i in f:
#     total += 1

# print(total)

# total_baris = sum(10 for _ in f) 
# print(total_baris)