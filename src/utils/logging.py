"""
Logging configuration for the Inverbot Data Pipeline.

This module provides structured logging setup with different log levels
and output formats for development and production environments.
"""

import logging
import sys
from typing import Optional
from pathlib import Path

import structlog
from rich.console import Console
from rich.logging import RichHandler

from .config import get_config


def setup_logging(
    log_level: Optional[str] = None,
    log_file: Optional[str] = None,
    enable_rich: bool = True
) -> None:
    """
    Setup structured logging for the application.
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional log file path
        enable_rich: Whether to enable rich console output
    """
    config = get_config()
    
    # Use provided log_level or default from config
    level = log_level or config.log_level
    level_num = getattr(logging, level.upper(), logging.INFO)
    
    # Configure structlog
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer() if config.is_production() else structlog.dev.ConsoleRenderer(),
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
    
    # Configure standard library logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=level_num,
    )
    
    # Add file handler if log_file is specified
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level_num)
        
        # Use JSON format for file logging
        file_formatter = logging.Formatter(
            '{"timestamp": "%(asctime)s", "level": "%(levelname)s", "logger": "%(name)s", "message": "%(message)s"}'
        )
        file_handler.setFormatter(file_formatter)
        
        # Add to root logger
        logging.getLogger().addHandler(file_handler)
    
    # Add rich console handler for development
    if enable_rich and config.is_development():
        console = Console()
        rich_handler = RichHandler(
            console=console,
            show_time=True,
            show_path=True,
            markup=True,
            rich_tracebacks=True,
        )
        rich_handler.setLevel(level_num)
        
        # Add to root logger
        logging.getLogger().addHandler(rich_handler)
    
    # Set specific logger levels
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("crewai").setLevel(logging.INFO)
    logging.getLogger("langchain").setLevel(logging.INFO)


def get_logger(name: str) -> structlog.BoundLogger:
    """
    Get a structured logger instance.
    
    Args:
        name: Logger name (usually __name__)
        
    Returns:
        Structured logger instance
    """
    return structlog.get_logger(name)


def log_pipeline_start(pipeline_name: str, **kwargs) -> None:
    """
    Log pipeline start event.
    
    Args:
        pipeline_name: Name of the pipeline
        **kwargs: Additional context to log
    """
    logger = get_logger(__name__)
    logger.info(
        "Pipeline started",
        pipeline_name=pipeline_name,
        **kwargs
    )


def log_pipeline_end(pipeline_name: str, duration: float, **kwargs) -> None:
    """
    Log pipeline end event.
    
    Args:
        pipeline_name: Name of the pipeline
        duration: Pipeline duration in seconds
        **kwargs: Additional context to log
    """
    logger = get_logger(__name__)
    logger.info(
        "Pipeline completed",
        pipeline_name=pipeline_name,
        duration=duration,
        **kwargs
    )


def log_pipeline_error(pipeline_name: str, error: Exception, **kwargs) -> None:
    """
    Log pipeline error event.
    
    Args:
        pipeline_name: Name of the pipeline
        error: Exception that occurred
        **kwargs: Additional context to log
    """
    logger = get_logger(__name__)
    logger.error(
        "Pipeline failed",
        pipeline_name=pipeline_name,
        error_type=type(error).__name__,
        error_message=str(error),
        **kwargs,
        exc_info=True
    )


def log_data_processing(
    stage: str,
    data_type: str,
    count: int,
    duration: float,
    **kwargs
) -> None:
    """
    Log data processing event.
    
    Args:
        stage: Processing stage (extraction, processing, loading, etc.)
        data_type: Type of data being processed
        count: Number of items processed
        duration: Processing duration in seconds
        **kwargs: Additional context to log
    """
    logger = get_logger(__name__)
    logger.info(
        "Data processing completed",
        stage=stage,
        data_type=data_type,
        count=count,
        duration=duration,
        **kwargs
    )


def log_model_request(
    model_type: str,
    endpoint: str,
    duration: float,
    success: bool,
    **kwargs
) -> None:
    """
    Log model API request.
    
    Args:
        model_type: Type of model (mistral, embedding)
        endpoint: API endpoint
        duration: Request duration in seconds
        success: Whether request was successful
        **kwargs: Additional context to log
    """
    logger = get_logger(__name__)
    log_level = "info" if success else "error"
    logger.log(
        log_level,
        "Model request completed",
        model_type=model_type,
        endpoint=endpoint,
        duration=duration,
        success=success,
        **kwargs
    )


def log_database_operation(
    operation: str,
    table: str,
    count: int,
    duration: float,
    success: bool,
    **kwargs
) -> None:
    """
    Log database operation.
    
    Args:
        operation: Database operation (insert, update, delete, query)
        table: Table name
        count: Number of records affected
        duration: Operation duration in seconds
        success: Whether operation was successful
        **kwargs: Additional context to log
    """
    logger = get_logger(__name__)
    log_level = "info" if success else "error"
    logger.log(
        log_level,
        "Database operation completed",
        operation=operation,
        table=table,
        count=count,
        duration=duration,
        success=success,
        **kwargs
    ) 