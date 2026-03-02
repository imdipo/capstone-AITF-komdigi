import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from collections import deque

"""
halo,
jadi script ini aku asumsi kalau struktur tiap portal berita emang beda beda, tapi...
pasti ada kesamaan kayak lokasi berita rekomendasi dan lokasi main articlenya

intinya kalian tinggal tinggal ctrl + shift + i terus ya udah tinggal cari container html nya
buat lebih jelas mungkin boleh tanya di grup yaks
"""

# ini nge-test doang, bisa sih insyaallah kedepannya kita ubah jadi input dari kalian aja
list_link_compas = "wSpec-list"
main_content_compas = "read__content"

# kita pake bfs jadi butuh 2 hal yaitu:
# set() biar ga ada link yang sama yang masuk jadi ga ada data redundant dan mencegah infinite loop
# list (sebagai queue) buat queue atau ya antrian url yang mau kita olah
start_url = "https://megapolitan.kompas.com/read/2026/02/20/10120241/kronologi-kereta-bandara-tabrak-truk-di-stasiun-poris"
visited_urls = set()
queue_urls = deque([start_url])
paragraph= []

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}   

def dapet_link_dari_kompas(parser):
    container_links = parser.find("div", class_= list_link_compas)
    # print(container_links)

    if container_links is None:
        print("ga ada, coba cek lagi deh nama class html nya")
        return
    else:
        links = container_links.find_all("div", class_="wSpec-item") # ini return list ternyata
        # print(f"jumlah link: {len(links)}")
        # print(f"contoh link {links[2]}")

    for item in links:
        href = item.get("data-url")
        print(href)
        # data-url, dari:
        # <div id="recItem-922-0" class="wSpec-item" ... data-url="https://nasional.kompas.com/...">

        if not href: continue
        

        if href and href != "#":
            print(f"href: {href}")
            if urlparse(href).netloc == urlparse(start_url).netloc:
                if href not in visited_urls:
                    queue_urls.append(href)
# <scheme>://<netloc>/<path>;<params>?<query>#<fragment>
# kita ambil netloc nya doang, biar domainnya ga kemana mana (stay di portal berita yang lagi kalian crawl)
        
        else: print("ga ada")
        

def paragraf_kompas(parser):
    container_paragraf = parser.find("div", class_= main_content_compas)

    paragraf = container_paragraf.find_all("p")

    for p in paragraf:
        paragraph.append(p.get_text(strip=True))


def crawl_web(maximum):
    while queue_urls and len(visited_urls) < maximum:
        url = queue_urls.popleft()
        if url in visited_urls:
            continue
                
        print("crawling:", url)
        visited_urls.add(url)

        try:
            response = requests.get(url, timeout=10, headers=headers)
            response.raise_for_status()
            # print(response.text[:3000]) 
        except: continue
        soup = BeautifulSoup(response.content, 'html.parser') 

        dapet_link_dari_kompas(soup)
        paragraf_kompas(soup)

crawl_web(3)

"""
sneaky, sneaky ada beberapa masalah ternyata
1. bs4 ini kayaknya ngambil struktur html tapi bagian rekomendasi-nya itu belum fully load (belum diisi API dari js nya). 
jadi yang keambil cuman placeholder (#). tapi paragraf di url utama tetep keambil
ga tau deh, apakah portal berita yang masih "kecil" bakal work
2. gw belum terlalu ngerti gimana caranya biar bisa langsung request ke API nya
3. damn, yodah gw sambil belajar. mungkin bakal juga sambil nyoba beberapa strategi lain
"""




    
