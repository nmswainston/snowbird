
"""
Version management and update tracking for the Snowbird application.
"""
import json
import datetime
from pathlib import Path
from typing import Dict, List, Optional
import streamlit as st

class VersionManager:
    """Manage application versioning and updates"""
    
    def __init__(self):
        self.version_file = Path("version.json")
        self.current_version = self.load_current_version()
    
    def load_current_version(self) -> Dict[str, str]:
        """Load current version information"""
        default_version = {
            "version": "1.0.0",
            "build": "2024.01.15.001",
            "release_date": "2024-01-15",
            "environment": "development"
        }
        
        try:
            if self.version_file.exists():
                with open(self.version_file, 'r') as f:
                    return json.load(f)
        except Exception:
            pass
        
        return default_version
    
    def update_version(self, version: str, build: str = None, environment: str = "development"):
        """Update version information"""
        if not build:
            build = datetime.datetime.now().strftime("%Y.%m.%d.%H%M")
        
        version_info = {
            "version": version,
            "build": build,
            "release_date": datetime.date.today().isoformat(),
            "environment": environment,
            "updated_at": datetime.datetime.now().isoformat()
        }
        
        try:
            with open(self.version_file, 'w') as f:
                json.dump(version_info, f, indent=2)
            self.current_version = version_info
            return True
        except Exception as e:
            st.error(f"Failed to update version: {e}")
            return False
    
    def get_version_string(self) -> str:
        """Get formatted version string"""
        return f"v{self.current_version['version']} (build {self.current_version['build']})"
    
    def check_for_updates(self) -> Optional[Dict[str, str]]:
        """Check for available updates (placeholder for future implementation)"""
        # In a real implementation, this would check a remote endpoint
        return None
    
    def get_release_notes(self, version: str = None) -> List[str]:
        """Get release notes for a version"""
        # Parse CHANGELOG.md for release notes
        changelog_path = Path("CHANGELOG.md")
        if not changelog_path.exists():
            return ["No release notes available"]
        
        try:
            with open(changelog_path, 'r') as f:
                content = f.read()
            
            # Simple parser for markdown changelog
            lines = content.split('\n')
            notes = []
            in_version_section = False
            target_version = version or self.current_version['version']
            
            for line in lines:
                if line.startswith('## [') and target_version in line:
                    in_version_section = True
                    continue
                elif line.startswith('## [') and in_version_section:
                    break
                elif in_version_section and line.strip():
                    if line.startswith('### ') or line.startswith('- '):
                        notes.append(line.strip())
            
            return notes if notes else ["No release notes found for this version"]
            
        except Exception:
            return ["Error loading release notes"]

def render_version_info():
    """Render version information component"""
    version_manager = VersionManager()
    
    st.markdown("### 📋 Version Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info(f"""
        **Current Version**: {version_manager.get_version_string()}
        
        **Release Date**: {version_manager.current_version['release_date']}
        
        **Environment**: {version_manager.current_version['environment'].title()}
        """)
    
    with col2:
        if st.button("📋 View Release Notes"):
            st.session_state.show_release_notes = True
    
    # Show release notes if requested
    if st.session_state.get('show_release_notes', False):
        with st.expander("📋 Release Notes", expanded=True):
            notes = version_manager.get_release_notes()
            for note in notes:
                st.write(note)
        
        if st.button("Close Release Notes"):
            st.session_state.show_release_notes = False
            st.rerun()

# Global version manager
version_manager = VersionManager()
