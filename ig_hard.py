from scrapegraphai.graphs import SmartScraperGraph
import os
from dotenv import load_dotenv
from typing import List

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

# User prompt
prompt="Extract information about top 6 posts including: post URL, likes count, comments count, caption, author, & author URL."
source="https://www.instagram.com/leomessi/"

# Create the SmartScraperGraph instance
smart_scraper_graph = SmartScraperGraph(
    source=source,
    prompt=prompt,
    config=graph_config,
)

# Run the pipeline
result = smart_scraper_graph.run()

# Export data
import json
with open('data.json', 'w') as file:
    json.dump(result, file, indent=2)
