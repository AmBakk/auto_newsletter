
from scrapers.playbook_scraper import *
from scrapers.eurohoop_scraper import *
from scrapers.offthepitch_scraper import *
from scrapers.palco23_scraper import *
from scrapers.sportico_scraper import *
from scrapers.sportsbusiness_scraper import *
from scrapers.sportsbusinessjournal_scraper import *
from utils.api_calls import *
from utils.build_nl import *
from utils.send_email import *

relevant_articles = []

playbook_articles = []
playbook_articles = scrape_2playbook()

eurohoop_articles = []
eurohoop_articles = scrape_eurohoops()

offthepitch_articles = []
offthepitch_articles = scrape_offthepitch()

palco23_articles = []
palco23_articles = scrape_palco23()

sportico_articles = []
sportico_articles = scrape_sportico()

sportsbusiness_articles = []
sportsbusiness_articles = scrape_sportbusiness()

# sportsbusinessjournal_articles = []
# sportsbusinessjournal_articles = scrape_sportsbusinessjournal()

all_articles = [playbook_articles, eurohoop_articles, offthepitch_articles, palco23_articles, sportico_articles]


for pub in all_articles:
    for article in pub:
        relevance, summary = assess_relevance(article)
        if relevance == 'Relevant':
            relevant_articles.append({
                'title': article['title'],
                'link': article['link'],
                'publication_date': article['publication_date'],
                'summary': summary,
                'image_url': article['image_url'],
                'publication': article['publication']
            })


articles_by_publication = {}
for article in relevant_articles:
    publication = article['publication']
    if publication not in articles_by_publication:
        articles_by_publication[publication] = []
    articles_by_publication[publication].append(article)

# Generate the HTML sections for each publication
publications_html = ""
for publication, articles in articles_by_publication.items():
    publications_html += generate_publication_section(publication, articles)

# Create the final newsletter HTML
newsletter_html = html_template.replace("{publications}", publications_html)

# Send the email
send_email(newsletter_html)
