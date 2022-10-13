import requests

def fetch_img_content(link):
    response = requests.get(link)
    response.raise_for_status()

    return response.content


def save_img(img_path, img_binary):
    folder = Path(img_path).resolve().parent
    Path(folder).mkdir(parents=True, exist_ok=True)
    with open(img_path, 'wb') as img_file:
        img_file.write(img_binary)


def fetch_and_save(link, path):
    img_binary = fetch_img_content(link)
    save_img(path, img_binary)