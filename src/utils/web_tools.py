"""
Web scraping tools for the Inverbot Data Pipeline.

This module provides tools for web search and content extraction using
Serper API for search and Firecrawl API for web scraping.
"""

import requests
import json
from typing import Dict, Any, List, Optional
from urllib.parse import urlparse

from .logging import get_logger
from .config import get_config
from crewai.tools import tool

logger = get_logger(__name__)


@tool
def search_web_tool(query: str, num_results: int = 5) -> str:
    """
    Search the web using Serper API.
    
    Args:
        query: Search query
        num_results: Number of results to return
        
    Returns:
        List of search results with URLs and snippets
    """
    try:
        config = get_config()
        
        url = "https://google.serper.dev/search"
        headers = {
            "X-API-KEY": config.serper_api_key,
            "Content-Type": "application/json"
        }
        
        payload = {
            "q": query,
            "num": num_results
        }
        
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        
        data = response.json()
        results = []
        
        if "organic" in data:
            for result in data["organic"][:num_results]:
                results.append({
                    "title": result.get("title", ""),
                    "url": result.get("link", ""),
                    "snippet": result.get("snippet", ""),
                    "position": result.get("position", 0)
                })
        
        logger.info(f"Web search completed for query: {query}")
        return json.dumps(results, ensure_ascii=False, indent=2)
        
    except Exception as e:
        logger.error(f"Web search failed: {e}")
        return f"Error searching web: {str(e)}"


@tool
def scrape_webpage_tool(url: str) -> str:
    """
    Scrape webpage content using direct requests and BeautifulSoup.
    
    Args:
        url: URL to scrape
        
    Returns:
        Dictionary with scraped content and metadata
    """
    try:
        import requests
        from bs4 import BeautifulSoup
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Get text content
        text = soup.get_text()
        
        # Clean up text
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        # Get title
        title = soup.find('title')
        title_text = title.get_text() if title else ""
        
        result = {
            "url": url,
            "title": title_text,
            "content": text[:5000],  # Limit content length
            "text": text,
            "metadata": {
                "status": "success",
                "timestamp": response.headers.get("date", ""),
                "domain": urlparse(url).netloc
            }
        }
        
        logger.info(f"Webpage scraped successfully: {url}")
        return json.dumps(result, ensure_ascii=False, indent=2)
        
    except Exception as e:
        logger.error(f"Webpage scraping failed for {url}: {e}")
        return f"Error scraping webpage {url}: {str(e)}"


@tool
def extract_financial_data_tool(url: str) -> str:
    """
    Extract financial data from a webpage.
    
    Args:
        url: URL to extract data from
        
    Returns:
        Dictionary with extracted financial data
    """
    try:
        # Scrape the webpage
        scraped_data = scrape_webpage(url)
        
        if not scraped_data.get("content"):
            return {"error": "No content found", "url": url}
        
        # Use LLM to extract financial data
        from langchain_google_genai import ChatGoogleGenerativeAI
        config = get_config()
        model_config = config.get_model_config()
        
        llm = ChatGoogleGenerativeAI(
            model=model_config["llm_model"],
            google_api_key=model_config["api_key"],
            temperature=model_config["temperature"],
            max_tokens=model_config["max_output_tokens"]
        )
        
        prompt = f"""
        Extrae datos financieros y económicos de este contenido web:
        
        URL: {url}
        Título: {scraped_data.get('title', '')}
        Contenido: {scraped_data.get('content', '')[:2000]}
        
        Identifica y extrae:
        1. Datos de bolsa de valores (tickers, precios, volúmenes)
        2. Indicadores económicos (PIB, inflación, desempleo)
        3. Datos fiscales (ingresos, gastos, deuda)
        4. Fechas y períodos relevantes
        
        Responde en formato JSON estructurado.
        """
        
        response = llm.invoke(prompt)
        
        result = {
            "url": url,
            "extracted_data": response.content,
            "raw_content": scraped_data.get("content", "")[:500],
            "metadata": scraped_data.get("metadata", {})
        }
        return json.dumps(result, ensure_ascii=False, indent=2)
        
    except Exception as e:
        logger.error(f"Financial data extraction failed for {url}: {e}")
        return f"Error extracting financial data from {url}: {str(e)}"


@tool
def search_financial_institutions_tool(query: str) -> str:
    """
    Search for financial institutions and their data.
    
    Args:
        query: Search query for financial institutions
        
    Returns:
        List of search results with financial data
    """
    try:
        # Search for financial institutions
        search_results = search_web(f"site:gov.py {query}", num_results=3)
        
        extracted_data = []
        
        for result in search_results:
            url = result["url"]
            
            # Extract financial data from each result
            financial_data = extract_financial_data(url)
            
            if financial_data and "error" not in financial_data:
                extracted_data.append({
                    "search_result": result,
                    "financial_data": financial_data
                })
        
        return extracted_data
        
    except Exception as e:
        logger.error(f"Financial institution search failed: {e}")
        return []


 