import requests
from bs4 import BeautifulSoup
import json

def scrape_quotes(urls):
    all_data = []
    base_url = "http://quotes.toscrape.com"
    
    for start_url in urls:
        current_url = start_url
        while current_url:
            response = requests.get(base_url + current_url)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            quotes = soup.select(".quote")
            for quote in quotes:
                content = quote.select_one(".text").get_text(strip=True)
                author = quote.select_one(".author").get_text(strip=True)
                author_url = base_url + quote.select_one("span a")['href']
                tags = [tag.get_text(strip=True) for tag in quote.select(".tag")]
                
                all_data.append({
                    "content": content,
                    "author": author,
                    "author_url": author_url,
                    "tags": tags
                })
                
            next_button = soup.select_one(".next a")
            current_url = next_button['href'] if next_button else None
            
    return all_data

if __name__ == "__main__":
    target_urls = ["/page/1/"]
    data = scrape_quotes(target_urls)
    print(json.dumps(data, indent=4))