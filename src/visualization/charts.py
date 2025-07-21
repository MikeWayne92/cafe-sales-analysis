"""
Advanced visualization module for Cafe Sales Analysis.
Provides interactive charts with modern design and custom styling.
"""

import plotly.graph_objects as go
import plotly.express as px
import plotly.subplots as sp
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime, timedelta
import warnings
from pathlib import Path

from src.utils.config import get_visualization_config, get_analysis_config
from src.utils.logger import get_logger, PerformanceLogger

logger = get_logger(__name__)

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')


class ChartStyler:
    """Handles chart styling and theme configuration."""
    
    def __init__(self):
        """Initialize chart styler with configuration."""
        self.config = get_visualization_config()
        self.colors = self.config.colors
        self.style = self.config.style
        self.dimensions = self.config.dimensions
        
    def get_layout_template(self, title: str, width: int = 1200, height: int = 800) -> Dict[str, Any]:
        """
        Get standardized layout template for charts.
        
        Args:
            title: Chart title
            width: Chart width
            height: Chart height
            
        Returns:
            Layout dictionary
        """
        return {
            'title': {
                'text': title,
                'x': 0.5,
                'xanchor': 'center',
                'font': {
                    'size': 24,
                    'color': self.colors['primary'],
                    'family': self.style['font_family']
                }
            },
            'paper_bgcolor': self.style['background_color'],
            'plot_bgcolor': self.style['background_color'],
            'font': {
                'family': self.style['font_family'],
                'size': 12,
                'color': '#2C3E50'
            },
            'margin': {'l': 60, 'r': 60, 't': 80, 'b': 60},
            'width': width,
            'height': height,
            'showlegend': True,
            'legend': {
                'bgcolor': 'rgba(255,255,255,0.8)',
                'bordercolor': self.colors['neutral'],
                'borderwidth': 1
            },
            'hovermode': 'closest' if self.config.interactive['enable_hover'] else False
        }
    
    def get_color_palette(self, n_colors: int) -> List[str]:
        """
        Get a color palette for charts.
        
        Args:
            n_colors: Number of colors needed
            
        Returns:
            List of color hex codes
        """
        base_colors = [
            self.colors['primary'],
            self.colors['secondary'],
            self.colors['accent'],
            self.colors['success'],
            '#6C5CE7',  # Purple
            '#00B894',  # Green
            '#FDCB6E',  # Yellow
            '#E17055',  # Orange
            '#74B9FF',  # Blue
            '#A29BFE'   # Light Purple
        ]
        
        if n_colors <= len(base_colors):
            return base_colors[:n_colors]
        else:
            # Generate additional colors if needed
            import colorsys
            colors = []
            for i in range(n_colors):
                hue = i / n_colors
                rgb = colorsys.hsv_to_rgb(hue, 0.7, 0.8)
                colors.append(f'rgb({int(rgb[0]*255)}, {int(rgb[1]*255)}, {int(rgb[2]*255)})')
            return colors


