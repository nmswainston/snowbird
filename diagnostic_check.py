
#!/usr/bin/env python3
"""
Diagnostic script to check Snowbird app health and configuration
"""

import sys
import os
import importlib
import traceback
from pathlib import Path

def check_python_version():
    """Check Python version compatibility"""
    print(f"✓ Python version: {sys.version}")
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required")
        return False
    return True

def check_required_modules():
    """Check if all required modules can be imported"""
    required_modules = [
        'streamlit', 'pandas', 'plotly', 'pydantic', 
        'loguru', 'datetime', 'json', 'pathlib'
    ]
    
    missing = []
    for module in required_modules:
        try:
            importlib.import_module(module)
            print(f"✓ {module}")
        except ImportError as e:
            print(f"❌ {module}: {e}")
            missing.append(module)
    
    return len(missing) == 0

def check_file_structure():
    """Check if required files and directories exist"""
    required_paths = [
        'main.py', 'config.py', 'utils/', 'components/', 
        'logs/', 'static/', '.streamlit/config.toml'
    ]
    
    missing = []
    for path in required_paths:
        if not Path(path).exists():
            print(f"❌ Missing: {path}")
            missing.append(path)
        else:
            print(f"✓ {path}")
    
    return len(missing) == 0

def check_configuration():
    """Check application configuration"""
    try:
        # Try to import main configuration
        from config import config
        print(f"✓ Config loaded - Environment: {config.environment}")
        print(f"✓ Debug mode: {config.debug}")
        print(f"✓ Server port: {config.server_port}")
        return True
    except Exception as e:
        print(f"❌ Config error: {e}")
        traceback.print_exc()
        return False

def check_streamlit_config():
    """Check Streamlit configuration"""
    config_file = Path('.streamlit/config.toml')
    if config_file.exists():
        print(f"✓ Streamlit config exists")
        try:
            with open(config_file, 'r') as f:
                content = f.read()
                print("Streamlit config preview:")
                print(content[:200] + "..." if len(content) > 200 else content)
        except Exception as e:
            print(f"❌ Error reading Streamlit config: {e}")
            return False
    else:
        print("❌ No Streamlit config found")
        return False
    return True

def check_main_app():
    """Try to import main application modules"""
    try:
        print("Importing main application components...")
        
        # Test basic imports
        from utils.error_handling import handle_errors
        print("✓ Error handling imported")
        
        from components.dashboard import render_dashboard
        print("✓ Dashboard component imported")
        
        from utils.data_models import SnowbirdData
        print("✓ Data models imported")
        
        return True
    except Exception as e:
        print(f"❌ Main app import error: {e}")
        traceback.print_exc()
        return False

def main():
    """Run all diagnostic checks"""
    print("🔍 Snowbird Application Diagnostic Check")
    print("=" * 50)
    
    checks = [
        ("Python Version", check_python_version),
        ("Required Modules", check_required_modules),
        ("File Structure", check_file_structure),
        ("Configuration", check_configuration),
        ("Streamlit Config", check_streamlit_config),
        ("Main Application", check_main_app)
    ]
    
    results = {}
    for name, check_func in checks:
        print(f"\n📋 Checking {name}...")
        try:
            results[name] = check_func()
        except Exception as e:
            print(f"❌ {name} check failed: {e}")
            results[name] = False
    
    print("\n" + "=" * 50)
    print("📊 DIAGNOSTIC SUMMARY")
    print("=" * 50)
    
    all_passed = True
    for name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{name}: {status}")
        if not passed:
            all_passed = False
    
    if all_passed:
        print("\n🎉 All checks passed! The application should start normally.")
    else:
        print("\n⚠️  Some checks failed. Please address the issues above.")
        print("\n💡 Suggested fixes:")
        print("- Install missing modules: pip install streamlit pandas plotly pydantic loguru")
        print("- Check file permissions and paths")
        print("- Verify configuration files")
    
    return all_passed

if __name__ == "__main__":
    main()
