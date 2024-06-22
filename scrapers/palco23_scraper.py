import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta


def is_published_yesterday(publication_date):
    try:
        # Convert the publication date to a datetime object
        pub_date = datetime.strptime(publication_date, "%d %b %Y - %H:%M")
        yesterday = datetime.today() - timedelta(days=1)
        return pub_date.date() == yesterday.date()
    except ValueError as e:
        print(f"Date parsing error: {e}")
        return False


def clean_text(text):
    # Remove unwanted characters and strip leading/trailing whitespace
    return text.replace('\xa0', ' ').replace('\n', ' ').strip()


def extract_article_details_p23(article_url):
    response = requests.get(article_url)
    article_soup = BeautifulSoup(response.content, 'html.parser')

    # Extract the subhead as the main content
    content_tag = article_soup.find('div', class_='news_detail_content_text detail_text')
    content = ''
    if content_tag:
        for p in content_tag.find_all('p'):
            content += p.get_text(strip=True) + ' '

    content = clean_text(content.strip())

    # Extract the image URL
    image_tag = article_soup.find('img', class_='image')
    image_url = 'https://www.palco23.com' + image_tag['src'] if image_tag else None

    return content, image_url


def scrape_palco23():
    url = 'https://www.palco23.com/'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    articles = []
    for link_tag in soup.find_all('a', class_='title'):
        title_tag = link_tag.find('h2')
        info_tag = link_tag.find_next('div', class_='info')
        date_tag = info_tag.find('p', class_='date') if info_tag else None

        if title_tag and date_tag:
            title = title_tag.get_text(strip=True)
            link = 'https://www.palco23.com' + link_tag['href']
            publication_date = date_tag.get_text(strip=True)

            if is_published_yesterday(publication_date):
                content, image_url = extract_article_details_p23(link)
                articles.append({
                    'title': title,
                    'link': link,
                    'publication_date': publication_date,
                    'subhead': content,
                    'image_url': image_url,
                    'publication': 'Palco23'
                })

    return articles
