import argparse
import datetime
import os

from dotenv import load_dotenv
import requests
from urllib import parse

from img_handlers import fetch_and_save


def init_argparse():
    parser = argparse.ArgumentParser(
        description='NASA EPIC photo parser'
    )
    parser.add_argument(
        '-a',
        '--all',
        action='store_true',
        help='Fetch all last available photos. Fetch only last if not provided'
    )
    parser.add_argument(
        '-d',
        '--directory',
        help='Defaut directory where images will be fetched',
        default='images'
    )
    return parser.parse_args()


def fetch_all_epic_links(api_key):
    params = {
        'api_key': api_key,
    }

    response = requests.get(
        'https://api.nasa.gov/EPIC/api/natural/images',
        params=params
    )

    response.raise_for_status()

    return response.json()


def fetch_all_epic_photos(api_key, directory):
    params = {
        'api_key': api_key
    }
    for photo_meta in fetch_all_epic_links(api_key):
        photo_link = create_photo_link(photo_meta)
        fetch_and_save(
            photo_link,
            f'{directory}/epic_{photo_meta["date"]}.png',
            params=params
        )


def fetch_latest_epic_photo(api_key, directory):
    params = {
        'api_key': api_key
    }
    photo_meta = fetch_all_epic_links(api_key)[-1]
    photo_link = create_photo_link(photo_meta)
    fetch_and_save(
        photo_link,
        f'{directory}/epic_{photo_meta["date"]}.png',
        params=params
    )


def create_photo_link(photo_meta):
    filename = photo_meta['image']
    photo_date = datetime.datetime.fromisoformat(photo_meta['date']).date()
    date_formatted = photo_date.strftime('%Y/%m/%d')
    photo_link = ('https://api.nasa.gov/EPIC/archive/natural/'
                  f'{date_formatted}/png/{filename}.png')
    return photo_link


def main():
    load_dotenv()
    api_key = os.getenv('DVMN_NASA_API_KEY')
    args = init_argparse()
    if args.all:
        fetch_all_epic_photos(api_key, args.directory)
    else:
        fetch_latest_epic_photo(api_key, args.directory)


if __name__ == '__main__':
    main()
