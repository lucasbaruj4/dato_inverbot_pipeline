"""
Structured Processing Logic Module

This module contains the core processing functionality for extracting structured data
from raw content using AI models according to predefined database schemas.
"""

import json
import os
import requests
from typing import List, Dict, Any, Optional, Union
import logging
from datetime import datetime

from .schemas import SUPABASE_SCHEMAS, get_schema_info, get_required_fields
from dotenv import load_dotenv

# Load environment variables for model connections
load_dotenv('.env.local')

logger = logging.getLogger(__name__)

class StructuredProcessingLogic:
    """
    Core structured processing logic for extracting data according to database schemas.
    
    This class provides methods to:
    - Extract structured data from raw content using AI models
    - Process different content types (text, JSON, file paths)
    - Validate extracted data against schema requirements
    - Handle multiple schemas and content types
    """
    
    def __init__(self, mistral_url: Optional[str] = None):
        """
        Initialize the structured processing logic.
        
        Args:
            mistral_url: URL for the remote Mistral model (optional, will use env var if not provided)
        """
        self.mistral_url = mistral_url or os.getenv('MISTRAL_MODEL_URL')
        self.headers = {
            'bypass-tunnel-reminder': 'true',
            'Content-Type': 'application/json'
        }
        
        if not self.mistral_url:
            logger.warning("MISTRAL_MODEL_URL not found in environment variables")
        
        logger.info(f"StructuredProcessingLogic initialized with Mistral URL: {self.mistral_url}")

    def _read_file_content(self, file_path: str) -> Optional[str]:
        """
        Read content from a file.
        
        Args:
            file_path: Path to the file to read
            
        Returns:
            File content as string, or None if reading fails
        """
        try:
            if not os.path.exists(file_path):
                logger.error(f"File not found: {file_path}")
                return None
                
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            logger.info(f"Successfully read file: {file_path}")
            return content
            
        except Exception as e:
            logger.error(f"Error reading file {file_path}: {e}")
            return None

    def _call_mistral_model(self, prompt: str) -> Optional[str]:
        """
        Call the remote Mistral model with a prompt.
        
        Args:
            prompt: The prompt to send to the model
            
        Returns:
            Model response as string, or None if call fails
        """
        if not self.mistral_url:
            logger.error("Mistral URL not configured")
            return None
            
        try:
            payload = {
                "prompt": prompt,
                "max_tokens": 1000,
                "temperature": 0.3
            }
            
            response = requests.post(
                f"{self.mistral_url}/generate",
                headers=self.headers,
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                full_response = result.get('response', '')
                original_prompt = result.get('prompt', '')
                generated_text = full_response.replace(original_prompt, '').strip()
                
                logger.info("Successfully called Mistral model")
                return generated_text
            else:
                logger.error(f"Mistral API call failed with status {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Error calling Mistral model: {e}")
            return None

    def _prepare_extraction_prompt(self, content: str, schema_name: str, schema_description: str) -> str:
        """
        Prepare a prompt for structured data extraction.
        
        Args:
            content: The content to extract data from
            schema_name: Name of the target schema
            schema_description: Description of the schema structure
            
        Returns:
            Formatted prompt for the AI model
        """
        schema_info = get_schema_info(schema_name)
        fields = schema_info.get("fields", {})
        required_fields = schema_info.get("required_fields", [])
        
        prompt = f"""
You are an expert data extraction AI. Your task is to extract structured data from the provided content based on the given schema description.

Target Schema Name: {schema_name}
Target Schema Description: {schema_description}

Schema Fields:
"""
        
        for field_name, field_desc in fields.items():
            if field_name != "id":  # Skip auto-generated primary key
                required_marker = " (REQUIRED)" if field_name in required_fields else ""
                prompt += f"- {field_name}: {field_desc}{required_marker}\n"
        
        prompt += f"""
Required Fields: {', '.join(required_fields)}

Content to Extract From:
---
{content[:5000]}  # Limit content length to avoid token limits
---

Extract the data strictly following the schema. Pay attention to data types:
- Dates should be in YYYY-MM-DD format
- Numbers should be numeric values (not strings)
- Text fields should be strings
- JSONB fields should be structured as JSON objects

If a field is not found in the content, set it to null or a suitable default.
For required fields, make your best estimate if the information is not explicitly available.

Return the extracted data as a valid JSON object that can be parsed directly into a Python dictionary.
Only return the JSON output, nothing else.
"""
        
        return prompt

    def extract_structured_data(
        self, 
        content: Union[str, Dict[str, Any]], 
        schema_name: str
    ) -> Optional[Dict[str, Any]]:
        """
        Extract structured data from content according to a specific schema.
        
        Args:
            content: The content to extract data from (text, JSON, or file path)
            schema_name: Name of the target Supabase table schema
            
        Returns:
            Dictionary containing extracted structured data, or None if extraction fails
        """
        logger.info(f"Extracting structured data for schema: {schema_name}")
        
        # Validate schema exists
        if not validate_schema_exists(schema_name):
            logger.error(f"Schema '{schema_name}' not found")
            return None
        
        # Process content
        processed_content = None
        if isinstance(content, str):
            # Check if it's a file path
            if os.path.exists(content):
                processed_content = self._read_file_content(content)
            else:
                processed_content = content
        elif isinstance(content, dict):
            processed_content = json.dumps(content, indent=2)
        else:
            logger.error(f"Unsupported content type: {type(content)}")
            return None
        
        if not processed_content:
            logger.error("No content to process")
            return None
        
        # Get schema information
        schema_info = get_schema_info(schema_name)
        schema_description = schema_info.get("description", "")
        
        # Prepare and send prompt to Mistral
        prompt = self._prepare_extraction_prompt(processed_content, schema_name, schema_description)
        response = self._call_mistral_model(prompt)
        
        if not response:
            logger.error("Failed to get response from Mistral model")
            return None
        
        # Parse the response
        try:
            extracted_data = json.loads(response)
            logger.info(f"Successfully extracted data for schema {schema_name}")
            return extracted_data
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response from Mistral: {e}")
            logger.error(f"Response: {response[:500]}...")
            return None
        except Exception as e:
            logger.error(f"Unexpected error parsing response: {e}")
            return None

    def process_financial_reports(self, content: Union[str, Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """
        Process financial reports and extract structured data.
        
        Args:
            content: Raw content from financial reports
            
        Returns:
            Structured financial data
        """
        return self.extract_structured_data(content, "Resumen_Informe_Financiero")

    def process_daily_movements_json(self, content: Union[str, Dict[str, Any]]) -> Optional[List[Dict[str, Any]]]:
        """
        Process daily movements JSON data.
        
        Args:
            content: JSON content with daily movements
            
        Returns:
            List of structured movement records
        """
        result = self.extract_structured_data(content, "Movimiento_Diario_Bolsa")
        
        # Ensure result is a list for multiple records
        if isinstance(result, dict):
            return [result]
        elif isinstance(result, list):
            return result
        else:
            return None

    def process_macroeconomic_data(self, content: Union[str, Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """
        Process macroeconomic data and extract structured information.
        
        Args:
            content: Raw content with macroeconomic indicators
            
        Returns:
            Structured macroeconomic data
        """
        return self.extract_structured_data(content, "Dato_Macroeconomico")

    def process_public_contracts(self, content: Union[str, Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """
        Process public contracts and tenders data.
        
        Args:
            content: Raw content with contract information
            
        Returns:
            Structured contract data
        """
        return self.extract_structured_data(content, "Licitacion_Contrato")

    def process_general_reports_metadata(self, content: Union[str, Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """
        Process general report metadata.
        
        Args:
            content: Raw content with report information
            
        Returns:
            Structured report metadata
        """
        return self.extract_structured_data(content, "Informe_General")

    def validate_extracted_data(self, data: Dict[str, Any], schema_name: str) -> Dict[str, Any]:
        """
        Validate extracted data against schema requirements.
        
        Args:
            data: Extracted data to validate
            schema_name: Name of the schema to validate against
            
        Returns:
            Validation result with status and issues
        """
        schema_info = get_schema_info(schema_name)
        required_fields = schema_info.get("required_fields", [])
        
        validation_result = {
            "is_valid": True,
            "missing_fields": [],
            "issues": [],
            "validated_data": data
        }
        
        # Check for missing required fields
        for field in required_fields:
            if field not in data or data[field] is None:
                validation_result["missing_fields"].append(field)
                validation_result["is_valid"] = False
        
        # Add validation issues
        if validation_result["missing_fields"]:
            validation_result["issues"].append(
                f"Missing required fields: {', '.join(validation_result['missing_fields'])}"
            )
        
        logger.info(f"Validation completed for {schema_name}. Valid: {validation_result['is_valid']}")
        return validation_result

def validate_schema_exists(table_name: str) -> bool:
    """
    Validate if a schema exists for the given table name.
    
    Args:
        table_name: Name of the table to validate
        
    Returns:
        True if schema exists, False otherwise
    """
    return table_name in SUPABASE_SCHEMAS 