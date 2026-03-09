import time
import os
from dotenv import load_dotenv

from scrapegraphai.graphs import ScriptCreatorMultiGraph

load_dotenv()

API_KEY = os.getenv('GEMINI_API')
if not API_KEY:
    raise ValueError('Ensure GEMINI_API is set in your environment variables!')


# Define the configuration for the scraping pipeline
graph_config = {
   "llm": {
       "api_key": API_KEY,
       "model": "google_genai/gemini-3.1-flash-lite-preview",
   },
   "verbose": True,
   "headless": False,
   "library": "beautifulsoup4",  # <--- Ensure this is at the ROOT level of the dict
}

# User prompt & source
prompt="""Create a script that paginates pages & extracts books data from each book page. Inclusing:
Title, URL, image URL, price, availability, stars rating, description, information (dict).
- The script should loop over pages' URLs following the site's pagination logic and return a list of dicts.
- The script should implement smart delays to not get rate limited.
- The script should log progress messages to debug easier
"""
sources=["https://books.toscrape.com/", "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"]

# Define output schema
from pydantic import BaseModel, Field
from typing import Dict, List, Any

class BookData(BaseModel):
    title: str = Field(description="The full title of the book")
    url: str = Field(description="The full URL of the book detail page (homepage is 'https://books.toscrape.com/')")
    image_url: str = Field(description="The full URL of the book's cover image")
    price: float = Field(description="The price of the book including currency symbol (e.g., £51.77)")
    availability: str = Field(description="Availability status (e.g., 'In stock')")
    stars_rating: int = Field(description="The star rating of the book (e.g., 1 or 3 out of 5)")
    description: str = Field(description="A brief summary or description of the book's content")
    information: Dict[str, Any] = Field(
        description="A dictionary of the 'Product Information' table (e.g., UPC, Product Type, Tax, etc.)"
    )

OUTPUT_PATH = r"scalable_scraper.py"

# Create & run the ScriptCreatorMultiGraph instance
graph = ScriptCreatorMultiGraph(
    prompt=prompt,
    source=sources,
    config=graph_config,
    schema=BookData
)
result = graph.run()

# Save output script
if result:
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(result)
    print(f"\n✅ Scraper script saved to: {OUTPUT_PATH}")
    print("\n--- Preview (first 500 chars) ---")
    print(result[:500])
else:
    print("⚠️ Graph ran but returned empty output.")
