import requests
import json
import os
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
from config import HEADERS, MAP_PORTAL
from parse_portal import ambil_portal


def extract_informasi(url):
    try: 
        sumber_berita = ambil_portal(url) # nama web berita yang udah sesuai sama key dict nya
        config = MAP_PORTAL.get(sumber_berita)

        response = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
                
        # judul (dari Meta Tag - Universal)
        title = soup.find("meta", property="og:title")
        title = title["content"] if title else soup.find("h1").get_text(strip=True)
                
        # waktu (dari Meta Tag - Universal) # kadang ga ada tapi gapapa
        published_time = soup.find("meta", property="article:published_time")
        published_time = published_time["content"] if published_time else "N/A"

        if config:
            source = soup.find(config["tag", config["spec"]])
        else:
            source = soup.find("body")

        if source:
            # kita ilangin tag tag yang bermasalh dulu, sebelum ambil paragraf sisanya
            for sampah in source.find_all(["strong", "b", "blockquote", "img"]):
                sampah.decompose

            all_p = source.find_all(["p", "li"])

            # isi berita (panjangnya > 50 karakter. kalau dibawah rawan iklan)
            # biar ga dapet teks navigasi/menu
            content = "\n".join([p.get_text(strip=True) for p in all_p if len(p.get_text(strip=True)) > 50])

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
    os.makedirs("Scraping_ArtikelBerita/data", exist_ok=True)

        
    file_path = os.path.join("Scraping_ArtikelBerita/data", f"{output_jsonl}.jsonl")

    with open(file_path, "a", encoding="utf-8") as f_out:
        with ThreadPoolExecutor(max_workers=10) as executor:
            # tqdm buat munculin progress bar
            results = list(tqdm(executor.map(extract_informasi, file), total=len(file)))

            for res in results:
                if res and len(res['text']) > 200: # ambil yang teknys panjang 
                    f_out.write(json.dumps(res, ensure_ascii=False) + "\n")
