"""
Configuration management for Cafe Sales Analysis.
Handles loading, validation, and access to configuration parameters.
"""

import os
import yaml
from pathlib import Path
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field
import logging

logger = logging.getLogger(__name__)


class DataConfig(BaseModel):
    """Data configuration settings."""
    input_file: str = "dirty_cafe_sales.csv"
    output_dir: str = "output"
    charts_dir: str = "charts"
    reports_dir: str = "reports"


class AnalysisConfig(BaseModel):
    """Analysis parameters."""
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    min_transaction_amount: float = 0.01
    max_transaction_amount: float = 1000.0
    business_hours: Dict[str, str] = Field(default_factory=lambda: {"start": "06:00", "end": "22:00"})
    product_categories: Dict[str, list] = Field(default_factory=dict)


class VisualizationConfig(BaseModel):
    """Visualization settings."""
    charts_dir: str = "charts"
    colors: Dict[str, str] = Field(default_factory=lambda: {
        "primary": "#582f0e",      # Seal Brown - Main brand color
        "secondary": "#7f4f24",    # Russet - Secondary elements
        "accent": "#936639",       # Raw Umber - Accent highlights
        "success": "#656d4a",      # Reseda Green - Success indicators
        "neutral": "#b6ad90",      # Khaki - Neutral backgrounds
        "text_dark": "#333d29",    # Black Olive - Dark text
        "text_light": "#c2c5aa",   # Sage - Light text
        "background": "#a68a64",   # Lion - Background elements
        "highlight": "#a4ac86"     # Sage-2 - Highlight elements
    })
    style: Dict[str, str] = Field(default_factory=lambda: {
        "background_color": "#FFFFFF",
        "grid_color": "#E9ECEF",
        "font_family": "Inter, -apple-system, BlinkMacSystemFont, sans-serif"
    })
    dimensions: Dict[str, list] = Field(default_factory=lambda: {
        "small": [8, 6],
        "medium": [12, 8], 
        "large": [16, 10]
    })
    interactive: Dict[str, bool] = Field(default_factory=lambda: {
        "enable_hover": True,
        "enable_zoom": True,
        "enable_pan": True,
        "enable_selection": True
    })


class DashboardConfig(BaseModel):
    """Dashboard configuration."""
    title: str = "Cafe Sales Analytics Dashboard"
    theme: str = "light"
    refresh_interval: int = 300
    max_data_points: int = 10000


class APIConfig(BaseModel):
    """API configuration."""
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False
    cors_origins: list = Field(default_factory=lambda: ["*"])


class LoggingConfig(BaseModel):
    """Logging configuration."""
    level: str = "INFO"
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    file: str = "logs/analysis.log"


class PerformanceConfig(BaseModel):
    """Performance settings."""
    cache_enabled: bool = True
    cache_ttl: int = 3600
    parallel_processing: bool = True
    max_workers: int = 4


class ReportingConfig(BaseModel):
    """Reporting configuration."""
    format: list = Field(default_factory=lambda: ["html", "pdf"])
    include_charts: bool = True
    include_insights: bool = True
    auto_generate: bool = True


class AlertingConfig(BaseModel):
    """Alerting configuration."""
    enabled: bool = True
    thresholds: Dict[str, float] = Field(default_factory=lambda: {
        "sales_drop_percentage": 20,
        "unusual_transaction_amount": 500,
        "low_stock_threshold": 10
    })


class Config(BaseModel):
    """Main configuration class."""
    data: DataConfig = Field(default_factory=DataConfig)
    analysis: AnalysisConfig = Field(default_factory=AnalysisConfig)
    visualization: VisualizationConfig = Field(default_factory=VisualizationConfig)
    dashboard: DashboardConfig = Field(default_factory=DashboardConfig)
    api: APIConfig = Field(default_factory=APIConfig)
    logging: LoggingConfig = Field(default_factory=LoggingConfig)
    performance: PerformanceConfig = Field(default_factory=PerformanceConfig)
    reporting: ReportingConfig = Field(default_factory=ReportingConfig)
    alerting: AlertingConfig = Field(default_factory=AlertingConfig)


class ConfigManager:
    """Manages configuration loading and access."""
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize configuration manager.
        
        Args:
            config_path: Path to configuration file. Defaults to 'config.yaml'.
        """
        self.config_path = config_path or "config.yaml"
        self._config: Optional[Config] = None
        self._load_config()
    
    def _load_config(self) -> None:
        """Load configuration from YAML file."""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as file:
                    config_data = yaml.safe_load(file)
                    self._config = Config(**config_data)
                    logger.info(f"Configuration loaded from {self.config_path}")
            else:
                logger.warning(f"Configuration file {self.config_path} not found. Using defaults.")
                self._config = Config()
        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
            self._config = Config()
    
    def get_config(self) -> Config:
        """Get the current configuration."""
        return self._config
    
    def reload_config(self) -> None:
        """Reload configuration from file."""
        self._load_config()
    
    def get_data_config(self) -> DataConfig:
        """Get data configuration."""
        return self._config.data
    
    def get_analysis_config(self) -> AnalysisConfig:
        """Get analysis configuration."""
        return self._config.analysis
    
    def get_visualization_config(self) -> VisualizationConfig:
        """Get visualization configuration."""
        return self._config.visualization
    
    def get_dashboard_config(self) -> DashboardConfig:
        """Get dashboard configuration."""
        return self._config.dashboard
    
    def get_api_config(self) -> APIConfig:
        """Get API configuration."""
        return self._config.api
    
    def get_logging_config(self) -> LoggingConfig:
        """Get logging configuration."""
        return self._config.logging
    
    def get_performance_config(self) -> PerformanceConfig:
        """Get performance configuration."""
        return self._config.performance
    
    def get_reporting_config(self) -> ReportingConfig:
        """Get reporting configuration."""
        return self._config.reporting
    
    def get_alerting_config(self) -> AlertingConfig:
        """Get alerting configuration."""
        return self._config.alerting


# Global configuration instance
config_manager = ConfigManager()


def get_config() -> Config:
    """Get the global configuration instance."""
    return config_manager.get_config()


def get_data_config() -> DataConfig:
    """Get data configuration."""
    return config_manager.get_data_config()


def get_analysis_config() -> AnalysisConfig:
    """Get analysis configuration."""
    return config_manager.get_analysis_config()


def get_visualization_config() -> VisualizationConfig:
    """Get visualization configuration."""
    return config_manager.get_visualization_config()


def get_logging_config() -> LoggingConfig:
    """Get logging configuration."""
    return config_manager.get_logging_config()


def get_dashboard_config() -> DashboardConfig:
    """Get dashboard configuration."""
    return config_manager.get_dashboard_config() 