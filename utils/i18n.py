
"""
Internationalization (i18n) support for the Snowbird application.
"""
import json
from pathlib import Path
from typing import Dict, Optional
import streamlit as st

class I18nManager:
    """Manage internationalization and localization"""
    
    def __init__(self):
        self.translations_dir = Path("translations")
        self.translations_dir.mkdir(exist_ok=True)
        self.current_language = "en"
        self.translations = {}
        self.load_translations()
    
    def load_translations(self):
        """Load all translation files"""
        for lang_file in self.translations_dir.glob("*.json"):
            lang_code = lang_file.stem
            try:
                with open(lang_file, 'r', encoding='utf-8') as f:
                    self.translations[lang_code] = json.load(f)
            except Exception as e:
                print(f"Error loading translations for {lang_code}: {e}")
    
    def set_language(self, language_code: str):
        """Set the current language"""
        if language_code in self.translations:
            self.current_language = language_code
            st.session_state.language = language_code
    
    def get_text(self, key: str, **kwargs) -> str:
        """Get translated text for a key"""
        # Get from session state if available
        current_lang = st.session_state.get('language', self.current_language)
        
        # Try to get translation
        if current_lang in self.translations:
            text = self.translations[current_lang].get(key, key)
        else:
            text = key
        
        # Format with kwargs if provided
        if kwargs:
            try:
                text = text.format(**kwargs)
            except KeyError:
                pass  # Return unformatted text if formatting fails
        
        return text
    
    def get_available_languages(self) -> Dict[str, str]:
        """Get available languages"""
        return {
            "en": "English",
            "es": "Español", 
            "fr": "Français",
            "de": "Deutsch"
        }

# Global i18n manager
i18n = I18nManager()

def t(key: str, **kwargs) -> str:
    """Shorthand function for getting translations"""
    return i18n.get_text(key, **kwargs)

def render_language_selector():
    """Render language selector widget"""
    available_languages = i18n.get_available_languages()
    current_language = st.session_state.get('language', 'en')
    
    selected_language = st.selectbox(
        "🌐 Language / Idioma / Langue / Sprache",
        options=list(available_languages.keys()),
        format_func=lambda x: available_languages[x],
        index=list(available_languages.keys()).index(current_language),
        key="language_selector"
    )
    
    if selected_language != current_language:
        i18n.set_language(selected_language)
        st.rerun()
