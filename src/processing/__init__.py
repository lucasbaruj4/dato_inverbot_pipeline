"""
Processing Module

This module handles structured data processing using AI models to extract
and structure information from raw content according to database schemas.

The module provides:
- StructuredProcessingLogic: Core processing functionality
- StructuredProcessingAgent: CrewAI agent for structured processing tasks
- StructuredProcessingTasks: Task definitions for structured processing
- Schema definitions and validation for Supabase tables
"""

__version__ = "1.0.0"
__author__ = "Inverbot Team"
__description__ = "Structured data processing module for the Inverbot pipeline"

from .processing_logic import StructuredProcessingLogic
from .processing_agent import StructuredProcessingAgent
from .processing_tasks import StructuredProcessingTasks
from .schemas import SUPABASE_SCHEMAS

__all__ = [
    "StructuredProcessingLogic", 
    "StructuredProcessingAgent", 
    "StructuredProcessingTasks",
    "SUPABASE_SCHEMAS"
] 