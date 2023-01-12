import argparse
import datetime
import os

from dotenv import load_dotenv
import requests

from img_handlers import fetch_and_save
from img_handlers import get_img_extension


def init_argparse():
    parser = argparse.ArgumentParser(
        description='NASA APOD photo parser'
    )
    parser.add_argument(
        '-s',
        '--start_date',
        help='Start date (ISO format). Ignored if date (--date) provided',
    )
    parser.add_argument(
        '-e',
        '--end_date',
        help='End date (ISO format). Ignored if date (--date) provided'
        'Defaults to today',
    )
    parser.add_argument(
        '-t',
        '--date',
        help='Fetch APOD of the date (ISO format). Defaults to today'
    )
    parser.add_argument(
        '-d',
        '--directory',
        help='Defaut directory where images will be fetched',
        default='images'
    )
    return parser.parse_args()


def fetch_apod_picture(api_key, directory, date: datetime.datetime.date):
    params = {
        'api_key': api_key,
        'date': date.isoformat()
    }

    response = requests.get(
        'https://api.nasa.gov/planetary/apod',
        params=params
    )

    response.raise_for_status()

    photo_meta = response.json()
    if photo_meta['media_type'] == 'image':
        ext = get_img_extension(photo_meta['url'])
        fetch_and_save(
            photo_meta['url'],
            f'{directory}/apod_{date.isoformat()}{ext}'
            )


def fetch_apod_picture_today(api_key, directory):
    fetch_apod_picture(
        api_key,
        directory,
        datetime.datetime.today().date()
        )


def fetch_apod_pictures(api_key, directory, start_date, end_date):
    params = {
        'api_key': api_key,
        'start_date': start_date.isoformat(),
        'end_date': end_date.isoformat()
    }

    response = requests.get(
        'https://api.nasa.gov/planetary/apod',
        params=params
    )

    response.raise_for_status()

    photo_links = {}
    for apod_meta in response.json():
        if apod_meta['media_type'] == 'image':
            date = datetime.datetime.fromisoformat(apod_meta['date']).date()
            photo_links[date] = apod_meta['url']

    for date, link in photo_links.items():
        ext = get_img_extension(link)
        fetch_and_save(link, f'{directory}/apod_{date.isoformat()}{ext}')


def raise_for_minimal_date(minimal_date, date):
    if date < minimal_date:
        raise ValueError(
            f'Date earlier than minmal ({minimal_date.isoformat()})'
        )


def main():
    minimal_date = datetime.datetime.fromisoformat('1995-06-16').date()
    args = init_argparse()
    img_directory = args.directory
    load_dotenv()
    api_key = os.getenv('DVMN_NASA_API_KEY')
    if args.date:
        date = datetime.datetime.fromisoformat(args.date).date()
        raise_for_minimal_date(minimal_date, date)
        fetch_apod_picture(
            api_key,
            img_directory,
            datetime.datetime.fromisoformat(args.date).date()
        )
    elif args.start_date:
        if not args.end_date:
            end_date = datetime.datetime.today().date()
        else:
            end_date = datetime.datetime.fromisoformat(args.end_date).date()
        raise_for_minimal_date(minimal_date, end_date)
        start_date = datetime.datetime.fromisoformat(args.start_date).date()
        raise_for_minimal_date(minimal_date, start_date)
        fetch_apod_pictures(
            api_key,
            img_directory,
            start_date,
            end_date
        )
    else:
        fetch_apod_picture_today(api_key, img_directory)


if __name__ == '__main__':
    main()
