"""
Loading agent for the Inverbot Data Pipeline.

This module contains the CrewAI agent responsible for loading processed data
into Supabase (structured data) and Pinecone (vector data).
"""

import os
from typing import Dict, Any, List, Optional, Union

from crewai import Agent, Task, tool
from langchain_google_genai import ChatGoogleGenerativeAI

from ..utils.logging import get_logger
from ..utils.config import get_config
from .loading_logic import LoadingLogic

logger = get_logger(__name__)


class LoadingAgent:
    """
    CrewAI agent for data loading operations.
    
    This agent is responsible for:
    - Loading structured data into Supabase tables
    - Loading vector data into Pinecone indexes
    - Coordinating data loading tasks using Google's Gemini model
    - Ensuring data integrity and handling errors during loading
    - Managing batch operations and transaction consistency
    """
    
    def __init__(self, llm=None):
        """
        Initialize the loading agent.
        
        Args:
            llm: Language model for the agent (will use Google Gemini if not provided)
        """
        self.config = get_config()
        self.llm = llm or self._get_google_gemini_llm()
        self.loading_logic = LoadingLogic()
        self.agent = self._create_agent()
        logger.info("LoadingAgent initialized with Google Gemini")

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
        Create the CrewAI loading agent.
        
        Returns:
            Configured CrewAI Agent for loading tasks
        """
        return Agent(
            role="Data Loading Specialist",
            goal="Efficiently and reliably load processed data into target databases with full integrity",
            backstory="""You are an expert database loading specialist with extensive knowledge of 
            data warehousing, ETL processes, and database optimization. You excel at loading large 
            volumes of data efficiently while maintaining data integrity, handling errors gracefully, 
            and ensuring optimal performance. You understand both structured and vector databases 
            and their specific requirements.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            tools=[
                load_structured_data_tool,
                load_vector_data_tool,
                validate_data_integrity_tool,
                batch_load_data_tool,
                rollback_failed_operations_tool
            ]
        )
    
    def get_agent(self) -> Agent:
        """Get the configured CrewAI agent."""
        return self.agent 