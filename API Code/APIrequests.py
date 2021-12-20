# -----------------------------------------------------------
# This file contains the functions to request all the needed informations 
#      from the https://aniapi.com/ API and write them to csv files.
#
# 2021, Mirko Tritella, Aurora Cerabolini, Corinna Strada
# email m.tritella@campus.unimib.it
# -----------------------------------------------------------

import requests
from requests.api import get

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Ijg1MiIsIm5iZiI6MTYzOTg0NDA4NCwiZXhwIjoxNjQyNDM2MDg0LCJpYXQiOjE2Mzk4NDQwODR9.EGOLZz-qo91DKVc4gA0RxC0l0MmD44Vl3MhVcwobb0M"

# This dictionary maps format destination from integer value to text
formatDestination = {
    0 : "tv",
    1 : "tv short",
    2 : "movie",
    3 : "special",
    4 : "ova",
    5 : "ona",
    6 : "music",
}


# This dictionary maps release status from integer value to text
releaseStatus = {
    0 : "finished",
    1 : "releasing",
    2 : "not yet released",
    3 : "cancelled",
}


# Request the list of all the anime contained in the page pageNumber
def requestJson(pageNumber):
    url = "https://api.aniapi.com/v1/anime/?page={}".format(pageNumber)
    response = apiRequest(url, token)
    return response.json()


# Create API request with the needed parameters
def apiRequest(url, token):
    headers = {'Authorization': 'Bearer ' + token,
               'Content-Type': 'application/json',
               'Accept': 'application/json'}
    return requests.get(url, headers=headers)


# Check response status code
def checkResponseStatusCode(response):
    if response['status_code'] == 200:
        return True
    elif(response['status_code'] == 429):
        print("Rate Limit raggiunto, aspetta un po', la pagina raggiunta è: " + str(response.url))
        return False
    else:
        print("Errore: " + str(response['status_code']))
        return False


# Write the list of all the anime important informations to csv file
def animeInformationstoCSV(animeList):
    with open('../data/api/anime_informations.csv', 'a') as csvFile:
        for anime in animeList:
            fixedAnime = fixDictionary(anime)
            enTitle, _, episodesCount, episodeDuration, _, status, format, year, mal_id = getInformations(fixedAnime)
            csvFile.write(mal_id + ',' + enTitle + ',' + year + ',' + episodesCount + ',' + episodeDuration + ',' + formatDestination[format] + ',' + releaseStatus[status] + '\n')
    csvFile.close()
    print('Anime list written to csv file')
    return


# Write anime descriptions to csv file
def animeDescriptiontoCSV(animeList):
    with open('../data/api/anime_descriptions.csv', 'a') as csvFile:
        for anime in animeList:
            fixedAnime = fixDictionary(anime)
            _, description, _, _, _, _, _, _, mal_id = getInformations(fixedAnime)
            formattedDescription = formatDescription(description)
            csvFile.write(mal_id + '|' + formattedDescription  + '\n')
    csvFile.close()
    print('Anime descriptions written to csv file')
    return


# Write anime genres to csv file
def animeGenrestoCSV(animeList):
    with open('../data/api/anime_genres.csv', 'a') as csvFile:
        for anime in animeList:
            fixedAnime = fixDictionary(anime)
            _, _, _, _, genres, _, _, _, mal_id = getInformations(fixedAnime)
            for genre in genres:
                csvFile.write(mal_id + ',' + genre + '\n')
    csvFile.close()
    print('Anime genres written to csv file')
    return


# Format the dictionary to be able to get nested informations
def fixDictionary(anime):
    anime['en_title'] = anime['titles']['en']
    anime['en_description'] = anime['descriptions']['en']
    return anime


# Format the description of the anime to delete tabs, pipes and new lines
def formatDescription(description):
    return description.replace('\n', '').replace('\r', '').replace('\t', '').replace('|', '')

     
# Get the list of anime from the JSON response
def getAnimeListFromJson(response):
    animeList = response['data']['documents']
    return animeList


# Get the information of the anime in order to handle KeyError exception
def getInformations(anime):
    enTitle = anime.get('en_title', '')
    episodesCount = anime.get('episodes_count', '')
    episodeDuration = anime.get('episode_duration', '')
    description = anime.get('en_description', '')
    genres = anime.get('genres', [])
    releaseStatus = anime.get('status', '')
    formatDestination = anime.get('format', '')
    year = anime.get('season_year', '')
    mal_id = anime.get('mal_id', '')

    return str(enTitle), str(description), str(episodesCount), str(episodeDuration), genres, releaseStatus, formatDestination, str(year), str(mal_id)



if __name__ == "__main__":
    for pageNumber in range(1, 145):
        jsonResponse = requestJson(pageNumber)
        if checkResponseStatusCode(jsonResponse):
            animeList = getAnimeListFromJson(jsonResponse)
            animeInformationstoCSV(animeList)
            animeDescriptiontoCSV(animeList)
            animeGenrestoCSV(animeList)
        else:
            break
        print("Page number {} finished".format(pageNumber))

