import urllib.request as urllib
import json
from bs4 import BeautifulSoup
def get_soup(url):
    return BeautifulSoup(urllib.urlopen(urllib.Request(url, headers={'User-Agent': user_agent_header})), features="html5lib")

user_agent_header = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36'


def get_image_page_content(content):
    content = '+'.join(content.split())
    url = 'https://www.google.lv/search?q=' + content + '&source=lnms&tbm=isch&sa=X&sqi=2'
    print("Requesting for all image results..")
    req =  urllib.Request(url)
    req.add_header('User-Agent', user_agent_header)
    print("Opening requested image results..")
    resp = urllib.urlopen(req)
    return parse_image_results(url, resp.read())

def parse_image_results(url, results):
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

print(get_image_page_content('flying birds'))
