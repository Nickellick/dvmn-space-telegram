import requests
from pathlib import Path


def download_img(link):
    response = requests.get(link)
    response.raise_for_status()

    return response.content


def save_img(img_folder, img_name, img_binary):
    Path(img_folder).mkdir(parents=True, exist_ok=True)
    with open(f'{img_folder}/{img_name}', 'wb') as img_file:
        img_file.write(img_binary)


def main():
    img_binary = download_img(
        'https://upload.wikimedia.org/wikipedia/'
        'commons/3/3f/HST-SM4.jpeg'
    )
    save_img('images', 'hubble.jpeg', img_binary)


if __name__ == '__main__':
    main()