class InteractiveCharts:
    """Creates interactive charts using Plotly."""
    
    def __init__(self):
        """Initialize interactive charts with styling."""
        self.styler = ChartStyler()
        self.config = get_visualization_config()
        
    def sales_trend_chart(self, data: pd.DataFrame) -> go.Figure:
        """
        Create interactive sales trend chart.
        
        Args:
            data: Sales data DataFrame
            
        Returns:
            Plotly figure object
        """
        with PerformanceLogger(logger, "creating sales trend chart"):
            # Prepare data
            daily_sales = data.groupby(data['Transaction Date'].dt.date)['Total Spent'].agg([
                'sum', 'count', 'mean'
            ]).reset_index()
            daily_sales['Transaction Date'] = pd.to_datetime(daily_sales['Transaction Date'])
            
            # Create figure with secondary y-axis
            fig = make_subplots(
                rows=2, cols=1,
                subplot_titles=('Daily Sales Revenue', 'Daily Transaction Count'),
                vertical_spacing=0.1,
                specs=[[{"secondary_y": False}], [{"secondary_y": False}]]
            )
            
            # Revenue line
            fig.add_trace(
                go.Scatter(
                    x=daily_sales['Transaction Date'],
                    y=daily_sales['sum'],
                    mode='lines+markers',
                    name='Revenue',
                    line=dict(color=self.styler.colors['primary'], width=3),
                    marker=dict(size=6),
                    hovertemplate='<b>Date:</b> %{x}<br><b>Revenue:</b> $%{y:,.2f}<extra></extra>'
                ),
                row=1, col=1
            )
            
            # Transaction count
            fig.add_trace(
                go.Bar(
                    x=daily_sales['Transaction Date'],
                    y=daily_sales['count'],
                    name='Transactions',
                    marker_color=self.styler.colors['accent'],
                    opacity=0.7,
                    hovertemplate='<b>Date:</b> %{x}<br><b>Transactions:</b> %{y}<extra></extra>'
                ),
                row=2, col=1
            )
            
            # Update layout
            layout = self.styler.get_layout_template(
                "Sales Performance Over Time",
                width=1200,
                height=800
            )
            fig.update_layout(layout)
            
            # Update axes
            fig.update_xaxes(title_text="Date", row=1, col=1)
            fig.update_yaxes(title_text="Revenue ($)", row=1, col=1)
            fig.update_xaxes(title_text="Date", row=2, col=1)
            fig.update_yaxes(title_text="Transaction Count", row=2, col=1)
            
            return fig
    
    def product_performance_chart(self, data: pd.DataFrame) -> go.Figure:
        """
        Create interactive product performance chart.
        
        Args:
            data: Sales data DataFrame
            
        Returns:
            Plotly figure object
        """
        with PerformanceLogger(logger, "creating product performance chart"):
            # Prepare data
            product_stats = data.groupby('Item').agg({
                'Total Spent': ['sum', 'count', 'mean'],
                'Quantity': 'sum'
            }).round(2)
            product_stats.columns = ['Revenue', 'Transactions', 'Avg_Price', 'Units_Sold']
            product_stats = product_stats.sort_values('Revenue', ascending=False).head(15)
            
            # Create subplots
            fig = make_subplots(
                rows=2, cols=2,
                subplot_titles=(
                    'Top Products by Revenue',
                    'Top Products by Units Sold',
                    'Average Price by Product',
                    'Revenue vs Units Sold'
                ),
                specs=[[{"type": "bar"}, {"type": "bar"}],
                       [{"type": "bar"}, {"type": "scatter"}]]
            )
            
            colors = self.styler.get_color_palette(len(product_stats))
            
            # Revenue bar chart
            fig.add_trace(
                go.Bar(
                    x=product_stats.index,
                    y=product_stats['Revenue'],
                    name='Revenue',
                    marker_color=colors,
                    hovertemplate='<b>%{x}</b><br>Revenue: $%{y:,.2f}<extra></extra>'
                ),
                row=1, col=1
            )
            
            # Units sold bar chart
            fig.add_trace(
                go.Bar(
                    x=product_stats.index,
                    y=product_stats['Units_Sold'],
                    name='Units Sold',
                    marker_color=self.styler.colors['secondary'],
                    hovertemplate='<b>%{x}</b><br>Units: %{y}<extra></extra>'
                ),
                row=1, col=2
            )
            
            # Average price bar chart
            fig.add_trace(
                go.Bar(
                    x=product_stats.index,
                    y=product_stats['Avg_Price'],
                    name='Avg Price',
                    marker_color=self.styler.colors['accent'],
                    hovertemplate='<b>%{x}</b><br>Avg Price: $%{y:.2f}<extra></extra>'
                ),
                row=2, col=1
            )
            
            # Scatter plot: Revenue vs Units
            fig.add_trace(
                go.Scatter(
                    x=product_stats['Units_Sold'],
                    y=product_stats['Revenue'],
                    mode='markers+text',
                    text=product_stats.index,
                    textposition="top center",
                    name='Revenue vs Units',
                    marker=dict(
                        size=product_stats['Transactions'] / 10,
                        color=colors,
                        opacity=0.7
                    ),
                    hovertemplate='<b>%{text}</b><br>Revenue: $%{y:,.2f}<br>Units: %{x}<extra></extra>'
                ),
                row=2, col=2
            )
            
            # Update layout
            layout = self.styler.get_layout_template(
                "Product Performance Analysis",
                width=1400,
                height=1000
            )
            fig.update_layout(layout)
            
            # Update axes
            fig.update_xaxes(title_text="Product", row=1, col=1)
            fig.update_yaxes(title_text="Revenue ($)", row=1, col=1)
            fig.update_xaxes(title_text="Product", row=1, col=2)
            fig.update_yaxes(title_text="Units Sold", row=1, col=2)
            fig.update_xaxes(title_text="Product", row=2, col=1)
            fig.update_yaxes(title_text="Average Price ($)", row=2, col=1)
            fig.update_xaxes(title_text="Units Sold", row=2, col=2)
            fig.update_yaxes(title_text="Revenue ($)", row=2, col=2)
            
            return fig
    
    def time_heatmap(self, data: pd.DataFrame) -> go.Figure:
        """
        Create interactive time-based heatmap.
        
        Args:
            data: Sales data DataFrame
            
        Returns:
            Plotly figure object
        """
        with PerformanceLogger(logger, "creating time heatmap"):
            # Prepare data
            data['Day_of_Week'] = data['Transaction Date'].dt.day_name()
            data['Hour'] = data['Transaction Date'].dt.hour
            
            # Create pivot table
            heatmap_data = data.pivot_table(
                index='Day_of_Week',
                columns='Hour',
                values='Total Spent',
                aggfunc='sum',
                fill_value=0
            )
            
            # Reorder days
            day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            heatmap_data = heatmap_data.reindex(day_order)
            
            # Create heatmap
            fig = go.Figure(data=go.Heatmap(
                z=heatmap_data.values,
                x=heatmap_data.columns,
                y=heatmap_data.index,
                colorscale='Viridis',
                hovertemplate='<b>%{y} at %{x}:00</b><br>Revenue: $%{z:,.2f}<extra></extra>',
                colorbar=dict(title="Revenue ($)")
            ))
            
            # Update layout
            layout = self.styler.get_layout_template(
                "Sales Heatmap by Day and Hour",
                width=1000,
                height=600
            )
            layout.update({
                'xaxis': {'title': 'Hour of Day'},
                'yaxis': {'title': 'Day of Week'}
            })
            fig.update_layout(layout)
            
            return fig
    
    def location_analysis_chart(self, data: pd.DataFrame) -> go.Figure:
        """
        Create interactive location analysis chart.
        
        Args:
            data: Sales data DataFrame
            
        Returns:
            Plotly figure object
        """
        with PerformanceLogger(logger, "creating location analysis chart"):
            # Prepare data
            location_stats = data.groupby('Location').agg({
                'Total Spent': ['sum', 'count', 'mean'],
                'Item': 'nunique'
            }).round(2)
            location_stats.columns = ['Revenue', 'Transactions', 'Avg_Transaction', 'Unique_Items']
            location_stats = location_stats.sort_values('Revenue', ascending=False)
            
            # Create subplots
            fig = make_subplots(
                rows=2, cols=2,
                subplot_titles=(
                    'Revenue by Location',
                    'Transaction Count by Location',
                    'Average Transaction Value',
                    'Revenue vs Transaction Count'
                ),
                specs=[[{"type": "bar"}, {"type": "bar"}],
                       [{"type": "bar"}, {"type": "scatter"}]]
            )
            
            colors = self.styler.get_color_palette(len(location_stats))
            
            # Revenue bar chart
            fig.add_trace(
                go.Bar(
                    x=location_stats.index,
                    y=location_stats['Revenue'],
                    name='Revenue',
                    marker_color=colors,
                    hovertemplate='<b>%{x}</b><br>Revenue: $%{y:,.2f}<extra></extra>'
                ),
                row=1, col=1
            )
            
            # Transaction count bar chart
            fig.add_trace(
                go.Bar(
                    x=location_stats.index,
                    y=location_stats['Transactions'],
                    name='Transactions',
                    marker_color=self.styler.colors['secondary'],
                    hovertemplate='<b>%{x}</b><br>Transactions: %{y}<extra></extra>'
                ),
                row=1, col=2
            )
            
            # Average transaction value
            fig.add_trace(
                go.Bar(
                    x=location_stats.index,
                    y=location_stats['Avg_Transaction'],
                    name='Avg Transaction',
                    marker_color=self.styler.colors['accent'],
                    hovertemplate='<b>%{x}</b><br>Avg Transaction: $%{y:.2f}<extra></extra>'
                ),
                row=2, col=1
            )
            
            # Scatter plot: Revenue vs Transactions
            fig.add_trace(
                go.Scatter(
                    x=location_stats['Transactions'],
                    y=location_stats['Revenue'],
                    mode='markers+text',
                    text=location_stats.index,
                    textposition="top center",
                    name='Revenue vs Transactions',
                    marker=dict(
                        size=location_stats['Unique_Items'] * 2,
                        color=colors,
                        opacity=0.7
                    ),
                    hovertemplate='<b>%{text}</b><br>Revenue: $%{y:,.2f}<br>Transactions: %{x}<extra></extra>'
                ),
                row=2, col=2
            )
            
            # Update layout
            layout = self.styler.get_layout_template(
                "Location Performance Analysis",
                width=1400,
                height=1000
            )
            fig.update_layout(layout)
            
            # Update axes
            fig.update_xaxes(title_text="Location", row=1, col=1)
            fig.update_yaxes(title_text="Revenue ($)", row=1, col=1)
            fig.update_xaxes(title_text="Location", row=1, col=2)
            fig.update_yaxes(title_text="Transaction Count", row=1, col=2)
            fig.update_xaxes(title_text="Location", row=2, col=1)
            fig.update_yaxes(title_text="Average Transaction ($)", row=2, col=1)
            fig.update_xaxes(title_text="Transaction Count", row=2, col=2)
            fig.update_yaxes(title_text="Revenue ($)", row=2, col=2)
            
            return fig
    
    def payment_method_chart(self, data: pd.DataFrame) -> go.Figure:
        """
        Create interactive payment method analysis chart.
        
        Args:
            data: Sales data DataFrame
            
        Returns:
            Plotly figure object
        """
        with PerformanceLogger(logger, "creating payment method chart"):
            # Prepare data
            payment_stats = data.groupby('Payment Method').agg({
                'Total Spent': ['sum', 'count', 'mean']
            }).round(2)
            payment_stats.columns = ['Revenue', 'Transactions', 'Avg_Transaction']
            payment_stats = payment_stats.sort_values('Revenue', ascending=False)
            
            # Create subplots
            fig = make_subplots(
                rows=1, cols=3,
                subplot_titles=('Revenue by Payment Method', 'Transaction Count', 'Average Transaction Value'),
                specs=[[{"type": "pie"}, {"type": "bar"}, {"type": "bar"}]]
            )
            
            colors = self.styler.get_color_palette(len(payment_stats))
            
            # Pie chart for revenue
            fig.add_trace(
                go.Pie(
                    labels=payment_stats.index,
                    values=payment_stats['Revenue'],
                    name='Revenue',
                    marker_colors=colors,
                    hovertemplate='<b>%{label}</b><br>Revenue: $%{value:,.2f}<br>Share: %{percent}<extra></extra>'
                ),
                row=1, col=1
            )
            
            # Bar chart for transaction count
            fig.add_trace(
                go.Bar(
                    x=payment_stats.index,
                    y=payment_stats['Transactions'],
                    name='Transactions',
                    marker_color=self.styler.colors['secondary'],
                    hovertemplate='<b>%{x}</b><br>Transactions: %{y}<extra></extra>'
                ),
                row=1, col=2
            )
            
            # Bar chart for average transaction
            fig.add_trace(
                go.Bar(
                    x=payment_stats.index,
                    y=payment_stats['Avg_Transaction'],
                    name='Avg Transaction',
                    marker_color=self.styler.colors['accent'],
                    hovertemplate='<b>%{x}</b><br>Avg Transaction: $%{y:.2f}<extra></extra>'
                ),
                row=1, col=3
            )
            
            # Update layout
            layout = self.styler.get_layout_template(
                "Payment Method Analysis",
                width=1400,
                height=600
            )
            fig.update_layout(layout)
            
            return fig
    
    def save_chart(self, fig: go.Figure, filename: str, format: str = 'html') -> str:
        """
        Save chart to file.
        
        Args:
            fig: Plotly figure object
            filename: Output filename
            format: Output format (html, png, jpg, svg, pdf)
            
        Returns:
            Path to saved file
        """
        config = get_visualization_config()
        output_dir = Path(config.charts_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        filepath = output_dir / f"{filename}.{format}"
        
        if format == 'html':
            fig.write_html(str(filepath))
        else:
            fig.write_image(str(filepath))
        
        logger.info(f"Chart saved to {filepath}")
        return str(filepath)


def create_all_charts(data: pd.DataFrame) -> Dict[str, go.Figure]:
    """
    Create all interactive charts for the dataset.
    
    Args:
        data: Sales data DataFrame
        
    Returns:
        Dictionary of chart names and figures
    """
    charts = InteractiveCharts()
    
    chart_figures = {
        'sales_trend': charts.sales_trend_chart(data),
        'product_performance': charts.product_performance_chart(data),
        'time_heatmap': charts.time_heatmap(data),
        'location_analysis': charts.location_analysis_chart(data),
        'payment_methods': charts.payment_method_chart(data)
    }
    
    return chart_figures


if __name__ == "__main__":
    # Test the visualization module
    from src.data.loader import load_cafe_data
    
    try:
        data, summary = load_cafe_data()
        charts = InteractiveCharts()
        
        # Create and save a sample chart
        fig = charts.sales_trend_chart(data)
        charts.save_chart(fig, 'sample_sales_trend', 'html')
        
        print("Visualization test completed successfully!")
    except Exception as e:
        print(f"Error: {e}") 