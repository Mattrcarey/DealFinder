import sys
import SiteScraper as ss

#TODO:
# - Add a welcome print statement when first run
# - Add commands to input userdata into a new file
# - user data includes users email & User Agent


# commands:
# -a : add game to list
# -l : list games
# -r : remove a game
# -c : clear the list of games
# -h : generates a list of commands


def main() :
    if(len(sys.argv)==1) :
        scrape()

    elif(sys.argv[1] == "-s") :
        command_input()


#Todo:
# - only scrape the line if it doesnt = NA
# - email user of all games/locations where it is below willing price
def scrape() :
    webtypes = {
        1: ss.scrapeAmazon,
        2: ss.scrapeBestBuy,
        3: ss.scrapeWalmart,
        4: ss.scrapeNewEgg,
        5: ss.scrapeTarget,
        6: ss.scrapePSstore,
        7: ss.scrapeMstore,
        8: ss.scrapeSteam,
        9: ss.scrapeEpicGames
    }

    file = open("games.txt", "r")
    lines = file.readlines()

    linecount = 0
    for x in lines:
        command = webtypes.get(linecount % 10, lambda *args: None )
        linecount = linecount + 1
        command(x)


# adds a game to the list
#TODO:
# - add asserts statements for types
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
    print("")

    stores = [amazon, bestbuy, walmart, newegg, gamestop, psstore, mstore, steam, epicgames]

    file = open("games.txt", "a+")
    file.write(game + ", " + price + "\n") # change to \r if it doesn't work

    for i in stores :
        file.write(i+"\n") # change to /r if it doesn't work

    file.close()


# prints a list of all the games
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
        print(x.split(',')[0] + ":" + x.split(',')[1], end="")
    print("")
    file.close()


#TODO:
# - remove a game from the list, potentially take the last game and write over this one
def removeGame() :
    return None


# clears the file of all games
def clearGames() :
    open("games.txt", 'w').close()


# prints all commands
def printCommands() :
    print("Commands\n a: add game to list\n l: list games\n"
          " r: remove a game from the list\n c: clear all games\n"
          " h : list all commands\n")


# exit the program
def stop() :
    exit()


# takes commands as input and executes them until stop command is used
def command_input():
    command_switch = {
        "a" : addGame,
        "l" : listGames,
        "r" : removeGame,
        "c" : clearGames,
        "h" : printCommands,
        "s" : stop
    }
    while(True) :
        commandIn = input("Enter a command: ")
        command = command_switch.get(commandIn, lambda :print("Invalid Command"))
        command()



if __name__ == "__main__" :
    main()