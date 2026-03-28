HEADERS = {"User-Agent": "Mozilla/5.0"}

RANDOM_KATA = [
    "ya sayang",
    "beb",
    "bestie",
    "bosku",
    "abangku",
    "cantik",
    "ganteng",
]


MAP_PORTAL = {
   "cnnindonesia": {"tag": "div", "spec": {"class": "detail-text"}},
   "indozone": {"tag": "div", "spec": {"class": "article-ct"}},
   "kompas": {"tag": "div", "spec": {"class": "read__content"}},
   "detik": {"tag": "div", "spec":{"class": "detail__body-text"}},
   "liputan6": {"tag": "div", "spec": {"class": "article-content-body__item-content"}},
   "cnbcindonesia": {"tag": "div", "spec": {"class": "detail-text"}},
   "okezone": {"tag": "div", "spec":{"class" : "c-detail read"}}, 

   "kumparan": {"tag": "main", "spec":{"data-qa-id": "article-main"}}

   # "jpnn": {"tag": "div", "spec": {"itemprop": "articleBody"}},
#    "republika": {"tag": "div", "spec": {"class": "article-content"}}, # dia ga ada sitemap ternyata. bisa pake dari crawler(gagal).py tapi belum kurapihin 
   # "tribunnews": {"tag": "div", "spec": {"class": "side-article"}}, # ketahan waf. nanti kapan kapan aku belajar dulu 

}