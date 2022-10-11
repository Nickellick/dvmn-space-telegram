from pathlib import Path

import requests


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


def download_spacex_pictures(id, pic_folder):
    response = requests.get(f'https://api.spacexdata.com/v5/launches/{id}')

    response.raise_for_status()

    launch_data = response.json()
    picture_links = launch_data['links']['flickr']['original']

    for i, link in enumerate(picture_links):
        download_and_save(link, f'{pic_folder}/{i + 1}.jpg')


def main():
    download_spacex_pictures('60e3bf0d73359e1e20335c37', 'images')


if __name__ == '__main__':
    main()
