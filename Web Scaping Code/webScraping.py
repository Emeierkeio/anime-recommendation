# -----------------------------------------------------------
# This file contains the functions to scrape all the needed informations 
#      from https://www.anime-planet.com/ and write them to csv files.
#
# 2021, Mirko Tritella, Aurora Cerabolini, Corinna Strada
# email m.tritella@campus.unimib.it
# -----------------------------------------------------------

import requests
from bs4 import BeautifulSoup

URL = "https://www.anime-planet.com/anime/"


# Get the page that you need to scrape starting from the name of the anime
def getPage(animeTitle):
    URL = "https://www.anime-planet.com/anime/" + formatName(animeTitle)
    page = requests.get(URL)
    return page.status_code, page.url, page.content

# Format the name of the anime to be used in the URL
def formatName(animeTitle):
    animeTitle = animeTitle.lower()

    animeTitle = animeTitle.replace(" ", "-")
    animeTitle = animeTitle.replace("'", "")
    animeTitle = animeTitle.replace(".", "")
    animeTitle = animeTitle.replace(",", "")
    animeTitle = animeTitle.replace(":", "")
    animeTitle = animeTitle.replace(";", "")
    animeTitle = animeTitle.replace("!", "")
    animeTitle = animeTitle.replace("?", "")
    animeTitle = animeTitle.replace("(", "")
    animeTitle = animeTitle.replace(")", "")
    animeTitle = animeTitle.replace("[", "")
    animeTitle = animeTitle.replace("]", "")
    animeTitle = animeTitle.replace("{", "")
    animeTitle = animeTitle.replace("}", "")
    animeTitle = animeTitle.replace("/", "")
    animeTitle = animeTitle.replace("\\", "")
    animeTitle = animeTitle.replace("*", "")
    animeTitle = animeTitle.replace("&", "")
    animeTitle = animeTitle.replace("%", "")
    animeTitle = animeTitle.replace("$", "")
    animeTitle = animeTitle.replace("#", "")
    animeTitle = animeTitle.replace("@", "")
    animeTitle = animeTitle.replace("+", "")
    animeTitle = animeTitle.replace("=", "")
    animeTitle = animeTitle.replace("|", "")
    animeTitle = animeTitle.replace("~", "")
    animeTitle = animeTitle.replace("`", "")
    animeTitle = animeTitle.replace("^", "")
    animeTitle = animeTitle.replace("<", "")
    animeTitle = animeTitle.replace(">", "")
    animeTitle = animeTitle.replace("\"", "")
    animeTitle = animeTitle.replace("'", "")

    animeTitle = removeNonAlphaNumeric(animeTitle)

    return animeTitle

# Get the list of titles of the anime from csv file
def getAnimeList():
    animeList = []
    with open("../data/api/anime_informations.csv", "r") as file:
        for line in file:
            animeTitle = formatName(line.strip().split(",")[1])
            animeList.append(animeTitle)
    return animeList

# Remove all the non-alphanumeric characters (i.e: ☆)
def removeNonAlphaNumeric(animeTitle):
    for char in animeTitle:
        if char not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-":
            animeTitle = animeTitle.replace(char, "")
    return animeTitle

if __name__ == "__main__":
    # Get the page from every element in animeList
    animeList = getAnimeList()
    status = {}
    for animeTitle in animeList:
        status_code, url, _ = getPage(animeTitle)
        print(status_code, url)
    

