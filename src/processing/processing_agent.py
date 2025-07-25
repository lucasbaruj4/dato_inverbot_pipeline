"""
Structured Processing Agent Module

This module defines the CrewAI agent for structured data processing operations.
"""

from crewai import Agent
from crewai.tools import tool
from typing import List, Dict, Any, Union, Optional
import logging
import requests
import os
from dotenv import load_dotenv

from .processing_logic import StructuredProcessingLogic
from .schemas import SUPABASE_SCHEMAS, get_schema_info, validate_schema_exists

logger = logging.getLogger(__name__)

# Load environment variables for model connections
load_dotenv('.env.local')

@tool
def extract_structured_data_tool(
    content: Union[str, Dict[str, Any]], 
    schema_name: str
) -> Optional[Dict[str, Any]]:
    """
    A tool to extract structured data from raw content according to a specific schema.
    
    This tool uses the StructuredProcessingLogic to extract structured data from various
    content types (text, JSON, file paths) according to predefined Supabase schemas.
    
    Args:
        content: The raw content to extract data from (text, JSON dict, or file path)
        schema_name: Name of the target Supabase table schema
        
    Returns:
        Dictionary containing extracted structured data, or None if extraction fails
    """
    logger.info(f"Extract structured data tool called for schema: {schema_name}")
    
    try:
        # Create processing logic instance
        processing_logic = StructuredProcessingLogic()
        
        # Extract structured data
        extracted_data = processing_logic.extract_structured_data(content, schema_name)
        
        if extracted_data:
            logger.info(f"Successfully extracted data for schema {schema_name}")
            return extracted_data
        else:
            logger.warning(f"Failed to extract data for schema {schema_name}")
            return None
            
    except Exception as e:
        logger.error(f"Error in extract_structured_data_tool: {e}")
        return None

