# A function to scrape texte from an article
import csv
import os

import requests
from bs4 import BeautifulSoup


def scrape_article(url):
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        article_text = soup.get_text()
        return article_text
    else:
        print(f"Failed to retrieve the article. Status code: {response.status_code}")
        return None


def save_article_text(article_id, article_text, dest_dir):
    with open(f"{dest_dir}{article_id}.txt", "w", encoding="utf-8") as f:
        f.write(article_text)


# Example usage
if __name__ == "__main__":
    dest_dir = "data/raw/articles/"
    csv_file = "data/clean/gdelt_benin_clean.csv"
    visited_urls = set()
    with open(csv_file) as file:
        reader = csv.DictReader(file)
        for row in reader:
            url = row["SOURCEURL"]
            try:
                if url in visited_urls or os.path.exists(f"{dest_dir}{row['GLOBALEVENTID']}.txt"):
                    print(f"Skipping URL {url} as it has already been processed.")
                    continue

                article_text = scrape_article(url)
                if article_text:
                    article_id = row["GLOBALEVENTID"]
                    save_article_text(article_id, article_text, dest_dir)
                visited_urls.add(url)
            except Exception as e:
                print(f"Error processing URL {url}: {e}")
