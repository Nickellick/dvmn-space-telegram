from pty import slave_open
import requests
from pathlib import Path


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


def main():
    img_binary = download_and_save(
        'https://upload.wikimedia.org/wikipedia/'
        'commons/3/3f/HST-SM4.jpeg',
        'images/hubble.jpeg'
    )


if __name__ == '__main__':
    main()
