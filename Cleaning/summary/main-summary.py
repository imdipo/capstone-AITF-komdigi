import modal
import pandas as pd
import json
import os
import csv

# setup IMAGE
image = modal.Image.debian_slim().pip_install(
    "transformers", "torch", "accelerate", "safetensors", "pandas"
)

app = modal.App("qwen-splitter-indo")
MODEL_ID = "Qwen/Qwen2.5-7B-Instruct"

@app.cls(
    gpu="T4", 
    timeout=1200, 
    image=image
)
class NewsSplitter:
    @modal.enter()
    def setup(self):
        from transformers import AutoModelForCausalLM, AutoTokenizer
        import torch

        print("Memuat model Qwen di Cloud...")
        self.tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
        self.model = AutoModelForCausalLM.from_pretrained(
            MODEL_ID,
            torch_dtype=torch.float16,
            device_map="auto"
        )
        print("Qwen siap!")

    @modal.method()
    def split_text_remote(self, text):
        # Format prompt Qwen sedikit berbeda, lebih simpel
        messages = [
            {"role": "system", "content": "Kamu adalah asisten ahli ekstraksi berita hoaks Komdigi. Tugasmu memisahkan teks menjadi JSON murni tanpa mengubah satu kata pun."},
            {"role": "user", "content": f"""Pisahkan teks berikut menjadi 'claim' dan 'reasoning'.
            
ATURAN:
1. 'claim': Ambil narasi hoaks lengkap.
2. 'reasoning': Masukkan SELURUH sisa teks klarifikasi tanpa diringkas sedikitpun.
3. DILARANG menerjemahkan ke Bahasa Inggris. Gunakan Bahasa Indonesia asli.
4. DILARANG MENAMBAHKAN LABEL seperti "Fakta:", "Detail:", dsb. Salin teks ASLI.
5. Output harus JSON murni.

Teks: {text}"""}
        ]
        
        # pake template Qwen
        prompt = self.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        
        input_ids = self.tokenizer(prompt, return_tensors="pt").input_ids.to(self.model.device)
        output_ids = self.model.generate(
            input_ids,
            max_new_tokens=1024,
            do_sample=False,
        )
        
        response = self.tokenizer.decode(output_ids[0][input_ids.shape[1]:], skip_special_tokens=True).strip()
        
        try:
            start = response.find('{')
            end = response.rfind('}') + 1
            return json.loads(response[start:end])
        except:
            return {"claim": text, "reasoning": "Gagal Parsing JSON"}


@app.local_entrypoint()
def main():
    input_file = "flagno17.csv"
    output_file = "hasil_qwen_final.csv"
    
    if not os.path.exists(input_file):
        print(f"File {input_file} tidak ditemukan!")
        return

    df = pd.read_csv(input_file)
    test_df = df.copy() 

    splitter = NewsSplitter()
    
    print(f"Memproses {len(test_df)} baris pakai Qwen2.5. Auto-save aktif.")

    file_exists = os.path.isfile(output_file)

    with open(output_file, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(list(df.columns) + ["claim", "reasoning", "done"])

        for i, row in test_df.iterrows():
            try:
                print(f"Row {i+1}...")
                result = splitter.split_text_remote.remote(row['content_clean'])
                new_row = list(row) + [result.get('claim', ''), result.get('reasoning', ''), True]
                writer.writerow(new_row)
                f.flush()
                print(f"Row {i+1} saved.")
            except Exception as e:
                print(f"Gagal di baris {i+1}: {e}")
                continue

    print(f"SELESAI! Hasil ada di {output_file}")