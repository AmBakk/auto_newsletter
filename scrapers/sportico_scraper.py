import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import re


def is_published_yesterday_sco(publication_date):
    try:
        if 'hours ago' in publication_date:
            hours_ago = int(re.search(r'(\d+) hours ago', publication_date).group(1))
            pub_date = datetime.now() - timedelta(hours=hours_ago)
        elif 'hour ago' in publication_date:
            pub_date = datetime.now() - timedelta(hours=1)
        elif 'mins ago' in publication_date:
            pub_date = datetime.now() - timedelta(minutes=30)
        else:
            pub_date = datetime.strptime(publication_date, "%b %d, %Y %I:%M %p")

        yesterday = datetime.today() - timedelta(days=0)
        return pub_date.date() == yesterday.date()
    except ValueError as e:
        print(f"Date parsing error: {e}")
        return False


def clean_text(text):
    # Remove unwanted characters and strip leading/trailing whitespace
    return text.replace('\xa0', ' ').replace('\n', ' ').strip()


def extract_article_details(article_url):
    response = requests.get(article_url)
    article_soup = BeautifulSoup(response.content, 'html.parser')

    # Extract the article content
    content_tag = article_soup.find('div',
                                    class_='a-content a-content--left-space lrv-a-floated-parent lrv-u-font-family-body lrv-u-line-height-large lrv-u-font-size-18 u-color-black-16')
    content = ''
    if content_tag:
        for p in content_tag.find_all('p'):
            content += p.get_text(strip=True) + ' '

    content = clean_text(content.strip())

    # Extract the image URL
    image_tag = article_soup.find('img', class_='c-lazy-image__img')
    image_url = image_tag['src'] if image_tag else None

    # Check for different class or fallback options if image not found
    if not image_url:
        image_tag = article_soup.find('img', {'srcset': True})
        image_url = image_tag['src'] if image_tag else None

    return content, image_url


def scrape_sportico():
    url = 'https://www.sportico.com/'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    articles = []
    for title_tag in soup.find_all('h3', class_='c-title'):
        link_tag = title_tag.find('a', class_='c-title__link')
        byline_tag = title_tag.find_next('ul', class_='o-article-byline')
        date_tag = byline_tag.find('time') if byline_tag else None

        if link_tag and date_tag:
            title = clean_text(link_tag.get_text(strip=True))
            link = link_tag['href']
            publication_date = date_tag.get_text(strip=True)

            if is_published_yesterday_sco(publication_date):
                content, image_url = extract_article_details(link)
                articles.append({
                    'title': title,
                    'link': link,
                    'publication_date': publication_date,
                    'subhead': content,
                    'image_url': image_url,
                    'publication': 'Sportico'
                })

    return articles
