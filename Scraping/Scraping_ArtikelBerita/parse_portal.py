from urllib.parse import urlparse
from config import MAP_PORTAL
# link = "https://megapolitan.kompas.com/sitemap.xml"

"""
beberapa berita punya variasi nama tergantung fokus berita
misal:
A.com, Sport.A.com, Finance.A.com dll
jadi ini buat ngambil hanya A nya aja, soalnya kita butuh buat bandingin sama key dari MAP_PORTAL 
"""

def ambil_portal(url):
    homepage = urlparse(url).netloc
    # print(homepage)

    nama_web = homepage.split(".")
    # print(nama_web)

    nama_portal = [web for web in nama_web if web in MAP_PORTAL]
    nama = nama_portal[0]

    return nama

# ambil_portal(link)