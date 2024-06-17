import requests
import os

auth_key = os.getenv('TMBD_KEY')
if not auth_key:
    print("no auth key")
    exit()

configuration_url = 'https://api.themoviedb.org/3/configuration?&api_key={}'.format(auth_key)
response = requests.get(configuration_url)
value = response.json()

base_url = value["images"]["base_url"]
poster_size = value["images"]["poster_sizes"][0]


movie = "jackass"
api_url = 'https://api.themoviedb.org/3/search/movie?query={}&api_key={}'.format(movie, auth_key)
response = requests.get(api_url)
value = response.json()
print(value["results"][0])

poster_url = "{}/{}{}".format(base_url, poster_size, value["results"][0]["poster_path"])
response = requests.get(poster_url)

with open("jackass.jpeg", mode="wb") as file:
    file.write(response.content)
