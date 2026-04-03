import modal
import json
import os
from tqdm import tqdm

"""
kemaren api openAI nya broken (ternyata api OpenRouter, bilang geh kan ga tau aku ya)
jadi buat labellin pake qwen aja
"""

# Setup Image & Dependencies
image = modal.Image.debian_slim().pip_install(
    "transformers", "torch", "accelerate", "safetensors", "tqdm"
)

app = modal.App("qwen-news-labeling")
MODEL_ID = "Qwen/Qwen2.5-7B-Instruct"

@app.cls(
    gpu="T4",
    timeout=3600, 
    image=image
)
class NewsLabeler:
    @modal.enter()
    def setup(self):
        from transformers import AutoModelForCausalLM, AutoTokenizer
        import torch

        print("Memuat Qwen2.5-7B di Cloud...")
        self.tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
        self.model = AutoModelForCausalLM.from_pretrained(
            MODEL_ID,
            torch_dtype=torch.float16,
            device_map="auto"
        )
        self.labels = ["Agama", "Politik", "Kesehatan", "Sosial Budaya", "Ekonomi & Bisnis",
                       "Sains & Teknologi", "Bencana & Keamanan", "Kriminalitas", "Hiburan & Olahraga", "Lainnya"]

    @modal.method()
    def label_batch_remote(self, batch_data):
        # batching
        formatted_news = ""
        for i, item in enumerate(batch_data):
            snippet = item.get('content', '').replace('\n', ' ')[:250]
            formatted_news += f"ID: {i} | T: {item.get('title', 'N/A')} | C: {snippet}\n"

        messages = [
            {"role": "system", "content": "You are an Indonesian news classification expert. Output ONLY valid JSON."},
            {"role": "user", "content": f"""Klasifikasikan berita berikut ke label: {self.labels}.
            
FORMAT OUTPUT: {{"data": [{{"id": 0, "label": "NamaLabel"}}, ...]}}

Berita:
{formatted_news}"""}
        ]
        
        prompt = self.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
        
        outputs = self.model.generate(
            **inputs,
            max_new_tokens=1024,
            do_sample=False,
            
        )
        
        response = self.tokenizer.decode(outputs[0][inputs.input_ids.shape[1]:], skip_special_tokens=True).strip()
        
        try:
            start = response.find('{')
            end = response.rfind('}') + 1
            return json.loads(response[start:end])
        except:
            return {"data": []}

@app.local_entrypoint()
def main():
    input_file = "data/filtered_output4.jsonl"
    output_file = "data/filtered_outputq4_labeled_qwen.jsonl"
    
    if not os.path.exists(input_file):
        print(f"File {input_file} tidak ditemukan!")
        return

    with open(input_file, 'r', encoding='utf-8') as f:
        total_data = sum(1 for i in f)

    labeler = NewsLabeler()
    batch_size = 30 

    print(f"Memproses {total_data} berita dengan Qwen...")

    def get_batches():
        batch = []
        with open(input_file, 'r', encoding='utf-8') as f:
            for line in f:
                batch.append(json.loads(line))
                if len(batch) == batch_size:
                    yield batch
                    batch = []
            if batch:
                yield batch

    with open(output_file, 'a', encoding='utf-8') as f_out:
        for chunk in tqdm(get_batches(), total=(total_data // batch_size + 1)):
            try:
                # Panggil model di GPU Cloud Modal
                res_json = labeler.label_batch_remote.remote(chunk)
                labels_list = res_json.get('data', [])

                for i, berita in enumerate(chunk):
                    # Mapping ID
                    label_info = next((x for x in labels_list if x.get('id') == i), None)
                    berita['label'] = label_info.get('label', 'Lainnya') if label_info else "Lainnya"
                    
                    f_out.write(json.dumps(berita, ensure_ascii=False) + '\n')
                
                f_out.flush() # Auto-save per batch
            except Exception as e:
                print(f"Gagal di batch tertentu: {e}")
                continue

    print(f"SELESAI! Hasil tersimpan di {output_file}")