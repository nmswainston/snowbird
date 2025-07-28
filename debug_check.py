
#!/usr/bin/env python3
"""
Quick diagnostic script to check for common issues
"""

import sys
import traceback

def check_imports():
    """Check if all required modules can be imported"""
    print("🔍 Checking Python environment...")
    print(f"Python version: {sys.version}")
    
    required_modules = [
        'streamlit',
        'pandas', 
        'plotly',
        'pydantic',
        'loguru'
    ]
    
    failed_imports = []
    
    for module in required_modules:
        try:
            __import__(module)
            print(f"✅ {module}: OK")
        except ImportError as e:
            print(f"❌ {module}: FAILED - {e}")
            failed_imports.append(module)
    
    return failed_imports

def check_main_files():
    """Check if main application files exist and can be imported"""
    print("\n🔍 Checking main application files...")
    
    files_to_check = [
        'main.py',
        'main_app.py', 
        'config.py',
        'utils/config.py'
    ]
    
    for file_path in files_to_check:
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            print(f"✅ {file_path}: EXISTS ({len(content)} chars)")
        except FileNotFoundError:
            print(f"❌ {file_path}: NOT FOUND")
        except Exception as e:
            print(f"⚠️ {file_path}: ERROR - {e}")

def check_streamlit_imports():
    """Check if Streamlit can import main_app"""
    print("\n🔍 Testing main_app import...")
    try:
        from main_app import main
        print("✅ main_app.main: OK")
        return True
    except Exception as e:
        print(f"❌ main_app.main: FAILED")
        print(f"Error: {e}")
        print(f"Traceback:\n{traceback.format_exc()}")
        return False

if __name__ == "__main__":
    print("=== Snowbird App Diagnostic Check ===\n")
    
    # Check imports
    failed_imports = check_imports()
    
    # Check files
    check_main_files()
    
    # Check streamlit compatibility
    can_import_main = check_streamlit_imports()
    
    print("\n=== Summary ===")
    if failed_imports:
        print(f"❌ Missing modules: {', '.join(failed_imports)}")
    else:
        print("✅ All required modules available")
    
    if can_import_main:
        print("✅ Main app can be imported")
    else:
        print("❌ Main app has import issues")
    
    print("\n=== Recommendations ===")
    if failed_imports:
        print("1. Install missing modules with: pip install " + " ".join(failed_imports))
    
    if not can_import_main:
        print("2. Check main_app.py for syntax or import errors")
        print("3. Verify all utility modules are properly configured")
    
    if not failed_imports and can_import_main:
        print("🎉 Everything looks good! Try running the Streamlit app.")
