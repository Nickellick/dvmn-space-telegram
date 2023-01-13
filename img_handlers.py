import os
from pathlib import Path

import requests
from urllib import parse


def fetch_img_content(link, params=None):
    response = requests.get(link, params)
    response.raise_for_status()

    return response.content


def save_img(img_path, img_binary):
    folder = Path(img_path).resolve().parent
    Path(folder).mkdir(parents=True, exist_ok=True)
    with open(img_path, 'wb') as img_file:
        img_file.write(img_binary)


def fetch_and_save(link, path, params=None):
    img_binary = fetch_img_content(link, params=params)
    save_img(path, img_binary)


def get_img_extension(link):
    link_decoded = parse.unquote(link)
    path = parse.urlsplit(link_decoded).path
    _, ext = os.path.splitext(path)
    return ext