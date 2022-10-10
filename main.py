import requests


def download_img(link):
    response = requests.get(link)
    response.raise_for_status()

    return response.content


def save_img(path, img_binary):
    with open(path, 'wb') as img_file:
        img_file.write(img_binary)


def main():
    img_binary = download_img('https://upload.wikimedia.org/wikipedia/commons/3/3f/HST-SM4.jpeg')
    save_img('hubble.jpeg', img_binary)


if __name__ == '__main__':
    main()