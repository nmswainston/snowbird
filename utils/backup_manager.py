
import json
import os
import streamlit as st
from datetime import datetime, timedelta
from pathlib import Path
import zipfile
import hashlib
from typing import List, Dict

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
    
    def create_zip_backup(self) -> bytes:
        """
        Create a ZIP backup with enhanced metadata and validation
        
        Returns:
            bytes: ZIP file content as bytes
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Collect comprehensive session state data
        backup_data = {
            'timestamp': datetime.now().isoformat(),
            'version': '1.0.0',
            'app_version': 'Snowbird v2.0',
            'data': {
                'states': dict(getattr(st.session_state, 'states', {})),
                'home_budgets': dict(getattr(st.session_state, 'home_budgets', {})),
                'seasonal_cash_flow': dict(getattr(st.session_state, 'seasonal_cash_flow', {})),
                'tax_threshold': getattr(st.session_state, 'tax_threshold', 183),
                'risk_warning_days': getattr(st.session_state, 'risk_warning_days', 14),
                'default_state': getattr(st.session_state, 'default_state', 'Arizona'),
                'user_preferences': {
                    'theme': getattr(st.session_state, 'theme', 'light'),
                    'notifications': getattr(st.session_state, 'notify_email', False),
                    'auto_save': getattr(st.session_state, 'auto_save', True),
                    'show_tips': getattr(st.session_state, 'show_tips', True)
                },
                'migration_checklist': dict(getattr(st.session_state, 'migration_checklist', {})),
                'bills': dict(getattr(st.session_state, 'bills', {}))
            }
        }
        
        # Create ZIP in memory
        import io
        zip_buffer = io.BytesIO()
        
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            # Add main backup file
            backup_json = json.dumps(backup_data, indent=2, default=str)
            zip_file.writestr(f"snowbird_backup_{timestamp}.json", backup_json)
            
            # Add metadata file with checksums
            metadata = {
                'backup_date': backup_data['timestamp'],
                'total_days_az': backup_data['data']['states'].get('Arizona', 0),
                'total_days_mn': backup_data['data']['states'].get('Minnesota', 0),
                'backup_size': len(backup_json),
                'checksum': hashlib.md5(backup_json.encode()).hexdigest(),
                'data_integrity': self._calculate_data_checksum(backup_data['data'])
            }
            zip_file.writestr("backup_metadata.json", json.dumps(metadata, indent=2))
            
            # Add readme file
            readme_content = f"""
Snowbird Financial Assistant - Data Backup
==========================================

Backup Date: {backup_data['timestamp']}
App Version: {backup_data['app_version']}
Data Version: {backup_data['version']}

Contents:
- snowbird_backup_{timestamp}.json: Main backup data
- backup_metadata.json: Backup metadata and checksums
- README.txt: This file

To restore:
1. Go to Settings > Backup & Restore in the Snowbird app
2. Click "Choose backup file" and select this ZIP
3. Click "Restore Data"

Data Summary:
- Arizona Days: {metadata['total_days_az']}
- Minnesota Days: {metadata['total_days_mn']}
- Tax Threshold: {backup_data['data']['tax_threshold']} days
"""
            zip_file.writestr("README.txt", readme_content)
        
        zip_buffer.seek(0)
        return zip_buffer.getvalue()
    
    def _calculate_data_checksum(self, data: dict) -> str:
        """Calculate checksum for data integrity verification"""
        # Create a consistent string representation for checksum
        data_str = json.dumps(data, sort_keys=True, default=str)
        return hashlib.md5(data_str.encode()).hexdigest()
    
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
