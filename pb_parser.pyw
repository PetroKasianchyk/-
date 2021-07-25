import requests
from bs4 import BeautifulSoup
import csv
import xlrd
import pandas as pd

CSV = 'title_new.csv'
HOST = 'https://www.rbc.ua/'
URL = 'https://www.rbc.ua/ukr/'
HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0'
}


def get_html(url, params=''): #отримуємо сторінку HTML повністю за вказаним URL та params
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_content(html): #передаємо сторінку HTML для опрацювання
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='item')

    new = []

    for item in items:
        new.append(
            {
                'time_new': item.find('a').get_text(strip=True)[0:5],
                'title_new': item.find('a').get_text(strip=True)[5:len(item.find('a').get_text(strip=True))],
                'link_new': item.find('a').get('href')
            }
        )
    return new

def hyper_link_new(text, link):
    return '=HYPERLINK("%s","%s")'%(link, text)
    #return '-HYPERLINK("%s","%s")'%(text, link)


def save_new(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Час новини','Заголовок новини','Посилання на статтю'])
        for item in items:
            writer.writerow([item['time_new'], item['title_new'], item['link_new']])
            #writer.writerow([item['time_new'], hyper_link_new(item['title_new'], item['link_new'])])

def parser():
    html = get_html(URL)
    if html.status_code == 200:
        new=[]
        html = get_html(URL)
        new.extend(get_content(html.text))
        save_new(new, CSV)
        pass
    else:
       print('Сторінка недоступна.')


parser()

