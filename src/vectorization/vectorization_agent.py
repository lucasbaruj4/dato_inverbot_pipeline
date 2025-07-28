"""
Vectorization agent for the Inverbot Data Pipeline.

This module contains the CrewAI agent responsible for text chunking, embedding generation,
and preparing vector data for storage in Pinecone.
"""

import os
from typing import Dict, Any, List, Optional

from crewai import Agent, Task, tool
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings

from ..utils.logging import get_logger
from ..utils.config import get_config
from .vectorization_logic import VectorizationLogic

logger = get_logger(__name__)


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
            
            llm = ChatGoogleGenerativeAI(
                model=model_config["llm_model"],
                google_api_key=model_config["api_key"],
                temperature=model_config["temperature"],
                max_tokens=model_config["max_output_tokens"]
            )
            
            logger.info(f"Configured Google Gemini LLM: {model_config['llm_model']}")
            return llm
            
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
            role="Text Vectorization Specialist",
            goal="Generate high-quality embeddings and prepare vector data for efficient semantic search",
            backstory="""You are an expert in text processing and vector embeddings with deep 
            knowledge of semantic search, text chunking strategies, and vector database optimization. 
            You excel at creating meaningful text chunks and generating embeddings that capture 
            semantic relationships. You ensure optimal vector data preparation for storage and 
            retrieval in vector databases.""",
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