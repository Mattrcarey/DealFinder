import requests
import re
from bs4 import BeautifulSoup
from selectorlib import Extractor
import json

#TODO:
# - take user_agent from userdata file instead of hardcoding
# - add try-catch statements to each method to check for bad links
# - remove prints and add returns to method with sitename and price

def scrapeAmazon(URL) :
    e = Extractor.from_yaml_file('amazon.yml')
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
    headers = {'User-Agent': user_agent}
    page = requests.get(URL, headers=headers)
    data = e.extract(page.text)
    print(json.dumps(data, indent=True))

    # TODO: if price = null then try with amazon2.yml



def scrapeBestBuy(URL) :
    e = Extractor.from_yaml_file('BestBuy.yml')
    scrape(URL, e)



def scrapeWalmart(URL) :
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
    headers = {'User-Agent': user_agent}
    URL = URL.rstrip()
    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')

    items = soup.find_all('span', class_="price-characteristic")

    paragraphs = []
    for x in items:
        paragraphs.append(str(x))
    price = re.findall('\d+', paragraphs[0])
    print(price[0] + "." + price[1])



def scrapeNewEgg(URL) :
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
    headers = {'User-Agent': user_agent}
    URL = URL.rstrip()
    page = requests.get(URL, headers=headers)

    soup = BeautifulSoup(page.content, 'html.parser')
    items = soup.find_all('script', type="application/ld+json")
    paragraphs = []
    for x in items:
        paragraphs.append(str(x))
    price = paragraphs[2].find('"price":')
    price = re.findall('\d+', paragraphs[2][price:])
    print(price[0] + "." + price[1])


#TODO:
# - implement this method
def scrapeTarget(URL) :
    print("Target")


#TODO:
# - implement this method
def scrapePSstore(URL) :
    print("PSstore")


#TODO:
# - implement this method
def scrapeMstore(URL) :
    print("Mstore")


#TODO:
# - implement this method
def scrapeSteam(URL) :
    print("Steam")


#TODO:
# - implement this method
def scrapeEpicGames(ULR) :
    print("EpicGames")



def scrape(URL, e) :
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
    headers = {'User-Agent': user_agent}
    page = requests.get(URL, headers=headers)
    data = e.extract(page.text)
    print(json.dumps(data, indent=True))