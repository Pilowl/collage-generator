import urllib.request as urllib
import json
import os, shutil, time
from bs4 import BeautifulSoup
def get_soup(url):
    return BeautifulSoup(urllib.urlopen(urllib.Request(url, headers={'User-Agent': user_agent_header})), features="html5lib")

user_agent_header = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36'

src_folder = "sources/"

def get_image_page_content(content):
    # splitting keyword into google image GET request
    content = '+'.join(content.split())
    url = 'https://www.google.lv/search?q=' + content + '&source=lnms&tbm=isch&sa=X&sqi=2'
    print("Requesting for all image results..")
    req =  urllib.Request(url)
    req.add_header('User-Agent', user_agent_header)
    print("Opening requested image results..")
    resp = urllib.urlopen(req)
    return parse_image_results(url, resp.read())

def parse_image_results(url, results):
    # parsing image out of results using soup
    images = []
    soup = get_soup(url)
    print("Finding all images on the page..")
    parsed_images = soup.find_all("div",{"class":"rg_meta"})
    size = len(parsed_images)
    for i, a in enumerate(parsed_images):
        print("%d image parsing out of %d" % (i+1, size))
        link, Type = json.loads(a.text)["ou"], json.loads(a.text)["ity"]
        images.append((link, Type))
    return images

def download_image(name, url_ext):

    if url_ext[1] != "":
        name = str(name) + "." + url_ext[1]
    else:
        name = str(name)
    urllib.urlretrieve(url_ext[0], src_folder + name)   

def create_src_dir():
    print("Recreating image source directory..")
    if os.path.isdir(src_folder):
        shutil.rmtree(src_folder)
    os.makedirs(src_folder)

def save_images_by_keyword(keyword):
    urls = []
    for word in keyword:
        urls += get_image_page_content(word)
    create_src_dir()
    size = len(urls)
    final_size = size
    for i, tupl in enumerate(urls):
        print("Downloading %d image out of %d.." % (i+1, size))
        try:
            download_image(i, tupl)
        except Exception as e:
            print("Failed to download from " + tupl[0])
            final_size -= 1
            print(e)
    print("Succesfuly downloaded %d pictures of %d" % (final_size, size))


save_images_by_keyword(["Art", "Amon Amath", "Minecraft", "Java", "Zeal and Ardor", "Cola", "Aliens", "Mafia 2", "Mafia", "HZ"])
