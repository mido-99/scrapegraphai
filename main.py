from scrapegraphai.graphs import SmartScraperGraph
import os
from dotenv import load_dotenv

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
}

# Define output schema
from pydantic import BaseModel, Field

class ArticleData(BaseModel):
    content: str = Field(description="Main quote content")
    author: str = Field(description="The author's name")
    author_url: str = Field(description="The author's page URL full URL, homepage is 'https://quotes.toscrape.com'")
    description: str = Field(description="Brief explanation of the quote's meaning")
    tags: list = Field(description="Quote tags")

# User prompt
prompt="""
Extract useful information about each quote in the page, including: 
- content
- author
- author URL
- tags
- brief explanation
"""

# Create the SmartScraperGraph instance
smart_scraper_graph = SmartScraperGraph(
    prompt=prompt,
    source="https://quotes.toscrape.com/",
    config=graph_config,
    schema=ArticleData
)

# Run the pipeline
result = smart_scraper_graph.run()

import json
with open('data.json', 'w') as file:
    json.dump(result, file, indent=2)
