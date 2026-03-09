import time

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
prompt="""Create a script that extracts the quote's data from each page. Inclusing:
content, author, author URL & tags.
- The script should loop over pages' URLs following the site's pagination logic and return a list of dicts.
"""
source=["https://quotes.toscrape.com/"]

# Define output schema
from pydantic import BaseModel, Field

class ArticleData(BaseModel):
    content: str = Field(description="Main quote content")
    author: str = Field(description="The author's name")
    author_url: str = Field(description="The author's page URL full URL, homepage is 'https://quotes.toscrape.com'")
    tags: list = Field(description="Quote tags")

OUTPUT_PATH = r"scalable_scraper.py"

# ── Retry wrapper ─────────────────────────────────────────────────────────
MAX_RETRIES = 3
RETRY_DELAY = 10  # seconds to wait between retries (increase if hitting RPM limits)

def run_with_retry(graph_config, sources, prompt, max_retries=MAX_RETRIES):
    attempt = 0
    last_error = None

    while attempt < max_retries:
        try:
            print(f"[Attempt {attempt + 1}/{max_retries}] Running ScriptCreatorMultiGraph...")
            graph = ScriptCreatorMultiGraph(
                prompt=prompt,
                source=sources,
                config=graph_config,
            )
            result = graph.run()
            return result  # success — return immediately

        except Exception as e:
            last_error = e
            attempt += 1
            error_str = str(e).lower()

            # Stop immediately on rate limit errors — don't waste quota
            if "rate limit" in error_str or "429" in error_str or "quota" in error_str:
                print(f"[Rate limit hit] Stopping after {attempt} attempt(s). Error: {e}")
                raise  # re-raise so you know it was a rate limit, not a bug

            if attempt < max_retries:
                print(f"[Retrying in {RETRY_DELAY}s] Error: {e}")
                time.sleep(RETRY_DELAY)
            else:
                print(f"[Max retries reached] Last error: {e}")

    raise last_error  # all attempts exhausted


# ── Run & Save ────────────────────────────────────────────────────────────
try:
    result = run_with_retry(graph_config, source, prompt)

    # result is a string of Python code
    if result:
        with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
            f.write(result)
        print(f"\n✅ Scraper script saved to: {OUTPUT_PATH}")
        print("\n--- Preview (first 500 chars) ---")
        print(result[:500])
    else:
        print("⚠️ Graph ran but returned empty output.")

except Exception as e:
    print(f"\n❌ Failed: {e}")
