from urllib.parse import urlparse
from parse_portal import ambil_portal
from scraping_links import getting_all_link
from scraping_contents import harvest_informations
from utils import save_txt

"""
Halo, disini proses yang kulakuin adalah:
1. kita akses file sitemap.xml dari setiap homepage portal berita 
2. baru kita scrap isinya

harusnya ini ga bakal seberat selenium sih, dan menurutku kayak kalian tinggal masukin link 
dan hasilnya keluar, itu udah lumayan efisien
"""

def main(homepage):
    nama_portal = ambil_portal(homepage)

    urls = getting_all_link(homepage)

    save_txt(urls, nama_portal)

    harvest_informations(urls, nama_portal)



homepage = "https://megapolitan.kompas.com/sitemap.xml"

if __name__ == "__main__":
    main(homepage=homepage)






# print(f"udah dikumpul sebanyak {len(link_terkumpul)} link disimpan di {file_link}")