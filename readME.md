
# Auto Newsletter Project

## Project Overview

The Auto Newsletter project automates the generation and distribution of a business newsletter focused on Real Madrid's corporate side and related industry news. The project scrapes articles from various sources, processes their relevance using OpenAI's GPT model, compiles the relevant articles into an HTML newsletter, and sends the newsletter via email.

## Repository Structure

```
auto_newsletter/
├── .github/
│   └── workflows/
│       └── newsletter.yml  # GitHub Actions workflow file
├── .venv/                   # Python virtual environment directory
├── scrapers/
│   ├── eurohoop_scraper.py
│   ├── offthepitch_scraper.py
│   ├── palco23_scraper.py
│   ├── playbook_scraper.py
│   ├── sportico_scraper.py
│   ├── sportsbusiness_scraper.py
│   └── sportsbusinessjournal_scraper.py
├── utils/
│   ├── api_calls.py
│   ├── build_nl.py
│   ├── send_email.py
│   └── main.py
├── README.md
├── requirements.txt
└── main.py
```

## Setup and Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your-username/auto_newsletter.git
   cd auto_newsletter
   ```

2. **Create and activate a virtual environment:**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows, use `.venv\Scriptsctivate`
   ```

3. **Install the required dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**

   Create a `.env` file in the root directory with the following content:

   ```env
   EMAIL_USERNAME=your_email_username
   EMAIL_PASSWORD=your_email_password
   OPENAI_API_KEY=your_openai_api_key
   RECEIVER_EMAILS=example@email.com
   ```

## Running the Project

To run the project locally:

```bash
python main.py
```

This will scrape articles, process them for relevance, generate the newsletter, and send it via email.

## GitHub Actions Workflow

The project is set up to run automatically using GitHub Actions. The workflow is defined in `.github/workflows/newsletter.yml`.

### Workflow Configuration

The workflow is scheduled to run every weekday at 9:00 AM and can also be triggered manually.

**newsletter.yml:**

```yaml
name: Auto Newsletter

on:
  schedule:
    - cron: '0 9 * * 1-5'  # Runs at 9:00 every weekday
  workflow_dispatch:  # Allows for manual trigger

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v2

      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.9

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Run main.py
        env:
          EMAIL_USERNAME: ${{ secrets.EMAIL_USERNAME }}
          EMAIL_PASSWORD: ${{ secrets.EMAIL_PASSWORD }}
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
          RECEIVER_EMAILS: ${{ secrets.RECEIVER_EMAILS }}
        run: python main.py
```

### Setting up GitHub Secrets

To set up the necessary secrets in your GitHub repository:

1. Go to your repository on GitHub.
2. Navigate to `Settings` -> `Secrets and variables` -> `Actions`.
3. Add the following secrets:
   - `EMAIL_USERNAME`
   - `EMAIL_PASSWORD`
   - `OPENAI_API_KEY`
   - `RECEIVER_EMAILS` (comma-separated list of emails)

## Project Components

### Scrapers

Each scraper file in the `scrapers` directory is responsible for scraping articles from different sources. For example:

- `eurohoop_scraper.py`
- `offthepitch_scraper.py`
- `palco23_scraper.py`
- `playbook_scraper.py`
- `sportico_scraper.py`
- `sportsbusiness_scraper.py`
- `sportsbusinessjournal_scraper.py`

### Utility Scripts

- **api_calls.py**: Handles communication with the OpenAI API to assess article relevance.
- **build_nl.py**: Compiles the relevant articles into an HTML structure.
- **send_email.py**: Sends the generated newsletter via email.
- **main.py**: Orchestrates the entire process, integrating the scrapers, API calls, HTML generation, and email sending.

## Troubleshooting

If you encounter issues:

1. **Check Environment Variables**: Ensure all required environment variables are set.
2. **Inspect Logs**: Review logs from GitHub Actions for detailed error messages.
3. **Dependencies**: Ensure all dependencies are installed correctly.

## Contributing

1. Fork the repository.
2. Create a new branch.
3. Make your changes.
4. Submit a pull request.

## License

This project is licensed under the MIT License.

---

This README provides a comprehensive guide to setting up, running, and troubleshooting the Auto Newsletter project. Make sure to replace placeholders with your actual information where necessary.
