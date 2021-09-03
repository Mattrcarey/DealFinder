import requests 
import re
from selectorlib import Extractor
import pandas as pd
import sys
import ssl
import os
import json
import smtplib

EMAIL = "bigbeefygameboi@gmail.com"
EMAIL_PASSWORD = "gameboi1$"

email_on = False 


# Scrapes Amazon and gets returns the current price of a product.
def scrapeAmazon(URL, userdata) :
    try:
        e = Extractor.from_yaml_file('amazon.yml')
        user_agent = userdata[0]
        headers = {'User-Agent': user_agent}
        headers = {
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': user_agent,
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://www.amazon.com/',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        }
        page = requests.get(URL, headers=headers)
        data = e.extract(page.text)
        
        csslist = ["price_new","price", "kindle_price", "price_kindle", "app_price", "price_game", "price_apps", "price_books"]
       
        for x in  csslist : 
            try : 
                prices = re.findall("\d+\.\d+", (data[x]))
                price = float(prices[0])
                break
            except :
                continue
        return {"amazon" : price}
    except :
        print("Error with amazon scrape")
        return {"amazon" : -1}


def main() :
    global email_on
    if(len(sys.argv)==1) :
        scrape()
    elif(sys.argv[1] == "-s") :
        print("Welcome to DealFinder, for a list of commands press h. Before running you must initialize")
        command_input()
    elif(sys.argv[1] == "-e") :
        email_on = True
        scrape()


def scrape() :
    functypes = {
        0: getProductData,
        1: scrapeAmazon
    }
    userdata = getUserData()
    if (not os.path.exists("products.txt")) :
        return
    file = open("products.txt", "r")
    lines = file.readlines()
    data = {}
    linecount = 0
    for x in lines: 
        command = functypes.get(linecount % 2, lambda *args: None)
        linecount = linecount + 1
        data.update(command(x, userdata))
        if(linecount % 2 == 0) :
            checkDeals(data)
            data = {}
    file.close()
    sendEmail(userdata)


# Sends the contents of email.txt (if exists and not empty) to the email in userdata.txt
def sendEmail(userdata) :
    global email_on, EMAIL, EMAIL_PASSWORD
    if (not os.path.exists("email.txt")):
        return None
    if (os.stat("email.txt").st_size == 0) :
        return None
    if (not email_on) :
        open("email.txt", 'w').close()
        return
    file = open("email.txt", "r")
    contents = file.read()
    subject = "Products below your willingness to pay!"
    message = 'Subject: {}\n\n{}'.format(subject, contents)
    port = 465
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server :
        server.login("bigbeefygameboi@gmail.com", "gameboi1$")
        server.sendmail("bigbeefygameboi@gmail.com", userdata[1], message)
    open("email.txt", 'w').close()
    return


# Checks if any of the products are below willingness to pay and adds them to the email.txt file
def checkDeals(data) :
    if (len(data) == 0):
        return None 
    wtp = data["wtp"]
    product = data["product"]
    price = data["amazon"]
    print(str(product) + ":\nWillingness:", wtp, "\nCurrent Price:", price, "\n")
    file = open("email.txt", "a+")
    for key in data :
        if((key!="product") and (key!="wtp")) :
            if((data[key]>0) and (data[key])<= wtp) :
                file.write(str(product) + " is available at " + str(key) + " at the price " + str(data[key]) + "\n")
    file.close()


# Gets product and willingness to pay from the string
def getProductData(data, userdata) :
    values = data.split(', ')
    product = values[0]
    wtp = float(values[1])
    return {"product": product, "wtp": wtp}


# Gets the users email and user agent
def getUserData() :
    if(not os.path.exists("userdata.txt")) :
        print("not initialized run with argument '-s'")
        return
    file = open("userdata.txt", "r")
    useragent = file.readline().strip()
    email = file.readline().strip()
    data = [useragent, email]
    file.close()
    return data


# Adds a product to the list
def addProduct() :
    product = input("Enter the name of the product: ")
    price = input("Enter the price you are willing to pay: ")
    amazon = input("Enter the URL for the product on amazon: ")
    print("")
    file = open("products.txt", "a+")
    file.write(product + ", " + price + "\n")
    file.write(amazon+"\n")
    file.close()


# Initializes user agent and email
def initialize() :
    Userdata = input("Enter the user agent for the device you are running this on (google 'my user agent') : ")
    Email = input("Enter the email you want updates sent to : ")
    file = open("userdata.txt", "w+")
    file.write(Userdata+"\n"+Email+"\n")
    file.close()
    return None


# Prints a list of all the products
def listProducts() :
    if (not os.path.exists("products.txt")) :
        print("No products")
        return None
    file = open("products.txt", "r")
    lines = file.readlines()
    products = []
    linecount = 0
    for x in lines :
        if(linecount%2 == 0) :
            products.append(x) 
        linecount = linecount + 1
    for x in products :
        print(x.split(',')[0] + ":" + x.split(',')[1], end="")
    print("")
    file.close()



# Remove a product from the list
def removeProduct() :
    product = input("Enter the name of the product: ")
    if(not os.path.exists("products.txt")) :
        print("no products.txt file found")
        return None
    file = open("products.txt", "r")
    lines = file.readlines()
    file.close()
    file = open("products.txt", "w")
    line_iterator = iter(lines)
    for line in line_iterator:
        if(line.split(',')[0] == product) :
            next(line_iterator)
        else :
            file.write(line)
    file.close()


# Clears the file of all products
def clearProducts() :
    open("products.txt", 'w').close()


# Prints all commands
def printCommands() :
    print("Commands\n a: add product to list\n l: list products\n"
          " r: remove a product from the list\n c: clear all products\n"
          " h : list all commands\n i: initialize\n s : stop\n")


# Takes commands as input and executes them until stop command is used
def command_input():
    command_switch = {
        "i" : initialize,
        "a" : addProduct,
        "l" : listProducts,
        "r" : removeProduct,
        "c" : clearProducts,
        "h" : printCommands,
        "s" : exit
    }
    while(True) :
        commandIn = input("Enter a command: ")
        command = command_switch.get(commandIn, lambda :print("Invalid Command"))
        command()


if __name__ == "__main__" :
    main()


