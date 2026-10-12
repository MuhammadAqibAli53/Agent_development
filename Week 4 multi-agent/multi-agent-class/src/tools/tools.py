from langchain.tools import tool 
import requests
from dotenv import load_dotenv
import os
from tavily import TavilyClient
from rich import print
from bs4 import BeautifulSoup
from readability import Document
import trafilatura
import re 


load_dotenv()

@tool
def web_search(query : str) -> str:
    """Search Tavily for research information. Returns titles, URLs and snippets; requires TAVILY_API_KEY."""
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        return "Tavily is unavailable: missing TAVILY_API_KEY. Try duckduckgo_search."
    try:
        results = TavilyClient(api_key=api_key).search(query=query, max_results=5)
    except Exception:
        return "Tavily search failed. Try duckduckgo_search."

    out = []

    for r in results['results']:
        out.append(
            f"Title: {r['title']}\nURL: {r['url']}\nSnippet: {r['content'][:300]}\n"
        )
    
    return "\n----\n".join(out) or "No Tavily results found. Try duckduckgo_search."


@tool
def duckduckgo_search(query: str) -> str:
    """Search DuckDuckGo for general web information without an API key. Returns titles, URLs and snippets."""
    try:
        from ddgs import DDGS

        results = DDGS(timeout=15).text(query, max_results=5, backend="duckduckgo")
        out = [
            f"Title: {r.get('title', '')}\nURL: {r.get('href', '')}\n"
            f"Snippet: {r.get('body', '')[:300]}\n"
            for r in results
        ]
        return "\n----\n".join(out) or "No DuckDuckGo results found. Try web_search."
    except ImportError:
        return "DuckDuckGo is unavailable: install ddgs from requirements.txt. Try web_search."
    except Exception:
        return "DuckDuckGo search failed. Try web_search."

   
    

@tool
def scrape_url(url: str) -> str:
    """
    Scrape and extract clean readable content from a URL.
    Uses multiple extraction strategies for better reliability.
    """

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0 Safari/537.36"
        ),
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com/",
    }

    try:
        # ── Fetch page ─────────────────────────────────────
        response = requests.get(
            url,
            headers=headers,
            timeout=15
        )

        response.raise_for_status()

        html = response.text

        # ──────────────────────────────────────────────────
        # Strategy 1 → trafilatura (BEST for articles/blogs)
        # ──────────────────────────────────────────────────
        extracted = trafilatura.extract(
            html,
            include_comments=False,
            include_tables=False
        )

        if extracted and len(extracted.strip()) > 200:
            cleaned = re.sub(r'\s+', ' ', extracted)
            return cleaned[:5000]

        # ──────────────────────────────────────────────────
        # Strategy 2 → readability
        # ──────────────────────────────────────────────────
        doc = Document(html)
        clean_html = doc.summary()

        soup = BeautifulSoup(clean_html, "html.parser")

        for tag in soup([
            "script",
            "style",
            "nav",
            "footer",
            "header",
            "aside",
            "form"
        ]):
            tag.decompose()

        text = soup.get_text(separator=" ", strip=True)

        if text and len(text.strip()) > 200:
            cleaned = re.sub(r'\s+', ' ', text)
            return cleaned[:5000]

        # ──────────────────────────────────────────────────
        # Strategy 3 → fallback full page extraction
        # ──────────────────────────────────────────────────
        soup = BeautifulSoup(html, "html.parser")

        for tag in soup([
            "script",
            "style",
            "nav",
            "footer",
            "header",
            "aside",
            "form"
        ]):
            tag.decompose()

        text = soup.get_text(separator=" ", strip=True)

        cleaned = re.sub(r'\s+', ' ', text)

        if cleaned:
            return cleaned[:5000]

        return "Could not extract meaningful content from the page."

    except requests.exceptions.Timeout:
        return "Request timed out while scraping the URL."

    except requests.exceptions.HTTPError as e:
        return f"HTTP error occurred: {str(e)}"

    except Exception as e:
        return f"Could not scrape URL: {str(e)}"
