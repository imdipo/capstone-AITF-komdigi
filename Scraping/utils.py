def save_txt(urls, source_name):
    file_link = f"link_portal_{source_name}.txt"
    with open(file_link, 'w') as f:  
        for element in sorted(urls):
            f.write(element + "\n")
    print("udah disimpen file txt nya ya")