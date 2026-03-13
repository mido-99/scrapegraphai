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
    "loader_kwargs": {
        "backend": "playwright",
        "load_state": "load",   # valid ChromiumLoader param, other options on: https://playwright.dev/docs/api/class-page#page-go-back-option-wait-until
        # "proxy": {...}               # also valid here
    },
    # browser_config goes at root level for launch args:
    "browser_config": {
        "args": ["--disable-blink-features=AutomationControlled"],  # Chromium launch flags
    }
}

# Define output schema
from pydantic import BaseModel, Field
from typing import List, Dict

class DataModel(BaseModel):
    description: str = Field(description="Description about the page")
    plugins: List[str] = Field(description="List of all listed plugins in the page")
    links: Dict[str, str] = Field(description="Social media URLs on the page")

# User prompt
prompt="Extract Useful info about the page, include all plugins available too"
source="https://www.make.com/en/integrations/"

# Create the SmartScraperGraph instance
smart_scraper_graph = SmartScraperGraph(
    source=source,
    prompt=prompt,
    config=graph_config,
    schema=DataModel
)

# Run the pipeline
result = smart_scraper_graph.run()

# Export data
import json
with open('data.json', 'w', encoding='utf8') as file:
    json.dump(result, file, indent=2)
