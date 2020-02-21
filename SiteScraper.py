import requests
import re
from bs4 import BeautifulSoup
from selectorlib import Extractor
import pandas as pd

#TODO:
# - take user_agent from userdata file instead of hardcoding
# - add directories for code / textfiles / yml files


def scrapeAmazon(URL) :
    # try :
        e = Extractor.from_yaml_file('amazon.yml')
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
        headers = {'User-Agent': user_agent}
        page = requests.get(URL, headers=headers)
        data = e.extract(page.text)
        dollars = float(data["full_num"])
        cents =  float(data["cents"])
        price = dollars + cents/100
        return {"amazon" : price}
    # except :
    #     return {"amazon" : -1}



def scrapeBestBuy(URL) :
    #try :
        e = Extractor.from_yaml_file('BestBuy.yml')
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
        headers = {'User-Agent': user_agent}
        page = requests.get(URL, headers=headers)
        data = e.extract(page.text)
        value = (data["Price"])
        values = re.findall('\d+', data["Price"])
        dollars = float(values[0])
        cents = float(values[1])
        price = dollars + cents/100
        return {"bestbuy": price}
    # except :
    #     return {"bestbuy": -1}



def scrapeWalmart(URL) :
    # try :
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
        headers = {'User-Agent': user_agent}
        URL = URL.rstrip()
        page = requests.get(URL, headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')
        items = soup.find_all('span', class_="price-characteristic")
        paragraphs = []
        for x in items:
            paragraphs.append(str(x))
        values = re.findall('\d+', paragraphs[0])
        price = float(values[0]) + float(values[1])/100
        return {"walmart": price}
    # except :
    #     return {"walmart": -1}



def scrapeNewEgg(URL) :
    # try :
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
        headers = {'User-Agent': user_agent}
        URL = URL.rstrip()
        page = requests.get(URL, headers=headers)

        soup = BeautifulSoup(page.content, 'html.parser')
        items = soup.find_all('script', type="application/ld+json")
        paragraphs = []
        for x in items:
            paragraphs.append(str(x))
        value = paragraphs[2].find('"price":')
        values = re.findall('\d+', paragraphs[2][value:])
        price = float(values[0]) + float(values[1]) / 100
        return {"newegg": price}
    # except :
    #     return {"newegg": -1}


# scrapes Target to get the TSIN number then uses that to get the price
def scrapeTarget(URL) :
    # try :
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
        headers = {'User-Agent': user_agent}
        URL = URL.rstrip()
        page = requests.get(URL, headers=headers)

        soup = BeautifulSoup(page.content, 'html.parser')
        items = soup.find_all('div', class_="Col-favj32-0 fVmltG h-padding-h-default" )


        paragraphs = []
        for x in items:
            paragraphs.append(str(x))


        TSIN = paragraphs[0].find('TCIN')
        nums = re.findall('\d+', paragraphs[0][TSIN:])
        ProductID = nums[0]

        s = requests.session()
        s.get('https://www.target.com')

        key = s.cookies['visitorId']
        location = s.cookies['GuestLocation'].split('|')[0]

        store_id = requests.get(
            'https://redsky.target.com/v3/stores/nearby/%s?key=%s&limit=1&within=100&unit=mile' % (location, key)).json()
        store_id = store_id[0]['locations'][0]['location_id']

        product_id = ProductID
        url = 'https://redsky.target.com/web/pdp_location/v1/tcin/%s' % product_id
        payload = {
            'pricing_store_id': store_id,
            'key': key}

        jsonData = requests.get(url, params=payload).json()
        df = pd.DataFrame(jsonData['price'], index=[0])

        values = re.findall('\d+', df.to_string())
        price = float(values[5]) + float(values[4])/100
        return {"target": price}
    # except :
    #     return {"target": -1}



def scrapePSstore(URL) :
    try :
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
        headers = {'User-Agent': user_agent}
        URL = URL.rstrip()
        page = requests.get(URL, headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')
        items = soup.find_all('div', class_="price-display__price--is-plus-upsell")
        paragraphs = []
        for x in items:
            paragraphs.append(str(x))
        values = re.findall('\d+', paragraphs[0])
        price = float(values[0]) + float(values[1]) / 100
        return {"psstore": price}
    except :
        try :
            user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
            headers = {'User-Agent': user_agent}
            URL = URL.rstrip()
            page = requests.get(URL, headers=headers)
            soup = BeautifulSoup(page.content, 'html.parser')
            items = soup.find_all('script', class_= "ember-view")
            paragraphs = []
            for x in items:
                paragraphs.append(str(x))
            number = paragraphs[0].find('"price":')
            values = re.findall('\d+', paragraphs[0][number:])
            price = float(values[0]) + float(values[1]) / 100
            return {"psstore": price}
        except :
            return {"psstore": -1}


#TODO:
# - implement this method
def scrapeMstore(URL) :
    return {"mstore" : -1}


#TODO:
# - implement this method
def scrapeSteam(URL) :
    return {"steam" : -1}


#TODO:
# - implement this method
def scrapeEpicGames(ULR) :
    return {"epicgames" : -1}


