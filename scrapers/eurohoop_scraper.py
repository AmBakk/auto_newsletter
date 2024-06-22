import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta


def is_published_today_eh(publication_date):
    try:
        # Convert the publication date to a datetime object
        pub_date = datetime.strptime(publication_date, "%d/%b/%y %H:%M")
        yesterday = datetime.today() - timedelta(days=0)
        return pub_date.date() == yesterday.date()
    except ValueError as e:
        print(f"Date parsing error: {e}")
        return False


def clean_text(text):
    return ' '.join(text.split())


def scrape_eurohoops():
    articles = []

    for page in range(1, 3):  # Assuming we are scraping the first two pages
        url = f'https://www.eurohoops.net/latest-news/page/{page}/?lang=en'
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Scrape articles
        for article in soup.find_all('article', class_='looped'):
            link_tag = article.find('a', href=True)
            title_tag = article.find('h2', class_='post-loop__title')
            date_tag = article.find('span', class_='post-loop__date')

            if link_tag and title_tag and date_tag:
                link = link_tag['href']
                title = clean_text(title_tag.get_text(strip=True))
                publication_date = clean_text(date_tag.get_text(strip=True))

                if is_published_today_eh(publication_date):
                    # Access the article's page to get the subhead and image
                    article_response = requests.get(link)
                    article_soup = BeautifulSoup(article_response.content, 'html.parser')
                    subhead_tag = article_soup.find('div', class_='single__content')
                    image_tag = article_soup.find('figure', class_='single__image').find('img')

                    if subhead_tag and image_tag:
                        subhead = clean_text(subhead_tag.get_text(strip=True))
                        image_url = image_tag['src']

                        articles.append({
                            'title': title,
                            'link': link,
                            'publication_date': publication_date,
                            'subhead': subhead,
                            'image_url': image_url,
                            'publication': 'Eurohoop'
                        })

    return articles
