"""
Vectorization Module

This module handles text chunking, embedding generation, and vector processing
for storing data in vector databases like Pinecone.

The module provides:
- VectorizationLogic: Core vectorization functionality
- VectorizationAgent: CrewAI agent for vectorization tasks
- VectorizationTasks: Task definitions for vectorization pipeline
- Pinecone index schemas and metadata preparation
"""

__version__ = "1.0.0"
__author__ = "Inverbot Team"
__description__ = "Vectorization module for the Inverbot pipeline"

from .vectorization_logic import VectorizationLogic
from .vectorization_agent import VectorizationAgent
from .vectorization_tasks import VectorizationTasks
from .pinecone_schemas import PINECONE_SCHEMAS

__all__ = [
    "VectorizationLogic", 
    "VectorizationAgent", 
    "VectorizationTasks",
    "PINECONE_SCHEMAS"
] 