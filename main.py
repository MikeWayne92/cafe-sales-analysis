#!/usr/bin/env python3
"""
Main entry point for Cafe Sales Analysis.
Provides command-line interface for running the complete analysis pipeline.
"""

import argparse
import sys
import os
from pathlib import Path
from typing import Optional
import warnings

# Add src to path for imports
sys.path.append(str(Path(__file__).parent / "src"))

from src.data.loader import load_cafe_data
from src.visualization.charts import create_all_charts, InteractiveCharts
from src.utils.config import get_config, get_data_config
from src.utils.logger import setup_logging, get_logger, PerformanceLogger
from src.dashboard.streamlit_app import CafeDashboard

# Suppress warnings
warnings.filterwarnings('ignore')


class CafeAnalysisPipeline:
    """Main analysis pipeline for cafe sales data."""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the analysis pipeline.
        
        Args:
            config_path: Path to configuration file
        """
        self.config = get_config()
        self.logger = setup_logging()
        self.data = None
        self.summary = None
        
    def run_data_loading(self) -> bool:
        """
        Run the data loading and validation step.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            with PerformanceLogger(self.logger, "data loading and validation"):
                self.data, self.summary = load_cafe_data()
                self.logger.info("Data loading completed successfully")
                return True
        except Exception as e:
            self.logger.error(f"Data loading failed: {e}")
            return False
    
    def run_visualization(self, save_formats: list = ['html']) -> bool:
        """
        Run the visualization generation step.
        
        Args:
            save_formats: List of formats to save charts in
            
        Returns:
            True if successful, False otherwise
        """
        try:
            with PerformanceLogger(self.logger, "visualization generation"):
                charts = InteractiveCharts()
                
                # Create all charts
                chart_figures = create_all_charts(self.data)
                
                # Save charts in specified formats
                for chart_name, fig in chart_figures.items():
                    for format in save_formats:
                        charts.save_chart(fig, chart_name, format)
                
                self.logger.info(f"Visualization generation completed. Saved {len(chart_figures)} charts in {save_formats} format(s)")
                return True
        except Exception as e:
            self.logger.error(f"Visualization generation failed: {e}")
            return False
    
    def run_dashboard(self) -> bool:
        """
        Run the interactive dashboard.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            self.logger.info("Starting interactive dashboard...")
            dashboard = CafeDashboard()
            dashboard.run()
            return True
        except Exception as e:
            self.logger.error(f"Dashboard failed: {e}")
            return False
    
    def print_summary(self):
        """Print analysis summary to console."""
        if not self.summary:
            self.logger.warning("No summary available. Run data loading first.")
            return
        
        print("\n" + "="*60)
        print("📊 CAFE SALES ANALYSIS SUMMARY")
        print("="*60)
        
        print(f"\n📈 Key Metrics:")
        print(f"   • Total Records: {self.summary['total_records']:,}")
        print(f"   • Total Revenue: ${self.summary['total_sales']:,.2f}")
        print(f"   • Unique Items: {self.summary['unique_items']}")
        print(f"   • Unique Locations: {self.summary['unique_locations']}")
        
        print(f"\n📅 Date Range:")
        print(f"   • Start: {self.summary['date_range']['start'].strftime('%Y-%m-%d')}")
        print(f"   • End: {self.summary['date_range']['end'].strftime('%Y-%m-%d')}")
        
        print(f"\n💳 Payment Methods:")
        for method, count in self.summary['payment_methods'].items():
            print(f"   • {method}: {count:,} transactions")
        
        print(f"\n⚠️  Data Quality:")
        missing_values = {k: v for k, v in self.summary['missing_values'].items() if v > 0}
        if missing_values:
            for col, count in missing_values.items():
                print(f"   • {col}: {count} missing values")
        else:
            print("   • No missing values found")
        
        print("\n" + "="*60)
    
    def run_full_pipeline(self, save_formats: list = ['html'], show_dashboard: bool = False) -> bool:
        """
        Run the complete analysis pipeline.
        
        Args:
            save_formats: List of formats to save charts in
            show_dashboard: Whether to launch the interactive dashboard
            
        Returns:
            True if successful, False otherwise
        """
        self.logger.info("Starting Cafe Sales Analysis Pipeline")
        
        # Step 1: Data Loading
        if not self.run_data_loading():
            return False
        
        # Step 2: Print Summary
        self.print_summary()
        
        # Step 3: Visualization
        if not self.run_visualization(save_formats):
            return False
        
        # Step 4: Dashboard (if requested)
        if show_dashboard:
            if not self.run_dashboard():
                return False
        
        self.logger.info("Analysis pipeline completed successfully!")
        return True


def main():
    """Main function with command-line interface."""
    parser = argparse.ArgumentParser(
        description="Cafe Sales Analysis Pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run full analysis with HTML charts
  python main.py --full
  
  # Run analysis and launch dashboard
  python main.py --full --dashboard
  
  # Generate charts in multiple formats
  python main.py --full --formats html png pdf
  
  # Only generate visualizations
  python main.py --visualize
  
  # Only launch dashboard
  python main.py --dashboard
        """
    )
    
    parser.add_argument(
        '--full', 
        action='store_true',
        help='Run the complete analysis pipeline'
    )
    
    parser.add_argument(
        '--visualize', 
        action='store_true',
        help='Generate visualizations only'
    )
    
    parser.add_argument(
        '--dashboard', 
        action='store_true',
        help='Launch interactive dashboard'
    )
    
    parser.add_argument(
        '--formats', 
        nargs='+',
        default=['html'],
        choices=['html', 'png', 'jpg', 'svg', 'pdf'],
        help='Chart output formats (default: html)'
    )
    
    parser.add_argument(
        '--config', 
        type=str,
        help='Path to configuration file'
    )
    
    parser.add_argument(
        '--verbose', 
        action='store_true',
        help='Enable verbose logging'
    )
    
    args = parser.parse_args()
    
    # Set up logging level
    if args.verbose:
        setup_logging(level='DEBUG')
    else:
        setup_logging(level='INFO')
    
    logger = get_logger()
    
    try:
        # Initialize pipeline
        pipeline = CafeAnalysisPipeline(args.config)
        
        if args.full:
            # Run complete pipeline
            success = pipeline.run_full_pipeline(
                save_formats=args.formats,
                show_dashboard=args.dashboard
            )
        elif args.visualize:
            # Only generate visualizations
            if pipeline.run_data_loading():
                pipeline.print_summary()
                success = pipeline.run_visualization(args.formats)
            else:
                success = False
        elif args.dashboard:
            # Only launch dashboard
            success = pipeline.run_dashboard()
        else:
            # Default: run full pipeline without dashboard
            success = pipeline.run_full_pipeline(save_formats=args.formats)
        
        if success:
            logger.info("Analysis completed successfully!")
            sys.exit(0)
        else:
            logger.error("Analysis failed!")
            sys.exit(1)
            
    except KeyboardInterrupt:
        logger.info("Analysis interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 