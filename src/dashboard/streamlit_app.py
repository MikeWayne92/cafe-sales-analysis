"""
Interactive Streamlit Dashboard for Cafe Sales Analysis.
Provides real-time data exploration with modern UI design.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
import warnings

# Import our custom modules
from src.data.loader import load_cafe_data
from src.visualization.charts import InteractiveCharts, ChartStyler
from src.utils.config import get_dashboard_config, get_visualization_config
from src.utils.logger import get_logger

# Suppress warnings
warnings.filterwarnings('ignore')

# Configure logger
logger = get_logger(__name__)

# Page configuration
st.set_page_config(
    page_title="Cafe Sales Analytics Dashboard",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: 700;
        color: #2E86AB;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
    }
    
    .metric-label {
        font-size: 1rem;
        opacity: 0.9;
        margin: 0;
    }
    
    .chart-container {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
    }
    
    .stSelectbox > div > div {
        background: white;
        border-radius: 10px;
    }
    
    .stDateInput > div > div {
        background: white;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)


class CafeDashboard:
    """Main dashboard class for cafe sales analytics."""
    
    def __init__(self):
        """Initialize dashboard with data and configuration."""
        self.config = get_dashboard_config()
        self.viz_config = get_visualization_config()
        self.charts = InteractiveCharts()
        self.data = None
        self.filtered_data = None
        
    def load_data(self):
        """Load and prepare data for the dashboard."""
        try:
            with st.spinner("Loading cafe sales data..."):
                self.data, self.summary = load_cafe_data()
                self.filtered_data = self.data.copy()
                st.success("Data loaded successfully!")
        except Exception as e:
            st.error(f"Error loading data: {e}")
            return False
        return True
    
    def render_header(self):
        """Render the main header section."""
        st.markdown(f"""
        <div class="main-header">
            ☕ {self.config.title}
        </div>
        """, unsafe_allow_html=True)
        
        # Add last updated timestamp
        st.markdown(f"""
        <div style="text-align: center; color: #666; margin-bottom: 2rem;">
            Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        </div>
        """, unsafe_allow_html=True)
    
    def render_sidebar_filters(self):
        """Render sidebar filters for data exploration."""
        st.sidebar.markdown("## 🔍 Data Filters")
        
        # Date range filter
        st.sidebar.markdown("### 📅 Date Range")
        min_date = self.data['Transaction Date'].min().date()
        max_date = self.data['Transaction Date'].max().date()
        
        date_range = st.sidebar.date_input(
            "Select date range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )
        
        if len(date_range) == 2:
            start_date, end_date = date_range
            self.filtered_data = self.data[
                (self.data['Transaction Date'].dt.date >= start_date) &
                (self.data['Transaction Date'].dt.date <= end_date)
            ]
        
        # Location filter
        st.sidebar.markdown("### 📍 Location")
        locations = ['All'] + sorted(self.data['Location'].unique().tolist())
        selected_location = st.sidebar.selectbox("Select location", locations)
        
        if selected_location != 'All':
            self.filtered_data = self.filtered_data[
                self.filtered_data['Location'] == selected_location
            ]
        
        # Payment method filter
        st.sidebar.markdown("### 💳 Payment Method")
        payment_methods = ['All'] + sorted(self.data['Payment Method'].unique().tolist())
        selected_payment = st.sidebar.selectbox("Select payment method", payment_methods)
        
        if selected_payment != 'All':
            self.filtered_data = self.filtered_data[
                self.filtered_data['Payment Method'] == selected_payment
            ]
        
        # Product filter
        st.sidebar.markdown("### 🍽️ Product Category")
        products = ['All'] + sorted(self.data['Item'].unique().tolist())
        selected_product = st.sidebar.selectbox("Select product", products)
        
        if selected_product != 'All':
            self.filtered_data = self.filtered_data[
                self.filtered_data['Item'] == selected_product
            ]
        
        # Reset filters button
        if st.sidebar.button("🔄 Reset Filters"):
            self.filtered_data = self.data.copy()
            st.rerun()
    
    def render_key_metrics(self):
        """Render key performance metrics."""
        st.markdown("## 📊 Key Performance Metrics")
        
        # Calculate metrics
        total_revenue = self.filtered_data['Total Spent'].sum()
        total_transactions = len(self.filtered_data)
        avg_transaction = self.filtered_data['Total Spent'].mean()
        unique_customers = self.filtered_data['Location'].nunique()
        
        # Create metric columns
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <p class="metric-value">${total_revenue:,.0f}</p>
                <p class="metric-label">Total Revenue</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <p class="metric-value">{total_transactions:,}</p>
                <p class="metric-label">Total Transactions</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <p class="metric-value">${avg_transaction:.2f}</p>
                <p class="metric-label">Average Transaction</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="metric-card">
                <p class="metric-value">{unique_customers}</p>
                <p class="metric-label">Active Locations</p>
            </div>
            """, unsafe_allow_html=True)
    
    def render_sales_trends(self):
        """Render sales trends section."""
        st.markdown("## 📈 Sales Trends")
        
        # Create sales trend chart
        fig = self.charts.sales_trend_chart(self.filtered_data)
        
        # Display in container
        with st.container():
            st.plotly_chart(fig, use_container_width=True)
    
    def render_product_analysis(self):
        """Render product analysis section."""
        st.markdown("## 🍽️ Product Performance")
        
        # Create product performance chart
        fig = self.charts.product_performance_chart(self.filtered_data)
        
        # Display in container
        with st.container():
            st.plotly_chart(fig, use_container_width=True)
    
    def render_time_analysis(self):
        """Render time-based analysis."""
        st.markdown("## ⏰ Time-Based Analysis")
        
        # Create time heatmap
        fig = self.charts.time_heatmap(self.filtered_data)
        
        # Display in container
        with st.container():
            st.plotly_chart(fig, use_container_width=True)
    
    def render_location_analysis(self):
        """Render location analysis."""
        st.markdown("## 📍 Location Performance")
        
        # Create location analysis chart
        fig = self.charts.location_analysis_chart(self.filtered_data)
        
        # Display in container
        with st.container():
            st.plotly_chart(fig, use_container_width=True)
    
    def render_payment_analysis(self):
        """Render payment method analysis."""
        st.markdown("## 💳 Payment Method Analysis")
        
        # Create payment method chart
        fig = self.charts.payment_method_chart(self.filtered_data)
        
        # Display in container
        with st.container():
            st.plotly_chart(fig, use_container_width=True)
    
    def render_data_explorer(self):
        """Render interactive data explorer."""
        st.markdown("## 🔍 Data Explorer")
        
        # Data summary
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📋 Data Summary")
            summary_data = {
                'Metric': ['Total Records', 'Date Range', 'Unique Items', 'Missing Values'],
                'Value': [
                    len(self.filtered_data),
                    f"{self.filtered_data['Transaction Date'].min().date()} to {self.filtered_data['Transaction Date'].max().date()}",
                    self.filtered_data['Item'].nunique(),
                    self.filtered_data.isnull().sum().sum()
                ]
            }
            st.dataframe(pd.DataFrame(summary_data), use_container_width=True)
        
        with col2:
            st.markdown("### 📊 Top Products")
            top_products = self.filtered_data.groupby('Item')['Total Spent'].sum().sort_values(ascending=False).head(10)
            st.dataframe(top_products.reset_index(), use_container_width=True)
        
        # Raw data viewer
        st.markdown("### 📄 Raw Data")
        if st.checkbox("Show raw data"):
            st.dataframe(self.filtered_data, use_container_width=True)
    
    def render_insights(self):
        """Render automated insights."""
        st.markdown("## 💡 Automated Insights")
        
        # Calculate insights
        insights = self._generate_insights()
        
        # Display insights in cards
        for i, insight in enumerate(insights):
            with st.container():
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                            padding: 1rem; border-radius: 10px; margin: 0.5rem 0; color: white;">
                    <h4>💡 Insight {i+1}</h4>
                    <p>{insight}</p>
                </div>
                """, unsafe_allow_html=True)
    
    def _generate_insights(self) -> list:
        """Generate automated insights from the data."""
        insights = []
        
        # Revenue insights
        total_revenue = self.filtered_data['Total Spent'].sum()
        avg_daily_revenue = self.filtered_data.groupby(self.filtered_data['Transaction Date'].dt.date)['Total Spent'].sum().mean()
        insights.append(f"Average daily revenue is ${avg_daily_revenue:,.2f}")
        
        # Product insights
        top_product = self.filtered_data.groupby('Item')['Total Spent'].sum().idxmax()
        top_product_revenue = self.filtered_data.groupby('Item')['Total Spent'].sum().max()
        insights.append(f"'{top_product}' is the highest-grossing product with ${top_product_revenue:,.2f} in sales")
        
        # Time insights
        peak_hour = self.filtered_data.groupby(self.filtered_data['Transaction Date'].dt.hour)['Total Spent'].sum().idxmax()
        insights.append(f"Peak sales hour is {peak_hour}:00 with highest revenue generation")
        
        # Location insights
        top_location = self.filtered_data.groupby('Location')['Total Spent'].sum().idxmax()
        top_location_revenue = self.filtered_data.groupby('Location')['Total Spent'].sum().max()
        insights.append(f"'{top_location}' is the best-performing location with ${top_location_revenue:,.2f} in revenue")
        
        # Payment insights
        preferred_payment = self.filtered_data['Payment Method'].mode().iloc[0]
        insights.append(f"'{preferred_payment}' is the most preferred payment method among customers")
        
        return insights
    
    def run(self):
        """Run the complete dashboard."""
        # Load data
        if not self.load_data():
            return
        
        # Render dashboard components
        self.render_header()
        self.render_sidebar_filters()
        self.render_key_metrics()
        
        # Create tabs for different sections
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "📈 Sales Trends", "🍽️ Products", "⏰ Time Analysis", 
            "📍 Locations", "💳 Payments", "🔍 Explorer"
        ])
        
        with tab1:
            self.render_sales_trends()
        
        with tab2:
            self.render_product_analysis()
        
        with tab3:
            self.render_time_analysis()
        
        with tab4:
            self.render_location_analysis()
        
        with tab5:
            self.render_payment_analysis()
        
        with tab6:
            self.render_data_explorer()
            self.render_insights()


def main():
    """Main function to run the dashboard."""
    try:
        dashboard = CafeDashboard()
        dashboard.run()
    except Exception as e:
        st.error(f"An error occurred: {e}")
        logger.error(f"Dashboard error: {e}")


if __name__ == "__main__":
    main() 