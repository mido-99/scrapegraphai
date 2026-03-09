from scrapegraphai.graphs import SearchGraph
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
   "max_results": 3,    # Number of websites to search (default: 3)
   "verbose": True,
   "headless": False,
}

# Perform AI-powered web search
result = SearchGraph(
    prompt="What is the latest version of Python and what are its main features?",
    config=graph_config,
)
response = result.run()

with open('search_result.json', 'w', encoding='utf8') as file:
    import json
    json.dump(response, file, indent=2)