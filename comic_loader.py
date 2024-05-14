import requests
import random
import os
import telegram
from dotenv import load_dotenv


def download_comic(filename, png_url):
    response = requests.get(png_url)
    response.raise_for_status()
    with open(filename, 'wb') as file:
        file.write(response.content)
    

def get_comic_number():
    url = 'https://xkcd.com/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    comic_info = response.json()
    number = comic_info['num']
    return number

def save_comic(random_comic):
    url = f'https://xkcd.com/{random_comic}/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    comic_info = response.json()
    png_url = comic_info['img']
    alt = comic_info['alt']
    title = comic_info['title']
    return png_url, alt, title 

def upload_file(bot_api_key, chat_id, title, alt):
    filename = f'{title}.png'
    bot = telegram.Bot(token=bot_api_key)
    with open(filename, 'rb') as file:
        bot.send_photo(chat_id=chat_id, photo=file, caption=alt)
    return filename



def main():
    load_dotenv()
    bot_api_key = os.environ['TG_BOT_API']
    chat_id = os.environ['TG_CHAT_ID']
    try:
        random_comic = random.randint(1, get_comic_number())
        png_url, alt, title = save_comic(random_comic)
        download_comic(f'{title}.png', png_url)
        filename = upload_file(bot_api_key, chat_id, title, alt)
    finally:
        os.remove(filename)


if __name__ == '__main__':
    main()
