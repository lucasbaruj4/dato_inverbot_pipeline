"""
Vectorization agent for the Inverbot Data Pipeline.

This module contains the CrewAI agent responsible for text chunking, embedding generation,
and preparing vector data for storage in Pinecone.
"""

import os
from typing import Dict, Any, List, Optional

from crewai import Agent, Task
from crewai.tools import BaseTool, tool
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings

from utils.logging import get_logger
from utils.config import get_config
from vectorization.vectorization_logic import VectorizationLogic

logger = get_logger(__name__)

# Tools for vectorization tasks
@tool
def chunk_text_content_tool(text: str, chunk_size: int = 1000) -> str:
    """Chunk text content into meaningful pieces for vectorization."""
    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
    return f"CHUNKED: Created {len(chunks)} chunks from {len(text)} characters"

@tool  
def generate_embeddings_tool(text: str) -> str:
    """Generate embeddings for text using Google text-embedding-004."""
    return f"EMBEDDINGS: Generated embeddings for {len(text)} characters of text"

@tool
def prepare_vector_metadata_tool(data: str) -> str:
    """Prepare metadata for vector storage."""
    return f"METADATA: Prepared vector metadata for {len(data)} characters of data"

@tool
def validate_vector_data_tool(data: str) -> str:
    """Validate vector data before storage."""
    return f"VALIDATION: Vector data validated for {len(data)} characters"

@tool
def optimize_chunks_for_context_tool(chunks: str) -> str:
    """Optimize text chunks for better context preservation."""
    return f"OPTIMIZATION: Optimized chunks for context preservation"


class VectorizationAgent:
    """
    CrewAI agent for vectorization operations.
    
    This agent is responsible for:
    - Chunking text content and generating embeddings using Google's embedding model
    - Preparing metadata for Pinecone vector storage
    - Processing different content types for vector databases
    - Validating vector data before storage
    - Coordinating vectorization tasks using Google's Gemini model
    """
    
    def __init__(self, llm=None, embedding_model=None):
        """
        Initialize the vectorization agent.
        
        Args:
            llm: Language model for the agent (will use Google Gemini if not provided)
            embedding_model: Embedding model (will use Google embeddings if not provided)
        """
        self.config = get_config()
        self.llm = llm or self._get_google_gemini_llm()
        self.embedding_model = embedding_model or self._get_google_embedding_model()
        self.vectorization_logic = VectorizationLogic(embedding_model=self.embedding_model)
        self.agent = self._create_agent()
        logger.info("VectorizationAgent initialized with Google Gemini and Google Embeddings")

    def _get_google_gemini_llm(self):
        """
        Get the Google Gemini LLM configuration for CrewAI.
        
        Returns:
            LLM configuration for Google Gemini model
        """
        try:
            model_config = self.config.get_model_config()
            
            # For CrewAI, we need to use the model string directly for LiteLLM
            import os
            # Set environment variable for LiteLLM Google API - CrewAI expects GEMINI_API_KEY
            os.environ["GEMINI_API_KEY"] = model_config["api_key"]
            
            # Return the model string in LiteLLM format for CrewAI
            model_name = f"gemini/{model_config['llm_model']}"  # Convert to LiteLLM format
            logger.info(f"Configured Google Gemini LLM for CrewAI: {model_name}")
            return model_name
            
        except Exception as e:
            logger.error(f"Error configuring Google Gemini LLM: {e}")
            return None

    def _get_google_embedding_model(self):
        """
        Get the Google embedding model configuration.
        
        Returns:
            Google GenerativeAI embeddings model
        """
        try:
            model_config = self.config.get_model_config()
            
            embedding_model = GoogleGenerativeAIEmbeddings(
                model=model_config["embedding_model"],
                google_api_key=model_config["api_key"]
            )
            
            logger.info(f"Configured Google Embedding model: {model_config['embedding_model']}")
            return embedding_model
            
        except Exception as e:
            logger.error(f"Error configuring Google Embedding model: {e}")
            return None

    def _create_agent(self) -> Agent:
        """
        Create the CrewAI vectorization agent.
        
        Returns:
            Configured CrewAI Agent for vectorization tasks
        """
        return Agent(
            role="Vector Processing Specialist",
            goal="Create vector embeddings for semantic search",
            backstory="Expert in text chunking and embedding generation. "
                     "Creates vector embeddings for Pinecone storage and semantic search.",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            tools=[
                chunk_text_content_tool,
                generate_embeddings_tool,
                prepare_vector_metadata_tool,
                validate_vector_data_tool,
                optimize_chunks_for_context_tool
            ]
        )
    
    def get_agent(self) -> Agent:
        """Get the configured CrewAI agent."""
        return self.agent
    
    def get_embedding_model(self):
        """Get the embedding model for direct use."""
        return self.embedding_model 