"""
Extraction Module

This module handles data extraction from various web sources including:
- HTML scraping
- JSON API calls
- File downloads (PDF, Excel, etc.)
- Content type detection and processing

The module provides:
- ExtractionLogic: Core extraction functionality
- ExtractionAgent: CrewAI agent for extraction tasks
- ExtractionTasks: Task definitions for the extraction pipeline
- Data sources configuration and management
"""

__version__ = "1.0.0"
__author__ = "Inverbot Team"
__description__ = "Data extraction module for the Inverbot pipeline"

from .extraction_logic import ExtractionLogic
from .extraction_agent import ExtractionAgent
from .extraction_tasks import ExtractionTasks
from .data_sources import DATA_SOURCES, TEST_DATA_SOURCES, get_data_sources

__all__ = [
    "ExtractionLogic", 
    "ExtractionAgent", 
    "ExtractionTasks",
    "DATA_SOURCES",
    "TEST_DATA_SOURCES", 
    "get_data_sources"
] 