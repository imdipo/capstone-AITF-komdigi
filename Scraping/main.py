from urllib.parse import urlparse

from scraping_links import getting_all_link
from scraping_contents import extract_informasi
from utils import save_txt

"""
belum selesai
"""

def main():
    homepage = "https://www.detik.com/sitemap.xml"
    nama_portal = urlparse(homepage).netloc
    urls = getting_all_link(homepage)
    print(f"dapat{len(urls)} links")

    save_txt(urls, nama_portal)




def harvest_contents(file_txt, output_jsonl):
    with open(file_txt, 'r') as f:
        links = [baris_link.strip() for baris_link in f.readlines()]

        print(f"sebanyak {len(links)} mulai dipanen")







# print(f"udah dikumpul sebanyak {len(link_terkumpul)} link disimpan di {file_link}")