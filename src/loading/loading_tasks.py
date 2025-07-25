"""
Loading Tasks Module

This module defines the CrewAI tasks for loading operations.
"""

from crewai import Task
from typing import List, Dict, Any, Union, Optional
import logging

logger = logging.getLogger(__name__)

class LoadingTasks:
    """
    Task definitions for the loading stage of the pipeline.
    
    This class provides CrewAI tasks for:
    - Loading structured data into Supabase
    - Loading vector data into Pinecone
    - Coordinating loading operations between databases
    - Validating data before loading
    - Handling loading errors and recovery
    """
    
    def __init__(self, agent):
        """
        Initialize loading tasks with a CrewAI agent.
        
        Args:
            agent: The CrewAI agent that will execute these tasks
        """
        self.agent = agent
        logger.info("LoadingTasks initialized")

    def load_structured_data(self) -> Task:
        """
        Create a task for loading structured data into Supabase.
        
        This task:
        - Takes processed structured data and loads it into appropriate Supabase tables
        - Validates data before insertion
        - Handles different table schemas and requirements
        - Returns loading status and results
        
        Returns:
            CrewAI Task for structured data loading
        """
        return Task(
            description=(
                "Load structured data into Supabase PostgreSQL database.\n"
                "Take the processed structured data and insert it into the appropriate Supabase tables.\n"
                "Validate the data before insertion to ensure it meets schema requirements.\n"
                "Handle different table types:\n"
                "- Financial reports: resumen_informe_financiero table\n"
                "- Macroeconomic data: dato_macroeconomico table\n"
                "- Public contracts: licitacion_contrato table\n"
                "- News content: noticia_relevante table\n"
                "- General reports: informe_general table\n"
                "- Stock movements: movimiento_diario_bolsa table\n"
                "- Issuers: emisores table\n"
                "Ensure all required fields are present and data types are correct.\n"
                "Return detailed loading results including success/failure status and record counts."
            ),
            expected_output=(
                "A dictionary containing loading results with:\n"
                "- 'status': 'success' or 'error' (string)\n"
                "- 'message': Description of the operation result (string)\n"
                "- 'table': Name of the table where data was loaded (string)\n"
                "- 'inserted_count': Number of records successfully inserted (integer)\n"
                "- 'data': The inserted data (list of dictionaries)\n"
                "Include any validation errors or database errors in the message."
            ),
            agent=self.agent,
            callback=lambda output: logger.info(f"Structured data loading completed. Status: {output.get('status', 'unknown')}")
        )

    def load_vector_data(self) -> Task:
        """
        Create a task for loading vector data into Pinecone.
        
        This task:
        - Takes processed vector data and loads it into appropriate Pinecone indexes
        - Validates vector structure and metadata
        - Handles different index types and schemas
        - Returns loading status and results
        
        Returns:
            CrewAI Task for vector data loading
        """
        return Task(
            description=(
                "Load vector data into Pinecone vector database.\n"
                "Take the processed vector data and upsert it into the appropriate Pinecone indexes.\n"
                "Validate vector structure before insertion:\n"
                "- Ensure each vector has 'id', 'values', and 'metadata' fields\n"
                "- Verify embedding dimension is 384 (sentence-transformers/all-MiniLM-L6-v2)\n"
                "- Check metadata completeness according to index schema\n"
                "Handle different index types:\n"
                "- Financial documents: documentos-informes-vector index\n"
                "- News content: noticia-relevante-vector index\n"
                "- Macroeconomic data: dato-macroeconomico-vector index\n"
                "- Public contracts: licitacion-contrato-vector index\n"
                "Ensure proper vector IDs and metadata formatting.\n"
                "Return detailed loading results including success/failure status and vector counts."
            ),
            expected_output=(
                "A dictionary containing loading results with:\n"
                "- 'status': 'success' or 'error' (string)\n"
                "- 'message': Description of the operation result (string)\n"
                "- 'index': Name of the index where vectors were loaded (string)\n"
                "- 'upserted_count': Number of vectors successfully upserted (integer)\n"
                "Include any validation errors or database errors in the message."
            ),
            agent=self.agent,
            callback=lambda output: logger.info(f"Vector data loading completed. Status: {output.get('status', 'unknown')}")
        )

    def load_financial_data(self) -> Task:
        """
        Create a task for loading financial data into both databases.
        
        This task:
        - Loads financial report data into Supabase resumen_informe_financiero table
        - Loads corresponding vectors into Pinecone documentos-informes-vector index
        - Coordinates loading between both databases
        - Returns comprehensive loading results
        
        Returns:
            CrewAI Task for financial data loading
        """
        return Task(
            description=(
                "Load financial data into both Supabase and Pinecone databases.\n"
                "Take financial report data and load it into the appropriate databases:\n"
                "- Structured data: Insert into Supabase 'resumen_informe_financiero' table\n"
                "- Vector data: Upsert into Pinecone 'documentos-informes-vector' index\n"
                "Coordinate the loading process to ensure data consistency.\n"
                "Validate both structured and vector data before loading.\n"
                "Handle any errors in either database and provide detailed feedback.\n"
                "Ensure proper linking between structured records and vector embeddings."
            ),
            expected_output=(
                "A dictionary containing comprehensive loading results with:\n"
                "- 'supabase': Results from Supabase loading operation\n"
                "- 'pinecone': Results from Pinecone loading operation\n"
                "- 'overall_status': 'success', 'partial', or 'failed' (string)\n"
                "Each database result should include status, message, and record/vector counts."
            ),
            agent=self.agent,
            callback=lambda output: logger.info(f"Financial data loading completed. Overall status: {output.get('overall_status', 'unknown')}")
        )

    def load_macroeconomic_data(self) -> Task:
        """
        Create a task for loading macroeconomic data into both databases.
        
        This task:
        - Loads macroeconomic indicators into Supabase dato_macroeconomico table
        - Loads corresponding vectors into Pinecone dato-macroeconomico-vector index
        - Coordinates loading between both databases
        - Returns comprehensive loading results
        
        Returns:
            CrewAI Task for macroeconomic data loading
        """
        return Task(
            description=(
                "Load macroeconomic data into both Supabase and Pinecone databases.\n"
                "Take macroeconomic indicator data and load it into the appropriate databases:\n"
                "- Structured data: Insert into Supabase 'dato_macroeconomico' table\n"
                "- Vector data: Upsert into Pinecone 'dato-macroeconomico-vector' index\n"
                "Coordinate the loading process to ensure data consistency.\n"
                "Validate both structured and vector data before loading.\n"
                "Handle any errors in either database and provide detailed feedback.\n"
                "Ensure proper linking between structured records and vector embeddings."
            ),
            expected_output=(
                "A dictionary containing comprehensive loading results with:\n"
                "- 'supabase': Results from Supabase loading operation\n"
                "- 'pinecone': Results from Pinecone loading operation\n"
                "- 'overall_status': 'success', 'partial', or 'failed' (string)\n"
                "Each database result should include status, message, and record/vector counts."
            ),
            agent=self.agent,
            callback=lambda output: logger.info(f"Macroeconomic data loading completed. Overall status: {output.get('overall_status', 'unknown')}")
        )

    def load_public_contracts(self) -> Task:
        """
        Create a task for loading public contract data into both databases.
        
        This task:
        - Loads public contract data into Supabase licitacion_contrato table
        - Loads corresponding vectors into Pinecone licitacion-contrato-vector index
        - Coordinates loading between both databases
        - Returns comprehensive loading results
        
        Returns:
            CrewAI Task for public contracts loading
        """
        return Task(
            description=(
                "Load public contract data into both Supabase and Pinecone databases.\n"
                "Take public contract and tender data and load it into the appropriate databases:\n"
                "- Structured data: Insert into Supabase 'licitacion_contrato' table\n"
                "- Vector data: Upsert into Pinecone 'licitacion-contrato-vector' index\n"
                "Coordinate the loading process to ensure data consistency.\n"
                "Validate both structured and vector data before loading.\n"
                "Handle any errors in either database and provide detailed feedback.\n"
                "Ensure proper linking between structured records and vector embeddings."
            ),
            expected_output=(
                "A dictionary containing comprehensive loading results with:\n"
                "- 'supabase': Results from Supabase loading operation\n"
                "- 'pinecone': Results from Pinecone loading operation\n"
                "- 'overall_status': 'success', 'partial', or 'failed' (string)\n"
                "Each database result should include status, message, and record/vector counts."
            ),
            agent=self.agent,
            callback=lambda output: logger.info(f"Public contracts loading completed. Overall status: {output.get('overall_status', 'unknown')}")
        )

    def load_news_data(self) -> Task:
        """
        Create a task for loading news data into both databases.
        
        This task:
        - Loads news content into Supabase noticia_relevante table
        - Loads corresponding vectors into Pinecone noticia-relevante-vector index
        - Coordinates loading between both databases
        - Returns comprehensive loading results
        
        Returns:
            CrewAI Task for news data loading
        """
        return Task(
            description=(
                "Load news data into both Supabase and Pinecone databases.\n"
                "Take news and market information data and load it into the appropriate databases:\n"
                "- Structured data: Insert into Supabase 'noticia_relevante' table\n"
                "- Vector data: Upsert into Pinecone 'noticia-relevante-vector' index\n"
                "Coordinate the loading process to ensure data consistency.\n"
                "Validate both structured and vector data before loading.\n"
                "Handle any errors in either database and provide detailed feedback.\n"
                "Ensure proper linking between structured records and vector embeddings."
            ),
            expected_output=(
                "A dictionary containing comprehensive loading results with:\n"
                "- 'supabase': Results from Supabase loading operation\n"
                "- 'pinecone': Results from Pinecone loading operation\n"
                "- 'overall_status': 'success', 'partial', or 'failed' (string)\n"
                "Each database result should include status, message, and record/vector counts."
            ),
            agent=self.agent,
            callback=lambda output: logger.info(f"News data loading completed. Overall status: {output.get('overall_status', 'unknown')}")
        )

    def validate_data_before_loading(self) -> Task:
        """
        Create a task for validating data before loading.
        
        This task:
        - Validates structured data against Supabase table schemas
        - Validates vector data against Pinecone index requirements
        - Checks data completeness and format
        - Returns validation results
        
        Returns:
            CrewAI Task for data validation
        """
        return Task(
            description=(
                "Validate data before loading into databases.\n"
                "Perform comprehensive validation on both structured and vector data:\n"
                "For structured data:\n"
                "- Check required fields are present for each table\n"
                "- Validate data types and formats\n"
                "- Ensure referential integrity where applicable\n"
                "For vector data:\n"
                "- Verify vector structure (id, values, metadata)\n"
                "- Check embedding dimensions (384 for sentence-transformers/all-MiniLM-L6-v2)\n"
                "- Validate metadata completeness according to index schemas\n"
                "Return detailed validation results with any issues found."
            ),
            expected_output=(
                "A dictionary containing validation results with:\n"
                "- 'structured_data_valid': Boolean indicating if structured data is valid\n"
                "- 'vector_data_valid': Boolean indicating if vector data is valid\n"
                "- 'structured_issues': List of issues found in structured data\n"
                "- 'vector_issues': List of issues found in vector data\n"
                "- 'overall_valid': Boolean indicating if all data is valid for loading\n"
                "Include specific error messages and field-level validation details."
            ),
            agent=self.agent,
            callback=lambda output: logger.info(f"Data validation completed. Overall valid: {output.get('overall_valid', False)}")
        )

    def handle_loading_errors(self) -> Task:
        """
        Create a task for handling loading errors and recovery.
        
        This task:
        - Analyzes loading errors and provides recovery strategies
        - Handles partial failures and rollback scenarios
        - Provides error reporting and logging
        - Returns error handling results
        
        Returns:
            CrewAI Task for error handling
        """
        return Task(
            description=(
                "Handle loading errors and implement recovery strategies.\n"
                "Analyze any errors that occurred during the loading process:\n"
                "- Identify the type and cause of errors\n"
                "- Determine if errors are recoverable\n"
                "- Implement appropriate recovery strategies\n"
                "- Handle partial failures (success in one database, failure in another)\n"
                "- Provide rollback mechanisms where necessary\n"
                "Common error scenarios to handle:\n"
                "- Database connection failures\n"
                "- Schema validation errors\n"
                "- Data type mismatches\n"
                "- Duplicate key violations\n"
                "- Network timeouts\n"
                "Return detailed error analysis and recovery recommendations."
            ),
            expected_output=(
                "A dictionary containing error handling results with:\n"
                "- 'errors_found': List of errors encountered\n"
                "- 'error_types': Categorization of error types\n"
                "- 'recovery_strategies': List of recommended recovery actions\n"
                "- 'can_recover': Boolean indicating if recovery is possible\n"
                "- 'recommended_actions': Specific actions to take\n"
                "Include detailed error messages and recovery step-by-step instructions."
            ),
            agent=self.agent,
            callback=lambda output: logger.info(f"Error handling completed. Can recover: {output.get('can_recover', False)}")
        )

    def get_loading_statistics(self) -> Task:
        """
        Create a task for retrieving loading statistics.
        
        This task:
        - Retrieves loading statistics from both databases
        - Provides database health and performance metrics
        - Returns comprehensive statistics
        
        Returns:
            CrewAI Task for statistics retrieval
        """
        return Task(
            description=(
                "Retrieve loading statistics and database health metrics.\n"
                "Gather comprehensive statistics from both databases:\n"
                "For Supabase:\n"
                "- Connection status and health\n"
                "- Table record counts\n"
                "- Recent loading activity\n"
                "For Pinecone:\n"
                "- Index statistics and health\n"
                "- Vector counts per index\n"
                "- Index performance metrics\n"
                "Overall pipeline metrics:\n"
                "- Total records/vectors loaded\n"
                "- Success/failure rates\n"
                "- Processing times\n"
                "Return detailed statistics for monitoring and optimization."
            ),
            expected_output=(
                "A dictionary containing comprehensive statistics with:\n"
                "- 'connections': Database connection status\n"
                "- 'supabase_stats': Supabase-specific statistics\n"
                "- 'pinecone_stats': Pinecone-specific statistics\n"
                "- 'pipeline_stats': Overall pipeline metrics\n"
                "- 'health_status': Overall system health assessment\n"
                "Include specific metrics, counts, and performance indicators."
            ),
            agent=self.agent,
            callback=lambda output: logger.info(f"Statistics retrieval completed. Health status: {output.get('health_status', 'unknown')}")
        )

    def load_data_by_type(self, data_type: str) -> Task:
        """
        Create a task for loading data by specific type.
        
        Args:
            data_type: Type of data to load ('financial', 'macroeconomic', 'contracts', 'news')
            
        Returns:
            CrewAI Task for specific data type loading
        """
        data_type_descriptions = {
            'financial': 'financial reports and documents',
            'macroeconomic': 'macroeconomic indicators and statistics',
            'contracts': 'public contracts and tenders',
            'news': 'news articles and market information'
        }
        
        description = data_type_descriptions.get(data_type, data_type)
        
        return Task(
            description=(
                f"Load {data_type} data into both Supabase and Pinecone databases.\n"
                f"Take {description} and load it into the appropriate databases:\n"
                f"- Structured data: Insert into corresponding Supabase table\n"
                f"- Vector data: Upsert into corresponding Pinecone index\n"
                f"Coordinate the loading process to ensure data consistency.\n"
                f"Validate both structured and vector data before loading.\n"
                f"Handle any errors in either database and provide detailed feedback.\n"
                f"Ensure proper linking between structured records and vector embeddings."
            ),
            expected_output=(
                "A dictionary containing comprehensive loading results with:\n"
                "- 'supabase': Results from Supabase loading operation\n"
                "- 'pinecone': Results from Pinecone loading operation\n"
                "- 'overall_status': 'success', 'partial', or 'failed' (string)\n"
                "Each database result should include status, message, and record/vector counts."
            ),
            agent=self.agent,
            callback=lambda output: logger.info(f"{data_type} data loading completed. Overall status: {output.get('overall_status', 'unknown')}")
        ) 