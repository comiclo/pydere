#!/usr/bin/env python

import argparse
import requests
import wget
import sys
import os
from time import sleep
from bs4 import BeautifulSoup

_ACCOUNT = 'pydere'
_PASS_HASH = 'd82e8cb24669a7d323a70e0588bdf64a0792f0b4'


class pydere():

    def __init__(self):
        self.s = requests.session()
        self.login(_ACCOUNT, _PASS_HASH)

    def login(self, account, pass_hash):
        r = self.s.get("https://yande.re/user/home",
                       cookies={"login": account, "pass_hash": pass_hash})
        if "Hello " + account + "!" in r.text:
            print("Login Successful.")

    def download_thumb(self, thumb_url):
        print("\n\nDownloading...", thumb_url)
        r = self.s.get(thumb_url)
        post_urls = []
        soup = BeautifulSoup(r.text, "html.parser")
        for a_soup in soup.find_all("a", {"class": "thumb"}):
            post_url = a_soup.find_next("span").text.split()[-1]
            post_urls.append(post_url)
        for post_url in post_urls:
            while True:
                try:
                    self.download_post(post_url)
                except Exception as e:
                    print(e)
                    print("Retrying after 30 seconds...")
                    sleep(30)
                    continue
                break
        return post_urls

    def download_post(self, post_url):
        print("\nDownloading...", post_url)
        r = self.s.get(post_url)
        soup = BeautifulSoup(r.text, "html.parser")
        original_file_changed = soup.find(
            "a", {"class": "original-file-changed", "id": "highres"})
        original_file_unchanged_png = soup.find(
            "a", {"class": "original-file-unchanged", "id": "png"})
        original_file_unchanged_jpg = soup.find(
            "a", {"class": "original-file-unchanged", "id": "highres"})

        image_url = None
        if original_file_unchanged_png:
            image_url = original_file_unchanged_png.get("href")
        elif original_file_unchanged_jpg:
            image_url = original_file_unchanged_jpg.get("href")
        elif original_file_changed:
            image_url = original_file_changed.get("href")
        else:
            print("Image URL not found.")
            return

        filename = requests.utils.unquote(image_url).split("/")[-1]

        if os.path.isfile(filename):
            print(filename, "alreadly exists.")
        else:
            wget.download(image_url, out=filename)
        return image_url

    def download_tag(self, tag):
        page = 1
        while True:
            thumb_url = 'https://yande.re/post?page=' + \
                str(page) + '&tags=' + tag.replace(" ", "_").strip()
            post_urls = self.download_thumb(thumb_url)
            if not post_urls:
                break
            page += 1


def main():
    parser = argparse.ArgumentParser(description='pydere')
    parser.add_argument("-t", "--tag", type=str, nargs='+')
    args = parser.parse_args()

    tag = "_".join(args.tag)

    if tag:
        pydere().download_tag(tag)

if __name__ == '__main__':
    main()
