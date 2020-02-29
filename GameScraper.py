import sys
import SiteScraper as ss
import smtplib
import ssl
import os


# windows cmd command to set proxy settings
# set http_proxy=http://proxy_address:port

# commands:
# i : initialize userdata file
# a : add game to list
# l : list games
# r : remove a game
# c : clear the list of games
# h : generates a list of commands


def main() :
    if(len(sys.argv)==1) :
        scrape()
    elif(sys.argv[1] == "-s") :
        print("Welcome to GameScraper, for a list of commands press h. Before running you must initialize")
        command_input()


# reads through the games.txt file and calls functions to scrape all websites for price
def scrape() :
    webtypes = {
        0: getGameData,
        1: ss.scrapeAmazon,
        2: ss.scrapeBestBuy,
        3: ss.scrapeWalmart,
        4: ss.scrapeNewEgg,
        5: ss.scrapeTarget,
        6: ss.scrapePSstore
    }
    userdata = getUserData()
    if (not os.path.exists("games.txt")) :          # checks if file exists
        return
    file = open("games.txt", "r")
    lines = file.readlines()
    data = {}
    linecount = 0
    for x in lines:
        if(linecount%7==6) :                        # the last line for a given game calls checkDeals at the end
            command = webtypes.get(linecount % 7, lambda *args: None)
            linecount = linecount + 1
            data.update(command(x, userdata))
            checkDeals(data)
            data = {}
            continue
        command = webtypes.get(linecount % 7, lambda *args: None )
        linecount = linecount + 1
        data.update(command(x, userdata))
    file.close()
    sendEmail(userdata)


# sends the contents of email.txt (if exists and not empty) to the email in userdata.txt
def sendEmail(userdata) :
    if (os.stat("email.txt").st_size == 0) :
        return None
    file = open("email.txt", "r")
    contents = file.read()
    subject = "Games below your willingness to pay!"
    message = 'Subject: {}\n\n{}'.format(subject, contents)
    port = 465
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server :
        server.login("bigbeefygameboi@gmail.com", "gameboi1$")                      # placeholder email I made
        server.sendmail("bigbeefygameboi@gmail.com", userdata[1], message)
    open("email.txt", 'w').close()      # clears the email.txt file at the end


# checks if any of the games are below willingness to pay and add them to the email.txt file
def checkDeals(data) :
    if (len(data) == 0):
        return None
    # print(data)
    wtp = data["wtp"]
    game = data["game"]
    file = open("email.txt", "a+")
    for key in data :
        if((key!="game") and (key!="wtp")) :
            if((data[key]>0) and (data[key])<= wtp) :
                file.write(str(game) + " is available at " + str(key) + " at the price " + str(data[key]) + "\n")
    file.close()


# gets game and willingness to pay from the string
def getGameData(data, userdata) :
    values = data.split(', ')
    game = values[0]
    wtp = float(values[1])
    return {"game": game, "wtp": wtp}


# gets the users email and user agent
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


# adds a game to the list
def addGame() :
    game = input("Enter the name of the game: ")
    price = input("Enter the price you are willing to pay: ")
    amazon = input("Enter the URL for the game on amazon or NA: ")
    bestbuy = input("Enter the URL for the game at Bestbuy or NA: ")
    walmart = input("Enter the URL for the game at Walmart or NA: ")
    newegg = input("Enter the URL for the game on Newegg or NA: ")
    target = input("Enter the URL for the game at GameStop or NA: ")
    psstore = input("Enter the URL for the game on the playstation store or NA: ")
    print("")
    stores = [amazon, bestbuy, walmart, newegg, target, psstore]
    file = open("games.txt", "a+")
    file.write(game + ", " + price + "\n")
    for i in stores :
        file.write(i+"\n")
    file.close()


# initializes user agent and email
def initialize() :
    Userdata = input("Enter the user agent for the device you are running this on (google 'my user agent') : ")
    Email = input("Enter the email you want updates sent to you : ")
    file = open("userdata.txt", "w+")
    file.write(Userdata+"\n"+Email+"\n")
    file.close()
    return None


# prints a list of all the games
def listGames() :
    if (not os.path.exists("games.txt")) :
        print("No games")
        return None
    file = open("games.txt", "r")
    lines = file.readlines()
    games = []
    linecount = 0
    for x in lines :
        if(linecount%7 == 0) :
            games.append(x)
        linecount = linecount + 1
    for x in games :
        print(x.split(',')[0] + ":" + x.split(',')[1], end="")
    print("")
    file.close()


#TODO:
# - remove a game from the list, potentially take the last game and write over this one
def removeGame() :
    game = input("Enter the name of the game: ")
    if(not os.path.exists("games.txt")) :
        print("no games.txt file found")
        return None
    file = open("games.txt", "r")
    lines = file.readlines()
    file.close()
    file = open("games.txt", "w")
    line_iterator = iter(lines)
    for line in line_iterator:
        if(line.split(',')[0] == game) :
            for x in range(6) :
                next(line_iterator)
        else :
            file.write(line)
    file.close()



# clears the file of all games
def clearGames() :
    open("games.txt", 'w').close()


# prints all commands
def printCommands() :
    print("Commands\n a: add game to list\n l: list games\n"
          " r: remove a game from the list\n c: clear all games\n"
          " h : list all commands\n i: initialize\n s : stop\n")


# takes commands as input and executes them until stop command is used
def command_input():
    command_switch = {
        "i" : initialize,
        "a" : addGame,
        "l" : listGames,
        "r" : removeGame,
        "c" : clearGames,
        "h" : printCommands,
        "s" : exit
    }
    while(True) :
        commandIn = input("Enter a command: ")
        command = command_switch.get(commandIn, lambda :print("Invalid Command"))
        command()


if __name__ == "__main__" :
    main()