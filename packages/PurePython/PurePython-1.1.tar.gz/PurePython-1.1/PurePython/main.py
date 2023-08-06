"""
    Main file for PurePython class
"""
import requests
import bs4
import re
import json


class PurePython(object):
    """
        This is PurePython Package. This package contain many useful tools.

        Features - 
        --------------------------

        1. PurePython.DownloadInstagramPhoto(url):
            This will be used to download instagram photos from url

        Other Methods - 
        --------------------------

        1. PurePython.verbose(flag):
            Change verbosity to True/False

    """

    def __init__(self):
        """
            Initialize the PurePython class.
        """
        self.verbose_attr = True

    def verbose(self, flag):
        """
            Change Verosity

            Parameters:
            ------------------------------------------
            flag : bool
                New verbosity value

        """
        self.verbose_attr = flag

    def pprint(self, msg):
        """
            Custom Print Function for PurePython

            Parameters:
            ------------------------------------------
            msg : str
                Msg value

        """
        if self.verbose_attr:
            print(msg)

    def __downloadPhoto(self, url, path):
        """
            Private method to download photo and save to given path.
        """
        try:
            response = requests.get(url, allow_redirects=True)
            with open(path, 'wb') as file:
                file.write(response.content)
        except:
            self.pprint("Some error occurred in downloading or saving")

    def DownloadInstagramPhoto(self, url, file=None):
        """
            Download Instagram Photo from the Url.

            Parameters:
            ------------------------------------------
            url : str
                Url of the image to be downloaded

            Returns:
            ------------------------------------------
            bool: True if task is successfull and False if some error is occurred.

        """
        if not url:
            self.pprint("Url is not passed")
            return False
        url_regex = re.compile(
            r'^(?:http|ftp)s?://'  # http:// or https://
            # domain...
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        if re.match(url_regex, url) is None:
            self.pprint("Wrong url is passed.")
            return False
        try:
            response = str(requests.get(url).text)
        except:
            self.pprint("Error fetching data from instagram")
            return False
        try:
            user_data_reg = r'<script type="text/javascript">window._sharedData = (.+);</script>'
            json_data = re.findall(user_data_reg, response)
            json_data = json.loads(json_data[0])
        except:
            self.pprint("Error parsing data")
            return False
        try:
            photo_data = json_data['entry_data']['PostPage'][0]['graphql']['shortcode_media']
        except:
            self.pprint("Image not found. Probably instagram block.")
            return False
        try:
            if file is None:
                self.__downloadPhoto(
                    photo_data["display_url"], str(photo_data["id"]) + ".jpg")
                self.pprint("File saved as " + str(photo_data["id"]) + ".jpg")
            else:
                self.__downloadPhoto(photo_data["display_url"], file)
                self.pprint("File saved as " + file)
        except:
            self.pprint("Error in downloading and saving photo")
            return False
        return True
