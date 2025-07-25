#!/usr/bin/env python3
"""
Automated script to update GitHub Pages with latest charts and data.
This script runs the analysis, generates charts, and prepares the GitHub Pages deployment.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_analysis():
    """Run the main analysis to generate charts."""
    print("🔍 Running cafe sales analysis...")
    try:
        result = subprocess.run([sys.executable, "main.py"], 
                              capture_output=True, text=True, check=True)
        print("✅ Analysis completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Analysis failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def prepare_github_pages():
    """Prepare files for GitHub Pages deployment."""
    print("📁 Preparing GitHub Pages deployment...")
    
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
        
        # Copy PNG files as well
        for png_file in charts_dir.glob("*.png"):
            shutil.copy2(png_file, docs_dir / png_file.name)
            print(f"   ✅ Copied {png_file.name}")
    
    print("✅ GitHub Pages preparation complete!")

def git_commit_and_push():
    """Commit and push changes to trigger GitHub Pages deployment."""
    print("🚀 Committing and pushing changes...")
    
    try:
        # Add all changes
        subprocess.run(["git", "add", "docs/"], check=True)
        print("   ✅ Added docs/ to git")
        
        # Commit changes
        subprocess.run(["git", "commit", "-m", "Update GitHub Pages with latest charts and analysis"], check=True)
        print("   ✅ Committed changes")
        
        # Push to main branch
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("   ✅ Pushed to main branch")
        
        print("🎉 Successfully triggered GitHub Pages deployment!")
        print("📝 Your dashboard will be updated at: https://mikewayne92.github.io/cafe-sales-analysis/")
        print("⏱️  It may take a few minutes for the changes to appear.")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Git operation failed: {e}")
        return False
    
    return True

def main():
    """Main function to orchestrate the entire update process."""
    print("🚀 Starting GitHub Pages update process...")
    print("=" * 50)
    
    # Step 1: Run analysis
    if not run_analysis():
        print("❌ Failed to run analysis. Exiting.")
        sys.exit(1)
    
    # Step 2: Prepare GitHub Pages
    prepare_github_pages()
    
    # Step 3: Commit and push
    if not git_commit_and_push():
        print("❌ Failed to commit and push changes. Exiting.")
        sys.exit(1)
    
    print("=" * 50)
    print("🎉 GitHub Pages update completed successfully!")
    print("📊 Your dashboard is now live with the latest data and charts.")

if __name__ == "__main__":
    main() 