
import streamlit as st
from datetime import datetime

def render_properties_manager():
    """Render the properties management interface"""
    
    # Initialize properties if not exists
    if 'properties' not in st.session_state:
        st.session_state.properties = {}
    
    # Property management tabs
    prop_tabs = st.tabs(["🏠 My Properties", "➕ Add Property", "📊 Property Analysis"])
    
    with prop_tabs[0]:
        render_property_list()
    
    with prop_tabs[1]:
        render_add_property()
    
    with prop_tabs[2]:
        render_property_analysis()

def render_property_list():
    """Display list of properties"""
    st.subheader("🏠 Your Properties")
    
    if not st.session_state.properties:
        st.info("No properties added yet. Use the 'Add Property' tab to get started!")
        return
    
    for prop_id, property_data in st.session_state.properties.items():
        with st.expander(f"🏡 {property_data['name']}", expanded=False):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.write(f"**Address:** {property_data.get('address', 'N/A')}")
                st.write(f"**State:** {property_data.get('state', 'N/A')}")
                st.write(f"**Type:** {property_data.get('property_type', 'N/A')}")
                st.write(f"**Purchase Date:** {property_data.get('purchase_date', 'N/A')}")
                
                if property_data.get('notes'):
                    st.write(f"**Notes:** {property_data['notes']}")
            
            with col2:
                if property_data.get('purchase_price'):
                    st.metric("Purchase Price", f"${property_data['purchase_price']:,}")
                
                if st.button(f"🗑️ Remove", key=f"remove_prop_{prop_id}"):
                    del st.session_state.properties[prop_id]
                    st.success("Property removed!")
                    st.rerun()

def render_add_property():
    """Add new property form"""
    st.subheader("➕ Add New Property")
    
    with st.form("add_property_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            prop_name = st.text_input("Property Name *", placeholder="e.g., Arizona Winter Home")
            address = st.text_area("Address", placeholder="123 Sunny St, Phoenix, AZ")
            state = st.selectbox("State", ["Arizona", "Minnesota", "Other"])
            
        with col2:
            prop_type = st.selectbox("Property Type", [
                "Primary Residence", 
                "Vacation Home", 
                "Rental Property", 
                "Condo", 
                "Other"
            ])
            
            purchase_date = st.date_input("Purchase Date", value=None)
            purchase_price = st.number_input("Purchase Price ($)", min_value=0, step=1000)
        
        notes = st.text_area("Notes", placeholder="Additional details about this property...")
        
        submitted = st.form_submit_button("🏠 Add Property")
        
        if submitted and prop_name:
            # Generate unique ID
            prop_id = f"prop_{len(st.session_state.properties) + 1}_{int(datetime.now().timestamp())}"
            
            # Add property
            st.session_state.properties[prop_id] = {
                "name": prop_name,
                "address": address,
                "state": state,
                "property_type": prop_type,
                "purchase_date": purchase_date.isoformat() if purchase_date else None,
                "purchase_price": purchase_price if purchase_price > 0 else None,
                "notes": notes,
                "created_date": datetime.now().isoformat()
            }
            
            st.success(f"✅ Added property: {prop_name}")
            st.rerun()

def render_property_analysis():
    """Display property analysis and insights"""
    st.subheader("📊 Property Analysis")
    
    if not st.session_state.properties:
        st.info("Add properties to see analysis and insights.")
        return
    
    # Basic statistics
    total_properties = len(st.session_state.properties)
    
    # Count by state
    state_counts = {}
    total_value = 0
    
    for prop_data in st.session_state.properties.values():
        state = prop_data.get('state', 'Unknown')
        state_counts[state] = state_counts.get(state, 0) + 1
        
        if prop_data.get('purchase_price'):
            total_value += prop_data['purchase_price']
    
    # Display metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Properties", total_properties)
    
    with col2:
        if total_value > 0:
            st.metric("Total Property Value", f"${total_value:,}")
        else:
            st.metric("Total Property Value", "Not Available")
    
    with col3:
        avg_value = total_value / total_properties if total_properties > 0 and total_value > 0 else 0
        if avg_value > 0:
            st.metric("Average Property Value", f"${avg_value:,}")
        else:
            st.metric("Average Property Value", "Not Available")
    
    # Properties by state
    if state_counts:
        st.subheader("Properties by State")
        for state, count in state_counts.items():
            st.write(f"**{state}:** {count} properties")
        
        # Simple chart if plotly is available
        try:
            import plotly.express as px
            import pandas as pd
            
            df = pd.DataFrame(list(state_counts.items()), columns=['State', 'Count'])
            fig = px.bar(df, x='State', y='Count', title="Properties by State")
            st.plotly_chart(fig, use_container_width=True)
        except ImportError:
            pass
    
    # Property timeline
    st.subheader("Property Timeline")
    properties_with_dates = [
        (prop_data['name'], prop_data.get('purchase_date'))
        for prop_data in st.session_state.properties.values()
        if prop_data.get('purchase_date')
    ]
    
    if properties_with_dates:
        for name, date in sorted(properties_with_dates, key=lambda x: x[1] or ''):
            st.write(f"🏠 **{name}** - {date}")
    else:
        st.info("Add purchase dates to see property timeline.")
