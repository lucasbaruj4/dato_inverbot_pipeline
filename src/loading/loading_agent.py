"""
Loading Agent Module

This module defines the CrewAI agent for loading operations.
"""

from crewai import Agent
from crewai.tools import tool
from typing import List, Dict, Any, Union, Optional
import logging
import os
from dotenv import load_dotenv

from .loading_logic import LoadingLogic
from .database_connectors import SupabaseConnector, PineconeConnector

logger = logging.getLogger(__name__)

# Load environment variables for model connections
load_dotenv('.env.local')

@tool
def load_structured_data_tool(table_name: str, data: Union[Dict[str, Any], List[Dict[str, Any]]]) -> Dict[str, Any]:
    """
    A tool to load structured data into Supabase tables.
    
    Args:
        table_name: Name of the target table
        data: Data to insert (single record or list of records)
        
    Returns:
        Dictionary with loading status and details
    """
    logger.info(f"Load structured data tool called for table: {table_name}")
    
    try:
        # Create loading logic instance
        loading_logic = LoadingLogic()
        
        # Load structured data
        result = loading_logic.load_structured_data(table_name, data)
        
        if result['status'] == 'success':
            logger.info(f"Successfully loaded {result['inserted_count']} records into {table_name}")
        else:
            logger.error(f"Failed to load data into {table_name}: {result['message']}")
        
        return result
        
    except Exception as e:
        logger.error(f"Error in load_structured_data_tool: {e}")
        return {
            'status': 'error',
            'message': f'Loading failed: {str(e)}',
            'table': table_name
        }

