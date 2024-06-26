import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

month_mapping = {
    "enero": "January",
    "febrero": "February",
    "marzo": "March",
    "abril": "April",
    "mayo": "May",
    "junio": "June",
    "julio": "July",
    "agosto": "August",
    "septiembre": "September",
    "octubre": "October",
    "noviembre": "November",
    "diciembre": "December"
}


def is_published_yesterday(publication_date):
    try:
        # Replace Spanish month names with English month names
        for spanish, english in month_mapping.items():
            publication_date = publication_date.replace(spanish, english)
        # Convert the publication date to a datetime object
        pub_date = datetime.strptime(publication_date, "%d de %B de %Y")
        yesterday = datetime.today() - timedelta(days=0)
        return pub_date.date() == yesterday.date()
    except ValueError as e:
        print(f"Date parsing error: {e}")
        return False


def clean_text(text):
    # Remove unwanted characters and strip leading/trailing whitespace
    return text.replace('\xa0', ' ').replace('\n', ' ').strip()


def extract_article_details_2pb(article_url):
    response = requests.get(article_url)
    article_soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract the publication date
    date_tag = article_soup.find('time', class_='c-mainarticle__time')
    publication_date = clean_text(date_tag.get_text(strip=True)) if date_tag else ''
    
    # Extract the subhead
    subhead = ''
    subhead_tag = article_soup.find('div', class_='c-mainarticle__body')
    if subhead_tag:
        for element in subhead_tag.find_all(['p', 'h2', 'h3'], recursive=False):
            if element.name == 'hr' or "Sobre 2Playbook Intelligence" in element.get_text():
                break
            subhead += element.get_text(strip=True) + ' '
    
    subhead = clean_text(subhead.strip())

    # Extract the image URL
    image_tag = article_soup.find('img', class_='c-mainarticle__img')
    image_url = image_tag['data-src'] if image_tag else ''

    return publication_date, subhead, image_url


def scrape_2playbook():
    url = 'https://www.2playbook.com/'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    articles = []

    # Find all relevant article tags
    article_tags = soup.find_all('h2', class_=['c-articles__title', 'c-articles__title--arrow-up', 'c-articles__title-main-2'])
    
    for article_tag in article_tags:
        link_tag = article_tag.find('a', class_='c-articles__title-link')
        if link_tag:
            link = link_tag['href']
            title = clean_text(link_tag.get_text(strip=True))
            publication_date, subhead, image_url = extract_article_details_2pb(link)
            if publication_date and is_published_yesterday(publication_date):
                articles.append({
                    'title': title,
                    'link': link,
                    'publication_date': publication_date,
                    'subhead': subhead,
                    'image_url': image_url,
                    'publication': '2playbook'
                })

    return articles
