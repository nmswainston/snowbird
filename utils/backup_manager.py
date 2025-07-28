
import json
import os
import streamlit as st
from datetime import datetime, timedelta
from pathlib import Path
import zipfile

class BackupManager:
    """Automated backup system for user data"""
    
    def __init__(self, backup_dir: str = "backups"):
        self.backup_dir = Path(backup_dir)
        self.backup_dir.mkdir(exist_ok=True)
        
    def create_backup(self) -> str:
        """Create a backup of current session data"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = self.backup_dir / f"snowbird_backup_{timestamp}.json"
        
        # Collect all session state data
        backup_data = {
            'timestamp': timestamp,
            'version': '1.0.0',
            'data': {
                'states': getattr(st.session_state, 'states', {}),
                'home_budgets': getattr(st.session_state, 'home_budgets', {}),
                'tax_threshold': getattr(st.session_state, 'tax_threshold', 183),
                'user_preferences': {
                    'theme': getattr(st.session_state, 'theme', 'light'),
                    'notifications': getattr(st.session_state, 'notify_email', False)
                }
            }
        }
        
        with open(backup_file, 'w') as f:
            json.dump(backup_data, f, indent=2, default=str)
            
        return str(backup_file)
    
    def restore_backup(self, backup_file: str) -> bool:
        """Restore data from backup file"""
        try:
            with open(backup_file, 'r') as f:
                backup_data = json.load(f)
            
            # Restore session state
            data = backup_data.get('data', {})
            st.session_state.states = data.get('states', {})
            st.session_state.home_budgets = data.get('home_budgets', {})
            st.session_state.tax_threshold = data.get('tax_threshold', 183)
            
            # Restore preferences
            prefs = data.get('user_preferences', {})
            st.session_state.theme = prefs.get('theme', 'light')
            st.session_state.notify_email = prefs.get('notifications', False)
            
            return True
        except Exception as e:
            st.error(f"Backup restore failed: {e}")
            return False
    
    def cleanup_old_backups(self, keep_days: int = 30):
        """Remove backups older than specified days"""
        cutoff_date = datetime.now() - timedelta(days=keep_days)
        
        for backup_file in self.backup_dir.glob("snowbird_backup_*.json"):
            if backup_file.stat().st_mtime < cutoff_date.timestamp():
                backup_file.unlink()
    
    def get_backup_list(self) -> List[Dict]:
        """Get list of available backups"""
        backups = []
        
        for backup_file in sorted(self.backup_dir.glob("snowbird_backup_*.json"), reverse=True):
            try:
                with open(backup_file, 'r') as f:
                    data = json.load(f)
                
                backups.append({
                    'filename': backup_file.name,
                    'path': str(backup_file),
                    'timestamp': data.get('timestamp', 'Unknown'),
                    'size': backup_file.stat().st_size,
                    'version': data.get('version', '1.0.0')
                })
            except:
                continue
                
        return backups

# Global backup manager
backup_manager = BackupManager()
