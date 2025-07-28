"""
Logging utilities for the Inverbot Data Pipeline.

This module provides centralized logging configuration and utilities.
"""

import logging
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

from utils.config import get_config

# Global token usage tracker
_token_usage = {
    'total_input_tokens': 0,
    'total_output_tokens': 0,
    'agent_usage': {},
    'session_start': datetime.now().isoformat()
}

def get_logger(name: str) -> logging.Logger:
    """
    Get a configured logger for the given name.
    
    Args:
        name: Logger name (usually __name__)
        
    Returns:
        Configured logger instance
    """
    config = get_config()
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, config.log_level.upper()))
    
    # Avoid duplicate handlers
    if not logger.handlers:
        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(getattr(logging, config.log_level.upper()))
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(formatter)
        
        # Add handler to logger
        logger.addHandler(console_handler)
    
    return logger

def log_token_usage(agent_name: str, input_tokens: int, output_tokens: int, 
                   model_name: str = "gemini-1.5-flash") -> None:
    """
    Log token usage for cost monitoring.
    
    Args:
        agent_name: Name of the agent using tokens
        input_tokens: Number of input tokens used
        output_tokens: Number of output tokens used
        model_name: Name of the model used
    """
    global _token_usage
    config = get_config()
    
    if not config.enable_token_monitoring:
        return
    
    # Update global usage
    _token_usage['total_input_tokens'] += input_tokens
    _token_usage['total_output_tokens'] += output_tokens
    
    # Update agent-specific usage
    if agent_name not in _token_usage['agent_usage']:
        _token_usage['agent_usage'][agent_name] = {
            'input_tokens': 0,
            'output_tokens': 0,
            'model': model_name
        }
    
    _token_usage['agent_usage'][agent_name]['input_tokens'] += input_tokens
    _token_usage['agent_usage'][agent_name]['output_tokens'] += output_tokens
    
    # Save to file
    try:
        token_file = Path(config.token_monitoring_file)
        token_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(token_file, 'w') as f:
            json.dump(_token_usage, f, indent=2)
            
    except Exception as e:
        logger = get_logger(__name__)
        logger.warning(f"Failed to save token usage: {e}")

def get_token_usage_summary() -> Dict[str, Any]:
    """
    Get current token usage summary.
    
    Returns:
        Dictionary with token usage statistics
    """
    global _token_usage
    
    total_cost = 0
    # Rough cost calculation (Google Gemini pricing)
    # Input: $0.10/1M tokens, Output: $0.40/1M tokens
    input_cost = (_token_usage['total_input_tokens'] / 1_000_000) * 0.10
    output_cost = (_token_usage['total_output_tokens'] / 1_000_000) * 0.40
    total_cost = input_cost + output_cost
    
    return {
        'total_input_tokens': _token_usage['total_input_tokens'],
        'total_output_tokens': _token_usage['total_output_tokens'],
        'estimated_cost_usd': round(total_cost, 4),
        'agent_usage': _token_usage['agent_usage'],
        'session_start': _token_usage['session_start']
    }

def reset_token_usage() -> None:
    """Reset token usage tracking."""
    global _token_usage
    _token_usage = {
        'total_input_tokens': 0,
        'total_output_tokens': 0,
        'agent_usage': {},
        'session_start': datetime.now().isoformat()
    } 