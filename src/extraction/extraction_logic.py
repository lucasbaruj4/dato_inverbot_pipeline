"""
Extraction Logic Module

This module contains the core extraction functionality for downloading and scraping
content from various web sources including HTML pages, JSON feeds, and file downloads.
"""

import os
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class ExtractionLogic:
    """
    Core extraction logic for handling various content types from web sources.
    
    This class provides methods to:
    - Download files (PDF, Excel, etc.)
    - Scrape HTML content and find file links
    - Fetch JSON data from APIs
    - Process different content types based on source configuration
    """
    
    def __init__(self, data_sources: List[Dict[str, Any]], download_dir: str = "/tmp/inverbot_downloads"):
        """
        Initialize the extraction logic with data sources.
        
        Args:
            data_sources: List of dictionaries containing source information
                         Each dict should have: category, url, content_type, description
            download_dir: Directory to store downloaded files
        """
        self.data_sources = data_sources
        self.download_dir = download_dir
        
        # Create download directory if it doesn't exist
        os.makedirs(self.download_dir, exist_ok=True)
        
        logger.info(f"ExtractionLogic initialized with {len(data_sources)} data sources")
        logger.info(f"Download directory: {self.download_dir}")

    def _download_file(self, url: str, category: str) -> Optional[str]:
        """
        Download a file from a URL and save it to the temporary directory.
        
        Args:
            url: URL of the file to download
            category: Category of the data source for logging
            
        Returns:
            Local file path if successful, None otherwise
        """
        try:
            logger.info(f"Downloading file from {url} for category {category}")
            
            response = requests.get(url, stream=True, timeout=30)
            response.raise_for_status()

            # Determine file extension from URL or headers
            filename = url.split('/')[-1] or f"downloaded_file_{len(os.listdir(self.download_dir))}"
            
            if '.' not in filename:
                # Try to get content type from headers to guess extension
                content_type = response.headers.get('Content-Type', '').lower()
                if 'pdf' in content_type:
                    filename += '.pdf'
                elif 'excel' in content_type or 'spreadsheetml' in content_type:
                    filename += '.xlsx'
                elif 'png' in content_type:
                    filename += '.png'
                elif 'presentation' in content_type:
                    filename += '.pptx'
                elif 'word' in content_type:
                    filename += '.docx'
                else:
                    filename += '.txt'  # Default fallback

            file_path = os.path.join(self.download_dir, filename)

            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            logger.info(f"Successfully downloaded file to {file_path}")
            return file_path

        except requests.exceptions.RequestException as e:
            logger.error(f"Error downloading file from {url}: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error downloading {url}: {e}")
            return None

    def _scrape_html(self, url: str, category: str) -> Dict[str, Any]:
        """
        Scrape text content and find file links from an HTML page.
        
        Args:
            url: URL of the page to scrape
            category: Category of the data source for logging
            
        Returns:
            Dictionary containing text_content and file_links
        """
        try:
            logger.info(f"Scraping HTML from {url} for category {category}")
            
            response = requests.get(url, timeout=30)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            # Find potential file links (PDF, EXCEL, PNG, PPT)
            file_links = []
            for link in soup.find_all('a', href=True):
                href = link['href']
                full_url = urljoin(url, href)  # Handle relative URLs
                
                # Check for file extensions
                if any(full_url.lower().endswith(ext) for ext in 
                       ['.pdf', '.xls', '.xlsx', '.png', '.ppt', '.pptx', '.doc', '.docx']):
                    file_links.append(full_url)

            # Extract text, removing script and style elements
            for script_or_style in soup(["script", "style"]):
                script_or_style.extract()
            
            text = soup.get_text()
            # Clean up whitespace
            text = ' '.join(text.split())

            logger.info(f"Successfully scraped HTML from {url}")
            logger.info(f"Found {len(file_links)} file links")
            
            return {"text_content": text, "file_links": file_links}

        except requests.exceptions.RequestException as e:
            logger.error(f"Error scraping HTML from {url}: {e}")
            return {"text_content": None, "file_links": []}
        except Exception as e:
            logger.error(f"Unexpected error scraping {url}: {e}")
            return {"text_content": None, "file_links": []}

    def _fetch_json(self, url: str, category: str) -> Optional[Dict[str, Any]]:
        """
        Fetch and return JSON data from a URL.
        
        Args:
            url: URL to fetch JSON from
            category: Category of the data source for logging
            
        Returns:
            JSON data if successful, None otherwise
        """
        try:
            logger.info(f"Fetching JSON from {url} for category {category}")
            
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            json_data = response.json()
            logger.info(f"Successfully fetched JSON from {url}")
            return json_data

        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching JSON from {url}: {e}")
            return None
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON from {url}: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error fetching JSON from {url}: {e}")
            return None

    def run_extraction(self) -> List[Dict[str, Any]]:
        """
        Iterate through data sources and extract content.
        
        Returns:
            List of dictionaries containing extracted data
            Each dict has: source_category, source_url, content_type, raw_content
        """
        extracted_data = []
        
        logger.info(f"Starting extraction for {len(self.data_sources)} sources")
        
        for source in self.data_sources:
            category = source["category"]
            url = source["url"]
            content_types = source["content_type"]

            logger.info(f"Processing source: {category} from {url}")

            # Prioritize JSON if expected
            if "JSON" in content_types:
                raw_content = self._fetch_json(url, category)
                if raw_content is not None:
                    extracted_data.append({
                        "source_category": category,
                        "source_url": url,
                        "content_type": "JSON",
                        "raw_content": raw_content
                    })
                    
            # Otherwise, attempt to scrape HTML and look for files
            elif any(ct in content_types for ct in ["TEXT", "PDF", "EXCEL", "PPT", "PNG"]):
                scraped_result = self._scrape_html(url, category)
                
                if scraped_result.get("text_content") is not None:
                    extracted_data.append({
                        "source_category": category,
                        "source_url": url,
                        "content_type": "TEXT",
                        "raw_content": scraped_result["text_content"]
                    })

                # Download found files
                for file_url in scraped_result.get("file_links", []):
                    file_path = self._download_file(file_url, category)
                    if file_path:
                        # Determine file type from extension
                        file_ext = os.path.splitext(file_path)[1].lstrip('.').upper()
                        extracted_data.append({
                            "source_category": category,
                            "source_url": file_url,
                            "content_type": file_ext,
                            "raw_content": file_path
                        })
            else:
                logger.warning(f"No extraction logic defined for content types {content_types} for source {category}")

        logger.info(f"Extraction completed. Extracted {len(extracted_data)} items")
        return extracted_data 