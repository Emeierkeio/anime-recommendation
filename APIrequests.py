import requests
from requests.api import get

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Ijg1MiIsIm5iZiI6MTYzOTg0NDA4NCwiZXhwIjoxNjQyNDM2MDg0LCJpYXQiOjE2Mzk4NDQwODR9.EGOLZz-qo91DKVc4gA0RxC0l0MmD44Vl3MhVcwobb0M"

# Dictionary for format destination
format_destination = {
    0 : "tv",
    1 : "tv short",
    2 : "movie",
    3 : "special",
    4 : "ova",
    5 : "ona",
    6 : "music",
}

# Dictionary for release status
release_status = {
    0 : "finished",
    1 : "releasing",
    2 : "not yet released",
    3 : "cancelled",
}


# Request the list of all the anime in the database
def get_anime_list(page_number):
    url = "https://api.aniapi.com/v1/anime/?page={}".format(page_number)
    response = api_request(url, token)
    return response.json()

# API request
def api_request(url, token):
    headers = {'Authorization': 'Bearer ' + token,
               'Content-Type': 'application/json',
               'Accept': 'application/json'}
    return requests.get(url, headers=headers)

# Check response status code
def check_response_status_code(response):
    if response['status_code'] == 200:
        return True
    elif(response['status_code'] == 429):
        print("Rate Limit raggiunto, aspetta un po', la pagina raggiunta è: " + str(response.url))
        return False
    else:
        print("Errore: " + str(response.status_code) + " " + str(response.url))
        return False


# Write the list of all the anime important informations to csv file
def write_anime_list_to_csv(anime_list):
    with open('anime_informations.csv', 'a') as csv_file:
        for anime in anime_list:
            formatted_anime = format_anime(anime)
            id, en_title, _, episodes_count, episode_duration, _, status, format, year = get_information(formatted_anime)
            csv_file.write(id + ',' + en_title + ',' + year + ',' + episodes_count + ',' + episode_duration + ',' + format_destination[format] + ',' + release_status[status] + '\n')
    csv_file.close()
    print('Anime list written to csv file')
    return

# Write anime descriptions to csv file
def write_anime_descriptions_to_csv(anime_list):
    with open('anime_descriptions.csv', 'a') as csv_file:
        for anime in anime_list:
            formatted_anime = format_anime(anime)
            id, _, description, _, _, _, _, _ = get_information(formatted_anime)
            csv_file.write(id + ',' + description  + '\n')
    csv_file.close()
    print('Anime descriptions written to csv file')
    return

# Write anime genres to csv file
def write_anime_genres_to_csv(anime_list):
    with open('anime_genres.csv', 'a') as csv_file:
        for anime in anime_list:
            formatted_anime = format_anime(anime)
            id, _, _, _, _, genres, _, _ = get_information(formatted_anime)
            for genre in genres:
                csv_file.write(id + ',' + genre + '\n')
    csv_file.close()
    print('Anime genres written to csv file')
    return

# Format the anime to be able to get the information
def format_anime(anime):
    anime['en_title'] = anime['titles']['en']
    anime['en_description'] = anime['descriptions']['en']
    return anime

     
# Get the list of anime from the json response
def get_anime_list_from_json(response):
    anime_list = response['data']['documents']
    return anime_list

# Get the information of the anime in order to handle KeyError exception
def get_information(anime):
    id = anime.get('id', '')
    en_title = anime.get('en_title', '')
    episodes_count = anime.get('episodes_count', '')
    episode_duration = anime.get('episode_duration', '')
    description = anime.get('en_description', '')
    genres = anime.get('genres', [])
    release_status = anime.get('status', '')
    format_destination = anime.get('format', '')
    year = anime.get('season_year', '')

    return str(id), str(en_title), str(description), str(episodes_count), str(episode_duration), genres, release_status, format_destination, str(year)

if __name__ == "__main__":
    for page_number in range(1, 145):
        anime_list = get_anime_list(page_number)
        if check_response_status_code(anime_list):
            jsonResponse = get_anime_list_from_json(anime_list)
            write_anime_list_to_csv(jsonResponse)
            write_anime_descriptions_to_csv(jsonResponse)
            write_anime_genres_to_csv(jsonResponse)
        else:
            break
        print("Page number {} finished".format(page_number))