@tool
def process_financial_reports_tool(content: Union[str, Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """
    A tool to process financial reports and extract structured data.
    
    Args:
        content: Raw content from financial reports
        
    Returns:
        Structured financial data
    """
    logger.info("Process financial reports tool called")
    
    try:
        processing_logic = StructuredProcessingLogic()
        result = processing_logic.process_financial_reports(content)
        
        if result:
            logger.info("Successfully processed financial reports")
            return result
        else:
            logger.warning("Failed to process financial reports")
            return None
            
    except Exception as e:
        logger.error(f"Error in process_financial_reports_tool: {e}")
        return None

@tool
def process_daily_movements_tool(content: Union[str, Dict[str, Any]]) -> Optional[List[Dict[str, Any]]]:
    """
    A tool to process daily movements JSON data.
    
    Args:
        content: JSON content with daily movements
        
    Returns:
        List of structured movement records
    """
    logger.info("Process daily movements tool called")
    
    try:
        processing_logic = StructuredProcessingLogic()
        result = processing_logic.process_daily_movements_json(content)
        
        if result:
            logger.info(f"Successfully processed daily movements. Records: {len(result)}")
            return result
        else:
            logger.warning("Failed to process daily movements")
            return None
            
    except Exception as e:
        logger.error(f"Error in process_daily_movements_tool: {e}")
        return None

@tool
def process_macroeconomic_data_tool(content: Union[str, Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """
    A tool to process macroeconomic data and extract structured information.
    
    Args:
        content: Raw content with macroeconomic indicators
        
    Returns:
        Structured macroeconomic data
    """
    logger.info("Process macroeconomic data tool called")
    
    try:
        processing_logic = StructuredProcessingLogic()
        result = processing_logic.process_macroeconomic_data(content)
        
        if result:
            logger.info("Successfully processed macroeconomic data")
            return result
        else:
            logger.warning("Failed to process macroeconomic data")
            return None
            
    except Exception as e:
        logger.error(f"Error in process_macroeconomic_data_tool: {e}")
        return None

@tool
def process_public_contracts_tool(content: Union[str, Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """
    A tool to process public contracts and tenders data.
    
    Args:
        content: Raw content with contract information
        
    Returns:
        Structured contract data
    """
    logger.info("Process public contracts tool called")
    
    try:
        processing_logic = StructuredProcessingLogic()
        result = processing_logic.process_public_contracts(content)
        
        if result:
            logger.info("Successfully processed public contracts")
            return result
        else:
            logger.warning("Failed to process public contracts")
            return None
            
    except Exception as e:
        logger.error(f"Error in process_public_contracts_tool: {e}")
        return None

@tool
def validate_data_tool(data: Dict[str, Any], schema_name: str) -> Dict[str, Any]:
    """
    A tool to validate extracted data against schema requirements.
    
    Args:
        data: Extracted data to validate
        schema_name: Name of the schema to validate against
        
    Returns:
        Validation result with status and issues
    """
    logger.info(f"Validate data tool called for schema: {schema_name}")
    
    try:
        processing_logic = StructuredProcessingLogic()
        validation_result = processing_logic.validate_extracted_data(data, schema_name)
        
        logger.info(f"Validation completed. Valid: {validation_result['is_valid']}")
        return validation_result
        
    except Exception as e:
        logger.error(f"Error in validate_data_tool: {e}")
        return {
            "is_valid": False,
            "missing_fields": [],
            "issues": [f"Validation error: {str(e)}"],
            "validated_data": data
        }

class StructuredProcessingAgent:
    """
    CrewAI agent for structured data processing operations.
    
    This agent is responsible for:
    - Extracting structured data from raw content using AI models
    - Processing different content types according to database schemas
    - Validating extracted data against schema requirements
    - Coordinating processing tasks using the remote Mistral model
    """
    
    def __init__(self, llm=None):
        """
        Initialize the structured processing agent.
        
        Args:
            llm: Language model for the agent (will use remote Mistral if not provided)
        """
        self.llm = llm or self._get_remote_mistral_llm()
        self.agent = self._create_agent()
        logger.info("StructuredProcessingAgent initialized")

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
            
        try:
            from langchain_community.llms import ChatOpenAI
            
            # Configure to use the remote Mistral endpoint
            llm = ChatOpenAI(
                base_url=mistral_url,
                api_key="dummy",  # Not needed for localtunnel
                model="mistral-7b-instruct",
                temperature=0.3,
                max_tokens=1000
            )
            
            logger.info(f"Configured remote Mistral LLM at {mistral_url}")
            return llm
            
        except Exception as e:
            logger.error(f"Error configuring remote Mistral LLM: {e}")
            return None

    def _create_agent(self) -> Agent:
        """
        Create the CrewAI structured processing agent.
        
        Returns:
            Configured CrewAI Agent for structured processing
        """
        return Agent(
            role='Structured Data Processor',
            goal='Extract and structure key information from raw content according to the Supabase schema.',
            backstory=(
                "You are an expert in parsing diverse data formats (text, JSON, documents) "
                "and transforming them into structured records that match predefined database schemas. "
                "You use advanced language models to intelligently identify and extract relevant data points. "
                "You understand financial reports, market data, macroeconomic indicators, and public contracts. "
                "You are thorough and ensure all required fields are properly extracted and validated."
            ),
            tools=[
                extract_structured_data_tool,
                process_financial_reports_tool,
                process_daily_movements_tool,
                process_macroeconomic_data_tool,
                process_public_contracts_tool,
                validate_data_tool
            ],
            verbose=True,
            allow_delegation=False,  # This agent focuses only on structured processing
            llm=self.llm
        )

    def get_agent(self) -> Agent:
        """
        Get the configured CrewAI agent.
        
        Returns:
            The structured processing agent
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
                "prompt": "Hello, this is a connection test for structured processing.",
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

    def get_available_schemas(self) -> List[str]:
        """
        Get list of available schema names.
        
        Returns:
            List of available schema names
        """
        return list(SUPABASE_SCHEMAS.keys())

    def get_schema_info(self, schema_name: str) -> Dict[str, Any]:
        """
        Get information about a specific schema.
        
        Args:
            schema_name: Name of the schema
            
        Returns:
            Schema information dictionary
        """
        return get_schema_info(schema_name) 