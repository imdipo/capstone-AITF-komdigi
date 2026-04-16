import requests
import re
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
        response = requests.get(homepage, headers=HEADERS, timeout=60)
        soup = BeautifulSoup(response.content, 'xml')
        
        sitemap_lain = soup.find_all(re.compile("sitemap$"))
        # beberapa folder sitemap.xml itu dalemnya belum link link berita 
        if sitemap_lain:
            print(f"ada sebanyak {len(sitemap_lain)} sitemap")  

            # ini kita ambil yang 2025 keatas, sebenernya bebas sih kalau mau ambil yang 2024+ atau berapapun. cuman tadi sempet tes yang 2023 beritanya udah ga ada
            for sitemap in sitemap_lain:
                loc_tag = sitemap.find(re.compile("loc$"))
                print(loc_tag)

                if loc_tag:
                    raw_text = loc_tag.get_text(strip=True)
                    clean_url = raw_text.replace("<![CDATA[", "").replace("]]>", "")
                    if not clean_url.startswith("http"):
                        base_url = "https://koran-jakarta.com/"
                        if clean_url.startswith("web") or clean_url.startswith("news"):
                            sub_urls = base_url + clean_url[1:]
                        else: sub_urls = base_url + clean_url
    
                    sub_urls = sub_urls.strip()

                    lastmod = sitemap.find(re.compile("lastmod$"))
                    if lastmod:
                        raw_tanggal = lastmod.get_text(strip=True)
                        clean_tanggal = raw_tanggal.replace("<![CDATA[", "").replace("]]>", "")
                        tanggal = clean_tanggal.strip()

                        print(f"tanggal-1 {tanggal}")
                        tahun = int(tanggal[:4])
                        print(f"tanggal-2 {tanggal}")
                        if tahun >= 2024:
                            getting_all_link(sub_urls, link_terkumpul)

                # else: getting_all_link(sub_urls, link_terkumpul)

        # kondisi kalau ini udah di link berita (daun nya)
        urls = soup.find_all(re.compile("url$"))
        if urls:
            print(f"okei, udah di page file link. ada sebanyak {len(urls)} link disini {biar_ga_bosen()}")
            for link in urls:
                # print(link)
                loc_tag = link.find(re.compile("loc$"))
                link_berita_raw = loc_tag.get_text()
                link_berita_bersih = link_berita_raw.replace("<![CDATA[", "").replace("]]>", "")
                link_berita = link_berita_bersih.strip()
                # print(f"jvebvje {link_berita}")

                link_berita = link_berita + "?page=all" # ntah work atau ngga wkwk, cuman pada bisa sih ya
                link_terkumpul.add(link_berita) # pake set dulu sebelum txt biar ga ada duplikat  
        # else: print("ga ada somehow")  
    

    except Exception as e:
        print(f"Error di {homepage}: {e}")

    return link_terkumpul