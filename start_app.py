
#!/usr/bin/env python3
"""
Robust startup script for Snowbird app with comprehensive error handling
"""

import sys
import subprocess
import time
import os
import signal
from pathlib import Path

def kill_existing_streamlit():
    """Kill any existing Streamlit processes"""
    try:
        # Use pkill to kill streamlit processes
        subprocess.run(['pkill', '-f', 'streamlit'], check=False)
        time.sleep(2)  # Give processes time to die
        print("✓ Cleaned up existing Streamlit processes")
    except Exception as e:
        print(f"Warning: Could not clean up processes: {e}")

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
        print(f"❌ Missing required modules: {', '.join(missing)}")
        print(f"Installing missing modules...")
        try:
            subprocess.run([sys.executable, '-m', 'pip', 'install'] + missing, check=True)
            print("✓ Dependencies installed")
        except subprocess.CalledProcessError:
            print("❌ Failed to install dependencies")
            return False
    
    return True

def ensure_directories():
    """Ensure required directories exist"""
    directories = ['logs', 'static', '.streamlit']
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
    print("✓ Required directories created")

def create_streamlit_config():
    """Create optimized Streamlit configuration"""
    config_dir = Path('.streamlit')
    config_dir.mkdir(exist_ok=True)
    
    config_content = """
[server]
port = 8501
address = "0.0.0.0"
headless = true
enableCORS = false
enableXsrfProtection = false
enableWebsocketCompression = false
maxMessageSize = 200
maxUploadSize = 200
fileWatcherType = "none"
runOnSave = false

[browser]
gatherUsageStats = false

[theme]
base = "light"
primaryColor = "#12BDF2"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F4F8"
textColor = "#1E293B"

[logger]
level = "warning"
"""
    
    config_file = config_dir / 'config.toml'
    with open(config_file, 'w') as f:
        f.write(config_content.strip())
    
    print("✓ Streamlit configuration created")

def start_streamlit():
    """Start Streamlit with optimized settings"""
    cmd = [
        sys.executable, '-m', 'streamlit', 'run', 'main.py',
        '--server.port', '8501',
        '--server.address', '0.0.0.0',
        '--server.headless', 'true',
        '--server.enableCORS', 'false',
        '--server.enableXsrfProtection', 'false',
        '--server.enableWebsocketCompression', 'false',
        '--server.fileWatcherType', 'none',
        '--server.maxMessageSize', '200',
        '--browser.gatherUsageStats', 'false',
        '--logger.level', 'warning'
    ]
    
    print("🚀 Starting Streamlit server...")
    print(f"Command: {' '.join(cmd)}")
    
    try:
        # Start the process
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )
        
        # Monitor startup for first few seconds
        startup_success = False
        for i in range(15):  # Wait up to 15 seconds
            if process.poll() is not None:
                # Process has terminated
                output, _ = process.communicate()
                print(f"❌ Process exited early with code: {process.returncode}")
                print("Output:", output)
                return False
            
            time.sleep(1)
            if i == 5:
                print("✓ Server starting...")
            elif i == 10:
                print("✓ Server should be ready soon...")
        
        print("✅ Streamlit server started successfully!")
        print("🌐 Access your app at: http://localhost:8501")
        print("📱 Or from external: http://0.0.0.0:8501")
        
        # Keep the process running and monitor it
        try:
            process.wait()
        except KeyboardInterrupt:
            print("\n🛑 Shutting down server...")
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to start Streamlit: {e}")
        return False

def main():
    """Main startup function"""
    print("🔄 Starting Snowbird Financial Assistant...")
    print("=" * 50)
    
    # Step 1: Clean up any existing processes
    kill_existing_streamlit()
    
    # Step 2: Check dependencies
    if not check_dependencies():
        print("❌ Dependency check failed")
        return 1
    
    # Step 3: Ensure directories exist
    ensure_directories()
    
    # Step 4: Create optimized config
    create_streamlit_config()
    
    # Step 5: Start the application
    if start_streamlit():
        print("✅ Application started successfully!")
        return 0
    else:
        print("❌ Failed to start application")
        return 1

if __name__ == "__main__":
    sys.exit(main())
