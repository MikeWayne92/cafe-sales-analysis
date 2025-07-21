"""
Logging configuration and utilities for Cafe Sales Analysis.
Provides structured logging with file rotation and different log levels.
"""

import logging
import logging.handlers
import os
from pathlib import Path
from typing import Optional
from datetime import datetime
from src.utils.config import get_logging_config


class ColoredFormatter(logging.Formatter):
    """Custom formatter with colors for console output."""
    
    # ANSI color codes
    COLORS = {
        'DEBUG': '\033[36m',    # Cyan
        'INFO': '\033[32m',     # Green
        'WARNING': '\033[33m',  # Yellow
        'ERROR': '\033[31m',    # Red
        'CRITICAL': '\033[35m', # Magenta
        'RESET': '\033[0m'      # Reset
    }
    
    def format(self, record):
        # Add color to the level name
        if record.levelname in self.COLORS:
            record.levelname = f"{self.COLORS[record.levelname]}{record.levelname}{self.COLORS['RESET']}"
        
        return super().format(record)


def setup_logging(
    name: str = "cafe_analytics",
    level: Optional[str] = None,
    log_file: Optional[str] = None,
    max_bytes: int = 10 * 1024 * 1024,  # 10MB
    backup_count: int = 5
) -> logging.Logger:
    """
    Set up logging configuration.
    
    Args:
        name: Logger name
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Path to log file
        max_bytes: Maximum size of log file before rotation
        backup_count: Number of backup files to keep
        
    Returns:
        Configured logger instance
    """
    
    # Get configuration
    config = get_logging_config()
    level = level or config.level
    log_file = log_file or config.file
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))
    
    # Clear existing handlers
    logger.handlers.clear()
    
    # Create formatters
    console_formatter = ColoredFormatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    file_formatter = logging.Formatter(
        config.format,
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, level.upper()))
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    # File handler with rotation
    if log_file:
        # Ensure log directory exists
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding='utf-8'
        )
        file_handler.setLevel(getattr(logging, level.upper()))
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
    
    return logger


def get_logger(name: str = "cafe_analytics") -> logging.Logger:
    """
    Get a logger instance.
    
    Args:
        name: Logger name
        
    Returns:
        Logger instance
    """
    return logging.getLogger(name)


class PerformanceLogger:
    """Context manager for logging performance metrics."""
    
    def __init__(self, logger: logging.Logger, operation: str):
        """
        Initialize performance logger.
        
        Args:
            logger: Logger instance
            operation: Name of the operation being timed
        """
        self.logger = logger
        self.operation = operation
        self.start_time = None
    
    def __enter__(self):
        """Start timing the operation."""
        self.start_time = datetime.now()
        self.logger.info(f"Starting {self.operation}")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """End timing and log the duration."""
        if self.start_time:
            duration = datetime.now() - self.start_time
            if exc_type:
                self.logger.error(f"Failed {self.operation} after {duration.total_seconds():.2f}s")
            else:
                self.logger.info(f"Completed {self.operation} in {duration.total_seconds():.2f}s")


def log_function_call(func):
    """Decorator to log function calls with performance metrics."""
    def wrapper(*args, **kwargs):
        logger = get_logger()
        with PerformanceLogger(logger, f"function {func.__name__}"):
            return func(*args, **kwargs)
    return wrapper


def log_data_info(logger: logging.Logger, data, name: str = "Data"):
    """
    Log information about a dataset.
    
    Args:
        logger: Logger instance
        data: Dataset (pandas DataFrame)
        name: Name of the dataset
    """
    logger.info(f"{name} shape: {data.shape}")
    logger.info(f"{name} columns: {list(data.columns)}")
    logger.info(f"{name} data types: {data.dtypes.to_dict()}")
    logger.info(f"{name} memory usage: {data.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
    
    if hasattr(data, 'isnull'):
        null_counts = data.isnull().sum()
        if null_counts.sum() > 0:
            logger.warning(f"{name} missing values: {null_counts[null_counts > 0].to_dict()}")


# Initialize default logger
default_logger = setup_logging() 