"""
Vectorization Logic Module

This module contains the core vectorization functionality for text chunking,
embedding generation, and metadata preparation for Pinecone vector storage.
"""

import json
import os
import requests
from typing import List, Dict, Any, Optional, Union
import logging
from datetime import datetime

from .pinecone_schemas import (
    PINECONE_SCHEMAS, 
    get_pinecone_schema_info, 
    get_required_metadata,
    validate_index_exists,
    validate_metadata_completeness
)
from dotenv import load_dotenv

# Load environment variables for model connections
load_dotenv('.env.local')

logger = logging.getLogger(__name__)

class VectorizationLogic:
    """
    Core vectorization logic for text chunking and embedding generation.
    
    This class provides methods to:
    - Chunk text content into smaller pieces
    - Generate embeddings using remote embedding model
    - Prepare metadata for Pinecone vector storage
    - Handle different content types and sources
    """
    
    def __init__(self, embedding_url: Optional[str] = None):
        """
        Initialize the vectorization logic.
        
        Args:
            embedding_url: URL for the remote embedding model (optional, will use env var if not provided)
        """
        self.embedding_url = embedding_url or os.getenv('EMBEDDING_MODEL_URL')
        self.headers = {
            'bypass-tunnel-reminder': 'true',
            'Content-Type': 'application/json'
        }
        
        if not self.embedding_url:
            logger.warning("EMBEDDING_MODEL_URL not found in environment variables")
        
        logger.info(f"VectorizationLogic initialized with embedding URL: {self.embedding_url}")

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

    def _call_embedding_model(self, text: str) -> Optional[List[float]]:
        """
        Call the remote embedding model to generate embeddings.
        
        Args:
            text: The text to generate embeddings for
            
        Returns:
            List of embedding values, or None if call fails
        """
        if not self.embedding_url:
            logger.error("Embedding URL not configured")
            return None
            
        try:
            payload = {
                "text": text
            }
            
            response = requests.post(
                f"{self.embedding_url}/embed",
                headers=self.headers,
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                embeddings = result.get('embeddings', [])
                
                if embeddings and len(embeddings) > 0:
                    embedding = embeddings[0]  # Get first embedding
                    logger.info(f"Successfully generated embedding of dimension {len(embedding)}")
                    return embedding
                else:
                    logger.error("No embeddings returned from model")
                    return None
            else:
                logger.error(f"Embedding API call failed with status {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Error calling embedding model: {e}")
            return None

    def _call_embedding_model_batch(self, texts: List[str]) -> Optional[List[List[float]]]:
        """
        Call the remote embedding model to generate embeddings for multiple texts.
        
        Args:
            texts: List of texts to generate embeddings for
            
        Returns:
            List of embedding lists, or None if call fails
        """
        if not self.embedding_url:
            logger.error("Embedding URL not configured")
            return None
            
        try:
            payload = {
                "texts": texts
            }
            
            response = requests.post(
                f"{self.embedding_url}/embed",
                headers=self.headers,
                json=payload,
                timeout=120
            )
            
            if response.status_code == 200:
                result = response.json()
                embeddings = result.get('embeddings', [])
                
                logger.info(f"Successfully generated {len(embeddings)} embeddings")
                return embeddings
            else:
                logger.error(f"Embedding API call failed with status {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Error calling embedding model: {e}")
            return None

    def chunk_text(
        self, 
        text: str, 
        chunk_size: int = 500, 
        chunk_overlap: int = 50
    ) -> List[str]:
        """
        Split text into chunks for vectorization.
        
        Args:
            text: The text to chunk
            chunk_size: Maximum size of each chunk
            chunk_overlap: Number of characters to overlap between chunks
            
        Returns:
            List of text chunks
        """
        if not text:
            return []
        
        try:
            from langchain_text_splitters import RecursiveCharacterTextSplitter
            
            # Initialize text splitter
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
                length_function=len,
                is_separator_regex=False
            )
            
            # Split the text into chunks
            chunks = text_splitter.split_text(text)
            
            logger.info(f"Successfully chunked text into {len(chunks)} chunks")
            return chunks
            
        except ImportError:
            logger.warning("langchain_text_splitters not available, using simple chunking")
            # Fallback to simple chunking
            chunks = []
            start = 0
            while start < len(text):
                end = start + chunk_size
                chunk = text[start:end]
                chunks.append(chunk)
                start = end - chunk_overlap
                if start >= len(text):
                    break
            
            logger.info(f"Simple chunking created {len(chunks)} chunks")
            return chunks
        except Exception as e:
            logger.error(f"Error chunking text: {e}")
            return []

    def generate_embeddings_for_chunks(self, chunks: List[str]) -> List[Dict[str, Any]]:
        """
        Generate embeddings for a list of text chunks.
        
        Args:
            chunks: List of text chunks to generate embeddings for
            
        Returns:
            List of dictionaries containing chunks and their embeddings
        """
        if not chunks:
            return []
        
        logger.info(f"Generating embeddings for {len(chunks)} chunks")
        
        # Generate embeddings in batch
        embeddings = self._call_embedding_model_batch(chunks)
        
        if not embeddings:
            logger.error("Failed to generate embeddings")
            return []
        
        # Combine chunks with their embeddings
        chunk_embeddings = []
        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            chunk_embeddings.append({
                'chunk_text': chunk,
                'embedding': embedding,
                'chunk_id': i
            })
        
        logger.info(f"Successfully generated embeddings for {len(chunk_embeddings)} chunks")
        return chunk_embeddings

    def chunk_and_embed_content(
        self, 
        content: Union[str, Dict[str, Any]], 
        chunk_size: int = 500, 
        chunk_overlap: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Chunk content and generate embeddings for each chunk.
        
        Args:
            content: The content to process (text, JSON, or file path)
            chunk_size: Maximum size of each chunk
            chunk_overlap: Number of characters to overlap between chunks
            
        Returns:
            List of dictionaries containing chunks and their embeddings
        """
        logger.info(f"Processing content for chunking and embedding")
        
        # Process content
        processed_text = None
        if isinstance(content, str):
            # Check if it's a file path
            if os.path.exists(content):
                processed_text = self._read_file_content(content)
            else:
                processed_text = content
        elif isinstance(content, dict):
            processed_text = json.dumps(content, indent=2)
        else:
            logger.error(f"Unsupported content type: {type(content)}")
            return []
        
        if not processed_text:
            logger.error("No content to process")
            return []
        
        # Chunk the text
        chunks = self.chunk_text(processed_text, chunk_size, chunk_overlap)
        
        if not chunks:
            logger.warning("No chunks created from content")
            return []
        
        # Generate embeddings for chunks
        chunk_embeddings = self.generate_embeddings_for_chunks(chunks)
        
        return chunk_embeddings

    def prepare_pinecone_metadata(
        self, 
        chunk_embeddings: List[Dict[str, Any]], 
        source_info: Dict[str, Any], 
        index_name: str
    ) -> List[Dict[str, Any]]:
        """
        Prepare metadata for Pinecone vector storage.
        
        Args:
            chunk_embeddings: List of chunks with embeddings
            source_info: Information about the source content
            index_name: Name of the target Pinecone index
            
        Returns:
            List of dictionaries ready for Pinecone upsert
        """
        logger.info(f"Preparing metadata for Pinecone index: {index_name}")
        
        # Validate index exists
        if not validate_index_exists(index_name):
            logger.error(f"Index '{index_name}' not found in schemas")
            return []
        
        # Get schema information
        schema_info = get_pinecone_schema_info(index_name)
        required_fields = get_required_metadata(index_name)
        
        # Prepare vectors for Pinecone
        vectors = []
        for chunk_data in chunk_embeddings:
            # Create base metadata
            metadata = {
                'chunk_text': chunk_data['chunk_text'],
                'chunk_id': chunk_data['chunk_id']
            }
            
            # Add source information to metadata
            metadata.update(source_info)
            
            # Validate metadata completeness
            validation = validate_metadata_completeness(metadata, index_name)
            if not validation['is_valid']:
                logger.warning(f"Missing required fields for chunk {chunk_data['chunk_id']}: {validation['missing_fields']}")
                # Continue with available fields
            
            # Create vector entry
            vector_entry = {
                'id': f"{source_info.get('source_id', 'unknown')}-{chunk_data['chunk_id']}",
                'values': chunk_data['embedding'],
                'metadata': metadata
            }
            
            vectors.append(vector_entry)
        
        logger.info(f"Prepared {len(vectors)} vectors for Pinecone index '{index_name}'")
        return vectors

    def process_content_for_index(
        self, 
        content: Union[str, Dict[str, Any]], 
        source_info: Dict[str, Any], 
        index_name: str,
        chunk_size: int = 500, 
        chunk_overlap: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Complete processing pipeline: chunk, embed, and prepare for Pinecone.
        
        Args:
            content: The content to process
            source_info: Information about the source content
            index_name: Target Pinecone index name
            chunk_size: Maximum chunk size
            chunk_overlap: Chunk overlap size
            
        Returns:
            List of vectors ready for Pinecone upsert
        """
        logger.info(f"Processing content for index: {index_name}")
        
        # Step 1: Chunk and embed content
        chunk_embeddings = self.chunk_and_embed_content(content, chunk_size, chunk_overlap)
        
        if not chunk_embeddings:
            logger.warning("No chunk embeddings generated")
            return []
        
        # Step 2: Prepare metadata for Pinecone
        vectors = self.prepare_pinecone_metadata(chunk_embeddings, source_info, index_name)
        
        return vectors

    def test_embedding_connection(self) -> Dict[str, Any]:
        """
        Test the connection to the remote embedding model.
        
        Returns:
            Dictionary with connection status and details
        """
        try:
            if not self.embedding_url:
                return {
                    'status': 'error',
                    'message': 'EMBEDDING_MODEL_URL not found in environment variables'
                }
            
            # Test with a simple text
            test_text = "Hello, this is a connection test."
            embedding = self._call_embedding_model(test_text)
            
            if embedding:
                return {
                    'status': 'success',
                    'message': f'Connection successful. Embedding dimension: {len(embedding)}',
                    'url': self.embedding_url,
                    'dimension': len(embedding)
                }
            else:
                return {
                    'status': 'error',
                    'message': 'Connection failed - no embedding generated',
                    'url': self.embedding_url
                }
                
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