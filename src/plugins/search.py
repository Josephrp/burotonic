# ./src/plugins.search.py

import requests
from googlesearch import search
from bs4 import BeautifulSoup
import os
query = "what is tonic ai"
output_folder = "website_data"  
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

for url in search(query, num_results=10,sleep_interval=2):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        paragraphs = soup.find_all('p')
        content = ' '.join([p.get_text() for p in paragraphs])
        filename = os.path.join(output_folder, url.split("//")[-1].replace("/", "_") + ".txt")
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)

        print(f"Data written to {filename}")
    except Exception as e:
        print(f"Error fetching {url}: {e}")
# basically google search is getting urls and some  urls are not worthy of scraping if anyone want you can send those urls to llm to see 
#which urls are relevant than scrape those urls  ith bs4 thats  the improvement you can do in it
        

