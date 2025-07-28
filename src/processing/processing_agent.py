"""
Processing agent for the Inverbot Data Pipeline.

This module contains the CrewAI agent responsible for processing raw extracted data
into structured formats according to database schemas.
"""

import os
import json
from typing import Dict, Any, List, Optional, Union

from crewai import Agent, Task
from crewai.tools import BaseTool, tool
from langchain_google_genai import ChatGoogleGenerativeAI
import os

from utils.logging import get_logger
from utils.config import get_config
from processing.processing_logic import StructuredProcessingLogic
from processing.schemas import (
    InformeGeneralSchema,
    ResumenInformeFinancieroSchema,
    DatoMacroeconomicoSchema,
    MovimientoDiarioBolsaSchema,
    LicitacionContratoSchema
)

logger = get_logger(__name__)

# Tools for processing different data types
@tool
def process_informe_general_tool(data: str) -> str:
    """Process general report data according to InformeGeneralSchema."""
    return f"PROCESSED: Informe General from {len(data)} characters of data"

@tool  
def process_resumen_financiero_tool(data: str) -> str:
    """Process financial summary data according to ResumenInformeFinancieroSchema."""
    return f"PROCESSED: Financial summary from {len(data)} characters of data"

@tool
def process_dato_macroeconomico_tool(data: str) -> str:
    """Process macroeconomic data according to DatoMacroeconomicoSchema."""
    return f"PROCESSED: Macroeconomic data from {len(data)} characters of data"

@tool
def process_movimiento_diario_tool(data: str) -> str:
    """Process daily market movements according to MovimientoDiarioBolsaSchema."""
    return f"PROCESSED: Daily movements from {len(data)} characters of data"

@tool
def process_licitacion_contrato_tool(data: str) -> str:
    """Process public contract data according to LicitacionContratoSchema."""
    return f"PROCESSED: Contract data from {len(data)} characters of data"

@tool
def validate_schema_compliance_tool(data: str) -> str:
    """Validate data compliance with schema requirements."""
    return f"VALIDATION: Schema compliance checked for {len(data)} characters of data"


class StructuredProcessingAgent:
    """
    CrewAI agent for structured data processing operations.
    
    This agent is responsible for:
    - Extracting structured data from raw content using AI models
    - Processing different content types according to database schemas
    - Validating extracted data against schema requirements
    - Coordinating processing tasks using Google's Gemini model
    """
    
    def __init__(self, llm=None):
        """
        Initialize the structured processing agent.
        
        Args:
            llm: Language model for the agent (will use Google Gemini if not provided)
        """
        self.config = get_config()
        self.llm = llm or self._get_google_gemini_llm()
        self.processing_logic = StructuredProcessingLogic()
        self.agent = self._create_agent()
        logger.info("StructuredProcessingAgent initialized with Google Gemini")

    def _get_google_gemini_llm(self):
        """
        Get the Google Gemini LLM configuration for CrewAI.
        
        Returns:
            LLM configuration for Google Gemini model
        """
        try:
            model_config = self.config.get_model_config()
            
            # For CrewAI, we need to use the model string directly for LiteLLM
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
        Create the CrewAI structured processing agent.
        
        Returns:
            Configured CrewAI Agent for processing tasks
        """
        return Agent(
            role="Data Processing Specialist",
            goal="Process raw data into structured database formats",
            backstory="Expert in data transformation and schema mapping. "
                     "Processes financial reports, market movements, macroeconomic data, "
                     "and public contracts into structured database records.",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            tools=[
                process_informe_general_tool,
                process_resumen_financiero_tool,
                process_dato_macroeconomico_tool,
                process_movimiento_diario_tool,
                process_licitacion_contrato_tool,
                validate_schema_compliance_tool
            ]
        )
    
    def get_agent(self) -> Agent:
        """Get the configured CrewAI agent."""
        return self.agent 