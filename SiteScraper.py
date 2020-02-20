import requests
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selectorlib import Extractor
import json
import lxml


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
    page = requests.get("https://www.walmart.com/ip/Death-Stranding-Sony-PlayStation-4-711719506027/52730201", headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')

    items = soup.find_all('span', class_="price-characteristic")
    cents = soup.find_all('span', class_="price-manitissa")

    paragraphs = []
    for x in items:
        paragraphs.append(str(x))
    price = re.findall('\d+', paragraphs[0])
    print(price[0] + "." + price[1])



def scrapeNewEgg(URL) :
    print("NewEgg")



def scrapeTarget(URL) :
    print("GameStop")



def scrapePSstore(ULR) :
    print("PSstore")



def scrapeMstore(ULR) :
    print("Mstore")



def scrapeSteam(ULR) :
    print("Steam")



def scrapeEpicGames(ULR) :
    print("EpicGames")


def scrape(URL, e) :
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
    headers = {'User-Agent': user_agent}
    page = requests.get(URL, headers=headers)
    data = e.extract(page.text)
    print(json.dumps(data, indent=True))