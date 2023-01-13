import argparse
import os
import random
import time

from dotenv import load_dotenv
from PIL import Image
import telegram


def init_argparse():
    parser = argparse.ArgumentParser(
        description='NASA/SpaceX Photos Uploader Telegram Bot'
    )
    parser.add_argument(
        '-p',
        '--period',
        type=float,
        help='Period between uploading photos (in hours). Supports float',
        default=4
    )
    parser.add_argument(
        '-d',
        '--directory',
        help='Defaut image uploading directory',
        default='images'
    )
    return parser.parse_args()


def get_img_paths(path):
    all_image_paths = []
    for walkstop in os.walk(path):
        parent_paths, _, image_names = walkstop
        img_paths = map(lambda x: os.path.join(parent_paths, x), image_names)
        for img_path in img_paths:
            all_image_paths.append(img_path)
    return all_image_paths


def compress_big_images(image_paths):
    for image_path in image_paths:
        image_size = os.path.getsize(image_path)
        # Check is size more than 20 MB
        while image_size >= 20 * 1024 * 1024:
            compress_image(image_path)
            image_size = os.path.getsize(image_path)


def compress_image(image_path):
    resize_coeff = 0.75
    image = Image.open(image_path)
    width, height = image.size
    rs_width, rs_height = resize_coeff * width, resize_coeff * height
    image.resize((rs_width, rs_height))
    image.save(image_path, optimize=True)


def main():
    load_dotenv()
    api_key = os.getenv('DVMN_TG_BOT_API_KEY')
    chat_id = os.getenv('DVMN_TG_BOT_CHAT_ID')
    args = init_argparse()
    compress_big_images(get_img_paths(args.directory))
    images_to_publish = []
    bot = telegram.Bot(token=api_key)
    while True:
        if not images_to_publish:
            images_to_publish = get_img_paths(args.directory)
            random.shuffle(images_to_publish)
        for image in images_to_publish.copy():
            with open(image, 'rb') as photo_file:
                bot.send_photo(
                    chat_id=chat_id,
                    photo=photo_file
                )
            images_to_publish.remove(image)
        time.sleep(60 * 60 * args.period)


if __name__ == '__main__':
    main()
