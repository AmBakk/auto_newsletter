import openai
import os

openai.api_key = os.getenv('OPENAI_API_KEY')


def assess_relevance(article):
    messages = [
        {"role": "system",
         "content": "You are an assistant that evaluates the relevance of articles for a business newsletter focused on sports business and industry news."},
        {"role": "user",
         "content": f"Article Title: {article['title']}\nArticle Subhead: {article['subhead']}\n\nDetermine if this article is relevant for a business newsletter for the corporate side of Real Madrid focused on the club's business and industry news. Specifically, make sure to include anything relevant to the big European Football leagues, UEFA, Super League or other sports, if Real Madrid is mentioned. Reply with 'Relevant' or 'Not Relevant'. If relevant, provide a short, two sentences, summary of the article in Spanish that can fit in the newsletter. Do not need to include why you think it is relevant."}
    ]

    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.7,
    )

    response_dict = response.model_dump()  # Convert to dictionary
    relevance_response = response_dict['choices'][0]['message']['content'].strip()

    if relevance_response.startswith('Relevant'):
        relevance = 'Relevant'
        summary = relevance_response.replace('Relevant', '').strip().replace('Summary:', '').strip()
        return relevance, summary
    else:
        return 'Not Relevant', ''


def clean_html(newsletter):
    messages = [
        {"role": "system",
         "content": '''You are the last step in a project that aggregates scrapped articles and puts together a 
                       newsletter. Your role is to clean up the HTML structure of the newsletter and remove any duplicate
                       articles.'''},
        {"role": "user",
         "content": f'''The following is the newsletter's HTML structure. Go through it and : \n
                        - Remove any articles that are present more than once 
                        - If a summary starts with the word 'summary', remove the word
                        - Only return the actual html structure, as your response will be directly emailed as the 
                          newsletter. \n{newsletter}'''}
    ]

    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        max_tokens=3000,
        n=1,
        stop=None,
        temperature=0.7,
    )

    response_dict = response.model_dump()  # Convert to dictionary
    newsletter = response_dict['choices'][0]['message']['content'].strip()

    return newsletter


