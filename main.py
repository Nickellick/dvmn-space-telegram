import datetime
import os
from pathlib import Path

import dotenv
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


def get_apod_pictures(start_date, end_date, api_key, pic_folder='images'):
    params = {
        'api_key': api_key,
        'start_date': start_date.strftime('%Y-%m-%d'),
        'end_date': end_date.strftime('%Y-%m-%d')
    }

    response = requests.get(
        'https://api.nasa.gov/planetary/apod',
        params=params
    )

    response.raise_for_status()

    photo_links = []
    for apod_meta in response.json():
        if apod_meta['media_type'] == 'image':
            photo_links.append(apod_meta['url'])

    for i, link in enumerate(photo_links):
        ext = get_img_extension(link)
        download_and_save(link, f'{pic_folder}/apod_{i}{ext}')


def get_epic_photos(api_key, pic_folder='images'):
    params = {
        'api_key': api_key,
    }

    response = requests.get(
        'https://api.nasa.gov/EPIC/api/natural/images',
        params=params
    )

    response.raise_for_status()

    for i, photo_meta in enumerate(response.json()):
        filename = photo_meta['image']
        photo_date = datetime.datetime.fromisoformat(photo_meta['date'])
        photo_link = 'https://api.nasa.gov/EPIC/archive/natural/'
        photo_link += f'{photo_date.year}/{photo_date.month}/{photo_date.day}/'
        photo_link += f'png/{filename}.png'
        photo_link += f'?{parse.urlencode(params)}'
        download_and_save(photo_link, f'{pic_folder}/epic_{i}.png')


def main():
    dotenv.load_dotenv()
    api_key = os.getenv('APOD_API_KEY')
    get_epic_photos(api_key)


if __name__ == '__main__':
    main()
