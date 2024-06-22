import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta


def is_published_yesterday(publication_date):
    try:
        pub_date = datetime.strptime(publication_date, "%B %d, %Y")
        yesterday = datetime.today() - timedelta(days=1)
        return pub_date.date() == yesterday.date()
    except ValueError as e:
        print(f"Date parsing error: {e}")
        return False


def clean_text(text):
    # Remove unwanted characters and strip leading/trailing whitespace
    return text.replace('\xa0', ' ').replace('\n', ' ').strip()


def extract_article_details_sb(article_url):
    response = requests.get(article_url)
    article_soup = BeautifulSoup(response.content, 'html.parser')

    # Extract the publication date
    date_tag = article_soup.find('div', class_='sb-article-info__date').find('time')
    publication_date = clean_text(date_tag.get_text(strip=True)) if date_tag else ''

    # Extract the article content
    content = ''
    content_tag = article_soup.find('div', class_='sb-article-main')
    if content_tag:
        for p in content_tag.find_all('p'):
            content += p.get_text(strip=True) + ' '

    content = clean_text(content.strip())

    # Extract the image URL
    image_tag = article_soup.find('div', class_='sb-article-hero').find('img')
    image_url = image_tag['src'] if image_tag else None

    return publication_date, content, image_url


def scrape_sportbusiness():
    url = 'https://www.sportbusiness.com/'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    articles = []

    # Scrape large post articles
    for text_container in soup.find_all('div', class_='sb-custom-blocks-post-large__text'):
        title_tag = text_container.find('div', class_='sb-custom-blocks-post-large__title')
        link_tag = title_tag.find('a') if title_tag else None

        if link_tag:
            title = clean_text(link_tag.get_text(strip=True))
            link = link_tag['href']
            publication_date, content, image_url = extract_article_details_sb(link)

            if publication_date: # and is_published_yesterday(publication_date):
                articles.append({
                    'title': title,
                    'link': link,
                    'publication_date': publication_date,
                    'content': content,
                    'image_url': image_url
                })

    # Scrape image post articles
    for header_container in soup.find_all('div', class_='sb-custom-blocks-post-image__header'):
        link_tag = header_container.find('a')

        if link_tag:
            title = clean_text(link_tag.get_text(strip=True))
            link = link_tag['href']
            publication_date, content, image_url = extract_article_details_sb(link)

            if publication_date: # and is_published_yesterday(publication_date):
                articles.append({
                    'title': title,
                    'link': link,
                    'publication_date': publication_date,
                    'content': content,
                    'image_url': image_url
                })

    # Scrape small post articles
    for title_container in soup.find_all('div', class_='sb-custom-blocks-post-small__title'):
        link_tag = title_container.find('a')

        if link_tag:
            title = clean_text(link_tag.get_text(strip=True))
            link = link_tag['href']
            publication_date, content, image_url = extract_article_details_sb(link)

            if publication_date and is_published_yesterday(publication_date):
                articles.append({
                    'title': title,
                    'link': link,
                    'publication_date': publication_date,
                    'subhead': content,
                    'image_url': image_url,
                    'publication': 'SportsBusiness'
                })

    return articles
