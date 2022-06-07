import requests
from bs4 import BeautifulSoup
import csv

URL = 'http://bashorg.org/byrating/'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36', 'accept': '*/*'}
FILE = 'quotes.csv'

def get_html(url):
    req = requests.get(url, headers=HEADERS, params=None)
    #print(req)
    return req

def get_page_num(html):
    soup = BeautifulSoup(html, 'html.parser')
    pages = soup.find('div', class_='navigation').get_text().split()
    page_nums = [int(num) for num in pages if num.isdigit()]
    page_max_num = max(page_nums)
    #print(page_max_num)
    return page_max_num


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.findAll('div', class_='q')
    #print(items)
    quotes = []
    for item in items:
        quotes.append({
            'quote-num': item.find('div', class_='vote').get_text(strip=True).split('|')[1],
            'quote-date': item.find('div', class_='vote').get_text(strip=True).split('|')[2],
            'quote-text': item.find('div', class_='quote').get_text(strip=True),
            'quote-rate': item.find('div', class_='vote').find_next('span').get_text()
        })
    return quotes

def save_file(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Цитата №', 'Дата', 'Цитата', 'Рейтинг'])
        for item in items:
            writer.writerow([item['quote-num'], item['quote-date'], item['quote-text'], item['quote-rate']])


def parse():
    html = get_html(URL)
    #print(html)
    if html.status_code == 200:
        quotes = []
        pages_count = get_page_num(html.text)
        #print(pages_count)
        for page in range(1, pages_count + 1):
            print(f'Парсинг страницы {page} из {pages_count}...')
            URL_Next = URL + 'page/' + str(page)
            #print(URL_Next)
            html = get_html(URL_Next)
            #print(html)
            quotes.extend(get_content(html.text))
        save_file(quotes, FILE)


    else:
        print('Бэшорг послал в жопу')

parse()
