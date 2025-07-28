
#!/usr/bin/env python3
"""
Robust startup script for Snowbird app with comprehensive error handling
"""

import sys
import subprocess
import time
import os
import signal
import psutil
from pathlib import Path

def kill_existing_streamlit():
    """Kill any existing Streamlit processes"""
    try:
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                cmdline = ' '.join(proc.info['cmdline'] or [])
                if 'streamlit' in cmdline and 'main.py' in cmdline:
                    print(f"Killing existing Streamlit process: {proc.info['pid']}")
                    proc.kill()
                    proc.wait(timeout=5)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.TimeoutExpired):
                pass
    except Exception as e:
        print(f"Warning: Could not check for existing processes: {e}")

def check_dependencies():
    """Check if all required dependencies are available"""
    required_modules = ['streamlit', 'pandas', 'plotly', 'pydantic', 'loguru']
    missing = []
    
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            missing.append(module)
    
    if missing:
        print(f"Error: Missing required modules: {', '.join(missing)}")
        print("Please install them with: pip install " + " ".join(missing))
        return False
    
    return True

def check_main_files():
    """Check if main application files exist"""
    required_files = ['main.py', 'main_app.py', 'config.py']
    missing = []
    
    for file_path in required_files:
        if not Path(file_path).exists():
            missing.append(file_path)
    
    if missing:
        print(f"Error: Missing required files: {', '.join(missing)}")
        return False
    
    return True

def create_logs_dir():
    """Ensure logs directory exists"""
    Path('logs').mkdir(exist_ok=True)

def start_streamlit():
    """Start Streamlit with optimized settings"""
    cmd = [
        sys.executable, '-m', 'streamlit', 'run', 'main.py',
        '--server.port', '8501',
        '--server.address', '0.0.0.0',
        '--server.headless', 'true',
        '--server.enableCORS', 'false',
        '--server.enableWebsocketCompression', 'false',
        '--server.fileWatcherType', 'none',
        '--browser.gatherUsageStats', 'false',
        '--logger.level', 'warning',
        '--server.maxMessageSize', '200',
        '--server.enableStaticServing', 'true',
        '--server.runOnSave', 'false'
    ]
    
    print("Starting Streamlit server...")
    print(f"Command: {' '.join(cmd)}")
    
    try:
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )
        
        # Monitor the process for a few seconds
        for i in range(10):
            if process.poll() is not None:
                print(f"Process exited with code: {process.returncode}")
                output = process.communicate()[0]
                print("Output:", output)
                return False
            time.sleep(1)
            print(f"Server starting... ({i+1}/10)")
        
        print("✅ Streamlit server appears to be running successfully!")
        print("🌐 Access your app at: http://localhost:8501")
        
        # Keep the process running
        try:
            process.wait()
        except KeyboardInterrupt:
            print("\n⏹️ Shutting down server...")
            process.terminate()
            process.wait()
        
        return True
        
    except Exception as e:
        print(f"Error starting Streamlit: {e}")
        return False

def main():
    """Main startup function"""
    print("🏠 Snowbird App Startup Script")
    print("=" * 40)
    
    # Kill existing processes
    print("🔄 Checking for existing Streamlit processes...")
    kill_existing_streamlit()
    time.sleep(2)
    
    # Check dependencies
    print("📦 Checking dependencies...")
    if not check_dependencies():
        sys.exit(1)
    
    # Check files
    print("📁 Checking required files...")
    if not check_main_files():
        sys.exit(1)
    
    # Create logs directory
    print("📝 Setting up logging...")
    create_logs_dir()
    
    # Start the server
    print("🚀 Starting Snowbird application...")
    success = start_streamlit()
    
    if not success:
        print("❌ Failed to start the application")
        sys.exit(1)

if __name__ == "__main__":
    main()
