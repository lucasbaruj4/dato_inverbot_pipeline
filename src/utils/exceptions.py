"""
Custom exceptions for the Inverbot Data Pipeline.

This module defines custom exception classes for different types of errors
that can occur during pipeline execution.
"""

from typing import Optional, Dict, Any


class PipelineError(Exception):
    """Base exception for all pipeline-related errors."""
    
    def __init__(
        self,
        message: str,
        error_code: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.error_code = error_code
        self.details = details or {}
        super().__init__(self.message)
    
    def __str__(self) -> str:
        if self.error_code:
            return f"[{self.error_code}] {self.message}"
        return self.message


class ValidationError(PipelineError):
    """Exception raised when data validation fails."""
    
    def __init__(
        self,
        message: str,
        field: Optional[str] = None,
        value: Optional[Any] = None,
        **kwargs
    ):
        super().__init__(message, error_code="VALIDATION_ERROR", **kwargs)
        self.field = field
        self.value = value


class ConnectionError(PipelineError):
    """Exception raised when connection to external services fails."""
    
    def __init__(
        self,
        message: str,
        service: Optional[str] = None,
        url: Optional[str] = None,
        **kwargs
    ):
        super().__init__(message, error_code="CONNECTION_ERROR", **kwargs)
        self.service = service
        self.url = url


class ModelError(PipelineError):
    """Exception raised when model operations fail."""
    
    def __init__(
        self,
        message: str,
        model_type: Optional[str] = None,
        endpoint: Optional[str] = None,
        **kwargs
    ):
        super().__init__(message, error_code="MODEL_ERROR", **kwargs)
        self.model_type = model_type
        self.endpoint = endpoint


class DatabaseError(PipelineError):
    """Exception raised when database operations fail."""
    
    def __init__(
        self,
        message: str,
        operation: Optional[str] = None,
        table: Optional[str] = None,
        **kwargs
    ):
        super().__init__(message, error_code="DATABASE_ERROR", **kwargs)
        self.operation = operation
        self.table = table


class ExtractionError(PipelineError):
    """Exception raised when data extraction fails."""
    
    def __init__(
        self,
        message: str,
        source_url: Optional[str] = None,
        content_type: Optional[str] = None,
        **kwargs
    ):
        super().__init__(message, error_code="EXTRACTION_ERROR", **kwargs)
        self.source_url = source_url
        self.content_type = content_type


class ProcessingError(PipelineError):
    """Exception raised when data processing fails."""
    
    def __init__(
        self,
        message: str,
        stage: Optional[str] = None,
        data_type: Optional[str] = None,
        **kwargs
    ):
        super().__init__(message, error_code="PROCESSING_ERROR", **kwargs)
        self.stage = stage
        self.data_type = data_type


class VectorizationError(PipelineError):
    """Exception raised when vectorization operations fail."""
    
    def __init__(
        self,
        message: str,
        model_name: Optional[str] = None,
        chunk_id: Optional[int] = None,
        **kwargs
    ):
        super().__init__(message, error_code="VECTORIZATION_ERROR", **kwargs)
        self.model_name = model_name
        self.chunk_id = chunk_id


class ConfigurationError(PipelineError):
    """Exception raised when configuration is invalid or missing."""
    
    def __init__(
        self,
        message: str,
        config_key: Optional[str] = None,
        **kwargs
    ):
        super().__init__(message, error_code="CONFIGURATION_ERROR", **kwargs)
        self.config_key = config_key


class RateLimitError(PipelineError):
    """Exception raised when rate limits are exceeded."""
    
    def __init__(
        self,
        message: str,
        service: Optional[str] = None,
        retry_after: Optional[int] = None,
        **kwargs
    ):
        super().__init__(message, error_code="RATE_LIMIT_ERROR", **kwargs)
        self.service = service
        self.retry_after = retry_after


class AuthenticationError(PipelineError):
    """Exception raised when authentication fails."""
    
    def __init__(
        self,
        message: str,
        service: Optional[str] = None,
        **kwargs
    ):
        super().__init__(message, error_code="AUTHENTICATION_ERROR", **kwargs)
        self.service = service


class FileError(PipelineError):
    """Exception raised when file operations fail."""
    
    def __init__(
        self,
        message: str,
        file_path: Optional[str] = None,
        operation: Optional[str] = None,
        **kwargs
    ):
        super().__init__(message, error_code="FILE_ERROR", **kwargs)
        self.file_path = file_path
        self.operation = operation


class CrewAIError(PipelineError):
    """Exception raised when CrewAI operations fail."""
    
    def __init__(
        self,
        message: str,
        agent: Optional[str] = None,
        task: Optional[str] = None,
        **kwargs
    ):
        super().__init__(message, error_code="CREWAI_ERROR", **kwargs)
        self.agent = agent
        self.task = task


def handle_pipeline_error(error: Exception, context: Optional[Dict[str, Any]] = None) -> PipelineError:
    """
    Convert generic exceptions to pipeline-specific exceptions.
    
    Args:
        error: The original exception
        context: Additional context about the error
        
    Returns:
        PipelineError instance
    """
    if isinstance(error, PipelineError):
        return error
    
    # Convert common exceptions to pipeline-specific ones
    if isinstance(error, (ConnectionError, TimeoutError)):
        return ConnectionError(
            message=str(error),
            details=context or {}
        )
    elif isinstance(error, ValueError):
        return ValidationError(
            message=str(error),
            details=context or {}
        )
    elif isinstance(error, FileNotFoundError):
        return FileError(
            message=str(error),
            file_path=getattr(error, 'filename', None),
            details=context or {}
        )
    else:
        return PipelineError(
            message=str(error),
            error_code="UNKNOWN_ERROR",
            details=context or {}
        ) 