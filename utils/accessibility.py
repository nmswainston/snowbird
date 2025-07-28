
"""
Accessibility utilities for WCAG compliance and screen reader support.
"""
import streamlit as st
from typing import Dict, List, Tuple

class AccessibilityManager:
    """Manage accessibility features and WCAG compliance"""
    
    @staticmethod
    def check_contrast_ratio(bg_color: str, text_color: str) -> Tuple[float, bool]:
        """
        Check if color combination meets WCAG AA contrast ratio (4.5:1)
        
        Args:
            bg_color: Background color in hex format
            text_color: Text color in hex format
            
        Returns:
            Tuple of (contrast_ratio, meets_wcag_aa)
        """
        def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
            hex_color = hex_color.lstrip('#')
            return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
        def luminance(rgb: Tuple[int, int, int]) -> float:
            r, g, b = [x / 255.0 for x in rgb]
            r = r / 12.92 if r <= 0.03928 else ((r + 0.055) / 1.055) ** 2.4
            g = g / 12.92 if g <= 0.03928 else ((g + 0.055) / 1.055) ** 2.4
            b = b / 12.92 if b <= 0.03928 else ((b + 0.055) / 1.055) ** 2.4
            return 0.2126 * r + 0.7152 * g + 0.0722 * b
        
        bg_rgb = hex_to_rgb(bg_color)
        text_rgb = hex_to_rgb(text_color)
        
        bg_lum = luminance(bg_rgb)
        text_lum = luminance(text_rgb)
        
        lighter = max(bg_lum, text_lum)
        darker = min(bg_lum, text_lum)
        
        contrast_ratio = (lighter + 0.05) / (darker + 0.05)
        meets_wcag_aa = contrast_ratio >= 4.5
        
        return contrast_ratio, meets_wcag_aa
    
    @staticmethod
    def add_screen_reader_text(text: str, element_id: str = None) -> str:
        """Add screen reader only text"""
        sr_id = f'id="{element_id}"' if element_id else ''
        return f'<span class="sr-only" {sr_id}>{text}</span>'
    
    @staticmethod
    def add_aria_label(content: str, label: str, role: str = None) -> str:
        """Add ARIA label to content"""
        role_attr = f'role="{role}"' if role else ''
        return f'<div aria-label="{label}" {role_attr}>{content}</div>'
    
    @staticmethod
    def keyboard_navigation_hint() -> None:
        """Display keyboard navigation instructions"""
        st.markdown("""
        <div class="keyboard-nav-hint" style="font-size: 0.8rem; color: #666; margin-bottom: 1rem;">
            <details>
                <summary>⌨️ Keyboard Navigation Help</summary>
                <ul style="margin: 0.5rem 0;">
                    <li><strong>Tab:</strong> Navigate between elements</li>
                    <li><strong>Enter/Space:</strong> Activate buttons</li>
                    <li><strong>Arrow keys:</strong> Navigate within components</li>
                    <li><strong>Escape:</strong> Close modals or dropdowns</li>
                </ul>
            </details>
        </div>
        """, unsafe_allow_html=True)

def add_accessibility_css():
    """Add CSS for accessibility improvements"""
    st.markdown("""
    <style>
    /* Screen reader only text */
    .sr-only {
        position: absolute;
        width: 1px;
        height: 1px;
        padding: 0;
        margin: -1px;
        overflow: hidden;
        clip: rect(0, 0, 0, 0);
        white-space: nowrap;
        border: 0;
    }
    
    /* Focus indicators */
    button:focus,
    input:focus,
    select:focus,
    textarea:focus {
        outline: 2px solid #4A90E2 !important;
        outline-offset: 2px !important;
    }
    
    /* High contrast mode support */
    @media (prefers-contrast: high) {
        .metric-card {
            border: 2px solid currentColor !important;
        }
    }
    
    /* Reduced motion support */
    @media (prefers-reduced-motion: reduce) {
        * {
            animation-duration: 0.01ms !important;
            animation-iteration-count: 1 !important;
            transition-duration: 0.01ms !important;
        }
    }
    
    /* Ensure sufficient color contrast */
    .status-safe { 
        color: #0d5016 !important; 
        background-color: #d4edda !important; 
        padding: 0.25rem 0.5rem;
        border-radius: 0.25rem;
    }
    .status-warning { 
        color: #856404 !important; 
        background-color: #fff3cd !important; 
        padding: 0.25rem 0.5rem;
        border-radius: 0.25rem;
    }
    .status-danger { 
        color: #721c24 !important; 
        background-color: #f8d7da !important; 
        padding: 0.25rem 0.5rem;
        border-radius: 0.25rem;
    }
    </style>
    """, unsafe_allow_html=True)

# Alt text mapping for icons
ICON_ALT_TEXT = {
    "home": "Home icon",
    "map-pin": "Location pin icon", 
    "dollar-sign": "Dollar sign icon",
    "brain": "AI brain icon",
    "activity": "Activity chart icon",
    "trending-up": "Trending up icon",
    "sparkles": "Sparkles icon",
    "alert-triangle": "Warning triangle icon",
    "check-circle": "Success checkmark icon",
    "x-circle": "Error X icon"
}

def accessible_icon(icon_name: str, size: str = "16") -> str:
    """Render accessible icon with alt text"""
    alt_text = ICON_ALT_TEXT.get(icon_name, f"{icon_name} icon")
    return f'<i data-lucide="{icon_name}" aria-label="{alt_text}" style="width: {size}px; height: {size}px;"></i>'
