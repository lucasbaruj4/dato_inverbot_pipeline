"""
Extraction Tasks Module

This module defines the CrewAI tasks for data extraction operations.
"""

from crewai import Task
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class ExtractionTasks:
    """
    Task definitions for the extraction stage of the pipeline.
    
    This class provides CrewAI tasks for:
    - Downloading and scraping content from data sources
    - Handling different content types (JSON, TEXT, PDF, EXCEL, etc.)
    - Processing source lists and returning structured extraction results
    """
    
    def __init__(self, agent):
        """
        Initialize extraction tasks with a CrewAI agent.
        
        Args:
            agent: The CrewAI agent that will execute these tasks
        """
        self.agent = agent
        logger.info("ExtractionTasks initialized")

    def download_and_scrape_content(self) -> Task:
        """
        Create a task for downloading and scraping content from data sources.
        
        This task:
        - Iterates through provided data sources
        - Downloads or scrapes content based on content type
        - Handles JSON, TEXT, PDF, EXCEL, PNG, PPT content types
        - Returns structured data with source info and raw content
        
        Returns:
            CrewAI Task for content extraction
        """
        return Task(
            description=(
                "Iterate through the provided data sources, download or scrape content based on type.\n"
                "Handle different content types: JSON (fetch data), TEXT (scrape HTML), PDF/EXCEL/PNG (download file).\n"
                "Return a list of dictionaries, each containing source info and raw content/file path.\n"
                "Input should be a list of dictionaries, each with 'category', 'url', and 'content_type'.\n"
                "For JSON sources: Fetch and return the JSON data directly.\n"
                "For TEXT sources: Scrape HTML content and extract text.\n"
                "For file sources (PDF, EXCEL, PNG, PPT): Download files and return local file paths.\n"
                "For mixed sources: Handle all expected content types appropriately."
            ),
            expected_output=(
                "A list of dictionaries, where each dictionary includes:\n"
                "- 'source_category': The category of the data source (string)\n"
                "- 'source_url': The URL from which the content was obtained (string)\n"
                "- 'content_type': The type of content ('JSON', 'TEXT', 'PDF', 'EXCEL', 'PNG', 'PPT', etc.) (string)\n"
                "- 'raw_content': The raw content (for JSON/TEXT) or local file path (for files) (string or dict)\n"
                "Ensure all extracted items are properly categorized and the content is accessible."
            ),
            agent=self.agent,
            callback=lambda output: logger.info(f"Extraction task completed. Extracted {len(output) if isinstance(output, list) else 1} items")
        )

    def extract_specific_content_type(self, content_type: str) -> Task:
        """
        Create a task for extracting specific content types.
        
        Args:
            content_type: The specific content type to extract (e.g., 'JSON', 'PDF')
            
        Returns:
            CrewAI Task for specific content type extraction
        """
        return Task(
            description=(
                f"Extract content specifically of type '{content_type}' from the provided data sources.\n"
                f"Focus only on sources that expect '{content_type}' content.\n"
                f"Apply appropriate extraction methods for '{content_type}' content.\n"
                "Return structured data with source info and extracted content."
            ),
            expected_output=(
                f"A list of dictionaries containing only '{content_type}' content, where each dictionary includes:\n"
                "- 'source_category': The category of the data source\n"
                "- 'source_url': The URL from which the content was obtained\n"
                "- 'content_type': '{content_type}'\n"
                "- 'raw_content': The extracted content in appropriate format"
            ),
            agent=self.agent,
            callback=lambda output: logger.info(f"Specific {content_type} extraction completed. Extracted {len(output) if isinstance(output, list) else 1} items")
        )

    def validate_extraction_results(self) -> Task:
        """
        Create a task for validating extraction results.
        
        This task validates that extracted content is properly formatted and accessible.
        
        Returns:
            CrewAI Task for validation
        """
        return Task(
            description=(
                "Validate the results from the extraction process.\n"
                "Check that all extracted items have required fields (source_category, source_url, content_type, raw_content).\n"
                "Verify that content is accessible (files exist, JSON is valid, text is not empty).\n"
                "Identify any extraction failures or missing content.\n"
                "Return a validation report with status and any issues found."
            ),
            expected_output=(
                "A validation report dictionary containing:\n"
                "- 'total_items': Number of items processed (int)\n"
                "- 'valid_items': Number of valid items (int)\n"
                "- 'invalid_items': Number of invalid items (int)\n"
                "- 'issues': List of validation issues found (list of strings)\n"
                "- 'validated_data': The original data with validation status added"
            ),
            agent=self.agent,
            callback=lambda output: logger.info(f"Validation completed. {output.get('valid_items', 0)}/{output.get('total_items', 0)} items valid")
        ) 