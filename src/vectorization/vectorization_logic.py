"""
Vectorization Logic for the Inverbot Data Pipeline.

This module handles text chunking, embedding generation, and vector preparation
for storage in Pinecone vector databases using Google's embedding models.
"""

import os
import requests
from typing import Dict, Any, List, Optional, Union
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from utils.logging import get_logger
from utils.config import get_config

logger = get_logger(__name__)


class VectorizationLogic:
    """
    Logic class for handling vectorization operations.
    
    This class is responsible for:
    - Chunking text content using optimized strategies
    - Generating embeddings using Google's embedding model
    - Preparing metadata for Pinecone storage
    - Validating vector data before storage
    """
    
    def __init__(self, embedding_model=None):
        """
        Initialize the vectorization logic.
        
        Args:
            embedding_model: Google embedding model instance (will create if not provided)
        """
        self.config = get_config()
        self.embedding_model = embedding_model or self._create_google_embedding_model()
        self.text_splitter = self._create_text_splitter()
        logger.info("VectorizationLogic initialized with Google embeddings")
    
    def _create_google_embedding_model(self):
        """
        Create Google embedding model instance.
        
        Returns:
            GoogleGenerativeAIEmbeddings instance
        """
        try:
            model_config = self.config.get_model_config()
            
            embedding_model = GoogleGenerativeAIEmbeddings(
                model=model_config["embedding_model"],
                google_api_key=model_config["api_key"]
            )
            
            logger.info(f"Created Google embedding model: {model_config['embedding_model']}")
            return embedding_model
            
        except Exception as e:
            logger.error(f"Error creating Google embedding model: {e}")
            return None
    
    def _create_text_splitter(self):
        """
        Create text splitter for chunking content.
        
        Returns:
            RecursiveCharacterTextSplitter instance
        """
        return RecursiveCharacterTextSplitter(
            chunk_size=self.config.chunk_size,
            chunk_overlap=self.config.chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
    
    def chunk_text(self, content: str) -> List[str]:
        """
        Split text content into chunks.
        
        Args:
            content: Text content to chunk
            
        Returns:
            List of text chunks
        """
        try:
            chunks = self.text_splitter.split_text(content)
            logger.info(f"Text split into {len(chunks)} chunks")
            return chunks
            
        except Exception as e:
            logger.error(f"Error chunking text: {e}")
            return []
    
    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of texts using Google's embedding model.
        
        Args:
            texts: List of text strings
            
        Returns:
            List of embedding vectors
        """
        if not self.embedding_model:
            logger.error("No embedding model available")
            return []
        
        try:
            # Use Google's embedding model to generate embeddings
            embeddings = self.embedding_model.embed_documents(texts)
            logger.info(f"Generated embeddings for {len(texts)} texts")
            return embeddings
            
        except Exception as e:
            logger.error(f"Error generating embeddings: {e}")
            return []
    
    def chunk_and_embed_content(self, content: Union[str, Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Chunk content and generate embeddings.
        
        Args:
            content: Content to process (string or dict with 'content' key)
            
        Returns:
            List of dictionaries with chunks and embeddings
        """
        try:
            # Extract text content
            if isinstance(content, dict):
                text_content = content.get('content', '')
            else:
                text_content = str(content)
            
            if not text_content.strip():
                logger.warning("No content to process")
                return []
            
            # Chunk the content
            chunks = self.chunk_text(text_content)
            if not chunks:
                logger.warning("No chunks generated")
                return []
            
            # Generate embeddings
            embeddings = self.generate_embeddings(chunks)
            if not embeddings or len(embeddings) != len(chunks):
                logger.error("Embedding generation failed or mismatch with chunks")
                return []
            
            # Combine chunks and embeddings
            chunk_embeddings = []
            for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
                chunk_embeddings.append({
                    'chunk_id': i,
                    'chunk_text': chunk,
                    'embedding': embedding,
                    'chunk_size': len(chunk)
                })
            
            logger.info(f"Successfully processed {len(chunk_embeddings)} chunk-embedding pairs")
            return chunk_embeddings
            
        except Exception as e:
            logger.error(f"Error in chunk_and_embed_content: {e}")
            return []
    
    def prepare_pinecone_metadata(
        self, 
        chunk_embeddings: List[Dict[str, Any]], 
        source_info: Dict[str, Any], 
        index_name: str
    ) -> List[Dict[str, Any]]:
        """
        Prepare vectors with metadata for Pinecone storage.
        
        Args:
            chunk_embeddings: List of chunks with embeddings
            source_info: Source information metadata
            index_name: Target Pinecone index name
            
        Returns:
            List of vectors ready for Pinecone upsert
        """
        try:
            vectors = []
            
            for chunk_data in chunk_embeddings:
                # Create unique vector ID
                vector_id = f"{source_info.get('category', 'unknown')}_{index_name}_{chunk_data['chunk_id']}_{hash(chunk_data['chunk_text'][:50])}"
                
                # Prepare metadata
                metadata = {
                    'chunk_text': chunk_data['chunk_text'],
                    'chunk_id': chunk_data['chunk_id'],
                    'source_url': source_info.get('url', ''),
                    'source_category': source_info.get('category', ''),
                    'content_type': source_info.get('content_type', ''),
                    'chunk_size': chunk_data['chunk_size'],
                    'index_name': index_name
                }
                
                # Create vector
                vector = {
                    'id': vector_id,
                    'values': chunk_data['embedding'],
                    'metadata': metadata
                }
                
                vectors.append(vector)
            
            logger.info(f"Prepared {len(vectors)} vectors for Pinecone index: {index_name}")
            return vectors
            
        except Exception as e:
            logger.error(f"Error preparing Pinecone metadata: {e}")
            return []
    
    def process_content_for_index(
        self, 
        content: Union[str, Dict[str, Any]], 
        source_info: Dict[str, Any], 
        index_name: str
    ) -> List[Dict[str, Any]]:
        """
        Complete processing pipeline for specific index.
        
        Args:
            content: Content to process
            source_info: Source information
            index_name: Target index name
            
        Returns:
            List of vectors ready for storage
        """
        try:
            # Chunk and embed content
            chunk_embeddings = self.chunk_and_embed_content(content)
            if not chunk_embeddings:
                logger.warning("No chunk embeddings generated")
                return []
            
            # Prepare vectors for Pinecone
            vectors = self.prepare_pinecone_metadata(chunk_embeddings, source_info, index_name)
            
            if vectors:
                logger.info(f"Successfully processed content for {index_name}. Generated {len(vectors)} vectors")
            else:
                logger.warning(f"No vectors generated for {index_name}")
            
            return vectors
            
        except Exception as e:
            logger.error(f"Error processing content for index {index_name}: {e}")
            return []
    
    def validate_vectors(self, vectors: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Validate vector data before storage.
        
        Args:
            vectors: List of vectors to validate
            
        Returns:
            Validation result dictionary
        """
        try:
            total_vectors = len(vectors)
            valid_vectors = 0
            issues = []
            
            for i, vector in enumerate(vectors):
                # Check required fields
                if not all(key in vector for key in ['id', 'values', 'metadata']):
                    issues.append(f"Vector {i}: Missing required fields")
                    continue
                
                # Check embedding dimension (Google embeddings are typically 768 or 1536)
                if not isinstance(vector['values'], list) or len(vector['values']) == 0:
                    issues.append(f"Vector {i}: Invalid embedding values")
                    continue
                
                # Check metadata
                if not isinstance(vector['metadata'], dict):
                    issues.append(f"Vector {i}: Invalid metadata")
                    continue
                
                valid_vectors += 1
            
            return {
                'total_vectors': total_vectors,
                'valid_vectors': valid_vectors,
                'invalid_vectors': total_vectors - valid_vectors,
                'issues': issues,
                'is_valid': valid_vectors == total_vectors
            }
            
        except Exception as e:
            logger.error(f"Error validating vectors: {e}")
            return {
                'total_vectors': len(vectors),
                'valid_vectors': 0,
                'invalid_vectors': len(vectors),
                'issues': [f"Validation error: {str(e)}"],
                'is_valid': False
            }
    
    def test_embedding_connection(self) -> Dict[str, Any]:
        """
        Test the Google embedding model connection.
        
        Returns:
            Connection test result
        """
        try:
            if not self.embedding_model:
                return {
                    'status': 'error',
                    'message': 'No embedding model configured'
                }
            
            # Test with a simple text
            test_text = "This is a test for Google embedding model connectivity."
            embedding = self.embedding_model.embed_query(test_text)
            
            if embedding and len(embedding) > 0:
                return {
                    'status': 'success',
                    'message': 'Google embedding model connection successful',
                    'embedding_dimension': len(embedding),
                    'model': self.config.google_embedding_model
                }
            else:
                return {
                    'status': 'error',
                    'message': 'Failed to generate test embedding'
                }
                
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Connection test failed: {str(e)}'
            } 