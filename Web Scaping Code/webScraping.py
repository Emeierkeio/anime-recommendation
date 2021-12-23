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
    return page.status_code, page.url, BeautifulSoup(page.content, "html.parser")


# Get the id of the first row of csv file
def getId():
    with open("../data/api/animeid.csv", "r") as file:
        # Get the first row of the csv file
        firstRow = file.readline()
        id = firstRow.split(",")[0]
    return id

# Create a csv file with the informations of the anime
def informationsCsv(id, animeStudios, producer):
    with open("../data/scraping/anime_informations.csv", "a") as file:
        file.write(str(id) + "," + animeStudios + "," + producer + "\n")
    file.close()

# Scrape the informations about animeStudios and Producer of the content of response
def getStudios(response):
    try:
        studio = response.find_all("span", class_="dark_text")
        for i in studio:
            if i.text == "Studios:":
                animeStudios = i.next_sibling.next_sibling.text.replace("\n", "").replace(",", " ")
        
        if animeStudios == "add some":
            animeStudios = ""
    except:
        animeStudios = ""
        print("Error in studios for id: " + str(id))
    return animeStudios

# Scrape the first element in the list of staff in content of response
def getProducer(response):
    try:
        staffDiv = response.find_all("div", class_="detail-characters-list clearfix")
        producer = staffDiv[1].find_all("img")[0].get("alt")
    except:
        producer = ""
        print("Error in producer for id: " + str(id))
    
    return producer.replace(",", "")


# Get recommendations from the page of the anime
def getRecommendations(id, response):
    try:
        # Get the list of div with class btn-anime
        recommendationList = response.find_all("li", class_="btn-anime")
        # Get the alt of every url in recommendations img
        recommendationsURLs = [recommendation.find("a").get("href") for recommendation in recommendationList]

        # Get the ids of the raccomendated animes
        recommendationsIDs = []
        for url in recommendationsURLs:
            if '/recommendations/' in url:
                urls = url.split('/')[5].split('-')
                urls.remove(id)
                recommendationsIDs.append(urls[0])
            else:
                recommendationsIDs.append(url.split('/')[4])
    except:
        recommendationsIDs = []
        print("Error in recommendations for id: " + str(id))
    return recommendationsIDs

# Get the reviews and votes of the anime
def getRatingAndReviews(response):
    try:
        # Get the votes
        rating = response.find_all("div", class_="mb8")
        votes = []
        for vote in rating:
            votes.append(vote.text.split(":")[1].replace("\n", "").replace(" ", ""))

        # Get the reviews text
        reviews = response.find_all("div", class_="textReadability")
        reviewsText = []

        # Remove the spaces from the reviews text
        for review in reviews:
            reviewsText.append(review.text.replace("\n", " ").replace("\r", " ").replace("Helpfulread more", "").replace("                  ", " ").replace("                              ", " ").replace("|", ""))
    except:
        votes = []
        reviewsText = []
        print("Error in votes and reviews for id: " + str(id))
    return votes, reviewsText

# Write the recommendations in a csv file
def recommendationsCsv(id, recommendations):
    with open("../data/scraping/recommendations.csv", "a") as file:
        for recommendation in recommendations:
            file.write(str(id) + ',' + str(recommendation) + "\n")
    file.close()

# Write the reviews in a csv file
def reviewsCsv(id, votes, reviews):
    with open("../data/scraping/reviews.csv", "a") as file:
        for i in range(len(votes)):
            file.write(str(id) + '|' + str(votes[i]) + '|' + str(reviews[i]) + "\n")
    file.close()

# Remove first row of csv file from which the id is taken
def removeFirstRow():
    with open("../data/api/animeid.csv", "r") as f:
        lines = f.readlines()
    with open("../data/api/animeid.csv", "w") as f:
        f.writelines(lines[1:])
    f.close()

if __name__ == "__main__":
    # Get the page from every element in animeList
    iteration = 0
    while True:
        id = getId()
        statusCode, url, content = getPage(id)
        if statusCode == 200:
            informationsCsv(id, getStudios(content), getProducer(content))
            recommendationsCsv(id, getRecommendations(id, content))
            votes, reviews = getRatingAndReviews(content)
            reviewsCsv(id, votes, reviews)
            print("Written correctly anime number {}; id: ".format(iteration) + str(id) + "; url: " + url)
            removeFirstRow()
            iteration += 1
        elif statusCode == 404:
            print("Assenza di id, passo al prossimo anime")
            removeFirstRow()
        elif statusCode == 403:
            print("Error in page: " + str(id) + " wait or change your ip address")
            break
    

