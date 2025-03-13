import streamlit as st
import pandas as pd
from datetime import datetime

# Custom CSS Styling
st.markdown("""
<style>
    :root {
        --primary: #1a73e8;
        --background: #ffffff;
        --text: #2c3e50;
    }
    [data-testid="stAppViewContainer"] {
        background: var(--background);
        max-width: 1200px;
        margin: auto;
        padding: 2rem 3rem;
    }
    .header {
        border-bottom: 2px solid #eee;
        padding-bottom: 1.5rem;
        margin-bottom: 2rem;
    }
    .conversion-card {
        background: #f8f9fa;
        border-radius: 15px;
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    .stButton > button {
        border-radius: 25px;
        padding: 0.7rem;
        transition: all 0.3s;
    }
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(26,115,232,0.2);
    }
</style>
""", unsafe_allow_html=True)

# Conversion Database
conversion_rates = {
    'length': {'meters': 1, 'kilometers': 1000, 'centimeters': 0.01, 'millimeters': 0.001, 'miles': 1609.34, 'yards': 0.9144, 'feet': 0.3048, 'inches': 0.0254},
    'weight': {'kilograms': 1, 'grams': 0.001, 'milligrams': 0.000001, 'pounds': 0.453592, 'ounces': 0.0283495},
    'volume': {'liters': 1, 'milliliters': 0.001, 'gallons': 3.78541, 'quarts': 0.946353, 'pints': 0.473176},
    'time': {'seconds': 1, 'minutes': 60, 'hours': 3600, 'days': 86400, 'weeks': 604800}
}

# Conversion Logic
def convert_units(value, from_unit, to_unit, category):
    try:
        base_value = value * conversion_rates[category][from_unit]
        return base_value / conversion_rates[category][to_unit]
    except KeyError:
        return None

# App Header
st.markdown('<div class="header">', unsafe_allow_html=True)
st.title("📐 Unit Converter")
st.caption("Convert between multiple units across various categories")
st.markdown('</div>', unsafe_allow_html=True)

# Main Interface
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("⚙️ Configuration")
    category = st.selectbox("Conversion Category", ["Length", "Weight", "Volume", "Time"], index=0).lower()
    
    units = list(conversion_rates[category].keys())
    
    from_unit = st.selectbox("From Unit", units, index=0)
    to_unit = st.selectbox("To Unit", [u for u in units if u != from_unit], index=0)

