
"""
Branding Manager for Pro User Customization
Handles logo uploads, color customization, and branding application.
"""

import streamlit as st
import base64
from PIL import Image
import io
from typing import Optional, Dict, Any
import os

class BrandingManager:
    """Manage Pro user branding customization features"""
    
    @staticmethod
    def is_pro_user() -> bool:
        """Check if current user has Pro access (placeholder for actual Pro logic)"""
        # In a real implementation, this would check user subscription status
        return st.session_state.get('is_pro_user', False)
    
    @staticmethod
    def get_uploaded_logo() -> Optional[str]:
        """Get base64 encoded uploaded logo from session state"""
        return st.session_state.get('custom_logo_base64', None)
    
    @staticmethod
    def get_custom_colors() -> Dict[str, str]:
        """Get custom brand colors from session state"""
        return {
            'primary': st.session_state.get('custom_primary_color', '#0EA5E9'),
            'accent': st.session_state.get('custom_accent_color', '#38BDF8'),
            'secondary': st.session_state.get('custom_secondary_color', '#0284C7')
        }
    
    @staticmethod
    def process_uploaded_logo(uploaded_file) -> Optional[str]:
        """
        Process uploaded logo file and convert to base64.
        
        Args:
            uploaded_file: Streamlit UploadedFile object
            
        Returns:
            str: Base64 encoded image string or None if processing fails
        """
        try:
            # Open and process the image
            image = Image.open(uploaded_file)
            
            # Resize image to reasonable dimensions (max 200px height)
            max_height = 200
            if image.height > max_height:
                ratio = max_height / image.height
                new_width = int(image.width * ratio)
                image = image.resize((new_width, max_height), Image.Resampling.LANCZOS)
            
            # Convert to RGB if necessary (for PNG with transparency)
            if image.mode in ('RGBA', 'LA', 'P'):
                # Create white background
                background = Image.new('RGB', image.size, (255, 255, 255))
                if image.mode == 'P':
                    image = image.convert('RGBA')
                background.paste(image, mask=image.split()[-1] if image.mode == 'RGBA' else None)
                image = background
            
            # Convert to base64
            buffer = io.BytesIO()
            image.save(buffer, format='PNG', optimize=True, quality=95)
            img_str = base64.b64encode(buffer.getvalue()).decode()
            
            return f"data:image/png;base64,{img_str}"
            
        except Exception as e:
            st.error(f"Error processing logo: {str(e)}")
            return None
    
    @staticmethod
    def save_branding_settings(logo_base64: Optional[str] = None, colors: Optional[Dict[str, str]] = None):
        """
        Save branding settings to session state.
        
        Args:
            logo_base64: Base64 encoded logo string
            colors: Dictionary of custom colors
        """
        if logo_base64:
            st.session_state.custom_logo_base64 = logo_base64
        
        if colors:
            for color_key, color_value in colors.items():
                st.session_state[f'custom_{color_key}_color'] = color_value
    
    @staticmethod
    def apply_custom_branding_css() -> str:
        """
        Generate CSS for custom branding.
        
        Returns:
            str: CSS string with custom branding styles
        """
        if not BrandingManager.is_pro_user():
            return ""
        
        custom_colors = BrandingManager.get_custom_colors()
        logo_base64 = BrandingManager.get_uploaded_logo()
        
        css = """
        <style>
        /* Custom Pro User Branding Styles */
        :root {
        """
        
        # Apply custom colors if they differ from defaults
        if custom_colors['primary'] != '#0EA5E9':
            css += f"    --custom-primary: {custom_colors['primary']};\n"
            css += f"    --primary: {custom_colors['primary']};\n"
        
        if custom_colors['accent'] != '#38BDF8':
            css += f"    --custom-accent: {custom_colors['accent']};\n"
            css += f"    --accent: {custom_colors['accent']};\n"
        
        if custom_colors['secondary'] != '#0284C7':
            css += f"    --custom-secondary: {custom_colors['secondary']};\n"
            css += f"    --secondary: {custom_colors['secondary']};\n"
        
        css += """
        }
        
        /* Update gradients with custom colors */
        .stButton > button {
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%) !important;
        }
        
        .main-title {
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 50%, var(--accent) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        /* Custom logo styling */
        """
        
        if logo_base64:
            css += f"""
        .custom-logo {{
            background-image: url('{logo_base64}');
            background-size: contain;
            background-repeat: no-repeat;
            background-position: center;
            height: 60px;
            width: auto;
            max-width: 200px;
            margin: 0 auto 1rem auto;
            display: block;
        }}
        
        .main-header::before {{
            content: '';
            display: block;
            background-image: url('{logo_base64}');
            background-size: contain;
            background-repeat: no-repeat;
            background-position: center top;
            height: 60px;
            width: 100%;
            margin-bottom: 1rem;
        }}
        """
        
        css += "</style>"
        return css
    
    @staticmethod
    def render_custom_header():
        """Render header with custom branding if Pro user"""
        if not BrandingManager.is_pro_user():
            return
        
        logo_base64 = BrandingManager.get_uploaded_logo()
        
        if logo_base64:
            # Render custom logo in header
            st.markdown(f"""
            <div class="main-header fade-in">
                <div class="custom-logo"></div>
                <h1 class="main-title">
                    <i data-lucide="home" class="icon-large"></i>
                    Snowbird: Your Seasonal Financial Assistant
                </h1>
                <p class="subtitle">Manage your multi-state lifestyle with confidence and style</p>
                <div style="margin-top: 1rem; opacity: 0.7; font-size: 0.9rem;">
                    <i data-lucide="sparkles" class="icon"></i>
                    Premium Financial Management Experience
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Render standard header
            st.markdown("""
            <div class="main-header fade-in">
                <h1 class="main-title">
                    <i data-lucide="home" class="icon-large"></i>
                    Snowbird: Your Seasonal Financial Assistant
                </h1>
                <p class="subtitle">Manage your multi-state lifestyle with confidence and style</p>
                <div style="margin-top: 1rem; opacity: 0.7; font-size: 0.9rem;">
                    <i data-lucide="sparkles" class="icon"></i>
                    Premium Financial Management Experience
                </div>
            </div>
            """, unsafe_allow_html=True)

def render_branding_settings():
    """Render Pro user branding settings interface"""
    st.markdown("### 🎨 Pro Branding Customization")
    
    if not BrandingManager.is_pro_user():
        st.info("🌟 **Upgrade to Pro** to customize your logo and brand colors!")
        
        # Show upgrade toggle for demo purposes
        if st.button("🚀 Enable Pro Features (Demo)", help="Toggle Pro features for demonstration"):
            st.session_state.is_pro_user = True
            st.success("✨ Pro features enabled! Refresh to see customization options.")
            st.rerun()
        return
    
    st.success("🌟 **Pro User** - Customize your branding below!")
    
    # Logo Upload Section
    st.markdown("#### 📸 Custom Logo")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Logo file uploader
        uploaded_logo = st.file_uploader(
            "Upload Your Logo",
            type=["png", "jpg", "jpeg"],
            help="Upload a PNG or JPG logo. Image will be resized to fit header (max 200px height).",
            key="logo_uploader"
        )
        
        if uploaded_logo is not None:
            # Process and save the uploaded logo
            logo_base64 = BrandingManager.process_uploaded_logo(uploaded_logo)
            
            if logo_base64:
                BrandingManager.save_branding_settings(logo_base64=logo_base64)
                st.success("✅ Logo uploaded and saved!")
                
                # Show preview
                st.markdown("**Logo Preview:**")
                st.image(uploaded_logo, width=200)
    
    with col2:
        # Show current logo if exists
        current_logo = BrandingManager.get_uploaded_logo()
        if current_logo:
            st.markdown("**Current Logo:**")
            st.markdown(f'<img src="{current_logo}" style="max-width: 150px; max-height: 80px;">', unsafe_allow_html=True)
            
            if st.button("🗑️ Remove Logo", key="remove_logo"):
                if 'custom_logo_base64' in st.session_state:
                    del st.session_state.custom_logo_base64
                st.success("Logo removed!")
                st.rerun()
        else:
            st.info("No logo uploaded yet")
    
    st.markdown("---")
    
    # Color Customization Section
    st.markdown("#### 🎨 Brand Colors")
    
    color_col1, color_col2, color_col3 = st.columns(3)
    
    current_colors = BrandingManager.get_custom_colors()
    
    with color_col1:
        # Primary color picker
        primary_color = st.color_picker(
            "Primary Color",
            value=current_colors['primary'],
            help="Main brand color used for buttons and highlights",
            key="primary_color_picker"
        )
    
    with color_col2:
        # Accent color picker
        accent_color = st.color_picker(
            "Accent Color",
            value=current_colors['accent'],
            help="Secondary accent color for gradients and highlights",
            key="accent_color_picker"
        )
    
    with color_col3:
        # Secondary color picker
        secondary_color = st.color_picker(
            "Secondary Color",
            value=current_colors['secondary'],
            help="Secondary color for gradients and depth",
            key="secondary_color_picker"
        )
    
    # Save colors button
    if st.button("💾 Save Brand Colors", type="primary", key="save_colors"):
        new_colors = {
            'primary': primary_color,
            'accent': accent_color,
            'secondary': secondary_color
        }
        BrandingManager.save_branding_settings(colors=new_colors)
        st.success("🎨 Brand colors saved! Changes will apply on next page refresh.")
        st.balloons()
    
    # Color preview
    st.markdown("---")
    st.markdown("#### 👀 Color Preview")
    
    preview_html = f"""
    <div style="display: flex; gap: 1rem; margin: 1rem 0;">
        <div style="
            background: {primary_color}; 
            color: white; 
            padding: 1rem; 
            border-radius: 8px; 
            text-align: center; 
            flex: 1;
            font-weight: 600;
        ">
            Primary Color<br><small>{primary_color}</small>
        </div>
        <div style="
            background: {accent_color}; 
            color: white; 
            padding: 1rem; 
            border-radius: 8px; 
            text-align: center; 
            flex: 1;
            font-weight: 600;
        ">
            Accent Color<br><small>{accent_color}</small>
        </div>
        <div style="
            background: {secondary_color}; 
            color: white; 
            padding: 1rem; 
            border-radius: 8px; 
            text-align: center; 
            flex: 1;
            font-weight: 600;
        ">
            Secondary Color<br><small>{secondary_color}</small>
        </div>
    </div>
    
    <div style="
        background: linear-gradient(135deg, {primary_color} 0%, {secondary_color} 50%, {accent_color} 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        margin: 1rem 0;
        font-weight: 600;
        font-size: 1.1rem;
    ">
        ✨ Gradient Preview - This is how your brand colors work together
    </div>
    """
    
    st.markdown(preview_html, unsafe_allow_html=True)
    
    # Reset to defaults
    st.markdown("---")
    if st.button("🔄 Reset to Default Colors", key="reset_colors"):
        # Reset colors to defaults
        default_colors = {
            'primary': '#0EA5E9',
            'accent': '#38BDF8', 
            'secondary': '#0284C7'
        }
        BrandingManager.save_branding_settings(colors=default_colors)
        st.success("Colors reset to defaults!")
        st.rerun()
