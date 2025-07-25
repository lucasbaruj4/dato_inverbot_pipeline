"""
Structured Processing Tasks Module

This module defines the CrewAI tasks for structured data processing operations.
"""

from crewai import Task
from typing import List, Dict, Any, Union
import logging

logger = logging.getLogger(__name__)

class StructuredProcessingTasks:
    """
    Task definitions for the structured processing stage of the pipeline.
    
    This class provides CrewAI tasks for:
    - Processing financial reports and extracting structured data
    - Processing daily movements JSON data
    - Processing macroeconomic data
    - Processing public contracts and tenders
    - Processing general report metadata
    - Validating extracted data against schemas
    """
    
    def __init__(self, agent):
        """
        Initialize structured processing tasks with a CrewAI agent.
        
        Args:
            agent: The CrewAI agent that will execute these tasks
        """
        self.agent = agent
        logger.info("StructuredProcessingTasks initialized")

    def process_financial_reports(self) -> Task:
        """
        Create a task for processing financial reports and extracting structured data.
        
        This task:
        - Analyzes raw content from financial reports (PDF text or scraped text)
        - Extracts key financial metrics, dates, currency, ratings
        - Maps data to 'Resumen_Informe_Financiero' and 'Informe_General' schemas
        - Handles variations in report formats gracefully
        
        Returns:
            CrewAI Task for financial report processing
        """
        return Task(
            description=(
                "Analyze raw content from financial reports (PDF text or scraped text related to balances/reports).\n"
                "Extract key financial metrics, dates, currency, ratings, and other relevant structured data points "
                "based on the 'Resumen_Informe_Financiero' and 'Informe_General' Supabase schemas.\n"
                "Handle potential variations in report formats and missing data gracefully.\n"
                "The output should be a structured dictionary or list of dictionaries conforming to the schema.\n"
                "Focus on extracting: total assets, total liabilities, net equity, operational income/expenses, "
                "net result, currency, risk rating, and other financial metrics.\n"
                "For dates, ensure they are in YYYY-MM-DD format.\n"
                "For numeric values, ensure they are actual numbers, not strings."
            ),
            expected_output=(
                "A dictionary or list of dictionaries, each representing a record for the Supabase tables "
                "'Resumen_Informe_Financiero' and/or 'Informe_General', containing extracted structured data "
                "(e.g., {'fecha_corte_informe': 'YYYY-MM-DD', 'activos_totales': 12345.67, 'moneda_informe': 1, ...}). "
                "Include necessary foreign keys like 'id_emisor' if identifiable from the source or context. "
                "Ensure all required fields are present and data types are correct."
            ),
            agent=self.agent,
            callback=lambda output: logger.info(f"Financial reports processing completed. Output type: {type(output)}")
        )

    def process_daily_movements_json(self) -> Task:
        """
        Create a task for processing daily movements JSON data.
        
        This task:
        - Parses raw JSON content from daily market movement reports
        - Extracts all relevant fields for the 'Movimiento_Diario_Bolsa' schema
        - Ensures data types are correct for database insertion
        
        Returns:
            CrewAI Task for daily movements processing
        """
        return Task(
            description=(
                "Parse the raw JSON content from daily market movement reports.\n"
                "Extract all relevant fields such as date, quantity, price, instrument ID, issuer ID, currency, etc., "
                "according to the 'Movimiento_Diario_Bolsa' Supabase schema.\n"
                "Ensure data types are correct for database insertion.\n"
                "Handle both single records and arrays of movement records.\n"
                "For dates, ensure they are in YYYY-MM-DD format.\n"
                "For numeric values (quantities, prices, amounts), ensure they are actual numbers."
            ),
            expected_output=(
                "A list of dictionaries, where each dictionary represents a record for the 'Movimiento_Diario_Bolsa' "
                "Supabase table, containing parsed JSON data (e.g., [{'fecha_operacion': 'YYYY-MM-DD', 'cantidad_operacion': 1000.00, ...}]). "
                "Ensure all required fields are present and data types are correct."
            ),
            agent=self.agent,
            callback=lambda output: logger.info(f"Daily movements processing completed. Records: {len(output) if isinstance(output, list) else 1}")
        )

    def process_macroeconomic_data(self) -> Task:
        """
        Create a task for processing macroeconomic data.
        
        This task:
        - Analyzes raw content related to macroeconomic indicators
        - Extracts specific indicators, values, dates, units of measure
        - Maps data to the 'Dato_Macroeconomico' schema
        
        Returns:
            CrewAI Task for macroeconomic data processing
        """
        return Task(
            description=(
                "Analyze raw content (text from pages, content from reports/spreadsheets) related to macroeconomic data.\n"
                "Identify and extract specific macroeconomic indicators, their values, dates, units of measure, frequency, "
                "and source links, mapping them to the 'Dato_Macroeconomico' Supabase schema.\n"
                "Handle different formats and potential ambiguity in text.\n"
                "Focus on indicators like: inflation, GDP, unemployment, interest rates, exchange rates, etc.\n"
                "For dates, ensure they are in YYYY-MM-DD format.\n"
                "For numeric values, ensure they are actual numbers."
            ),
            expected_output=(
                "A dictionary or list of dictionaries, each representing a record for the 'Dato_Macroeconomico' Supabase table, "
                "containing extracted macroeconomic data (e.g., {'indicador_nombre': 'Inflacion', 'fecha_dato': 'YYYY-MM-DD', 'valor_numerico': 5.2, ...}). "
                "Include relevant foreign keys ('unidad_medida', 'id_frecuencia', 'id_moneda', 'id_emisor' if applicable) by looking up or inferring IDs. "
                "Ensure all required fields are present."
            ),
            agent=self.agent,
            callback=lambda output: logger.info(f"Macroeconomic data processing completed. Output type: {type(output)}")
        )

    def process_public_contracts(self) -> Task:
        """
        Create a task for processing public contracts and tenders.
        
        This task:
        - Extracts structured information about public tenders and contracts
        - Identifies key fields for the 'Licitacion_Contrato' schema
        - Handles variations in text structure
        
        Returns:
            CrewAI Task for public contracts processing
        """
        return Task(
            description=(
                "Extract structured information about public tenders and contracts from raw text content.\n"
                "Identify key fields such as title, contracting entity, awarded amount, currency, "
                "and award date, mapping them to the 'Licitacion_Contrato' Supabase schema.\n"
                "Handle variations in text structure and extract accurate numerical and date values.\n"
                "Focus on extracting: contract title, description, awarded amount, award date, start/end dates, "
                "awarded entity, currency, and tender status.\n"
                "For dates, ensure they are in YYYY-MM-DD format.\n"
                "For amounts, ensure they are actual numbers."
            ),
            expected_output=(
                "A dictionary or list of dictionaries, each representing a record for the 'Licitacion_Contrato' Supabase table, "
                "containing extracted contract data (e.g., {'titulo': 'Adquisicion de Servicios', 'monto_adjudicado': 150000.00, 'fecha_adjudicacion': 'YYYY-MM-DD', ...}). "
                "Include 'id_emisor_adjudicado' if the awarded entity can be identified and mapped to an existing emitter. "
                "Ensure all required fields are present."
            ),
            agent=self.agent,
            callback=lambda output: logger.info(f"Public contracts processing completed. Output type: {type(output)}")
        )

    def process_general_reports_metadata(self) -> Task:
        """
        Create a task for processing general report metadata.
        
        This task:
        - Extracts general metadata from various reports and documents
        - Maps information to the 'Informe_General' schema
        - Handles documents that don't fit specific schemas
        
        Returns:
            CrewAI Task for general reports metadata processing
        """
        return Task(
            description=(
                "Extract general metadata from various reports and documents (annual reports, investment data, etc.) "
                "that don't fit specifically into financial, macroeconomic, or contract schemas, "
                "but provide context about the document itself.\n"
                "Map this information to the 'Informe_General' Supabase schema fields like title, publication date, summary (if available).\n"
                "Focus on extracting: report title, summary, publication date, issuer information, "
                "report type, frequency, period, and source URL.\n"
                "For dates, ensure they are in YYYY-MM-DD format."
            ),
            expected_output=(
                "A dictionary or list of dictionaries, each representing a record for the 'Informe_General' Supabase table, "
                "containing general report metadata (e.g., {'titulo_informe': 'Informe Anual 2023', 'fecha_publicacion': 'YYYY-MM-DD', 'resumen_informe': '...'}). "
                "Include relevant foreign keys ('id_emisor', 'id_tipo_informe', 'id_frecuencia', 'id_periodo') by looking up or inferring IDs. "
                "Ensure all required fields are present."
            ),
            agent=self.agent,
            callback=lambda output: logger.info(f"General reports metadata processing completed. Output type: {type(output)}")
        )

    def validate_structured_data(self) -> Task:
        """
        Create a task for validating extracted structured data.
        
        This task:
        - Validates that extracted data conforms to schema requirements
        - Checks for missing required fields
        - Ensures data types are correct
        
        Returns:
            CrewAI Task for data validation
        """
        return Task(
            description=(
                "Validate the extracted structured data against the appropriate Supabase schemas.\n"
                "Check that all required fields are present and have appropriate values.\n"
                "Verify that data types are correct (dates in YYYY-MM-DD format, numbers as numeric values, etc.).\n"
                "Identify any validation issues or missing information.\n"
                "Return a validation report with status and any issues found."
            ),
            expected_output=(
                "A validation report dictionary containing:\n"
                "- 'validation_results': List of validation results for each processed item\n"
                "- 'total_items': Number of items processed (int)\n"
                "- 'valid_items': Number of valid items (int)\n"
                "- 'invalid_items': Number of invalid items (int)\n"
                "- 'issues': List of validation issues found (list of strings)\n"
                "- 'validated_data': The original data with validation status added"
            ),
            agent=self.agent,
            callback=lambda output: logger.info(f"Data validation completed. {output.get('valid_items', 0)}/{output.get('total_items', 0)} items valid")
        )

    def process_content_by_type(self, content_type: str) -> Task:
        """
        Create a task for processing content based on its type.
        
        Args:
            content_type: The type of content to process (e.g., 'financial', 'movements', 'macroeconomic')
            
        Returns:
            CrewAI Task for specific content type processing
        """
        content_type_descriptions = {
            'financial': 'financial reports and balance sheets',
            'movements': 'daily market movements and transactions',
            'macroeconomic': 'macroeconomic indicators and statistics',
            'contracts': 'public contracts and tenders',
            'general': 'general report metadata and information'
        }
        
        description = content_type_descriptions.get(content_type, content_type)
        
        return Task(
            description=(
                f"Process {description} from the provided raw content.\n"
                f"Apply appropriate extraction methods for {content_type} content.\n"
                f"Map the extracted data to the corresponding Supabase schema.\n"
                f"Ensure all required fields are extracted and data types are correct."
            ),
            expected_output=(
                f"Structured data extracted from {description}, conforming to the appropriate Supabase schema.\n"
                "The output should be a dictionary or list of dictionaries with all required fields present "
                "and data types correctly formatted."
            ),
            agent=self.agent,
            callback=lambda output: logger.info(f"{content_type} content processing completed. Output type: {type(output)}")
        ) 