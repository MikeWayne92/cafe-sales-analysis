#!/usr/bin/env python3
"""
Script to prepare GitHub Pages deployment.
Copies charts and creates static dashboard files.
"""

import os
import shutil
from pathlib import Path
import subprocess

def prepare_github_pages():
    """Prepare files for GitHub Pages deployment."""
    
    # Create docs directory if it doesn't exist
    docs_dir = Path("docs")
    docs_dir.mkdir(exist_ok=True)
    
    # Copy charts to docs directory
    charts_dir = Path("charts")
    if charts_dir.exists():
        print("📁 Copying charts to docs directory...")
        for chart_file in charts_dir.glob("*.html"):
            shutil.copy2(chart_file, docs_dir / chart_file.name)
            print(f"   ✅ Copied {chart_file.name}")
    
    # Create a simple README for the docs directory
    readme_content = """# Cafe Sales Analytics Dashboard

This directory contains the static files for the GitHub Pages deployment of the Cafe Sales Analytics Dashboard.

## Files
- `index.html` - Main dashboard page
- `*.html` - Interactive Plotly charts

## Access
Visit: https://mikewayne92.github.io/cafe-sales-analysis/

## Local Development
To run locally, simply open `index.html` in your web browser.
"""
    
    with open(docs_dir / "README.md", "w") as f:
        f.write(readme_content)
    
    print("✅ GitHub Pages preparation complete!")
    print("📝 Next steps:")
    print("   1. Commit and push the changes")
    print("   2. Enable GitHub Pages in repository settings")
    print("   3. Set source to 'GitHub Actions'")
    print("   4. Your dashboard will be available at: https://mikewayne92.github.io/cafe-sales-analysis/")

if __name__ == "__main__":
    prepare_github_pages() 