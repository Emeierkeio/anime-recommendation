# -----------------------------------------------------------
# This file contains the functions to request all the needed informations 
#      from the https://aniapi.com/ API and write them to csv files.
#
# 2021, Mirko Tritella, Aurora Cerabolini, Corinna Strada
# email m.tritella@campus.unimib.it
# -----------------------------------------------------------

import requests
from requests.api import get

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Ijg1MiIsIm5iZiI6MTYzOTg0NDA4NCwiZXhwIjoxNjQyNDM2MDg0LCJpYXQiOjE2Mzk4NDQwODR9.EGOLZz-qo91DKVc4gA0RxC0l0MmD44Vl3MhVcwobb0M" #: AniAPI token

formatDestination = {
    0 : "tv",
    1 : "tv short",
    2 : "movie",
    3 : "special",
    4 : "ova",
    5 : "ona",
    6 : "music",
} #: Dictionary that maps the integer value to the format destination of the anime


releaseStatus = {
    0 : "finished",
    1 : "releasing",
    2 : "not yet released",
    3 : "cancelled",
} #: Dictionary that maps the integer value to the release status of the anime


def requestJson(pageNumber:str) -> dict:
    """
    Return the response of the request.

    :param pageNumber: Page number needed for request pagination.
    :type pageNumber: str
    :return: Dictionary of response.
    :rtype: dict

    """
    url = "https://api.aniapi.com/v1/anime/?page={}".format(pageNumber)
    response = apiRequest(url, token)
    return response.json()


def apiRequest(url:str, token:str) -> requests.Response:
    """
    Set the parameters for the request.

    :param url: URL of the request.
    :type url: str
    :param token: AniAPI token.
    :type token: str
    :return: Response of the request.
    :rtype: requests.Response

    """
    headers = {'Authorization': 'Bearer ' + token,
               'Content-Type': 'application/json',
               'Accept': 'application/json'}
    return requests.get(url, headers=headers)


def checkResponseStatusCode(response:dict) -> bool:
    """
    Check the response status code to handle errors.

    :param response: Response of the request.
    :type response: dict
    :return: True if the status code is 200, Raise rate limit error if the status code is 429, False otherwise.
    :rtype: bool

    """
    if response['status_code'] == 200:
        return True
    elif(response['status_code'] == 429):
        print(response)
        print("Rate Limit raggiunto, aspetta un po'")
        return False
    else:
        print("Errore: " + str(response['status_code']))
        return False


def animeInformationstoCSV(animeList:list) -> None:
    """
    Write the list of all the animes' most important informations to a csv file named anime_information.csv.

    :param animeList: List of all the anime.
    :type animeList: list
    :return: None.
    :rtype: None
    
    """
    with open('../data/api/anime_informations.csv', 'a') as csvFile:
        for anime in animeList:
            fixedAnime = fixDictionary(anime)
            mal_id, enTitle, _, episodesCount, episodeDuration, _, status, format, year = getInformations(fixedAnime)
            csvFile.write(mal_id + '|' + enTitle + '|' + year + '|' + episodesCount + '|' + episodeDuration + '|' + formatDestination[format] + '|' + releaseStatus[status] + '\n')
    csvFile.close()
    print('Anime list written to csv file')
    return


def animeDescriptiontoCSV(animeList:list) -> None:
    """
    Write anime descriptions to csv file named anime_description.csv.

    :param animeList: List of all the anime.
    :type animeList: list
    :return: None.
    :rtype: None

    """
    with open('../data/api/anime_descriptions.csv', 'a') as csvFile:
        for anime in animeList:
            fixedAnime = fixDictionary(anime)
            mal_id, _, description, _, _, _, _, _, _ = getInformations(fixedAnime)
            formattedDescription = formatDescription(description)
            csvFile.write(mal_id + '|' + formattedDescription  + '\n')
    csvFile.close()
    print('Anime descriptions written to csv file')
    return


def animeGenrestoCSV(animeList:list) -> None:
    """
    Write anime genres to csv file named anime_genres.csv.

    :param animeList: List of all the anime.
    :type animeList: list
    :return: None.
    :rtype: None

    """
    with open('../data/api/anime_genres.csv', 'a') as csvFile:
        for anime in animeList:
            fixedAnime = fixDictionary(anime)
            mal_id, _, _, _, _, genres, _, _, _ = getInformations(fixedAnime)
            for genre in genres:
                csvFile.write(mal_id + ',' + genre + '\n')
    csvFile.close()
    print('Anime genres written to csv file')
    return


def fixDictionary(anime:dict) -> dict:
    """
    Format the dictionary to be able to get nested informations.

    :param anime: Dictionary that contains the anime informations.
    :type anime: dict
    :return: Dictionary with the fixed informations.
    :rtype: dict

    """
    anime['en_title'] = anime['titles']['en']
    anime['en_description'] = anime['descriptions']['en']
    return anime


def formatDescription(description:str) -> str:
    """
    Format the description of the anime to delete tabs, pipes and new lines.

    :param description: Anime description.
    :type description: str
    :return: Formatted description.
    :rtype: str

    """
    return description.replace('\n', '').replace('\r', '').replace('\t', '').replace('|', '')

     
def getAnimeListFromJson(response:dict) -> list:
    """
    Get the list of anime from the JSON response.

    :param response: Dictionary of the response.
    :type kind: dict
    :return: List of anime.
    :rtype: list

    """
    animeList = response['data']['documents']
    return animeList


def getInformations(anime:dict) -> list:
    """
    Get the information of the anime in order to handle KeyError exception.

    :param anime: Dictionary of the anime informations.
    :type anime: dict
    :return: List of anime informations without KeyError exception.
    :rtype: dict

    """
    enTitle = anime.get('en_title', '').replace("|", "")
    episodesCount = anime.get('episodes_count', '')
    episodeDuration = anime.get('episode_duration', '')
    description = anime.get('en_description', '')
    genres = anime.get('genres', [])
    releaseStatus = anime.get('status', '')
    formatDestination = anime.get('format', '')
    year = anime.get('season_year', '')
    mal_id = anime.get('mal_id', '')

    return str(mal_id), str(enTitle), str(description), str(episodesCount), str(episodeDuration), genres, releaseStatus, formatDestination, str(year)



if __name__ == "__main__":
    for pageNumber in range(1, 145):
        jsonResponse = requestJson(pageNumber)
        if checkResponseStatusCode(jsonResponse):
            animeList = getAnimeListFromJson(jsonResponse)
            animeInformationstoCSV(animeList)
            #animeDescriptiontoCSV(animeList)
            #animeGenrestoCSV(animeList)
        else:
            break
        print("Page number {} finished".format(pageNumber))

