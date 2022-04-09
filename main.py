import argparse
import os
from urllib.parse import urlparse

import requests
from dotenv import load_dotenv

BITLY_API = 'https://api-ssl.bitly.com/v4'


def check_link(url):
    response = requests.get(url)
    response.raise_for_status()


def shorten_link(headers, url):
    api_url = f"{BITLY_API}/shorten"
    data = {
        'long_url': url,
    }
    response = requests.post(api_url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()['link']


def count_clicks(headers, bitlink):
    url = urlparse(bitlink)
    api_url = f'{BITLY_API}/bitlinks/{url.netloc}{url.path}/clicks/summary'
    response = requests.get(api_url, headers=headers)
    response.raise_for_status()
    return response.json()['total_clicks']


def is_bitlink(headers, url):
    url_parsed = urlparse(url)
    api_url = f'{BITLY_API}/bitlinks/{url_parsed.netloc}{url_parsed.path}'
    response = requests.get(api_url, headers=headers)
    return response.ok


def main():
    load_dotenv()
    headers = {
        'Authorization': f"Bearer {os.environ['BITLY_TOKEN']}",
    }
    parser = argparse.ArgumentParser()
    parser.add_argument('url')
    args = parser.parse_args()
    try:
        check_link(args.url)
    except:
        print('Введена некорректная ссылка')
        exit()

    if is_bitlink(headers, args.url):
        print(f'По вашей ссылке прошли: {count_clicks(headers, args.url)} раз(а)')
    else:
        try:
            print('Битлинк: ', shorten_link(headers, args.url))
        except requests.exceptions.HTTPError as err:
            print(f'Ошибка при создании битлинка:\n{err}')


if __name__ == '__main__':
    main()
