import random
from config import RANDOM_KATA

"""
ini file txt ga kita pake, cuman gapapa simpen aja
"""
def save_txt(urls, source_name):
    file_link = f"link_portal_{source_name}.txt"
    with open(file_link, 'w', encoding="utf-8") as f:  
        for element in sorted(urls):
            f.write(element + "\n")
    print("\n udah disimpen file txt nya ya")
    print(f"\n dapat{len(urls)} links")


def biar_ga_bosen():
    return random.choice(RANDOM_KATA)
    