# -*- coding: utf-8 -*-
##############################################
# The MIT License (MIT)
# Copyright (c) 2014 Kevin Walchko
# see LICENSE for full details
##############################################
# some code taken from here:
# https://github.com/nsadawi/Download-Large-File-From-Google-Drive-Using-Python/blob/master/Download-Large-File-from-Google-Drive.ipynb
import requests
import mimetypes
from colorama import Fore
# from collections import namedtuple

# FileInfo = namedtuple("FileInfo", "filename bits")


class GoogleDrive:
    """
    Allow downloading of sharable files using their link
    """

    # get list of mime types
    _mimes = list(mimetypes.types_map.values())

    def url_to_id(self, url):
        x = url.split("/")
        return x[5]

    def download(self, link, destination=None, dumpHeader=False, download=True):
        """
        :link: shared link of file from google drive
        :destination: file name if you want over ride the original OR zipped files
        :dumpHeader: debug, print response info
        :download: debug, do everything but actually download file

        Return: (bool, filename)
        """
        id = self.url_to_id(link)
        URL = "https://docs.google.com/uc?export=download"

        session = requests.Session()
        response = session.get(URL, params = { 'id' : id }, stream = True)

        # IF file is not found (200), then return
        if response.status_code != 200:
            print(f"{Fore.RED}*** FAIL <{response.status_code}> ***{Fore.RESET}")
            return False, None

        # DEBUG: print out response header info
        if dumpHeader:
            print("-------------------------")
            for k,v in response.headers.items():
                print(f"{Fore.GREEN}{k}:{Fore.RESET} {v}")
            print("-------------------------")

        # IF the link isn't shared, then this is set
        if "X-Frame-Options" in response.headers:
            if response.headers["X-Frame-Options"] == "DENY":
                print(f"{Fore.RED}*** Google link is not shareable ***{Fore.RESET}")
                return False, None

        # for some reason, typical file types have sizes listed, but of
        # zip files, it isn't listed ... why?
        if "Content-Length" in response.headers:
            bits = int(response.headers["Content-Length"])
        else:
            bits = None

        if destination is None:
            ct = response.headers["Content-Type"]
            if ct in self._mimes:
                ff = response.headers["Content-Disposition"]
                for s in ff.split(";"):
                    if s.find("filename=") >= 0:
                        destination = s.split("=")[1].replace('"',"")
                if destination is None:
                    raise Exception("No file name found in file")
            elif "Content-Encoding" in response.headers:
                if response.headers["Content-Encoding"] == "gzip":
                    destination = "download.zip"

        token = self.get_confirm_token(response)

        if destination is None:
            # raise Exception("File name is None")
            print(f"{Fore.RED}*** File name is None ***{Fore.RESET}")
            return False, None

        # DEBUG: do everything, but don't download the file
        if not download:
            return False, destination

        if token:
            params = { 'id' : id, 'confirm' : token }
            response = session.get(URL, params = params, stream = True)

        self.save_response_content(response, destination)

        return True, destination

    def get_confirm_token(self, response):
        for key, value in response.cookies.items():
            if key.startswith('download_warning'):
                return value

        return None

    def save_response_content(self, response, destination):
        CHUNK_SIZE = 32768

        with open(destination, "wb") as f:
            for chunk in response.iter_content(CHUNK_SIZE):
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)
