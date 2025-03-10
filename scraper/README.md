# Termedia Scraper

## How to use

1. Install the requirements
    ```bash
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```
2. Run the following command to scrape the website:
    ```bash
    scrapy crawl termedia_spider -o output.json -s LOG_FILE=logs.log
    ```
3. The scraped data will be saved in `output.json` file and pdf files will be saved in `pdf` directory.