"""
Inverbot Data Pipeline

A modular data pipeline for collecting and processing Paraguayan financial/economic data
to support the Inverbot RAG system for investment advice.
"""

__version__ = "2.0.0"
__author__ = "Inverbot Team"
__description__ = "Automated data pipeline for Paraguayan financial data collection and processing"

from . import extraction, processing, vectorization, loading, utils

__all__ = [
    "extraction",
    "processing", 
    "vectorization",
    "loading",
    "utils"
] 