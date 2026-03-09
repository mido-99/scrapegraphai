import requests
from bs4 import BeautifulSoup
import time
import logging
import json

logging.basicConfig(level=logging.INFO)

def scrape_all_quotes(urls):
    base_url = "https://quotes.toscrape.com"
    all_extracted_data = []

    for start_url in urls:
        current_url = start_url
        logging.info(f"Starting extraction from: {base_url + current_url}")
        
        while current_url:
            logging.info(f"Scraping: {base_url + current_url}")
            try:
                response = requests.get(base_url + current_url)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')
                
                quotes = soup.find_all('div', class_='quote')
                for quote in quotes:
                    text = quote.find('span', class_='text').text
                    author = quote.find('small', class_='author').text
                    author_url = base_url + quote.find('a')['href']
                    tags = [tag.text for tag in quote.find_all('a', class_='tag')]
                    
                    all_extracted_data.append({
                        "content": text,
                        "author": author,
                        "author_url": author_url,
                        "tags": tags
                    })
                
                next_button = soup.find('li', class_='next')
                if next_button:
                    current_url = next_button.find('a')['href']
                    time.sleep(2)
                else:
                    current_url = None
            except Exception as e:
                logging.error(f"Error scraping {current_url}: {e}")
                break
                
    return all_extracted_data

def main():
    target_pages = ["/page/1/"]
    data = scrape_all_quotes(target_pages)
    print(json.dumps(data, indent=4))

if __name__ == "__main__":
    main()
