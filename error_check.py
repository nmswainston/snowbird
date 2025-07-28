
#!/usr/bin/env python3
"""
Comprehensive Error Check for Snowbird Financial Assistant
Identifies and reports potential issues in the codebase.
"""

import os
import sys
import importlib
import traceback
from pathlib import Path
import json
import ast

def check_imports():
    """Check if all required imports are available"""
    print("🔍 Checking imports...")
    
    required_modules = [
        'streamlit',
        'pandas',
        'plotly',
        'datetime',
        'json',
        'typing',
        'dataclasses'
    ]
    
    missing_modules = []
    for module in required_modules:
        try:
            importlib.import_module(module)
            print(f"  ✅ {module}")
        except ImportError as e:
            missing_modules.append(module)
            print(f"  ❌ {module}: {e}")
    
    return missing_modules

def check_file_structure():
    """Check if all required files and directories exist"""
    print("\n📁 Checking file structure...")
    
    required_files = [
        'main_app.py',
        'components/styles.py',
        'components/dashboard.py',
        'components/day_tracker.py',
        'components/session_state.py',
        'utils/data_models.py',
        'utils/auth.py'
    ]
    
    missing_files = []
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"  ✅ {file_path}")
        else:
            missing_files.append(file_path)
            print(f"  ❌ {file_path}")
    
    return missing_files

def check_syntax():
    """Check Python syntax in main files"""
    print("\n🐍 Checking Python syntax...")
    
    python_files = [
        'main_app.py',
        'components/styles.py',
        'components/dashboard.py',
        'components/day_tracker.py',
        'components/session_state.py'
    ]
    
    syntax_errors = []
    for file_path in python_files:
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                ast.parse(content)
                print(f"  ✅ {file_path}")
            except SyntaxError as e:
                syntax_errors.append((file_path, str(e)))
                print(f"  ❌ {file_path}: {e}")
            except Exception as e:
                syntax_errors.append((file_path, str(e)))
                print(f"  ⚠️ {file_path}: {e}")
        else:
            print(f"  ⏭️ {file_path} (file not found)")
    
    return syntax_errors

def check_imports_in_files():
    """Check for import issues in Python files"""
    print("\n📦 Checking imports in files...")
    
    python_files = [
        'main_app.py',
        'components/styles.py',
        'components/dashboard.py',
        'components/day_tracker.py'
    ]
    
    import_errors = []
    for file_path in python_files:
        if os.path.exists(file_path):
            try:
                # Try to import the module
                spec = importlib.util.spec_from_file_location("temp_module", file_path)
                if spec and spec.loader:
                    module = importlib.util.module_from_spec(spec)
                    sys.modules["temp_module"] = module
                    spec.loader.exec_module(module)
                    print(f"  ✅ {file_path}")
                    # Clean up
                    if "temp_module" in sys.modules:
                        del sys.modules["temp_module"]
            except Exception as e:
                import_errors.append((file_path, str(e)))
                print(f"  ❌ {file_path}: {e}")
    
    return import_errors

def check_streamlit_config():
    """Check Streamlit configuration"""
    print("\n⚙️ Checking Streamlit configuration...")
    
    config_path = ".streamlit/config.toml"
    if os.path.exists(config_path):
        print(f"  ✅ {config_path} exists")
        try:
            with open(config_path, 'r') as f:
                content = f.read()
                if 'port' in content.lower():
                    print("  ✅ Port configuration found")
                if 'address' in content.lower():
                    print("  ✅ Address configuration found")
        except Exception as e:
            print(f"  ⚠️ Error reading config: {e}")
    else:
        print(f"  ⚠️ {config_path} not found")

def check_environment():
    """Check environment variables and configuration"""
    print("\n🌍 Checking environment...")
    
    # Check if .env.example exists
    if os.path.exists('.env.example'):
        print("  ✅ .env.example exists")
    else:
        print("  ⚠️ .env.example not found")
    
    # Check for required environment variables
    env_vars = ['OPENAI_API_KEY']
    for var in env_vars:
        if os.getenv(var):
            print(f"  ✅ {var} is set")
        else:
            print(f"  ⚠️ {var} not set (optional)")

def check_static_files():
    """Check static files for PWA"""
    print("\n🌐 Checking static files...")
    
    static_files = [
        'static/manifest.json',
        'static/icon-192.png',
        'static/icon-512.png',
        'static/sw.js'
    ]
    
    for file_path in static_files:
        if os.path.exists(file_path):
            print(f"  ✅ {file_path}")
        else:
            print(f"  ⚠️ {file_path} missing (PWA feature may not work)")

def check_theme_system():
    """Check theme system integrity"""
    print("\n🎨 Checking theme system...")
    
    theme_files = [
        'components/theme_manager.py',
        'components/theme_selector.py'
    ]
    
    for file_path in theme_files:
        if os.path.exists(file_path):
            print(f"  ✅ {file_path}")
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if 'ThemeManager' in content or 'ThemeColors' in content:
                        print(f"    ✅ Theme classes found in {file_path}")
            except Exception as e:
                print(f"    ⚠️ Error reading {file_path}: {e}")
        else:
            print(f"  ❌ {file_path} missing")

def main():
    """Run comprehensive error check"""
    print("🔍 Snowbird App Error Check")
    print("=" * 50)
    
    # Track all issues
    all_issues = []
    
    # Run checks
    missing_modules = check_imports()
    if missing_modules:
        all_issues.extend([f"Missing module: {m}" for m in missing_modules])
    
    missing_files = check_file_structure()
    if missing_files:
        all_issues.extend([f"Missing file: {f}" for f in missing_files])
    
    syntax_errors = check_syntax()
    if syntax_errors:
        all_issues.extend([f"Syntax error in {f}: {e}" for f, e in syntax_errors])
    
    import_errors = check_imports_in_files()
    if import_errors:
        all_issues.extend([f"Import error in {f}: {e}" for f, e in import_errors])
    
    check_streamlit_config()
    check_environment()
    check_static_files()
    check_theme_system()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 SUMMARY")
    print("=" * 50)
    
    if all_issues:
        print(f"❌ Found {len(all_issues)} issues:")
        for i, issue in enumerate(all_issues, 1):
            print(f"  {i}. {issue}")
        
        print(f"\n💡 Recommendations:")
        if missing_modules:
            print("  • Install missing modules with: pip install " + " ".join(missing_modules))
        if missing_files:
            print("  • Create missing files or check file paths")
        if syntax_errors:
            print("  • Fix syntax errors in the reported files")
        if import_errors:
            print("  • Resolve import dependencies")
    else:
        print("✅ No critical issues found!")
        print("🎉 Your Snowbird app appears to be healthy!")
    
    print("\n🚀 To start the app, run: python -m streamlit run main_app.py")
    print("📱 Access at: http://0.0.0.0:8501")

if __name__ == "__main__":
    main()
