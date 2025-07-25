"""
Vectorization Agent Module

This module defines the CrewAI agent for vectorization operations.
"""

from crewai import Agent
from crewai.tools import tool
from typing import List, Dict, Any, Union, Optional
import logging
import requests
import os
from dotenv import load_dotenv

from .vectorization_logic import VectorizationLogic
from .pinecone_schemas import PINECONE_SCHEMAS, get_pinecone_schema_info, validate_index_exists

logger = logging.getLogger(__name__)

# Load environment variables for model connections
load_dotenv('.env.local')

@tool
def chunk_and_embed_tool(content: Union[str, Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    A tool to chunk text content and generate embeddings.
    
    This tool uses the VectorizationLogic to split content into chunks and generate
    embeddings for each chunk using the remote embedding model.
    
    Args:
        content: The content to process (text, JSON dict, or file path)
        
    Returns:
        List of dictionaries containing chunks and their embeddings
    """
    logger.info("Chunk and embed tool called")
    
    try:
        # Create vectorization logic instance
        vectorization_logic = VectorizationLogic()
        
        # Chunk and embed content
        chunk_embeddings = vectorization_logic.chunk_and_embed_content(content)
        
        if chunk_embeddings:
            logger.info(f"Successfully processed content. Chunks: {len(chunk_embeddings)}")
            return chunk_embeddings
        else:
            logger.warning("No chunk embeddings generated")
            return []
            
    except Exception as e:
        logger.error(f"Error in chunk_and_embed_tool: {e}")
        return []

@tool
def prepare_pinecone_vectors_tool(
    chunk_embeddings: List[Dict[str, Any]], 
    source_info: Dict[str, Any], 
    index_name: str
) -> List[Dict[str, Any]]:
    """
    A tool to prepare vectors for Pinecone storage.
    
    Args:
        chunk_embeddings: List of chunks with embeddings
        source_info: Information about the source content
        index_name: Name of the target Pinecone index
        
    Returns:
        List of vectors ready for Pinecone upsert
    """
    logger.info(f"Prepare Pinecone vectors tool called for index: {index_name}")
    
    try:
        # Create vectorization logic instance
        vectorization_logic = VectorizationLogic()
        
        # Prepare vectors for Pinecone
        vectors = vectorization_logic.prepare_pinecone_metadata(chunk_embeddings, source_info, index_name)
        
        if vectors:
            logger.info(f"Successfully prepared {len(vectors)} vectors for Pinecone")
            return vectors
        else:
            logger.warning("No vectors prepared for Pinecone")
            return []
            
    except Exception as e:
        logger.error(f"Error in prepare_pinecone_vectors_tool: {e}")
        return []

@tool
def process_financial_documents_tool(
    content: Union[str, Dict[str, Any]], 
    source_info: Dict[str, Any]
) -> List[Dict[str, Any]]:
    """
    A tool to process financial documents for vectorization.
    
    Args:
        content: Financial document content
        source_info: Information about the source document
        
    Returns:
        List of vectors ready for financial documents index
    """
    logger.info("Process financial documents tool called")
    
    try:
        # Create vectorization logic instance
        vectorization_logic = VectorizationLogic()
        
        # Process content for financial documents index
        vectors = vectorization_logic.process_content_for_index(
            content, 
            source_info, 
            "documentos-informes-vector"
        )
        
        if vectors:
            logger.info(f"Successfully processed financial documents. Vectors: {len(vectors)}")
            return vectors
        else:
            logger.warning("No vectors generated for financial documents")
            return []
            
    except Exception as e:
        logger.error(f"Error in process_financial_documents_tool: {e}")
        return []

@tool
def process_macroeconomic_data_tool(
    content: Union[str, Dict[str, Any]], 
    source_info: Dict[str, Any]
) -> List[Dict[str, Any]]:
    """
    A tool to process macroeconomic data for vectorization.
    
    Args:
        content: Macroeconomic data content
        source_info: Information about the source data
        
    Returns:
        List of vectors ready for macroeconomic data index
    """
    logger.info("Process macroeconomic data tool called")
    
    try:
        # Create vectorization logic instance
        vectorization_logic = VectorizationLogic()
        
        # Process content for macroeconomic data index
        vectors = vectorization_logic.process_content_for_index(
            content, 
            source_info, 
            "dato-macroeconomico-vector"
        )
        
        if vectors:
            logger.info(f"Successfully processed macroeconomic data. Vectors: {len(vectors)}")
            return vectors
        else:
            logger.warning("No vectors generated for macroeconomic data")
            return []
            
    except Exception as e:
        logger.error(f"Error in process_macroeconomic_data_tool: {e}")
        return []

@tool
def process_public_contracts_tool(
    content: Union[str, Dict[str, Any]], 
    source_info: Dict[str, Any]
) -> List[Dict[str, Any]]:
    """
    A tool to process public contracts for vectorization.
    
    Args:
        content: Public contract content
        source_info: Information about the source contract
        
    Returns:
        List of vectors ready for public contracts index
    """
    logger.info("Process public contracts tool called")
    
    try:
        # Create vectorization logic instance
        vectorization_logic = VectorizationLogic()
        
        # Process content for public contracts index
        vectors = vectorization_logic.process_content_for_index(
            content, 
            source_info, 
            "licitacion-contrato-vector"
        )
        
        if vectors:
            logger.info(f"Successfully processed public contracts. Vectors: {len(vectors)}")
            return vectors
        else:
            logger.warning("No vectors generated for public contracts")
            return []
            
    except Exception as e:
        logger.error(f"Error in process_public_contracts_tool: {e}")
        return []

@tool
def process_news_content_tool(
    content: Union[str, Dict[str, Any]], 
    source_info: Dict[str, Any]
) -> List[Dict[str, Any]]:
    """
    A tool to process news content for vectorization.
    
    Args:
        content: News content
        source_info: Information about the source news
        
    Returns:
        List of vectors ready for news content index
    """
    logger.info("Process news content tool called")
    
    try:
        # Create vectorization logic instance
        vectorization_logic = VectorizationLogic()
        
        # Process content for news content index
        vectors = vectorization_logic.process_content_for_index(
            content, 
            source_info, 
            "noticia-relevante-vector"
        )
        
        if vectors:
            logger.info(f"Successfully processed news content. Vectors: {len(vectors)}")
            return vectors
        else:
            logger.warning("No vectors generated for news content")
            return []
            
    except Exception as e:
        logger.error(f"Error in process_news_content_tool: {e}")
        return []

@tool
def validate_vector_data_tool(vectors: List[Dict[str, Any]], index_name: str) -> Dict[str, Any]:
    """
    A tool to validate vector data before storage.
    
    Args:
        vectors: List of vectors to validate
        index_name: Name of the target index
        
    Returns:
        Validation result with status and issues
    """
    logger.info(f"Validate vector data tool called for index: {index_name}")
    
    try:
        # Create vectorization logic instance
        vectorization_logic = VectorizationLogic()
        
        # Validate vectors
        total_vectors = len(vectors)
        valid_vectors = 0
        invalid_vectors = 0
        issues = []
        
        for i, vector in enumerate(vectors):
            # Check basic structure
            if not all(key in vector for key in ['id', 'values', 'metadata']):
                invalid_vectors += 1
                issues.append(f"Vector {i}: Missing required fields (id, values, metadata)")
                continue
            
            # Check embedding dimension
            if len(vector['values']) != 384:  # sentence-transformers/all-MiniLM-L6-v2 dimension
                invalid_vectors += 1
                issues.append(f"Vector {i}: Incorrect embedding dimension {len(vector['values'])} (expected 384)")
                continue
            
            # Validate metadata completeness
            validation = vectorization_logic.prepare_pinecone_metadata(
                [{'chunk_text': vector['metadata'].get('chunk_text', ''), 'embedding': vector['values'], 'chunk_id': i}],
                vector['metadata'],
                index_name
            )
            
            if validation:
                valid_vectors += 1
            else:
                invalid_vectors += 1
                issues.append(f"Vector {i}: Metadata validation failed")
        
        validation_result = {
            'total_vectors': total_vectors,
            'valid_vectors': valid_vectors,
            'invalid_vectors': invalid_vectors,
            'issues': issues,
            'validated_vectors': vectors,
            'embedding_dimension': 384
        }
        
        logger.info(f"Validation completed. {valid_vectors}/{total_vectors} vectors valid")
        return validation_result
        
    except Exception as e:
        logger.error(f"Error in validate_vector_data_tool: {e}")
        return {
            'total_vectors': len(vectors),
            'valid_vectors': 0,
            'invalid_vectors': len(vectors),
            'issues': [f"Validation error: {str(e)}"],
            'validated_vectors': vectors,
            'embedding_dimension': 384
        }

class VectorizationAgent:
    """
    CrewAI agent for vectorization operations.
    
    This agent is responsible for:
    - Chunking text content and generating embeddings
    - Preparing metadata for Pinecone vector storage
    - Processing different content types for vector databases
    - Validating vector data before storage
    - Coordinating vectorization tasks using the remote embedding model
    """
    
    def __init__(self, llm=None):
        """
        Initialize the vectorization agent.
        
        Args:
            llm: Language model for the agent (will use remote Mistral if not provided)
        """
        self.llm = llm or self._get_remote_mistral_llm()
        self.agent = self._create_agent()
        logger.info("VectorizationAgent initialized")

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
        Create the CrewAI vectorization agent.
        
        Returns:
            Configured CrewAI Agent for vectorization
        """
        return Agent(
            role='Vectorization Specialist',
            goal='Transform raw content into vector embeddings ready for storage in Pinecone.',
            backstory=(
                "You are an expert in text processing, chunking, and vector embedding generation. "
                "You understand how to split large documents into meaningful chunks while preserving context. "
                "You work with advanced embedding models to convert text into high-dimensional vectors. "
                "You are meticulous about metadata preparation and ensure all vectors are properly structured "
                "for vector database storage. You handle various content types and adapt your processing accordingly."
            ),
            tools=[
                chunk_and_embed_tool,
                prepare_pinecone_vectors_tool,
                process_financial_documents_tool,
                process_macroeconomic_data_tool,
                process_public_contracts_tool,
                process_news_content_tool,
                validate_vector_data_tool
            ],
            verbose=True,
            allow_delegation=False,  # This agent focuses only on vectorization
            llm=self.llm
        )

    def get_agent(self) -> Agent:
        """
        Get the configured CrewAI agent.
        
        Returns:
            The vectorization agent
        """
        return self.agent

    def test_connection(self) -> Dict[str, Any]:
        """
        Test the connection to the remote embedding model.
        
        Returns:
            Dictionary with connection status and details
        """
        try:
            vectorization_logic = VectorizationLogic()
            connection_result = vectorization_logic.test_embedding_connection()
            
            return connection_result
                
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Connection test failed: {str(e)}'
            }

    def get_available_indexes(self) -> List[str]:
        """
        Get list of available Pinecone indexes.
        
        Returns:
            List of available index names
        """
        return list(PINECONE_SCHEMAS.keys())

    def get_index_info(self, index_name: str) -> Dict[str, Any]:
        """
        Get information about a specific Pinecone index.
        
        Args:
            index_name: Name of the index
            
        Returns:
            Index information dictionary
        """
        return get_pinecone_schema_info(index_name) 