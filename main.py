import argparse
import os
from urllib.parse import urlparse

import requests
from dotenv import load_dotenv

BITLY_API = 'https://api-ssl.bitly.com/v4'


def check_link(url):
    response = requests.get(url)
    if not response.ok:
        raise requests.exceptions.HTTPError('Некорректная ссылка')


def shorten_link(headers, url):
    api_url = f"{BITLY_API}/shorten"
    data = {
        'long_url': url,
    }
    response = requests.post(api_url, headers=headers, json=data)
    if response.ok:    
        return response.json()['link']
    raise requests.exceptions.HTTPError("Ошибка при создании битлинка")


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
        if is_bitlink(headers, args.url):
            print(f'Переходов по ссылке: {count_clicks(headers,args.url)}')
        else:
            print('Битлинк: ', shorten_link(headers, args.url))
    except requests.exceptions.HTTPError as http_err:
        print(f'{http_err}')
    except Exception as err:
        print(f'Ошибка: {err}')


if __name__ == '__main__':
    main()
