# -----------------------------------------------------------
# This file contains the functions to scrape all the needed informations 
#      from https://www.anime-planet.com/ and write them to csv files.
#
# 2021, Mirko Tritella, Aurora Cerabolini, Corinna Strada
# email m.tritella@campus.unimib.it
# -----------------------------------------------------------

import requests
from bs4 import BeautifulSoup

# Get the page that you need to scrape starting from the id of the anime
def getPage(malId):
    URL = "https://myanimelist.net/anime/" + malId
    page = requests.get(URL)
    return page.status_code, page.url, page.content

# Get the list of MAL ID of the anime from csv file
def getMalIds():
    ids = []
    with open("../data/api/anime_informations.csv", "r") as file:
        for line in file:
            animeTitle = line.strip().split(",")[0]
            ids.append(animeTitle)
    return ids


if __name__ == "__main__":
    # Get the page from every element in animeList
    ids = getMalIds()
    for id in ids[1:]:
        status_code, url, _ = getPage(id)
        print(status_code, url)
    

