"""
Loading Module

This module handles data loading operations for both structured data (Supabase)
and vector data (Pinecone) in the Inverbot pipeline.

The module provides:
- LoadingLogic: Core loading functionality for databases
- LoadingAgent: CrewAI agent for loading operations
- LoadingTasks: Task definitions for loading pipeline
- Database connectors and transaction management
"""

__version__ = "1.0.0"
__author__ = "Inverbot Team"
__description__ = "Data loading module for the Inverbot pipeline"

from .loading_logic import LoadingLogic
from .loading_agent import LoadingAgent
from .loading_tasks import LoadingTasks
from .database_connectors import SupabaseConnector, PineconeConnector

__all__ = [
    "LoadingLogic", 
    "LoadingAgent", 
    "LoadingTasks",
    "SupabaseConnector",
    "PineconeConnector"
] 