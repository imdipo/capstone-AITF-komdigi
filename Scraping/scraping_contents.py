import requests
import json
import os
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
from config import HEADERS

def extract_informasi(url):
    try: 
        response = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
                
        # judul (dari Meta Tag - Universal)
        title = soup.find("meta", property="og:title")
        title = title["content"] if title else soup.find("h1").get_text(strip=True)
                
        # waktu (dari Meta Tag - Universal)
        published_time = soup.find("meta", property="article:published_time")
        published_time = published_time["content"] if published_time else "N/A"
                
        # isi berita (panjangnya > 50 karakter. kalau dibawah rawan iklan)
        # biar ga dapet teks navigasi/menu
        all_p = soup.find_all("p")
        content = "\n".join([p.get_text(strip=True) for p in all_p if len(p.get_text(strip=True)) > 50])

        # debug
        # print(f"title: {title}")
        # print(f"published_time: {published_time}") # ga semua portal ada, tapi gapapa
        # print(f"all_p: {content}")

        return {
            "url": url,
            "title": title,
            "published_at": published_time,
            "text": content
        }
    except: return None


def harvest_informations(file, output_jsonl):
    os.makedirs("data", exist_ok=True)

    file_path = 

    with open(f"{output_jsonl}.jsonl", "a", encoding="utf-8") as f_out:
        with ThreadPoolExecutor(max_workers=10) as executor:
            # tqdm buat munculin progress bar
            results = list(tqdm(executor.map(extract_informasi, file), total=len(file)))

            for res in results:
                if res and len(res['text']) > 200: # ambil yang teknys panjang 
                    f_out.write(json.dumps(res, ensure_ascii=False) + "\n")



harvest_informations("link_portal_megapolitan.kompas.com.txt", "test")

    # with open(file_txt, 'r') as f:
    #     links = [baris_link.strip() for baris_link in f.readlines()]

    #     print(f"sebanyak {len(links)} mulai dipanen")