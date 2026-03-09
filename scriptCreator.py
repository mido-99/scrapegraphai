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
prompt="""Create a script that extracts the quote's data from each page. Inclusing:
content, author, author URL & tags.
- The script should loop over pages' URLs following the site's pagination logic and return a list of dicts.
- The script should implement smart delays to not get rate limited.
- The script should log progress messages to debug easier
"""
# sources=["https://quotes.toscrape.com/"]
sources=["https://quotes.toscrape.com/"]

# Define output schema
from pydantic import BaseModel, Field

class ArticleData(BaseModel):
    content: str = Field(description="Main quote content")
    author: str = Field(description="The author's name")
    author_url: str = Field(description="The author's page URL full URL, homepage is 'https://quotes.toscrape.com'")
    tags: list = Field(description="Quote tags")

OUTPUT_PATH = r"scalable_scraper.py"

# Create & run the ScriptCreatorMultiGraph instance
graph = ScriptCreatorMultiGraph(
    prompt=prompt,
    source=sources,
    config=graph_config,
    schema=ArticleData
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
