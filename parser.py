import requests
from bs4 import BeautifulSoup
import csv

URL = 'http://bashorg.org/byrating/'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36', 'accept': '*/*'}
FILE = 'quotes.csv'

def get_server_response(url):
    req = requests.get(url, headers=HEADERS, params=None)
    return req

def get_page_num(response):
    soup = BeautifulSoup(response, 'html.parser')
    pages = soup.find('div', class_='navigation').get_text().split()
    page_nums = [int(num) for num in pages if num.isdigit()]
    page_max_num = max(page_nums)
    return page_max_num


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.findAll('div', class_='q')
    quotes = []
    for item in items:
        quotes.append({
            'quote-num': item.find('div', class_='vote').get_text(strip=True).split('|')[0],
            'quote-date': item.find('div', class_='vote').get_text(strip=True).split('|')[1],
            'quote-text': item.find('div', class_='quote').get_text(strip=True),
            'quote-rate': item.find('div', class_='vote').find_next('span').get_text()
        })
    return quotes

def save_file(items, path):
    with open(path, 'w', newline='', errors='replace') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Цитата №', 'Дата', 'Цитата', 'Рейтинг'])
        for item in items:
            writer.writerow([item['quote-num'], item['quote-date'], item['quote-text'], item['quote-rate']])


def main():
    response = get_server_response(URL)
    if response.status_code == 200:
        quotes = []
        pages_count = get_page_num(response.text)
        for page in range(1, pages_count + 1):
            print(f'Парсинг страницы {page} из {pages_count}...')
            URL_Next = URL + 'page/' + str(page)
            response = get_server_response(URL_Next)
            quotes.extend(get_content(response.text))
        save_file(quotes, FILE)


    else:
        print('Бэшорг послал в жопу')

main()
