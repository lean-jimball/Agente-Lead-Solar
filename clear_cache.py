#!/usr/bin/env python3
"""
Script to clear Streamlit cache and restart the application cleanly
"""
import os
import shutil
import subprocess
import sys

def clear_streamlit_cache():
    """Clear Streamlit cache directories"""
    cache_dirs = [
        os.path.expanduser("~/.streamlit"),
        ".streamlit",
        "__pycache__",
        ".cache"
    ]
    
    for cache_dir in cache_dirs:
        if os.path.exists(cache_dir):
            try:
                if os.path.isdir(cache_dir):
                    shutil.rmtree(cache_dir)
                    print(f"✅ Cleared cache directory: {cache_dir}")
                else:
                    os.remove(cache_dir)
                    print(f"✅ Cleared cache file: {cache_dir}")
            except Exception as e:
                print(f"⚠️ Could not clear {cache_dir}: {e}")

def restart_app():
    """Restart the Streamlit application"""
    print("\n🚀 Starting Streamlit application...")
    
    # Activate virtual environment and run app
    if os.name == 'nt':  # Windows
        cmd = [
            'powershell', '-Command',
            '.venv\\Scripts\\Activate.ps1; python -m streamlit run app.py --server.port 8505 --browser.gatherUsageStats false'
        ]
    else:  # Unix/Linux/Mac
        cmd = [
            'bash', '-c',
            'source .venv/bin/activate && python -m streamlit run app.py --server.port 8505 --browser.gatherUsageStats false'
        ]
    
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error starting application: {e}")
        return False
    except KeyboardInterrupt:
        print("\n⏹️ Application stopped by user")
        return True
    
    return True

if __name__ == "__main__":
    print("🧹 CySlean Lead Solar - Cache Cleaner & Restart")
    print("=" * 50)
    
    # Clear cache
    clear_streamlit_cache()
    
    # Ask user if they want to restart
    restart = input("\n🔄 Do you want to restart the application? (y/N): ").lower().strip()
    
    if restart in ['y', 'yes', 'si', 's']:
        restart_app()
    else:
        print("\n💡 To start the application manually, run:")
        print("   .venv\\Scripts\\Activate.ps1; python -m streamlit run app.py --server.port 8505")
        print("\n📝 If you still get JavaScript errors, try:")
        print("   1. Clear your browser cache (Ctrl+Shift+Delete)")
        print("   2. Open in incognito/private mode")
        print("   3. Try a different browser")