"""
Data loading and validation for Cafe Sales Analysis.
Handles loading CSV files, data validation, and initial preprocessing.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Optional, Dict, Any, Tuple
import logging
from datetime import datetime
import warnings

from src.utils.config import get_data_config, get_analysis_config
from src.utils.logger import get_logger, PerformanceLogger, log_data_info

logger = get_logger(__name__)


class DataLoader:
    """Handles data loading and initial validation."""
    
    def __init__(self, file_path: Optional[str] = None):
        """
        Initialize data loader.
        
        Args:
            file_path: Path to the data file. If None, uses config default.
        """
        self.config = get_data_config()
        self.analysis_config = get_analysis_config()
        self.file_path = file_path or self.config.input_file
        self.data: Optional[pd.DataFrame] = None
        
    def load_data(self) -> pd.DataFrame:
        """
        Load data from CSV file with validation and error handling.
        
        Returns:
            Loaded and validated DataFrame
            
        Raises:
            FileNotFoundError: If the data file doesn't exist
            ValueError: If the data format is invalid
        """
        with PerformanceLogger(logger, f"loading data from {self.file_path}"):
            try:
                # Check if file exists
                if not Path(self.file_path).exists():
                    raise FileNotFoundError(f"Data file not found: {self.file_path}")
                
                # Load data with optimized settings
                self.data = pd.read_csv(
                    self.file_path,
                    parse_dates=['Transaction Date'],
                    infer_datetime_format=True,
                    cache_dates=True
                )
                
                # Log data information
                log_data_info(logger, self.data, "Raw data")
                
                # Basic validation
                self._validate_data()
                
                # Apply date filtering if specified
                if self.analysis_config.start_date or self.analysis_config.end_date:
                    self._filter_by_date()
                
                logger.info(f"Successfully loaded {len(self.data)} records")
                return self.data
                
            except Exception as e:
                logger.error(f"Error loading data: {e}")
                raise
    
    def _validate_data(self) -> None:
        """Validate loaded data for required columns and basic quality."""
        required_columns = [
            'Transaction Date', 'Item', 'Quantity', 'Price Per Unit', 
            'Total Spent', 'Payment Method', 'Location'
        ]
        
        # Check required columns
        missing_columns = set(required_columns) - set(self.data.columns)
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")
        
        # Check for empty DataFrame
        if self.data.empty:
            raise ValueError("Data file is empty")
        
        # Validate data types
        self._validate_data_types()
        
        # Check for extreme outliers
        self._check_outliers()
    
    def _validate_data_types(self) -> None:
        """Validate and correct data types."""
        # Convert Total Spent to numeric, handling errors
        self.data['Total Spent'] = pd.to_numeric(
            self.data['Total Spent'], 
            errors='coerce'
        )
        
        # Convert Quantity to numeric
        self.data['Quantity'] = pd.to_numeric(
            self.data['Quantity'], 
            errors='coerce'
        )
        
        # Convert Price Per Unit to numeric
        self.data['Price Per Unit'] = pd.to_numeric(
            self.data['Price Per Unit'], 
            errors='coerce'
        )
        
        # Ensure Transaction Date is datetime
        if not pd.api.types.is_datetime64_any_dtype(self.data['Transaction Date']):
            self.data['Transaction Date'] = pd.to_datetime(
                self.data['Transaction Date'], 
                errors='coerce'
            )
        
        # Log data type information
        logger.info(f"Data types after validation: {self.data.dtypes.to_dict()}")
    
    def _check_outliers(self) -> None:
        """Check for extreme outliers in numeric columns."""
        numeric_columns = ['Total Spent', 'Quantity', 'Price Per Unit']
        
        for col in numeric_columns:
            if col in self.data.columns:
                # Remove NaN values for outlier detection
                clean_data = self.data[col].dropna()
                
                if len(clean_data) > 0:
                    Q1 = clean_data.quantile(0.25)
                    Q3 = clean_data.quantile(0.75)
                    IQR = Q3 - Q1
                    
                    lower_bound = Q1 - 3 * IQR
                    upper_bound = Q3 + 3 * IQR
                    
                    outliers = clean_data[
                        (clean_data < lower_bound) | (clean_data > upper_bound)
                    ]
                    
                    if len(outliers) > 0:
                        logger.warning(
                            f"Found {len(outliers)} outliers in {col}: "
                            f"range [{outliers.min():.2f}, {outliers.max():.2f}]"
                        )
    
    def _filter_by_date(self) -> None:
        """Filter data by date range if specified in config."""
        if self.analysis_config.start_date:
            start_date = pd.to_datetime(self.analysis_config.start_date)
            self.data = self.data[self.data['Transaction Date'] >= start_date]
            logger.info(f"Filtered data from {start_date.date()}")
        
        if self.analysis_config.end_date:
            end_date = pd.to_datetime(self.analysis_config.end_date)
            self.data = self.data[self.data['Transaction Date'] <= end_date]
            logger.info(f"Filtered data until {end_date.date()}")
    
    def get_data_summary(self) -> Dict[str, Any]:
        """
        Get comprehensive data summary.
        
        Returns:
            Dictionary containing data summary statistics
        """
        if self.data is None:
            raise ValueError("Data not loaded. Call load_data() first.")
        
        summary = {
            'total_records': len(self.data),
            'date_range': {
                'start': self.data['Transaction Date'].min(),
                'end': self.data['Transaction Date'].max()
            },
            'total_sales': self.data['Total Spent'].sum(),
            'unique_items': self.data['Item'].nunique(),
            'unique_locations': self.data['Location'].nunique(),
            'payment_methods': self.data['Payment Method'].value_counts().to_dict(),
            'missing_values': self.data.isnull().sum().to_dict(),
            'data_types': self.data.dtypes.to_dict()
        }
        
        return summary
    
    def save_processed_data(self, output_path: Optional[str] = None) -> None:
        """
        Save processed data to file.
        
        Args:
            output_path: Output file path. If None, uses config default.
        """
        if self.data is None:
            raise ValueError("Data not loaded. Call load_data() first.")
        
        output_path = output_path or f"{self.config.output_dir}/processed_data.csv"
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        with PerformanceLogger(logger, f"saving processed data to {output_path}"):
            self.data.to_csv(output_path, index=False)
            logger.info(f"Processed data saved to {output_path}")


def load_cafe_data(file_path: Optional[str] = None) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Convenience function to load cafe data and get summary.
    
    Args:
        file_path: Path to the data file
        
    Returns:
        Tuple of (DataFrame, summary_dict)
    """
    loader = DataLoader(file_path)
    data = loader.load_data()
    summary = loader.get_data_summary()
    
    return data, summary


if __name__ == "__main__":
    # Test the data loader
    try:
        data, summary = load_cafe_data()
        print("Data loaded successfully!")
        print(f"Summary: {summary}")
    except Exception as e:
        print(f"Error: {e}") 