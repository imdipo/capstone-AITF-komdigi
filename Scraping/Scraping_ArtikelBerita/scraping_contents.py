import requests
import random
import time
import json
import re
import os
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
from config import HEADERS, MAP_PORTAL
from parse_portal import ambil_portal


def extract_informasi(url):
    try: 
        sumber_berita = ambil_portal(url) # nama web berita yang udah sesuai sama key dict nya
        # print(sumber_berita)
        config = MAP_PORTAL.get(sumber_berita)
        time.sleep(random.uniform(1.0, 3.0)) 

        response = requests.get(url, headers=HEADERS, timeout=(6, 25))
        soup = BeautifulSoup(response.content, 'html.parser')
                
        # judul (dari Meta Tag - Universal)
        title = soup.find("meta", property="og:title")
        title = title["content"] if title else soup.find("h1").get_text(strip=True)
                
        # waktu (dari Meta Tag - Universal) # kadang ga ada tapi gapapa
        published_time = soup.find("meta", property="article:published_time")
        published_time = published_time["content"] if published_time else "N/A"

        if config:
            source = soup.find(config["tag"], attrs=config["spec"])
        else:
            source = soup.find("body")

        # if not source:
        #     print(f"[SKIP] source None: {url}")
        #     with open("debug_page.html", "w", encoding='utf-8') as f:
        #         f.write(response.text)
        #     return None
 
        if source:

            all_p = source.find_all(["p", "li"])
            total_paragraf = len(all_p)

            teks = []
            pattern_iklan = re.compile(r"(also|baca|simak|cek|lihat|bacaan)\s+(read|juga|berita|lainnya)|artikel\s+terkait", re.IGNORECASE)

            for p in all_p:
                text = p.get_text(separator=" ", strip=True)
                text = text.replace('\xa0', ' ').strip()
                text = re.sub(r"\s+([.,!?])", r"\1", text)  

                if not text:
                    continue    

                if pattern_iklan.search(text):
                    continue

                for sampah in p.find_all(["blockquote", "img", "figure"]): # hapus strong ama b. soalnya udah di handle ama regex
                    if sampah.name in ["strong", "b"] and sampah.find_parent("a"):
                        continue
                    sampah.decompose()
                
                text = p.get_text(separator=" ", strip=True)
                text = re.sub(r"\s+([.,!?])", r"\1", text)
                
                if text and len(text) > 25:
                    teks.append(text)

            clean_teks = []
            for i, paragraf in enumerate(teks):
                text = paragraf
                if i == 0:
                    text = re.sub(r'^[^\w\d]+', '', text).strip()
                    text = re.sub(r'^.*?\|\s*.*?\s*\|\s*', '', text)
                    text = re.sub(r'^[A-Z\s]{3,30}\.\s*[A-Z\s]{3,30}\.\s*', '', text)
                    text = re.sub(r'^[A-Z][a-zA-Z\s]{2,20}\s*\(\d{1,2}/\d{1,2}/\d{4}\)\s*[-—:]\s*', '', text)
                    text = re.sub(r'^[A-Za-z\.]+,\s*[A-Z\s]{2,20}[-—:]\s*', '', text)
                    text = re.sub(r'^[A-Z][A-Z\s,\.]{2,40}[-—:]\s*', '', text)
                    text = re.sub(r'^.{1,60}?[–—-]\s*', '', text)
                    # text = re.sub(r'^[A-Z0-9.\s]+[-—:]\s*', '', text)
                    # text = re.sub(r'^[^a-zA-Z0-9]+', '', text).strip()
                
                if i == total_paragraf - 1:
                    pattern_penutup = re.compile(r"seperti\s+apa|simak\s+video|baca\s+selengkapnya", re.IGNORECASE)
                    pattern_url_awal = re.compile(r"^\s*url\s*:\s*https?://", re.IGNORECASE)

                    if pattern_penutup.search(text) or pattern_url_awal.search(text):
                        continue

                    text = re.sub(r'\s*(?:\*+\s*)?\([^)]*\)\s*$', '', text)
                    text = re.sub(r'\*+\s*$', '', text)

                # text = p.get_text(" ", strip=True)
                # print(f"[CLEAN {i}] len={len(text)}, {text[:80]}")
                # print("-"*50)
                clean_teks.append(text)

            content = "\n".join(clean_teks)

            # debug
            # print(f"title: {title}")
            # print(f"published_time: {published_time}") # ga semua portal ada, tapi gapapa
            # print(f"all_p: {content}")

            return {
                "url": url,
                "title": title,
                "published_at": published_time,
                "text": content,
                "sumber_berita": sumber_berita
            }
        
    except Exception as e: 
        print(f"ada error: {e}")
        return None


def harvest_informations(file, output_jsonl):
    print(f"sebanyak {len(file)} mulai dipanen")

    base_folder = os.path.dirname(os.path.abspath(__file__))
    folder_data = os.path.join(base_folder, "data")
    os.makedirs(folder_data, exist_ok=True)

        
    file_path = os.path.join(folder_data, f"{output_jsonl}.jsonl")

    nomor_file = 0
    with open(file_path, "a", encoding="utf-8") as f_out:
        with ThreadPoolExecutor(max_workers=5) as executor:

            for hasil in tqdm(executor.map(extract_informasi, file), total=len(file)):
                if hasil and len(hasil['text']) > 50: # ambil yang teknys panjang 
                    f_out.write(json.dumps(hasil, ensure_ascii=False) + "\n")
                    f_out.flush()
                    nomor_file += 1
                # else:
                #     print("DROP:", hasil['text'], hasil["url"])
    
    print(f"sudah dipanen, total sekarang ada {nomor_file}")
