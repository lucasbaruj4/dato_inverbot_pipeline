"""
Extraction Agent Module

This module defines the CrewAI agent for data extraction operations.
"""

from crewai import Agent
from crewai.tools import tool
from typing import List, Dict, Any
import logging
import requests
import os
from dotenv import load_dotenv

from .extraction_logic import ExtractionLogic

logger = logging.getLogger(__name__)

# Load environment variables for model connections
load_dotenv('.env.local')

@tool
def extraction_tool(sources_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    A tool to extract raw content from provided data sources.
    
    This tool uses the ExtractionLogic class to handle various content types:
    - JSON: Fetch data from APIs
    - TEXT: Scrape HTML content
    - PDF/EXCEL/PNG/PPT: Download files
    
    Args:
        sources_list: List of dictionaries, each with 'category', 'url', and 'content_type'
        
    Returns:
        List of dictionaries containing extracted data with source info and raw content
    """
    logger.info(f"Extraction tool received sources_list with {len(sources_list)} items")
    
    try:
        # Create a new instance of ExtractionLogic with the provided sources
        extraction_handler = ExtractionLogic(data_sources=sources_list)
        
        # Run the extraction process
        extracted_data = extraction_handler.run_extraction()
        
        logger.info(f"Extraction tool completed. Extracted {len(extracted_data)} items")
        return extracted_data
        
    except Exception as e:
        logger.error(f"Error in extraction tool: {e}")
        return []

class ExtractionAgent:
    """
    CrewAI agent for data extraction operations.
    
    This agent is responsible for:
    - Downloading and scraping content from various web sources
    - Handling different content types (JSON, TEXT, PDF, EXCEL, etc.)
    - Coordinating extraction tasks using the remote Mistral model
    """
    
    def __init__(self, llm=None):
        """
        Initialize the extraction agent.
        
        Args:
            llm: Language model for the agent (will use remote Mistral if not provided)
        """
        self.llm = llm or self._get_remote_mistral_llm()
        self.agent = self._create_agent()
        logger.info("ExtractionAgent initialized")

    def _get_remote_mistral_llm(self):
        """
        Get the remote Mistral LLM configuration for CrewAI.
        
        Returns:
            LLM configuration for remote Mistral model
        """
        mistral_url = os.getenv('MISTRAL_MODEL_URL')
        if not mistral_url:
            logger.warning("MISTRAL_MODEL_URL not found in environment variables")
            return None
            
        # For CrewAI, we need to configure the LLM to use the remote endpoint
        # This is a simplified approach - in practice, you might need a custom LLM wrapper
        try:
            from langchain_community.llms import ChatOpenAI
            
            # Configure to use the remote Mistral endpoint
            llm = ChatOpenAI(
                base_url=mistral_url,
                api_key="dummy",  # Not needed for localtunnel
                model="mistral-7b-instruct",
                temperature=0.3,
                max_tokens=512
            )
            
            logger.info(f"Configured remote Mistral LLM at {mistral_url}")
            return llm
            
        except Exception as e:
            logger.error(f"Error configuring remote Mistral LLM: {e}")
            return None

    def _create_agent(self) -> Agent:
        """
        Create the CrewAI extraction agent.
        
        Returns:
            Configured CrewAI Agent for extraction
        """
        return Agent(
            role='Data Extractor',
            goal='Obtain raw content from various web sources based on provided URLs and content types.',
            backstory=(
                "You are an expert in web scraping, API calls, and file downloading. "
                "You can efficiently retrieve content from diverse online sources, including "
                "HTML pages, JSON feeds, PDFs, and Excel files. "
                "You understand different content types and know how to handle each appropriately. "
                "You are thorough and ensure all requested content is properly extracted and categorized."
            ),
            tools=[extraction_tool],
            verbose=True,
            allow_delegation=False,  # This agent focuses only on extraction
            llm=self.llm
        )

    def get_agent(self) -> Agent:
        """
        Get the configured CrewAI agent.
        
        Returns:
            The extraction agent
        """
        return self.agent

    def test_connection(self) -> Dict[str, Any]:
        """
        Test the connection to the remote Mistral model.
        
        Returns:
            Dictionary with connection status and details
        """
        try:
            mistral_url = os.getenv('MISTRAL_MODEL_URL')
            if not mistral_url:
                return {
                    'status': 'error',
                    'message': 'MISTRAL_MODEL_URL not found in environment variables'
                }
            
            # Test the connection by making a simple request
            headers = {
                'bypass-tunnel-reminder': 'true',
                'Content-Type': 'application/json'
            }
            
            test_payload = {
                "prompt": "Hello, this is a connection test.",
                "max_tokens": 10,
                "temperature": 0.3
            }
            
            response = requests.post(
                f"{mistral_url}/generate",
                headers=headers,
                json=test_payload,
                timeout=10
            )
            
            if response.status_code == 200:
                return {
                    'status': 'success',
                    'message': 'Connection to remote Mistral model successful',
                    'url': mistral_url
                }
            else:
                return {
                    'status': 'error',
                    'message': f'Connection failed with status {response.status_code}',
                    'url': mistral_url
                }
                
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Connection test failed: {str(e)}'
            } 