with col2:
    st.subheader("🧮 Conversion")
    value = st.number_input("Enter Value", min_value=0.0, value=1.0, step=0.1, format="%.4f")
    
    # Convert Button
    if st.button("Convert", type="primary"):
        if from_unit != to_unit and value:
            result = convert_units(value, from_unit, to_unit, category)
            
            if result is not None:
                st.markdown(f"""
                <div class="conversion-card">
                    <div style="font-size:1.2rem; color:#5f6368;">
                        Conversion Result
                    </div>
                    <div style="font-size:2.2rem; color:var(--primary); margin:1rem 0;">
                        {value:.2f} {from_unit} = 
                    </div>
                    <div style="font-size:2.8rem; color:var(--text);">
                        {result:.6f} {to_unit}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Save to History
                history_entry = {
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'value': value,
                    'from': from_unit,
                    'to': to_unit,
                    'result': result
                }
                
                if 'history' not in st.session_state:
                    st.session_state.history = []
                    
                st.session_state.history.insert(0, history_entry)
                
                # Keep only last 10 entries
                if len(st.session_state.history) > 10:
                    st.session_state.history.pop()
            else:
                st.error("Invalid unit conversion")
        else:
            st.warning("Please select different units and enter a value")

# History Section
if st.session_state.get('history'):
    with st.expander("📜 Conversion History (Last 10)"):
        for entry in st.session_state.history:
            st.write(f"""
            **{entry['timestamp']}**  
            {entry['value']} {entry['from']} → {entry['result']:.4f} {entry['to']}
            """)

# Bottom Controls
col3, col4 = st.columns(2)
with col3:
    if st.button("Clear History", type="secondary"):
        st.session_state.history = []
        st.success("History cleared!")
        st.rerun()

with col4:
    if st.session_state.get('history'):
        st.download_button(
            label="Export History as CSV",
            data=pd.DataFrame(st.session_state.history).to_csv(index=False).encode('utf-8'),
            file_name="conversion_history.csv",
            mime="text/csv"
        )

# Footer
st.markdown("""
<div style="text-align:center; color:#5f6368; margin-top:3rem; padding:1rem">
    <hr style="margin:2rem 0">
    Professional Unit Converter v2.1 • Built with Streamlit
</div>
""", unsafe_allow_html=True)








# import streamlit as st
# import pandas as pd
# from datetime import datetime

# # Custom CSS Styling
# st.markdown("""
# <style>
#     :root {
#         --primary: #1a73e8;
#         --background: #ffffff;
#         --text: #2c3e50;
#     }
#     [data-testid="stAppViewContainer"] {
#         background: var(--background);
#         max-width: 1200px;
#         margin: auto;
#         padding: 2rem 3rem;
#     }
#     .header {
#         border-bottom: 2px solid #eee;
#         padding-bottom: 1.5rem;
#         margin-bottom: 2rem;
#     }
#     .conversion-card {
#         background: #f8f9fa;
#         border-radius: 15px;
#         padding: 2rem;
#         margin: 1.5rem 0;
#         box-shadow: 0 2px 8px rgba(0,0,0,0.1);
#     }
#     .stButton > button {
#         border-radius: 25px;
#         padding: 0.7rem;
#         transition: all 0.3s;
#     }
#     .stButton > button:hover {
#         transform: translateY(-1px);
#         box-shadow: 0 4px 12px rgba(26,115,232,0.2);
#     }
# </style>
# """, unsafe_allow_html=True)

# # Conversion Database
# conversion_rates = {
#     'length': {
#         'meters': 1,
#         'kilometers': 1000,
#         'centimeters': 0.01,
#         'millimeters': 0.001,
#         'miles': 1609.34,
#         'yards': 0.9144,
#         'feet': 0.3048,
#         'inches': 0.0254
#     },
#     'weight': {
#         'kilograms': 1,
#         'grams': 0.001,
#         'milligrams': 0.000001,
#         'pounds': 0.453592,
#         'ounces': 0.0283495
#     },
#     'volume': {
#         'liters': 1,
#         'milliliters': 0.001,
#         'gallons': 3.78541,
#         'quarts': 0.946353,
#         'pints': 0.473176
#     },
#     'time': {
#         'seconds': 1,
#         'minutes': 60,
#         'hours': 3600,
#         'days': 86400,
#         'weeks': 604800
#     }
# }

# # Conversion Logic
# def convert_units(value, from_unit, to_unit, category):
#     try:
#         base_value = value * conversion_rates[category][from_unit]
#         return base_value / conversion_rates[category][to_unit]
#     except KeyError:
#         return None

# # App Header
# st.markdown('<div class="header">', unsafe_allow_html=True)
# st.title("📐 Unit Converter")
# st.caption("Convert between 40+ units across multiple categories with precision")
# st.markdown('</div>', unsafe_allow_html=True)

# # Main Interface
# col1, col2 = st.columns([1, 2])

# with col1:
#     st.subheader("⚙️ Configuration")
#     category = st.selectbox(
#         "Conversion Category",
#         ["Length", "Weight", "Volume", "Time"],
#         index=0
#     ).lower()
    
#     units = list(conversion_rates[category].keys())
    
#     from_unit = st.selectbox(
#         "From Unit",
#         units,
#         index=0
#     )
    
#     to_unit = st.selectbox(
#         "To Unit",
#         [u for u in units if u != from_unit],
#         index=0
#     )

# with col2:
#     st.subheader("🧮 Conversion")
#     value = st.number_input(
#         "Enter Value",
#         min_value=0.0,
#         value=1.0,
#         step=0.1,
#         format="%.4f"
#     )
    
#     # Convert Button
#     if st.button("Convert", type="primary"):
#         if from_unit != to_unit and value:
#             result = convert_units(value, from_unit, to_unit, category)
            
#             if result is not None:
#                 st.markdown(f"""
#                 <div class="conversion-card">
#                     <div style="font-size:1.2rem; color:#5f6368;">
#                         Conversion Result
#                     </div>
#                     <div style="font-size:2.2rem; color:var(--primary); margin:1rem 0;">
#                         {value:.2f} {from_unit} = 
#                     </div>
#                     <div style="font-size:2.8rem; color:var(--text);">
#                         {result:.6f} {to_unit}
#                     </div>
#                 </div>
#                 """, unsafe_allow_html=True)
                
#                 # Save to History
#                 history_entry = {
#                     'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#                     'value': value,
#                     'from': from_unit,
#                     'to': to_unit,
#                     'result': result
#                 }
                
#                 if 'history' not in st.session_state:
#                     st.session_state.history = []
                    
#                 st.session_state.history.insert(0, history_entry)
                
#                 # Keep only last 10 entries
#                 if len(st.session_state.history) > 10:
#                     st.session_state.history.pop()
#             else:
#                 st.error("Invalid unit conversion")
#         else:
#             st.warning("Please select different units and enter a value")

# # History Section
# if st.session_state.get('history'):
#     with st.expander("📜 Conversion History (Last 10)"):
#         for entry in st.session_state.history:
#             st.write(f"""
#             **{entry['timestamp']}**  
#             {entry['value']} {entry['from']} → {entry['result']:.4f} {entry['to']}
#             """)

# # Bottom Controls
# col3, col4 = st.columns(2)
# with col3:
#     if st.button("Clear History", type="secondary"):
#         st.session_state.history = []
#         st.success("History cleared!")

# with col4:
#     if st.session_state.get('history'):
#         st.download_button(
#             label="Export History as CSV",
#             data=pd.DataFrame(st.session_state.history).to_csv(index=False).encode('utf-8'),
#             file_name="conversion_history.csv",
#             mime="text/csv"
#         )

# # Footer
# st.markdown("""
# <div style="text-align:center; color:#5f6368; margin-top:3rem; padding:1rem">
#     <hr style="margin:2rem 0">
#     Professional Unit Converter v2.1 • Built with Streamlit
# </div>
# """, unsafe_allow_html=True) 