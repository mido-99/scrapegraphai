from scrapegraphai.graphs import ScriptCreatorMultiGraph
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
   "library": "beautifulsoup4",  # <--- Ensure this is at the ROOT level of the dict
}

# User prompt & source
prompt="Create a script that extracts the quote's content, author, author URL & tags."
source="https://quotes.toscrape.com/"

# Define output schema
from pydantic import BaseModel, Field

class ArticleData(BaseModel):
    content: str = Field(description="Main quote content")
    author: str = Field(description="The author's name")
    author_url: str = Field(description="The author's page URL full URL, homepage is 'https://quotes.toscrape.com'")
    tags: list = Field(description="Quote tags")

# 3. Initialize the ScriptCreatorMultiGraph
script_creator = ScriptCreatorMultiGraph(
    prompt=prompt,
    source=source,
    config=graph_config
)

# 4. Run the graph to generate the script
generated_code = script_creator.run()

# 5. Save the generated script to a file
with open("scalable_scraper.py", "w") as f:
    f.write(generated_code)

print("Reusable script generated as 'scalable_scraper.py'")
