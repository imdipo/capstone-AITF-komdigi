import requests
from bs4 import BeautifulSoup
from config import HEADERS
from utils import biar_ga_bosen

"""
hmm, karena aku lumayan males pake selenium. segala click click ribet
aku coba stay dengan bs4. jadi buat langkah pertama kita ambil link link terlebih dahulu
ini ga satu satu kok, kita tinggal cek sitemap.xml nya aja
terus kita jelajah sekalian ambil link link berita nya
"""

def getting_all_link(homepage, link_terkumpul = None):
    if link_terkumpul is None:
        link_terkumpul = set()
    
    try: 
        response = requests.get(homepage, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(response.content, 'xml')
        
        sitemap_lain = soup.find_all('sitemap')

        # beberapa folder sitemap.xml itu dalemnya belum link link berita 
        if sitemap_lain:
            print(f"ada sebanyak {len(sitemap_lain)} sitemap")  

            # ini kita ambil yang 2025 keatas, sebenernya bebas sih kalau mau ambil yang 2024+ atau berapapun. cuman tadi sempet tes yang 2023 beritanya udah ga ada
            for sitemap in sitemap_lain:
                sub_urls = sitemap.find('loc').text.strip()
                lastmod = sitemap.find('lastmod')

                if lastmod:
                    tanggal = lastmod.text.strip()
                    tahun = int(tanggal[:4])
                    if tahun >= 2025:
                        getting_all_link(sub_urls, link_terkumpul)

                else: getting_all_link(sub_urls, link_terkumpul)

        # kondisi kalau ini udah di link berita (daun nya)
        urls =  soup.find_all('url')
        if urls:
            print(f"okei, udah di page file link. ada sebanyak {len(urls)} link disini {biar_ga_bosen()}")
            for link in urls:
                link_berita = link.find('loc').text.strip().replace("\n", "").replace("\t", "")
                link_terkumpul.add(link_berita) # pake set dulu sebelum txt biar ga ada duplikat    
    

    except Exception as e:
        print(f"Error di {homepage}: {e}")

    return link_terkumpul