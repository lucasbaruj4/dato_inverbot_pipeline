"""
Vectorization Tasks Module

This module defines the CrewAI tasks for vectorization operations.
"""

from crewai import Task
from typing import List, Dict, Any, Union
import logging

logger = logging.getLogger(__name__)

class VectorizationTasks:
    """
    Task definitions for the vectorization stage of the pipeline.
    
    This class provides CrewAI tasks for:
    - Text chunking and embedding generation
    - Metadata preparation for Pinecone
    - Processing different content types for vector storage
    - Validation of vector data
    """
    
    def __init__(self, agent):
        """
        Initialize vectorization tasks with a CrewAI agent.
        
        Args:
            agent: The CrewAI agent that will execute these tasks
        """
        self.agent = agent
        logger.info("VectorizationTasks initialized")

    def chunk_and_embed_content(self) -> Task:
        """
        Create a task for chunking text and generating embeddings.
        
        This task:
        - Takes raw text content and splits it into manageable chunks
        - Generates embeddings for each chunk using the remote embedding model
        - Handles different content types (text, JSON, file paths)
        - Returns structured data with chunks and embeddings
        
        Returns:
            CrewAI Task for content chunking and embedding
        """
        return Task(
            description=(
                "Process raw content by chunking it into smaller pieces and generating embeddings.\n"
                "Take the provided content (text, JSON, or file path) and split it into chunks of appropriate size.\n"
                "Generate embeddings for each chunk using the remote embedding model.\n"
                "Handle different content types appropriately:\n"
                "- For text: Split into chunks with overlap\n"
                "- For JSON: Convert to text and then chunk\n"
                "- For file paths: Read file content and then chunk\n"
                "Return structured data containing chunks and their corresponding embeddings.\n"
                "Ensure chunks are of reasonable size (typically 500 characters with 50 character overlap)."
            ),
            expected_output=(
                "A list of dictionaries, where each dictionary contains:\n"
                "- 'chunk_text': The text chunk (string)\n"
                "- 'embedding': The embedding vector (list of floats)\n"
                "- 'chunk_id': Sequential identifier for the chunk (integer)\n"
                "Ensure all chunks have corresponding embeddings and the data is properly structured."
            ),
            agent=self.agent,
            callback=lambda output: logger.info(f"Chunking and embedding completed. Chunks: {len(output) if isinstance(output, list) else 1}")
        )

    def prepare_pinecone_vectors(self) -> Task:
        """
        Create a task for preparing vectors for Pinecone storage.
        
        This task:
        - Takes chunk embeddings and source information
        - Prepares metadata according to Pinecone schema requirements
        - Creates vector entries ready for Pinecone upsert
        - Validates metadata completeness
        
        Returns:
            CrewAI Task for Pinecone vector preparation
        """
        return Task(
            description=(
                "Prepare chunk embeddings for storage in Pinecone vector database.\n"
                "Take the chunk embeddings and source information, then prepare metadata "
                "according to the specified Pinecone index schema.\n"
                "Create vector entries with proper IDs, values, and metadata.\n"
                "Ensure all required metadata fields are present and properly formatted.\n"
                "Validate that the metadata matches the schema requirements.\n"
                "Handle different Pinecone indexes (documentos-informes-vector, noticia-relevante-vector, etc.)."
            ),
            expected_output=(
                "A list of dictionaries, where each dictionary represents a vector for Pinecone:\n"
                "- 'id': Unique vector identifier (string)\n"
                "- 'values': The embedding vector (list of floats)\n"
                "- 'metadata': Dictionary containing all required metadata fields\n"
                "Ensure all vectors have proper IDs and complete metadata according to the schema."
            ),
            agent=self.agent,
            callback=lambda output: logger.info(f"Pinecone vectors prepared. Vectors: {len(output) if isinstance(output, list) else 1}")
        )

    def process_financial_documents(self) -> Task:
        """
        Create a task for processing financial documents for vectorization.
        
        This task:
        - Processes financial reports and documents
        - Maps to the 'documentos-informes-vector' index
        - Extracts relevant metadata for financial content
        
        Returns:
            CrewAI Task for financial document processing
        """
        return Task(
            description=(
                "Process financial documents and reports for vector storage.\n"
                "Take financial content (reports, balance sheets, etc.) and prepare it for "
                "storage in the 'documentos-informes-vector' Pinecone index.\n"
                "Extract relevant metadata such as report title, publication date, issuer information, "
                "and content type.\n"
                "Chunk the content appropriately and generate embeddings.\n"
                "Prepare metadata according to the financial documents schema."
            ),
            expected_output=(
                "A list of vectors ready for the 'documentos-informes-vector' index, each containing:\n"
                "- Proper metadata with 'id_informe', 'fecha_publicacion', 'titulo_informe', etc.\n"
                "- 'tipo_contenido' set to 'financial_report' or appropriate type\n"
                "- Complete chunk information and embeddings\n"
                "Ensure all required fields for financial documents are present."
            ),
            agent=self.agent,
            callback=lambda output: logger.info(f"Financial documents processed. Vectors: {len(output) if isinstance(output, list) else 1}")
        )

    def process_macroeconomic_data(self) -> Task:
        """
        Create a task for processing macroeconomic data for vectorization.
        
        This task:
        - Processes macroeconomic indicators and statistics
        - Maps to the 'dato-macroeconomico-vector' index
        - Extracts relevant metadata for economic data
        
        Returns:
            CrewAI Task for macroeconomic data processing
        """
        return Task(
            description=(
                "Process macroeconomic data and indicators for vector storage.\n"
                "Take macroeconomic content (inflation rates, GDP data, unemployment figures, etc.) "
                "and prepare it for storage in the 'dato-macroeconomico-vector' Pinecone index.\n"
                "Extract relevant metadata such as indicator name, data date, numeric value, "
                "unit of measure, and data source.\n"
                "Chunk the content appropriately and generate embeddings.\n"
                "Prepare metadata according to the macroeconomic data schema."
            ),
            expected_output=(
                "A list of vectors ready for the 'dato-macroeconomico-vector' index, each containing:\n"
                "- Proper metadata with 'id_dato', 'indicador_nombre', 'fecha_dato', etc.\n"
                "- Complete chunk information and embeddings\n"
                "- Source information and frequency data\n"
                "Ensure all required fields for macroeconomic data are present."
            ),
            agent=self.agent,
            callback=lambda output: logger.info(f"Macroeconomic data processed. Vectors: {len(output) if isinstance(output, list) else 1}")
        )

    def process_public_contracts(self) -> Task:
        """
        Create a task for processing public contracts for vectorization.
        
        This task:
        - Processes public tenders and contracts
        - Maps to the 'licitacion-contrato-vector' index
        - Extracts relevant metadata for contract data
        
        Returns:
            CrewAI Task for public contracts processing
        """
        return Task(
            description=(
                "Process public contracts and tenders for vector storage.\n"
                "Take contract content (tender announcements, contract awards, etc.) "
                "and prepare it for storage in the 'licitacion-contrato-vector' Pinecone index.\n"
                "Extract relevant metadata such as tender title, award date, awarded amount, "
                "currency, tender status, and contracting entity.\n"
                "Chunk the content appropriately and generate embeddings.\n"
                "Prepare metadata according to the public contracts schema."
            ),
            expected_output=(
                "A list of vectors ready for the 'licitacion-contrato-vector' index, each containing:\n"
                "- Proper metadata with 'id_licitacion', 'titulo', 'fecha_adjudicacion', etc.\n"
                "- Complete chunk information and embeddings\n"
                "- Contract details and entity information\n"
                "Ensure all required fields for public contracts are present."
            ),
            agent=self.agent,
            callback=lambda output: logger.info(f"Public contracts processed. Vectors: {len(output) if isinstance(output, list) else 1}")
        )

    def process_news_content(self) -> Task:
        """
        Create a task for processing news content for vectorization.
        
        This task:
        - Processes news articles and market information
        - Maps to the 'noticia-relevante-vector' index
        - Extracts relevant metadata for news content
        
        Returns:
            CrewAI Task for news content processing
        """
        return Task(
            description=(
                "Process news articles and market information for vector storage.\n"
                "Take news content (market reports, economic news, financial updates, etc.) "
                "and prepare it for storage in the 'noticia-relevante-vector' Pinecone index.\n"
                "Extract relevant metadata such as news title, publication date, news source, "
                "category (market, economic, financial, political), and relevance score.\n"
                "Chunk the content appropriately and generate embeddings.\n"
                "Prepare metadata according to the news content schema."
            ),
            expected_output=(
                "A list of vectors ready for the 'noticia-relevante-vector' index, each containing:\n"
                "- Proper metadata with 'id_noticia', 'titulo_noticia', 'fecha_publicacion', etc.\n"
                "- Complete chunk information and embeddings\n"
                "- News source and category information\n"
                "Ensure all required fields for news content are present."
            ),
            agent=self.agent,
            callback=lambda output: logger.info(f"News content processed. Vectors: {len(output) if isinstance(output, list) else 1}")
        )

    def validate_vector_data(self) -> Task:
        """
        Create a task for validating vector data before storage.
        
        This task:
        - Validates that vectors have proper structure
        - Checks metadata completeness
        - Ensures embeddings have correct dimensions
        - Verifies data quality
        
        Returns:
            CrewAI Task for vector data validation
        """
        return Task(
            description=(
                "Validate vector data before storage in Pinecone.\n"
                "Check that all vectors have proper structure with 'id', 'values', and 'metadata'.\n"
                "Verify that embeddings have the correct dimension (384 for sentence-transformers/all-MiniLM-L6-v2).\n"
                "Ensure metadata contains all required fields according to the target index schema.\n"
                "Validate data quality and completeness.\n"
                "Return a validation report with any issues found."
            ),
            expected_output=(
                "A validation report dictionary containing:\n"
                "- 'total_vectors': Number of vectors processed (int)\n"
                "- 'valid_vectors': Number of valid vectors (int)\n"
                "- 'invalid_vectors': Number of invalid vectors (int)\n"
                "- 'issues': List of validation issues found (list of strings)\n"
                "- 'validated_vectors': The original vectors with validation status added\n"
                "- 'embedding_dimension': Expected embedding dimension (384)"
            ),
            agent=self.agent,
            callback=lambda output: logger.info(f"Vector validation completed. {output.get('valid_vectors', 0)}/{output.get('total_vectors', 0)} vectors valid")
        )

    def process_content_by_index(self, index_name: str) -> Task:
        """
        Create a task for processing content for a specific Pinecone index.
        
        Args:
            index_name: The target Pinecone index name
            
        Returns:
            CrewAI Task for specific index processing
        """
        index_descriptions = {
            'documentos-informes-vector': 'financial reports and general documents',
            'noticia-relevante-vector': 'news articles and market information',
            'dato-macroeconomico-vector': 'macroeconomic indicators and statistics',
            'licitacion-contrato-vector': 'public contracts and tenders'
        }
        
        description = index_descriptions.get(index_name, index_name)
        
        return Task(
            description=(
                f"Process content for storage in the '{index_name}' Pinecone index.\n"
                f"Take content related to {description} and prepare it for vector storage.\n"
                f"Chunk the content appropriately and generate embeddings.\n"
                f"Prepare metadata according to the '{index_name}' schema requirements.\n"
                f"Ensure all required fields are present and properly formatted."
            ),
            expected_output=(
                f"A list of vectors ready for the '{index_name}' index, each containing:\n"
                "- Proper metadata according to the index schema\n"
                "- Complete chunk information and embeddings\n"
                "- All required fields for the specific index type\n"
                "Ensure the vectors are properly structured for Pinecone storage."
            ),
            agent=self.agent,
            callback=lambda output: logger.info(f"{index_name} content processed. Vectors: {len(output) if isinstance(output, list) else 1}")
        ) 