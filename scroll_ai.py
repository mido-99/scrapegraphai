import os
from dotenv import load_dotenv
import asyncio
from scrapegraphai.docloaders.chromium import ChromiumLoader
from scrapegraphai.graphs import SmartScraperGraph

load_dotenv()

API_KEY = os.getenv('GEMINI_API')
if not API_KEY:
    raise ValueError('Ensure GEMINI_API is set in your environment variables!')


# fetch full doc
async def fetch_with_scroll(url: str) -> str:
    loader = ChromiumLoader(
        urls=[url],
        backend="playwright",
        headless=False,
        requires_js_support=True,
    )
    content = await loader.ascrape_playwright_scroll(
        url=url,
        timeout=60,
        scroll=5000,          # px to scroll each step
        sleep=2,              # seconds between scrolls
        scroll_to_bottom=True # keep scrolling until height stops changing
    )
    return content

html = asyncio.run(fetch_with_scroll("https://www.make.com/en/integrations"))

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
from typing import List, Dict

class DataModel(BaseModel):
    description: str = Field(description="Description about the page")
    plugins: List[str] = Field(description="List of all listed plugins in the page")
    links: Dict[str, str] = Field(description="Social media URLs on the page")

scraper = SmartScraperGraph(
    prompt="Extract Useful info about the page, include all plugins available too",
    source=html,   # ← pre-fetched HTML, not a URL
    config=graph_config,
    schema=DataModel
)
result = scraper.run()