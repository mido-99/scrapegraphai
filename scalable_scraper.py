import requests
from bs4 import BeautifulSoup
import time
import logging
import urllib.parse
import json
import re

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_star_rating(element):
    rating_map = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
    classes = element.get('class', [])
    for cls in classes:
        if cls in rating_map:
            return rating_map[cls]
    return 0

def scrape_book_details(session, book_url, base_url):
    response = session.get(book_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    title = soup.find('h1').text.strip()
    price = float(soup.find('p', class_='price_color').text.replace('£', ''))
    availability = soup.find('p', class_='instock availability').text.strip()
    stars = get_star_rating(soup.find('p', class_='star-rating'))
    
    desc_tag = soup.find('div', id='product_description')
    description = desc_tag.find_next_sibling('p').text if desc_tag else soup.find('meta', attrs={'name': 'description'})['content'].strip()
    
    image_url = urllib.parse.urljoin(base_url, soup.find('img')['src'])
    
    info_table = soup.find('table', class_='table-striped')
    information = {row.find('th').text: row.find('td').text for row in info_table.find_all('tr')}
    # clean prices
    for key, val in information.items():
        if 'Price' in key:
            try:
                print(key, val)
                matches = re.search(r"[\d\.]+", str(val))
                information[key] = matches.group()
            except Exception as e:
                print(f"Error cleaning {val}")
    
    return {
        "title": title,
        "url": book_url,
        "image_url": image_url,
        "price": price,
        "availability": availability,
        "stars_rating": stars,
        "description": description,
        "information": information
    }

def main():
    base_url = "https://books.toscrape.com/"
    start_url = "https://books.toscrape.com/catalogue/page-1.html"
    session = requests.Session()
    all_books = []
    current_url = start_url
    
    while current_url:
        logging.info(f"Scraping page: {current_url}")
        response = session.get(current_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        products = soup.find_all('article', class_='product_pod')
        for product in products[:2]:
            book_link = urllib.parse.urljoin(current_url, product.h3.a['href'])
            try:
                book_data = scrape_book_details(session, book_link, base_url)
                all_books.append(book_data)
                logging.info(f"Successfully scraped: {book_data['title']}")
                time.sleep(0.5)
            except Exception as e:
                logging.error(f"Error scraping {book_link}: {e}")
        
        next_button = soup.find('li', class_='next')
        if next_button:
            current_url = urllib.parse.urljoin(current_url, next_button.a['href'])
        else:
            current_url = None
        
        if 'page-3' in current_url:
            break
        time.sleep(1)
        
    print(json.dumps(all_books, indent=4))

if __name__ == "__main__":
    main()