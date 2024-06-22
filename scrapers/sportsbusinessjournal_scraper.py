import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta


def is_published_yesterday(publication_date):
    try:
        pub_date = datetime.strptime(publication_date, "%m.%d.%Y")
        yesterday = datetime.today() - timedelta(days=1)
        return pub_date.date() == yesterday.date()
    except ValueError as e:
        print(f"Date parsing error: {e}")
        return False


def clean_text(text):
    return text.replace('\xa0', ' ').replace('\n', ' ').strip()


def extract_article_details_sbj(article_url):
    response = requests.get('https://www.sportsbusinessjournal.com' + article_url)
    article_soup = BeautifulSoup(response.content, 'html.parser')

    # Extract the publication date
    date_tag = article_soup.find('time', itemprop='datePublished')
    publication_date = clean_text(date_tag.get_text(strip=True)) if date_tag else ''

    # Extract the article content
    content_wrap = article_soup.find('div', id='content-wrap')
    content = ''
    if content_wrap:
        for element in content_wrap.find_all_next(string=True, limit=20):
            if element.parent.name == 'style':
                break
            content += element.strip() + ' '
    content = clean_text(content.strip())

    # Extract the image URL
    image_tag = article_soup.find('div', class_='img fullWidth').find('img') if article_soup.find('div',
                                                                                                  class_='img fullWidth') else None
    image_url = image_tag['src'] if image_tag else None

    return publication_date, content, image_url


def scrape_sportsbusinessjournal():
    url = 'https://www.sportsbusinessjournal.com/Daily.aspx'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    articles = []

    for tag in soup.find_all(['h2', 'h3']):
        link_tag = tag.find('a')

        if link_tag:
            title = clean_text(link_tag.get_text(strip=True))
            link = link_tag['href']
            publication_date, content, image_url = extract_article_details_sbj(link)

            if publication_date and is_published_yesterday(publication_date):
                articles.append({
                    'title': title,
                    'link': 'https://www.sportsbusinessjournal.com' + link,
                    'publication_date': publication_date,
                    'subhead': content,
                    'image_url': image_url,
                    'publication': 'SportsBusinessJournal'
                })

    return articles
