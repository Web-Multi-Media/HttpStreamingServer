import requests
import os

import logging
logger = logging.getLogger("root")


class cover_downloader:

    def __init__(self):
        self.auth_key = ""
        env_auth_key = os.getenv('TMBD_KEY')
        if not env_auth_key:
            logger.error("cover downloader: no auth key")
            return
        self.auth_key = env_auth_key

        configuration_url = 'https://api.themoviedb.org/3/configuration?&api_key={}'.format(
            self.auth_key )

        response = requests.get(configuration_url)
        if response.status_code != 200:
            logger.error("cover downloader: Failed to get configuration")
            return
        value = response.json()

        self.base_url = value["images"]["base_url"]
        self.poster_size = value["images"]["poster_sizes"][0]

    def download_cover(self, name, outputfile, is_tv_show=False):

        if self.auth_key:

            if is_tv_show:
                api_url = 'https://api.themoviedb.org/3/search/tv?query={}&api_key={}'.format(
                    name.replace(" ", "+"), self.auth_key)
            else:
                api_url = 'https://api.themoviedb.org/3/search/movie?query={}&api_key={}'.format(
                    name.replace(" ", "+"), self.auth_key)
            response = requests.get(api_url)
            if response.status_code != 200:
                logger.error("cover downloader: Failed to search movie")
                return -1
            value = response.json()

            poster_url = "{}/{}{}".format(self.base_url, self.poster_size,
                                        value["results"][0]["poster_path"])
            response = requests.get(poster_url)
            if response.status_code != 200:
                logger.error("cover downloader: Failed to download cover")
                return -1

            with open(outputfile, mode="wb") as file:
                file.write(response.content)
            
            return 1
        else:
            logger.error("cover downloader: No properly initialized")
            return -1
