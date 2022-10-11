import os
from pathlib import Path

import requests
from urllib import parse

def download_img(link):
    response = requests.get(link)
    response.raise_for_status()

    return response.content


def save_img(img_path, img_binary):
    folder = Path(img_path).resolve().parent
    Path(folder).mkdir(parents=True, exist_ok=True)
    with open(img_path, 'wb') as img_file:
        img_file.write(img_binary)


def download_and_save(link, path):
    img_binary = download_img(link)
    save_img(path, img_binary)


def download_spacex_pictures(id_, pic_folder):
    response = requests.get(f'https://api.spacexdata.com/v5/launches/{id_}')

    response.raise_for_status()

    launch_data = response.json()
    picture_links = launch_data['links']['flickr']['original']

    for i, link in enumerate(picture_links):
        download_and_save(link, f'{pic_folder}/{i + 1}.jpg')


def fetch_spacex_last_launch(pic_folder):
    response = requests.get('https://api.spacexdata.com/v5/launches/latest')

    response.raise_for_status()

    id_ = response.json()['id']

    download_spacex_pictures(id_, pic_folder)


def get_img_extension(link):
    link_decoded = parse.unquote(link)
    path = parse.urlsplit(link_decoded).path
    _, ext = os.path.splitext(path)
    return ext


def main():
    print(get_img_extension('https://apod.nasa.gov/apod/image/2210/Pelican_Almeida_2000.png'))


if __name__ == '__main__':
    main()
