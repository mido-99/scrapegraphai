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
prompt="Extract Most Popular Software Categories & top 3 apps from each category"
source="https://www.g2.com/"

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
with open('data.json', 'w', encoding='utf8') as file:
    json.dump(result, file, indent=2)
