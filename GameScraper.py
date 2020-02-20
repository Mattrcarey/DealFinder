# from selenium import webdriver
# from BeautifulSoup import BeautifulSoup
# download libraries for selenium and bsoup

# read list of URLs and websites from txt file
# find URLs and append to txt file

# commands:
# -a : add game to list
# -l : list games
# -r : remove a game
# -c : clear the list of games
# -h : generates a list of commands


def main() :
    command_input()

def addGame() :

    game = input("Enter the name of the game: ")
    price = input("Enter the price you are willing to pay: ")

    amazon = input("Enter the URL for the game on amazon or NA: ")
    bestbuy = input("Enter the URL for the game at Bestbuy or NA: ")
    walmart = input("Enter the URL for the game at Walmart or NA: ")
    newegg = input("Enter the URL for the game on Newegg or NA: ")
    gamestop = input("Enter the URL for the game at GameStop or NA: ")
    psstore = input("Enter the URL for the game on the playstation store or NA: ")
    mstore = input("Enter the URL for the game on the microsoft store or NA: ")
    steam = input("Enter the URL for the game on Steam or NA: ")
    epicgames = input("Enter the URL for the game on Epic Games or NA: ")

    stores = [amazon, bestbuy, walmart, newegg, gamestop, psstore, mstore, steam, epicgames]

    file = open("games.txt", "a+")
    file.write(game + ", " + price + "\n") # change to \r if it doesn't work

    for i in stores :
        file.write(i+"\n") # change to /r if it doesn't work

    file.close()

def listGames() :
    file = open("games.txt", "r")
    lines = file.readlines()

    games = []
    linecount = 0
    for x in lines :
        if(linecount%10 == 0) :
            games.append(x)
        linecount = linecount + 1

    for x in games :
        print(x.split(',')[0])


def removeGame() :
    return None

def clearGames() :
    return None

def printCommands() :
    return None

def command_input():
    commandIn = input("Enter a command: ")
    command_switch = {
        "a" : addGame,
        "l" : listGames,
        "r" : removeGame,
        "c" : clearGames,
        "h" : printCommands
    }
    command = command_switch.get(commandIn, lambda :print("Invalid Command"))
    command()


if __name__ == "__main__" :
    main()