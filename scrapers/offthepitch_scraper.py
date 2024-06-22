import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta


def is_published_yesterday(publication_date):
    try:
        # Convert the publication date to a datetime object
        pub_date = datetime.strptime(publication_date, "%d %B %Y - %I:%M %p")
        yesterday = datetime.today() - timedelta(days=1)
        return pub_date.date() == yesterday.date()
    except ValueError as e:
        print(f"Date parsing error: {e}")
        return False


def clean_text(text):
    # Remove unwanted characters and strip leading/trailing whitespace
    return text.replace('\xa0', ' ').replace('\n', ' ').strip()


def extract_article_details_otp(article_url):
    response = requests.get(article_url)
    article_soup = BeautifulSoup(response.content, 'html.parser')

    # Extract the publication date
    date_tag = article_soup.find('p', class_='article-blocks-hero__created')
    publication_date = clean_text(date_tag.get_text(strip=True)) if date_tag else ''

    # Extract the subhead
    subhead_tag = article_soup.find('div', class_='article-blocks-text__body')
    subhead = ''
    if subhead_tag:
        for p in subhead_tag.find_all('p'):
            subhead += p.get_text(strip=True) + ' '

    subhead = clean_text(subhead.strip())

    # Extract the image URL
    image_tag = article_soup.find('img', loading='eager')
    image_url = 'https://offthepitch.com' + image_tag['src'] if image_tag else None

    return publication_date, subhead, image_url


def scrape_offthepitch():
    url = 'https://offthepitch.com/articles'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    articles = []

    # Scrape articles from teaser-card-hero-wrapper
    for teaser in soup.find_all('a', class_='teaser-card-hero-wrapper'):
        link = 'https://offthepitch.com' + teaser['href']
        title_tag = teaser.find('span', property='schema:name')

        if title_tag:
            title = clean_text(title_tag.get_text(strip=True))
            publication_date, subhead, image_url = extract_article_details_otp(link)

            if publication_date and is_published_yesterday(publication_date):
                articles.append({
                    'title': title,
                    'link': link,
                    'publication_date': publication_date,
                    'subhead': subhead,
                    'image_url': image_url
                })

    # Scrape articles from reference-card-wrapper
    for reference in soup.find_all('a', class_='reference-card-wrapper'):
        link = 'https://offthepitch.com' + reference['href']
        title_tag = reference.find('span', property='schema:name')
        date_tag = reference.find('time', class_='reference-card__date')

        if title_tag and date_tag:
            title = clean_text(title_tag.get_text(strip=True))
            publication_date = clean_text(date_tag.get_text(strip=True))

            if is_published_yesterday(publication_date):
                _, subhead, image_url = extract_article_details_otp(link)
                articles.append({
                    'title': title,
                    'link': link,
                    'publication_date': publication_date,
                    'subhead': subhead,
                    'image_url': image_url,
                    'publication': 'Off The Pitch'
                })

    return articles
