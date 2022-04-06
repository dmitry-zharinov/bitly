import os
import requests
from dotenv import load_dotenv
from pprint import pprint
from urllib.parse import urlparse


def get_token():
    return os.environ['BITLY_TOKEN']


def get_bitly_profile(token):
    api_url = "https://api-ssl.bitly.com/v4/user"
    headers = {
        'Authorization': f"Bearer {token}",
        'Content-Type': 'application/json',
    }
    #data = '{ "long_url": "https://dev.bitly.com", "domain": "bit.ly", "group_guid": "Ba1bc23dE4F" }'
    #response = requests.post('https://api-ssl.bitly.com/v4/shorten', headers=headers, data=data)
    response = requests.get(api_url, headers=headers)
    response.raise_for_status()
    return response.text


def shorten_link(token, url):
    api_url = "https://api-ssl.bitly.com/v4/shorten"
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
    bitlink_parsed = urlparse(bitlink)
    
    api_url = f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink_parsed.netloc}{bitlink_parsed.path}/clicks/summary'
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
    api_url = f'https://api-ssl.bitly.com/v4/bitlinks/{url_parsed.netloc}{url_parsed.path}'
    headers = {
        'Authorization': f"Bearer {token}",
        'Content-Type': 'application/json',
    }
    response = requests.get(api_url, headers=headers)
    return response.ok


def main():
    load_dotenv()
    #url = 'https://dvmn.org'
    #url = input('Введите url для сокращения: ')

    token = get_token()
    try:
        #bitlink = shorten_link(token, url)
        #print('Битлинк', bitlink)
        clicks_count = count_clicks(token, 'https://bit.ly/3JcgkHq')
        print(clicks_count)
    except requests.exceptions.HTTPError as err:
        print(f'Ошибка при создании битлинка:\n{err}')


if __name__ == '__main__':
    main()
    
    
