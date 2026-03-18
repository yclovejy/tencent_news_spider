# Tencent News Spider 📰

A Python project to scrape hot news and comments from Tencent News.  
Built with **Playwright**, the project extracts news titles, user comments, and stores them in CSV for further analysis.

## Features

- Scrape the top hot news from Tencent News.
- Automatically load comments by scrolling and clicking "View More".
- Save comments along with news title to `comments.csv`.
- Optional analysis scripts for sentiment and word cloud in `analysis.py`.

## Project Structure
```
tencent_news_spider/
├─ main.py
├─ spider.py
├─ comment_parser.py
├─ utils.py
├─ config.py
├─ requirements.txt
├─ comments.csv
├─ results/
│   ├─ top_words.txt
│   ├─ sentiment.png
│   └─ wordcloud.png
└─ README.md
```
## Installation
```
1. Clone the repository:


git clone https://github.com/yclovejy/tencent_news_spider.git
cd tencent_news_spider

2. Create a virtual environment:

python3 -m venv .venv
source .venv/bin/activate   # macOS/Linux
.venv\Scripts\activate      # Windows

3. Install dependencies:
pip install -r requirements.txt

Usage

Run the spider:
python main.py

Scraped comments will be saved in comments.csv.
You can use analysis.py to generate word clouds or sentiment analysis.

Notes
•	Playwright may require browser installation:
playwright install
```

License

MIT License © 2026 yclovejy