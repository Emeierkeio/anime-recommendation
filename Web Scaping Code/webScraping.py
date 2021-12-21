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
    URL = "https://myanimelist.net/anime/" + str(malId)
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


# Mantain only the even indices in the list
def even(list):
    return [list[i] for i in range(0, len(list), 2)]


# Create a csv file with the informations of the anime
def informationsCsv(id, animeStudios, producer):
    with open("../data/scraping/anime_informations.csv", "a") as file:
        file.write(str(id) + "," + animeStudios + "," + producer + "\n")
    file.close()

# Scrape the informations about animeStudios and Producer of the content of response
def getStudios(response):
    soup = BeautifulSoup(response, "html.parser")
    studio = soup.find_all("span", class_="dark_text")
    for i in studio:
        if i.text == "Studios:":
            animeStudios = i.next_sibling.next_sibling.text
        elif i.text == "Source:":
            source = i.next_sibling.text
    return animeStudios

# Scrape the first element in the list of staff in content of response
def getProducer(response):
    soup = BeautifulSoup(response, "html.parser")
    staffDiv = soup.find_all("div", class_="detail-characters-list clearfix")
    producer = staffDiv[1].find_all("img")[0].get("alt")
    
    return producer.replace(",", "")

# In case of error, save the anime informations in a csv file
def checkErrors(statusCode, url, id):
    if statusCode != 200:
        with open("../data/scraping/errors.csv", "a") as file:
            file.write(str(id) + "," + url + "," + str(statusCode) + "\n")
        file.close()
        return False
    else:
        return True

# Get reviews from the page of the anime
#def getReviews(response)


# Get recommendations from the page of the anime broken
def getRecommendations(response):
    soup = BeautifulSoup(response, "html.parser")
    recommendations = soup.find_all("div", class_="recommendations-container")
    recommendations = recommendations[0].find_all("a")
    recommendations = [recommendation.get("href") for recommendation in recommendations]
    recommendations = [recommendation.split("/")[2] for recommendation in recommendations]
    recommendations = even(recommendations)
    print(recommendations)

# Write the recommendations in a csv file
def recommendationsCsv(id, recommendations):
    with open("../data/scraping/recommendations.csv", "a") as file:
        for recommendation in recommendations:
            file.write(str(id) + ',' + str(recommendation) + "\n")
    file.close()

# Write the reviews in a csv file
def reviewsCsv(id, reviews, votes):
    with open("../data/scraping/reviews.csv", "a") as file:
        for review, vote in reviews, votes:
            file.write(str(id) + ',' + str(vote) + ',' + review + "\n")
    file.close()

# Remove all the spaces in string
def format(string):
    return string.replace("\n", "").replace("\r", "")

if __name__ == "__main__":
    # Get the page from every element in animeList
    #ids = getMalIds()
    _,_, content = getPage(22689)
    informationsCsv(22689, getStudios(content), getProducer(content))
    #for id in ids[1:]:
        #statusCode, url, content = getPage(id)
        #if checkErrors(statusCode, url, id):
            #informationsCsv(id, getStudios(content), getProducer(content))
            #recommendationsCsv(id, getRecommendations(content))
            #reviewsCsv(id, getReviews(content))
        #else:
            #print("Error in page: " + str(id))
    

