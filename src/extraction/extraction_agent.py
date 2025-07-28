"""
Extraction agent for the Inverbot Data Pipeline.

This module contains the CrewAI agent responsible for extracting data from various sources
including JSON, HTML, PDF, and Excel files from web sources.
"""

import os
import requests
import pandas as pd
from typing import Dict, Any, List, Optional
from urllib.parse import urljoin, urlparse

from crewai import Agent, Task
from crewai.tools import BaseTool
from langchain_google_genai import ChatGoogleGenerativeAI

from utils.logging import get_logger
from utils.config import get_config
from utils.web_tools import (
    search_web_tool,
    scrape_webpage_tool,
    extract_financial_data_tool,
    search_financial_institutions_tool
)
from extraction.extraction_logic import ExtractionLogic

logger = get_logger(__name__)


class ExtractionAgent:
    """
    CrewAI agent for data extraction operations.
    
    This agent is responsible for:
    - Extracting data from various web sources (JSON, HTML, PDF, Excel)
    - Processing different content types and formats
    - Coordinating extraction tasks using Google's Gemini model
    - Validating extracted data before processing
    - Web scraping using Serper and Firecrawl APIs
    """
    
    def __init__(self, llm=None):
        """
        Initialize the extraction agent.
        
        Args:
            llm: Language model for the agent (will use Google Gemini if not provided)
        """
        self.config = get_config()
        self.llm = llm or self._get_google_gemini_llm()
        from extraction.data_sources import DATA_SOURCES
        self.extraction_logic = ExtractionLogic(DATA_SOURCES)
        self.agent = self._create_agent()
        logger.info("ExtractionAgent initialized with Google Gemini and web scraping tools")

    def _get_google_gemini_llm(self):
        """
        Get the Google Gemini LLM configuration for CrewAI.
        
        Returns:
            LLM configuration for Google Gemini model
        """
        try:
            model_config = self.config.get_model_config()
            
            # For CrewAI, we need to use the model string directly for LiteLLM
            import os
            # Set environment variable for LiteLLM Google API - CrewAI expects GEMINI_API_KEY
            os.environ["GEMINI_API_KEY"] = model_config["api_key"]
            
            # Return the model string in LiteLLM format for CrewAI
            model_name = f"gemini/{model_config['llm_model']}"  # Convert to LiteLLM format
            logger.info(f"Configured Google Gemini LLM for CrewAI: {model_name}")
            return model_name
            
        except Exception as e:
            logger.error(f"Error configuring Google Gemini LLM: {e}")
            return None

    def _create_agent(self) -> Agent:
        """
        Create the CrewAI extraction agent.
        
        Returns:
            Configured CrewAI Agent for extraction tasks
        """
        return Agent(
            role="Data Extraction Specialist",
            goal="Extract and validate data from web sources efficiently",
            backstory="Expert in web scraping, document parsing, and data validation. "
                     "Extracts structured information from JSON APIs, HTML pages, PDF documents, "
                     "and Excel files. Validates data quality before processing.",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            tools=[
                search_web_tool,
                scrape_webpage_tool,
                extract_financial_data_tool,
                search_financial_institutions_tool
            ]
        )
    
    def get_agent(self) -> Agent:
        """Get the configured CrewAI agent."""
        return self.agent 