@tool
def load_vector_data_tool(index_name: str, vectors: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    A tool to load vector data into Pinecone indexes.
    
    Args:
        index_name: Name of the target index
        vectors: List of vectors to upsert
        
    Returns:
        Dictionary with loading status and details
    """
    logger.info(f"Load vector data tool called for index: {index_name}")
    
    try:
        # Create loading logic instance
        loading_logic = LoadingLogic()
        
        # Load vector data
        result = loading_logic.load_vector_data(index_name, vectors)
        
        if result['status'] == 'success':
            logger.info(f"Successfully loaded {result['upserted_count']} vectors into {index_name}")
        else:
            logger.error(f"Failed to load vectors into {index_name}: {result['message']}")
        
        return result
        
    except Exception as e:
        logger.error(f"Error in load_vector_data_tool: {e}")
        return {
            'status': 'error',
            'message': f'Loading failed: {str(e)}',
            'index': index_name
        }

@tool
def load_financial_data_tool(financial_data: Dict[str, Any], vectors: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
    """
    A tool to load financial data into both databases.
    
    Args:
        financial_data: Structured financial data for Supabase
        vectors: Vector data for Pinecone (optional)
        
    Returns:
        Dictionary with loading results for both databases
    """
    logger.info("Load financial data tool called")
    
    try:
        # Create loading logic instance
        loading_logic = LoadingLogic()
        
        # Load financial data
        result = loading_logic.load_financial_data(financial_data, vectors)
        
        if result['overall_status'] == 'success':
            logger.info("Financial data loaded successfully into both databases")
        elif result['overall_status'] == 'partial':
            logger.warning("Financial data loaded partially (some databases failed)")
        else:
            logger.error("Financial data loading failed in all databases")
        
        return result
        
    except Exception as e:
        logger.error(f"Error in load_financial_data_tool: {e}")
        return {
            'status': 'error',
            'message': f'Loading failed: {str(e)}',
            'overall_status': 'failed'
        }

@tool
def load_macroeconomic_data_tool(macro_data: Dict[str, Any], vectors: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
    """
    A tool to load macroeconomic data into both databases.
    
    Args:
        macro_data: Structured macroeconomic data for Supabase
        vectors: Vector data for Pinecone (optional)
        
    Returns:
        Dictionary with loading results for both databases
    """
    logger.info("Load macroeconomic data tool called")
    
    try:
        # Create loading logic instance
        loading_logic = LoadingLogic()
        
        # Load macroeconomic data
        result = loading_logic.load_macroeconomic_data(macro_data, vectors)
        
        if result['overall_status'] == 'success':
            logger.info("Macroeconomic data loaded successfully into both databases")
        elif result['overall_status'] == 'partial':
            logger.warning("Macroeconomic data loaded partially (some databases failed)")
        else:
            logger.error("Macroeconomic data loading failed in all databases")
        
        return result
        
    except Exception as e:
        logger.error(f"Error in load_macroeconomic_data_tool: {e}")
        return {
            'status': 'error',
            'message': f'Loading failed: {str(e)}',
            'overall_status': 'failed'
        }

@tool
def load_public_contracts_tool(contract_data: Dict[str, Any], vectors: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
    """
    A tool to load public contract data into both databases.
    
    Args:
        contract_data: Structured contract data for Supabase
        vectors: Vector data for Pinecone (optional)
        
    Returns:
        Dictionary with loading results for both databases
    """
    logger.info("Load public contracts tool called")
    
    try:
        # Create loading logic instance
        loading_logic = LoadingLogic()
        
        # Load public contracts data
        result = loading_logic.load_public_contracts(contract_data, vectors)
        
        if result['overall_status'] == 'success':
            logger.info("Public contracts data loaded successfully into both databases")
        elif result['overall_status'] == 'partial':
            logger.warning("Public contracts data loaded partially (some databases failed)")
        else:
            logger.error("Public contracts data loading failed in all databases")
        
        return result
        
    except Exception as e:
        logger.error(f"Error in load_public_contracts_tool: {e}")
        return {
            'status': 'error',
            'message': f'Loading failed: {str(e)}',
            'overall_status': 'failed'
        }

@tool
def load_news_data_tool(news_data: Dict[str, Any], vectors: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
    """
    A tool to load news data into both databases.
    
    Args:
        news_data: Structured news data for Supabase
        vectors: Vector data for Pinecone (optional)
        
    Returns:
        Dictionary with loading results for both databases
    """
    logger.info("Load news data tool called")
    
    try:
        # Create loading logic instance
        loading_logic = LoadingLogic()
        
        # Load news data
        result = loading_logic.load_news_data(news_data, vectors)
        
        if result['overall_status'] == 'success':
            logger.info("News data loaded successfully into both databases")
        elif result['overall_status'] == 'partial':
            logger.warning("News data loaded partially (some databases failed)")
        else:
            logger.error("News data loading failed in all databases")
        
        return result
        
    except Exception as e:
        logger.error(f"Error in load_news_data_tool: {e}")
        return {
            'status': 'error',
            'message': f'Loading failed: {str(e)}',
            'overall_status': 'failed'
        }

@tool
def validate_data_tool(structured_data: Optional[Dict[str, Any]] = None, vector_data: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
    """
    A tool to validate data before loading.
    
    Args:
        structured_data: Structured data to validate
        vector_data: Vector data to validate
        
    Returns:
        Validation result with status and issues
    """
    logger.info("Validate data tool called")
    
    try:
        # Create loading logic instance
        loading_logic = LoadingLogic()
        
        # Validate structured data
        structured_valid = True
        structured_issues = []
        if structured_data:
            # This is a simplified validation - in practice you'd validate against specific table schemas
            if not isinstance(structured_data, dict):
                structured_valid = False
                structured_issues.append("Structured data is not a dictionary")
        
        # Validate vector data
        vector_valid = True
        vector_issues = []
        if vector_data:
            if not isinstance(vector_data, list):
                vector_valid = False
                vector_issues.append("Vector data is not a list")
            else:
                for i, vector in enumerate(vector_data):
                    if not isinstance(vector, dict):
                        vector_issues.append(f"Vector {i}: Not a dictionary")
                        vector_valid = False
                    elif 'id' not in vector or 'values' not in vector or 'metadata' not in vector:
                        vector_issues.append(f"Vector {i}: Missing required fields (id, values, metadata)")
                        vector_valid = False
                    elif not isinstance(vector['values'], list) or len(vector['values']) != 384:
                        vector_issues.append(f"Vector {i}: Invalid embedding dimension (expected 384)")
                        vector_valid = False
        
        overall_valid = structured_valid and vector_valid
        
        return {
            'structured_data_valid': structured_valid,
            'vector_data_valid': vector_valid,
            'structured_issues': structured_issues,
            'vector_issues': vector_issues,
            'overall_valid': overall_valid
        }
        
    except Exception as e:
        logger.error(f"Error in validate_data_tool: {e}")
        return {
            'structured_data_valid': False,
            'vector_data_valid': False,
            'structured_issues': [f'Validation error: {str(e)}'],
            'vector_issues': [f'Validation error: {str(e)}'],
            'overall_valid': False
        }

@tool
def test_connections_tool() -> Dict[str, Any]:
    """
    A tool to test database connections.
    
    Returns:
        Dictionary with connection status for both databases
    """
    logger.info("Test connections tool called")
    
    try:
        # Create loading logic instance
        loading_logic = LoadingLogic()
        
        # Test connections
        result = loading_logic.test_connections()
        
        if result['all_connected']:
            logger.info("All database connections successful")
        else:
            logger.warning("Some database connections failed")
        
        return result
        
    except Exception as e:
        logger.error(f"Error in test_connections_tool: {e}")
        return {
            'supabase': {'status': 'error', 'message': str(e)},
            'pinecone': {'status': 'error', 'message': str(e)},
            'all_connected': False
        }

@tool
def get_loading_statistics_tool() -> Dict[str, Any]:
    """
    A tool to get loading statistics.
    
    Returns:
        Dictionary with loading statistics
    """
    logger.info("Get loading statistics tool called")
    
    try:
        # Create loading logic instance
        loading_logic = LoadingLogic()
        
        # Get statistics
        result = loading_logic.get_loading_statistics()
        
        return result
        
    except Exception as e:
        logger.error(f"Error in get_loading_statistics_tool: {e}")
        return {
            'error': str(e)
        }

class LoadingAgent:
    """
    CrewAI agent for loading operations.
    
    This agent is responsible for:
    - Loading structured data into Supabase tables
    - Loading vector data into Pinecone indexes
    - Coordinating loading operations between databases
    - Validating data before loading
    - Handling loading errors and recovery
    - Providing loading statistics and monitoring
    """
    
    def __init__(self, llm=None):
        """
        Initialize the loading agent.
        
        Args:
            llm: Language model for the agent (will use remote Mistral if not provided)
        """
        self.llm = llm or self._get_remote_mistral_llm()
        self.agent = self._create_agent()
        logger.info("LoadingAgent initialized")

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
        Create the CrewAI loading agent.
        
        Returns:
            Configured CrewAI Agent for loading operations
        """
        return Agent(
            role='Data Loading Specialist',
            goal='Efficiently load processed data into both Supabase and Pinecone databases while ensuring data integrity and consistency.',
            backstory=(
                "You are an expert in database operations and data loading pipelines. "
                "You understand the complexities of loading data into both structured (Supabase) "
                "and vector (Pinecone) databases. You are meticulous about data validation, "
                "error handling, and ensuring data consistency across multiple databases. "
                "You have extensive experience with PostgreSQL, vector databases, and "
                "coordinating complex loading operations. You always prioritize data integrity "
                "and provide detailed feedback on loading operations."
            ),
            tools=[
                load_structured_data_tool,
                load_vector_data_tool,
                load_financial_data_tool,
                load_macroeconomic_data_tool,
                load_public_contracts_tool,
                load_news_data_tool,
                validate_data_tool,
                test_connections_tool,
                get_loading_statistics_tool
            ],
            verbose=True,
            allow_delegation=False,  # This agent focuses only on loading
            llm=self.llm
        )

    def get_agent(self) -> Agent:
        """
        Get the configured CrewAI agent.
        
        Returns:
            The loading agent
        """
        return self.agent

    def test_connections(self) -> Dict[str, Any]:
        """
        Test the connections to both databases.
        
        Returns:
            Dictionary with connection status for both databases
        """
        try:
            loading_logic = LoadingLogic()
            connection_result = loading_logic.test_connections()
            
            return connection_result
                
        except Exception as e:
            return {
                'supabase': {'status': 'error', 'message': str(e)},
                'pinecone': {'status': 'error', 'message': str(e)},
                'all_connected': False
            }

    def get_loading_statistics(self) -> Dict[str, Any]:
        """
        Get loading statistics and database status.
        
        Returns:
            Dictionary with loading statistics
        """
        try:
            loading_logic = LoadingLogic()
            stats = loading_logic.get_loading_statistics()
            
            return stats
            
        except Exception as e:
            return {
                'error': str(e)
            }

    def get_available_tables(self) -> List[str]:
        """
        Get list of available Supabase tables.
        
        Returns:
            List of available table names
        """
        return [
            'resumen_informe_financiero',
            'dato_macroeconomico',
            'licitacion_contrato',
            'noticia_relevante',
            'informe_general',
            'movimiento_diario_bolsa',
            'emisores'
        ]

    def get_available_indexes(self) -> List[str]:
        """
        Get list of available Pinecone indexes.
        
        Returns:
            List of available index names
        """
        return [
            'documentos-informes-vector',
            'noticia-relevante-vector',
            'dato-macroeconomico-vector',
            'licitacion-contrato-vector'
        ] 