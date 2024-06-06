import csv
import json
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

url1 = 'https://news.ycombinator.com'
baseUrl = 'https://tengrinews.kz/news/'
news_data = []


def get_headlines_from_page(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')
    headlines = soup.find_all('span', class_='content_main_item_title')

    page_data = []
    for headline in headlines:
        title = headline.text.strip()
        relative_link = headline.find('a')['href']
        absolute_link = urljoin(baseUrl, relative_link)
        page_data.append({
            'Headline': title,
            'URL': absolute_link
        })
    return page_data


allNews = []
page_number = 1

while True:
    pageUrl = f"{baseUrl}page/{page_number}/"

    try:
        pageData = get_headlines_from_page(pageUrl)

        # if not page_number
        if page_number > 100:
            break
        allNews.extend(pageData)

        page_number += 1

    except Exception as e:
        print('Error' + e)

with open('tengrinews.json', 'w', encoding='utf-8') as file:
    json.dump(allNews, file, ensure_ascii=False, indent=4)
