import requests
from bs4 import BeautifulSoup
import json


base_url = 'http://quotes.toscrape.com'


def get_page_content(url):
    response = requests.get(url)
    return BeautifulSoup(response.text, 'html.parser')


def get_author_info(url):
    soup = get_page_content(url)
    info = soup.find('div', class_='author-details')
    fullname = info.find('h3', class_='author-title').text.strip()
    born_date = info.find('span', class_='author-born-date').text.strip()
    born_location = info.find('span', class_='author-born-location').text.strip()
    description = info.find('div', class_='author-description').text.strip()
    return {
        'fullname': fullname,
        'born_date': born_date,
        'born_location': born_location,
        'description': description
    }


def get_quotes_and_authors(base_url):
    authors = {}
    quotes = []
    next_page = True
    page_number = 1

    while next_page:
        url = f'{base_url}/page/{page_number}/'
        soup = get_page_content(url)
        quote_blocks = soup.find_all('div', class_='quote')

        if not quote_blocks:
            next_page = False
            break

        for block in quote_blocks:
            quote = block.find('span', class_='text').text.strip()
            author_name = block.find('small', class_='author').text.strip()
            author_link = block.find('a')['href']
            tags = block.find('div', class_='tags').find_all('a', class_='tag')
            tag_list = [tag.text.strip() for tag in tags]

            if author_link not in authors:
                author_url = f'{base_url}{author_link}'
                authors[author_link] = get_author_info(author_url)

            quotes.append({
                'tags': tag_list,
                'author': author_name,
                'quote': quote
                
            })

        page_number += 1

    return quotes, authors

if __name__ == '__main__':
    quotes, authors = get_quotes_and_authors(base_url)


    with open('files/qoutes.json', 'w', encoding='utf-8') as f:
        json.dump(quotes, f, ensure_ascii=False, indent=4)

    with open('files/authors.json', 'w', encoding='utf-8') as f:
        json.dump(list(authors.values()), f, ensure_ascii=False, indent=4)