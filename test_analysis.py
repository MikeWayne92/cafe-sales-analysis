#!/usr/bin/env python3
"""
Simple test script to verify the cafe analysis system works correctly.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

def test_imports():
    """Test that all modules can be imported correctly."""
    print("Testing imports...")
    
    try:
        from src.utils.config import get_config
        from src.utils.logger import setup_logging
        from src.data.loader import load_cafe_data
        from src.visualization.charts import InteractiveCharts
        print("✅ All imports successful")
        return True
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def test_config():
    """Test configuration loading."""
    print("Testing configuration...")
    
    try:
        from src.utils.config import get_config
        config = get_config()
        print(f"✅ Configuration loaded: {config.dashboard.title}")
        return True
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False

def test_data_loading():
    """Test data loading functionality."""
    print("Testing data loading...")
    
    try:
        from src.data.loader import load_cafe_data
        data, summary = load_cafe_data()
        print(f"✅ Data loaded: {len(data)} records")
        print(f"   Total revenue: ${summary['total_sales']:,.2f}")
        return True
    except Exception as e:
        print(f"❌ Data loading error: {e}")
        return False

def test_visualization():
    """Test visualization generation."""
    print("Testing visualization...")
    
    try:
        from src.data.loader import load_cafe_data
        from src.visualization.charts import InteractiveCharts
        
        data, _ = load_cafe_data()
        charts = InteractiveCharts()
        
        # Test creating a simple chart
        fig = charts.sales_trend_chart(data)
        print(f"✅ Chart created: {type(fig).__name__}")
        return True
    except Exception as e:
        print(f"❌ Visualization error: {e}")
        return False

def main():
    """Run all tests."""
    print("🧪 Testing Cafe Sales Analysis System")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_config,
        test_data_loading,
        test_visualization
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! System is ready to use.")
        print("\nNext steps:")
        print("1. Run full analysis: python main.py --full")
        print("2. Launch dashboard: python main.py --dashboard")
        print("3. Generate charts: python main.py --visualize")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 