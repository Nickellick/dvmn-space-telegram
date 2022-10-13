import argparse

import requests

from img_hander import fetch_and_save


def init_argparse():
    parser = argparse.ArgumentParser(
        description='SpaceX photo parser'
    )
    parser.add_argument(
        '-lid',
        '--launch_id',
        help='Launch id. Latest launch photos will be'
        'fetched if not provided',

    ),
    parser.add_argument(
        '-d',
        '--directory',
        help='defaut directory where images will be fetched',
        default='images'
    )
    return parser.parse_args()


def fetch_spacex_pictures(id_, pic_folder):
    response = requests.get(f'https://api.spacexdata.com/v5/launches/{id_}')

    response.raise_for_status()

    launch_data = response.json()
    picture_links = launch_data['links']['flickr']['original']

    for i, link in enumerate(picture_links):
        fetch_and_save(link, f'{pic_folder}/{i + 1}.jpg')


def fetch_spacex_last_launch(pic_folder):
    response = requests.get('https://api.spacexdata.com/v5/launches/latest')

    response.raise_for_status()

    id_ = response.json()['id']
    fetch_spacex_pictures(id_, pic_folder)


def main():
    args = init_argparse()
    img_directory = args.directory
    if args.launch_id:
        fetch_spacex_pictures(args.launch_id, img_directory)
    else:
        fetch_spacex_last_launch(img_directory)
