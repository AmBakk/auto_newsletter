import openai

openai.api_key = 'sk-proj-81rZ6VNZyLaFxlyk89YhT3BlbkFJ2wjFP5Xa3ZNU0OBU6aU4'


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
