import os
import requests
from dotenv import load_dotenv
from urllib.parse import urlparse

BITLY_API = 'https://api-ssl.bitly.com/v4'


def get_token():
    return os.environ['BITLY_TOKEN']


def shorten_link(token, url):
    api_url = f"{BITLY_API}/shorten"
    headers = {
        'Authorization': f"Bearer {token}",
        'Content-Type': 'application/json',
    }
    data = {
        'long_url': url,
    }
    response = requests.post(api_url, headers=headers, json=data)
    response.raise_for_status()
    bitlink = response.json()['link']
    return bitlink


def count_clicks(token, bitlink):
    url = urlparse(bitlink)
    api_url = f'{BITLY_API}/bitlinks/{url.netloc}{url.path}/clicks/summary'
    headers = {
        'Authorization': f"Bearer {token}",
        'Content-Type': 'application/json',
    }
    response = requests.get(api_url, headers=headers)
    response.raise_for_status()
    count_clicks = response.json()['total_clicks']
    return count_clicks


def is_bitlink(token, url):
    url_parsed = urlparse(url)
    api_url = f'{BITLY_API}/bitlinks/{url_parsed.netloc}{url_parsed.path}'
    headers = {
        'Authorization': f"Bearer {token}",
        'Content-Type': 'application/json',
    }
    response = requests.get(api_url, headers=headers)
    return response.ok


def main():
    load_dotenv()
    token = get_token()
    url = input('Введите ссылку: ')
    if is_bitlink(token, url):
        print(f'По вашей ссылке прошли: {count_clicks(token, url)} раз(а)')
    else:
        try:
            print('Битлинк: ', shorten_link(token, url))
        except requests.exceptions.HTTPError as err:
            print(f'Ошибка при создании битлинка:\n{err}')


if __name__ == '__main__':
    main()
