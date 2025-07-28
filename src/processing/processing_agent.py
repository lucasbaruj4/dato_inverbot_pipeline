"""
Processing agent for the Inverbot Data Pipeline.

This module contains the CrewAI agent responsible for processing raw extracted data
into structured formats according to database schemas.
"""

import os
import json
from typing import Dict, Any, List, Optional, Union

from crewai import Agent, Task, tool
from langchain_google_genai import ChatGoogleGenerativeAI

from ..utils.logging import get_logger
from ..utils.config import get_config
from .processing_logic import StructuredProcessingLogic
from .schemas import (
    InformeGeneralSchema,
    ResumenInformeFinancieroSchema,
    DatoMacroeconomicoSchema,
    MovimientoDiarioBolsaSchema,
    LicitacionContratoSchema
)

logger = get_logger(__name__)


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
        Create the CrewAI structured processing agent.
        
        Returns:
            Configured CrewAI Agent for processing tasks
        """
        return Agent(
            role="Structured Data Processing Specialist",
            goal="Transform raw data into structured formats according to database schemas with high accuracy",
            backstory="""You are an expert data processing specialist with extensive knowledge of 
            data transformation, schema validation, and structured data formats. You excel at 
            analyzing raw content and extracting relevant information that matches specific 
            database schemas. You ensure data quality, consistency, and completeness in all 
            your transformations.""",
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