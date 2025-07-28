
import streamlit as st
import datetime

def show_page():
    st.markdown('<h2 class="section-header">🔄 Reset & Data Management</h2>', unsafe_allow_html=True)
    
    # Warning message
    st.markdown('''
    <div class="winter-card" style="border-left: 4px solid #F59E0B; background: rgba(245, 158, 11, 0.1);">
        <h3>⚠️ Data Reset Options</h3>
        <p>Use these options carefully. Some actions cannot be undone.</p>
    </div>
    ''', unsafe_allow_html=True)
    
    # Reset options
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="winter-card ice-card">', unsafe_allow_html=True)
        st.subheader("📊 Partial Reset Options")
        
        # Day counters only
        st.markdown("**🔄 Reset Day Counters Only**")
        st.write("Resets all day counters and activity logs to zero, but keeps budgets and settings.")
        
        if st.button("🔄 Reset Day Counters", type="secondary", use_container_width=True):
            st.session_state.states = {"Arizona": 0, "Minnesota": 0}
            st.session_state.day_log = []
            st.session_state.last_nudge_date = None
            st.success("✅ Day counters and logs reset!")
            st.rerun()
        
        st.markdown("---")
        
        # Budget reset
        st.markdown("**💰 Reset Budget Data**")
        st.write("Resets home budgets and seasonal cash flow to defaults.")
        
        if st.button("💰 Reset Budgets", type="secondary", use_container_width=True):
            st.session_state.home_budgets = {
                "Arizona": {"Utilities": 200, "Insurance": 150, "HOA": 100},
                "Minnesota": {"Utilities": 250, "Insurance": 170, "HOA": 90}
            }
            st.session_state.seasonal_cash_flow = {
                "Travel": 300,
                "Healthcare": 400,
                "Supplemental Insurance": 200
            }
            st.success("✅ Budget data reset to defaults!")
            st.rerun()
        
        st.markdown("---")
        
        # Chat history reset
        st.markdown("**💬 Clear Chat History**")
        st.write("Removes all AI chat history and responses.")
        
        if st.button("💬 Clear Chat History", type="secondary", use_container_width=True):
            st.session_state.chat_response = ""
            if "chat_history" in st.session_state:
                st.session_state.chat_history = []
            st.success("✅ Chat history cleared!")
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="winter-card frost-card">', unsafe_allow_html=True)
        st.subheader("🗑️ Complete Reset Options")
        
        # Full reset warning
        st.markdown('''
        <div style="background: rgba(239, 68, 68, 0.1); border: 1px solid #EF4444; border-radius: 10px; padding: 1rem; margin: 1rem 0;">
            <h4 style="color: #EF4444; margin: 0;">⚠️ Complete Reset</h4>
            <p style="margin: 0.5rem 0 0 0;">This will reset ALL data to defaults. This action cannot be undone!</p>
        </div>
        ''', unsafe_allow_html=True)
        
        # Confirmation checkbox
        confirm_reset = st.checkbox("✅ I understand this will delete all my data", key="confirm_full_reset")
        
        # Full reset button
        if st.button("🗑️ Complete Reset to Defaults", 
                    type="secondary", 
                    disabled=not confirm_reset,
                    use_container_width=True):
            # Reset everything to defaults
            st.session_state.states = {"Arizona": 0, "Minnesota": 0}
            st.session_state.home_budgets = {
                "Arizona": {"Utilities": 200, "Insurance": 150, "HOA": 100},
                "Minnesota": {"Utilities": 250, "Insurance": 170, "HOA": 90}
            }
            st.session_state.seasonal_cash_flow = {
                "Travel": 300,
                "Healthcare": 400,
                "Supplemental Insurance": 200
            }
            st.session_state.tax_threshold = 183
            st.session_state.chat_response = ""
            st.session_state.day_log = []
            st.session_state.location_enabled = False
            st.session_state.current_location = None
            st.session_state.last_nudge_date = None
            if "chat_history" in st.session_state:
                st.session_state.chat_history = []
            
            st.success("✅ All data reset to defaults!")
            st.balloons()  # Celebratory animation
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Current data overview
    st.markdown('<div class="winter-card">', unsafe_allow_html=True)
    st.subheader("📋 Current Data Overview")
    
    # Show current state of data
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_days = sum(st.session_state.states.values())
        st.metric("📅 Total Days Logged", total_days)
    
    with col2:
        total_log_entries = len(st.session_state.day_log)
        st.metric("📝 Log Entries", total_log_entries)
    
    with col3:
        total_budget = sum(sum(budget.values()) for budget in st.session_state.home_budgets.values())
        st.metric("💰 Total Monthly Budgets", f"${total_budget:,}")
    
    with col4:
        seasonal_total = sum(st.session_state.seasonal_cash_flow.values())
        st.metric("💸 Monthly Seasonal Costs", f"${seasonal_total:,}")
    
    # Detailed breakdown
    st.markdown("**📊 Detailed Data Breakdown:**")
    
    # States and days
    st.write("**🏠 States and Days:**")
    for state, days in st.session_state.states.items():
        progress = min(days / st.session_state.tax_threshold, 1.0) * 100
        st.write(f"• {state}: {days} days ({progress:.1f}% of threshold)")
    
    # Recent activity
    if st.session_state.day_log:
        st.write("**📝 Recent Activity (last 5 entries):**")
        recent_logs = sorted(st.session_state.day_log, key=lambda x: x['date'], reverse=True)[:5]
        for log in recent_logs:
            date_obj = datetime.datetime.fromisoformat(log['date']).date()
            st.write(f"• {date_obj.strftime('%m/%d/%Y')}: {log['state']} ({log['method']})")
    
    # Budget summary
    st.write("**💰 Budget Summary:**")
    for state, budget in st.session_state.home_budgets.items():
        total = sum(budget.values())
        categories = list(budget.keys())
        st.write(f"• {state}: ${total:,}/month ({len(categories)} categories)")
    
    # Seasonal expenses
    if st.session_state.seasonal_cash_flow:
        st.write("**💸 Seasonal Expenses:**")
        for category, amount in st.session_state.seasonal_cash_flow.items():
            st.write(f"• {category}: ${amount:,}/month")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Data export before reset
    st.markdown('<div class="winter-card ice-card">', unsafe_allow_html=True)
    st.subheader("📤 Export Data Before Reset")
    st.write("💡 **Tip**: Export your data before resetting to keep a backup!")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📊 Export All Data (JSON)", type="primary", use_container_width=True):
            import json
            export_data = {
                'export_date': datetime.date.today().isoformat(),
                'export_type': 'complete_backup',
                'states': st.session_state.states,
                'home_budgets': st.session_state.home_budgets,
                'seasonal_cash_flow': st.session_state.seasonal_cash_flow,
                'tax_threshold': st.session_state.tax_threshold,
                'day_log': st.session_state.day_log,
                'chat_history': st.session_state.get('chat_history', [])
            }
            
            st.download_button(
                label="💾 Download Complete Backup",
                data=json.dumps(export_data, indent=2),
                file_name=f"snowbird_complete_backup_{datetime.date.today().isoformat()}.json",
                mime="application/json"
            )
    
    with col2:
        if st.button("📋 Export Activity Log (CSV)", type="primary", use_container_width=True):
            import csv
            from io import StringIO
            
            if st.session_state.day_log:
                csv_data = StringIO()
                fieldnames = ['date', 'state', 'method', 'timestamp']
                writer = csv.DictWriter(csv_data, fieldnames=fieldnames)
                writer.writeheader()
                for log in st.session_state.day_log:
                    writer.writerow(log)
                
                st.download_button(
                    label="💾 Download Activity Log",
                    data=csv_data.getvalue(),
                    file_name=f"snowbird_activity_log_{datetime.date.today().isoformat()}.csv",
                    mime="text/csv"
                )
            else:
                st.info("No activity log data to export")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Import data section
    st.markdown('<div class="winter-card">', unsafe_allow_html=True)
    st.subheader("📥 Import Data")
    st.write("Restore data from a previously exported backup file.")
    
    uploaded_file = st.file_uploader("Choose a backup JSON file", type=['json'])
    
    if uploaded_file is not None:
        try:
            import json
            data = json.load(uploaded_file)
            
            st.write("**📋 Preview of imported data:**")
            st.write(f"• Export date: {data.get('export_date', 'Unknown')}")
            st.write(f"• States: {list(data.get('states', {}).keys())}")
            st.write(f"• Day log entries: {len(data.get('day_log', []))}")
            st.write(f"• Chat history entries: {len(data.get('chat_history', []))}")
            
            if st.button("📥 Import This Data", type="primary"):
                # Import the data
                if 'states' in data:
                    st.session_state.states = data['states']
                if 'home_budgets' in data:
                    st.session_state.home_budgets = data['home_budgets']
                if 'seasonal_cash_flow' in data:
                    st.session_state.seasonal_cash_flow = data['seasonal_cash_flow']
                if 'tax_threshold' in data:
                    st.session_state.tax_threshold = data['tax_threshold']
                if 'day_log' in data:
                    st.session_state.day_log = data['day_log']
                if 'chat_history' in data:
                    st.session_state.chat_history = data['chat_history']
                
                st.success("✅ Data imported successfully!")
                st.balloons()
                st.rerun()
                
        except json.JSONDecodeError:
            st.error("❌ Invalid JSON file. Please upload a valid backup file.")
        except Exception as e:
            st.error(f"❌ Error importing data: {e}")
    
    st.markdown('</div>', unsafe_allow_html=True)
