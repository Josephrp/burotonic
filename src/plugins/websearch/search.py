# ./src/plugins

import os
import requests
import googlesearch
from googlesearch import search
from bs4 import BeautifulSoup

class WebScraper:
    def __init__(self, query, num_results=10, output_folder="website_data"):
        self.query = query
        self.num_results = num_results
        self.output_folder = output_folder
        self.create_output_folder()

    def create_output_folder(self):
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

    def fetch_urls(self):
        """Fetch URLs using Google search."""
        urls = search(self.query, num_results=self.num_results, sleep_interval=2)
        return urls

    def scrape_url(self, url):
        """Scrape content from a single URL."""
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            paragraphs = soup.find_all('p')
            content = ' '.join([p.get_text() for p in paragraphs])
            return content
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None

    def save_content_to_file(self, content, filename):
        """Save scraped content to a file."""
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Data written to {filename}")

    def run(self):
        """Run the scraper: fetch URLs, scrape content, and save to files."""
        urls = self.fetch_urls()
        for url in urls:
            content = self.scrape_url(url)
            if content:
                filename = os.path.join(self.output_folder, url.split("//")[-1].replace("/", "_") + ".txt")
                self.save_content_to_file(content, filename)
