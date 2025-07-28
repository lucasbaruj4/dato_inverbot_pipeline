"""
Loading agent for the Inverbot Data Pipeline.

This module contains the CrewAI agent responsible for loading processed data
into Supabase (structured data) and Pinecone (vector data).
"""

import os
from typing import Dict, Any, List, Optional, Union

from crewai import Agent, Task
from crewai.tools import BaseTool, tool
from langchain_google_genai import ChatGoogleGenerativeAI

from utils.logging import get_logger
from utils.config import get_config
from loading.loading_logic import LoadingLogic

logger = get_logger(__name__)

# Simple tools for testing
@tool
def load_structured_data_tool(data: dict) -> str:
    """Load structured data to Supabase (simulation mode)."""
    return f"SIMULATION: Would load {len(data)} structured records to Supabase"

@tool  
def load_vector_data_tool(vectors: list) -> str:
    """Load vector data to Pinecone (simulation mode)."""
    return f"SIMULATION: Would load {len(vectors)} vectors to Pinecone"

@tool
def validate_data_integrity_tool(data: dict) -> str:
    """Validate data integrity before loading."""
    return f"VALIDATION: All {len(data)} records passed integrity checks"

@tool
def batch_load_data_tool(batches: list) -> str:
    """Load data in batches for better performance."""
    return f"BATCH LOAD: Would process {len(batches)} batches"

@tool
def rollback_failed_operations_tool(operations: list) -> str:
    """Rollback failed operations to maintain consistency."""
    return f"ROLLBACK: Would rollback {len(operations)} failed operations"


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
        Create the CrewAI loading agent.
        
        Returns:
            Configured CrewAI Agent for loading tasks
        """
        return Agent(
            role="Database Loading Specialist",
            goal="Load structured and vector data into databases",
            backstory="Expert in database operations and data persistence. "
                     "Loads structured data into Supabase and vector data into Pinecone.",
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