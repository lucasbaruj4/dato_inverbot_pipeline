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

from ..utils.logging import get_logger
from ..utils.config import get_config
from .extraction_logic import ExtractionLogic

logger = get_logger(__name__)


class ExtractionAgent:
    """
    CrewAI agent for data extraction operations.
    
    This agent is responsible for:
    - Extracting data from various web sources (JSON, HTML, PDF, Excel)
    - Processing different content types and formats
    - Coordinating extraction tasks using Google's Gemini model
    - Validating extracted data before processing
    """
    
    def __init__(self, llm=None):
        """
        Initialize the extraction agent.
        
        Args:
            llm: Language model for the agent (will use Google Gemini if not provided)
        """
        self.config = get_config()
        self.llm = llm or self._get_google_gemini_llm()
        self.extraction_logic = ExtractionLogic()
        self.agent = self._create_agent()
        logger.info("ExtractionAgent initialized with Google Gemini")

    def _get_google_gemini_llm(self):
        """
        Get the Google Gemini LLM configuration for CrewAI.
        
        Returns:
            LLM configuration for Google Gemini model
        """
        try:
            model_config = self.config.get_model_config()
            
            llm = ChatGoogleGenerativeAI(
                model=model_config["llm_model"],
                google_api_key=model_config["api_key"],
                temperature=model_config["temperature"],
                max_tokens=model_config["max_output_tokens"]
            )
            
            logger.info(f"Configured Google Gemini LLM: {model_config['llm_model']}")
            return llm
            
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
            goal="Extract and validate data from various web sources efficiently and accurately",
            backstory="""You are an expert data extraction specialist with deep knowledge of 
            web scraping, document parsing, and data validation. You excel at extracting 
            structured information from diverse sources including JSON APIs, HTML pages, 
            PDF documents, and Excel files. You always validate data quality and format 
            before passing it to the next stage.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            tools=[
                extract_json_data_tool,
                extract_html_content_tool,
                extract_pdf_content_tool,
                extract_excel_data_tool,
                validate_extracted_data_tool
            ]
        )
    
    def get_agent(self) -> Agent:
        """Get the configured CrewAI agent."""
        return self.agent 