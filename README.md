# ☕ Cafe Sales Analytics Platform

A **professional, dynamic, and interactive** data analysis platform for cafe sales data. Built with modern Python technologies, featuring interactive visualizations, real-time dashboards, and automated insights generation.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![Plotly](https://img.shields.io/badge/Plotly-5.15+-purple.svg)
![Pandas](https://img.shields.io/badge/Pandas-2.0+-green.svg)

## 🚀 Features

### ✨ **Interactive & Dynamic**
- **Real-time Dashboard**: Beautiful Streamlit web application with live data exploration
- **Interactive Charts**: Plotly-powered visualizations with zoom, hover, and filtering
- **Dynamic Filtering**: Filter by date, location, payment method, and products
- **Automated Insights**: AI-generated insights and recommendations

### 🏗️ **Professional Architecture**
- **Modular Design**: Clean, maintainable code structure with separation of concerns
- **Configuration Management**: Centralized YAML configuration for all parameters
- **Comprehensive Logging**: Structured logging with performance metrics
- **Data Validation**: Robust data quality checks and error handling

### 📊 **Advanced Analytics**
- **Multi-dimensional Analysis**: Sales trends, product performance, location analysis
- **Time-based Insights**: Hourly, daily, and weekly patterns
- **Statistical Analysis**: Outlier detection, correlation analysis
- **Performance Optimization**: Caching, parallel processing, memory management

### 🎨 **Modern Design**
- **Custom Styling**: Beautiful, professional color schemes and typography
- **Responsive Layout**: Works seamlessly on desktop and mobile
- **Accessibility**: High contrast, readable fonts, and intuitive navigation

## 📁 Project Structure

```
Cafe Data/
├── src/                          # Source code
│   ├── data/                     # Data loading and validation
│   │   ├── __init__.py
│   │   └── loader.py
│   ├── analysis/                 # Analysis modules (future)
│   ├── visualization/            # Chart generation
│   │   ├── __init__.py
│   │   └── charts.py
│   ├── dashboard/                # Dashboard applications
│   │   ├── __init__.py
│   │   └── streamlit_app.py
│   ├── utils/                    # Utilities and helpers
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── logger.py
│   └── __init__.py
├── charts/                       # Generated charts
├── logs/                         # Application logs
├── output/                       # Processed data
├── reports/                      # Generated reports
├── tests/                        # Unit tests
├── config.yaml                   # Configuration file
├── main.py                       # Main entry point
├── requirements.txt              # Dependencies
└── README.md                     # This file
```

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Quick Start

1. **Clone the repository**:
   ```bash
   git clone https://github.com/MikeWayne92/cafe-sales-analysis.git
   cd cafe-sales-analysis
   ```

2. **Create virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify installation**:
   ```bash
   python main.py --help
   ```

## 🚀 Usage

### Command Line Interface

The platform provides a powerful command-line interface with multiple options:

#### **Full Analysis Pipeline**
```bash
# Run complete analysis with interactive HTML charts
python main.py --full

# Run analysis and launch dashboard
python main.py --full --dashboard

# Generate charts in multiple formats
python main.py --full --formats html png pdf
```

#### **Individual Components**
```bash
# Generate visualizations only
python main.py --visualize

# Launch interactive dashboard only
python main.py --dashboard

# Generate charts in specific formats
python main.py --visualize --formats html png
```

#### **Advanced Options**
```bash
# Use custom configuration file
python main.py --full --config custom_config.yaml

# Enable verbose logging
python main.py --full --verbose
```

### Interactive Dashboard

Launch the beautiful Streamlit dashboard:

```bash
# Method 1: Using main.py
python main.py --dashboard

# Method 2: Direct Streamlit command
streamlit run src/dashboard/streamlit_app.py
```

The dashboard features:
- **Real-time Data Exploration**: Filter and explore data dynamically
- **Interactive Charts**: Zoom, hover, and interact with visualizations
- **Key Metrics**: Live performance indicators
- **Automated Insights**: AI-generated business insights
- **Data Explorer**: Raw data viewer with summary statistics

### Configuration

Customize the analysis by editing `config.yaml`:

```yaml
# Data Configuration
data:
  input_file: "dirty_cafe_sales.csv"
  output_dir: "output"
  charts_dir: "charts"

# Analysis Parameters
analysis:
  min_transaction_amount: 0.01
  max_transaction_amount: 1000.0
  business_hours:
    start: "06:00"
    end: "22:00"

# Visualization Settings
visualization:
  colors:
    primary: "#2E86AB"
    secondary: "#A23B72"
    accent: "#F18F01"
```

## 📊 Analysis Features

### **Sales Trends Analysis**
- Daily, weekly, and monthly revenue trends
- Transaction volume patterns
- Seasonal variations and growth rates

### **Product Performance**
- Top-selling products by revenue and volume
- Product category analysis
- Price-performance correlation

### **Location Analytics**
- Location-wise performance comparison
- Geographic revenue distribution
- Store efficiency metrics

### **Time-based Insights**
- Peak hours and days identification
- Business hour optimization
- Seasonal trend analysis

### **Payment Method Analysis**
- Payment preference trends
- Transaction value by payment type
- Customer behavior patterns

## 🎨 Visualization Gallery

The platform generates beautiful, interactive charts:

- **Sales Trend Charts**: Multi-panel time series analysis
- **Product Performance**: Multi-dimensional product analysis
- **Time Heatmaps**: Day/hour sales patterns
- **Location Analysis**: Geographic performance visualization
- **Payment Method Charts**: Payment preference analysis

All charts feature:
- **Interactive Elements**: Zoom, pan, hover, selection
- **Professional Styling**: Custom color schemes and typography
- **Responsive Design**: Adapts to different screen sizes
- **Export Options**: Save in multiple formats (HTML, PNG, PDF)

## 🔧 Development

### **Adding New Analysis**
1. Create new module in `src/analysis/`
2. Implement analysis logic with proper logging
3. Add configuration options to `config.yaml`
4. Update main pipeline in `main.py`

### **Adding New Visualizations**
1. Add chart method to `InteractiveCharts` class
2. Implement with Plotly for interactivity
3. Add to `create_all_charts()` function
4. Update dashboard if needed

### **Testing**
```bash
# Run tests
pytest tests/

# Run with coverage
pytest --cov=src tests/
```

## 📈 Performance

The platform is optimized for performance:

- **Data Loading**: Optimized CSV parsing with caching
- **Visualization**: Efficient chart generation with lazy loading
- **Memory Management**: Smart data handling for large datasets
- **Caching**: Configurable caching for repeated operations

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes with proper documentation
4. Add tests for new functionality
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue on GitHub
- Check the documentation in the code
- Review the configuration examples

## 🔮 Roadmap

### **Planned Features**
- [ ] Machine Learning integration for predictive analytics
- [ ] Real-time data streaming capabilities
- [ ] Advanced statistical analysis modules
- [ ] API endpoints for external integrations
- [ ] Automated report generation and email delivery
- [ ] Multi-language support
- [ ] Mobile app companion

### **Performance Improvements**
- [ ] Database integration for large datasets
- [ ] Distributed processing capabilities
- [ ] Advanced caching strategies
- [ ] Real-time data synchronization

---

**Built with ❤️ for data-driven cafe management** 