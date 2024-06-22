html_template = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RMCF Business Newsletter</title>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            background-color: #ffffff;
            color: #003366;
        }
        .container {
            width: 80%;
            margin: 0 auto;
            padding: 20px;
        }
        .header {
            display: flex;
            align-items: center;
            justify-content: center;
            padding-bottom: 20px;
            position: relative;
        }
        .header img {
            position: absolute;
            left: 0;
            max-width: 100px;
        }
        .header h1 {
            margin: 0;
            font-size: 36px;
            color: #003366;
        }
        .publication-section {
            margin-top: 40px;
        }
        .publication-title {
            display: flex;
            align-items: center;
            color: #003366;
            font-size: 28px; /* Increased font size */
            font-weight: bold;
            margin-bottom: 10px;
        }
        .publication-title::before,
        .publication-title::after {
            content: "";
            flex: 1;
            border-bottom: 2px solid #FFD700;
            margin: 0 10px;
        }
        .publication-title::before {
            flex: 0;
            width: 100px;
        }
        .publication-title span {
            flex: 0;
            margin-left: 10px;
        }
        .articles {
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
            justify-content: flex-start; /* Aligned to left */
        }
        .article {
            width: calc(33.33% - 20px);
            background-color: #f8f8f8;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        .article img {
            width: 100%;
            height: 180px;
            object-fit: cover;
        }
        .article-content {
            padding: 15px;
        }
        .article-title {
            font-size: 18px;
            color: #003366;
            text-decoration: none;
        }
        .article-date {
            font-size: 14px;
            color: #666666;
            margin: 5px 0;
        }
        .article-summary {
            font-size: 14px;
            color: #333333;
        }
        .footer {
            text-align: center;
            padding: 20px 0;
            font-size: 14px;
            color: #666666;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <img src="https://www.logodesign.org/wp-content/uploads/2023/02/Real-Madrid-Emblem.png" alt="Real Madrid Logo">
            <h1>RMCF Business Newsletter</h1>
        </div>

        <!-- Start of publication sections -->
        {publications}
        <!-- End of publication sections -->

        <div class="footer">
            <p>&copy; 2024 RMCF Business Newsletter. All rights reserved.</p>
        </div>
    </div>
</body>
</html>
'''


def generate_article_html(article):
    return f'''
    <div class="article">
        <a href="{article['link']}">
            <img src="{article['image_url']}" alt="Article Image">
        </a>
        <div class="article-content">
            <a href="{article['link']}" class="article-title">
                {article['title']}
            </a>
            <p class="article-date">{article['publication_date']}</p>
            <p class="article-summary">{article['summary']}</p>
        </div>
    </div>
    '''


def generate_publication_section(publication_name, articles):
    articles_html = ''.join(generate_article_html(article) for article in articles)
    return f'''
    <div class="publication-section">
        <div class="publication-title"><span>{publication_name}</span></div>
        <div class="articles">
            {articles_html}
        </div>
        <hr style="border: 1px solid #FFD700; margin-top: 20px;"> <!-- Bottom line -->
    </div>
    '''

