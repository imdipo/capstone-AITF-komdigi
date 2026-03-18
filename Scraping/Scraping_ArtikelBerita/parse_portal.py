from urllib.parse import urlparse
from config import MAP_PORTAL
# link = "https://ekonomi.republika.co.id/berita/tc0ts8490/hadapi-investigasi-dagang-dari-as-airlangga-fokus-isu-kapasitas-produksi-dan-kerja-paksa-part2?page=all"

"""
beberapa berita punya variasi nama tergantung fokus berita
misal:
A.com, Sport.A.com, Finance.A.com dll
jadi ini buat ngambil hanya A nya aja, soalnya kita butuh buat bandingin sama key dari MAP_PORTAL 
"""

def ambil_portal(url):
    homepage = urlparse(url).netloc
    print(homepage)

    nama_web = homepage.split(".")
    print(nama_web)

    nama_portal = [web for web in nama_web if web in MAP_PORTAL]
    nama = nama_portal[0]

    return nama
