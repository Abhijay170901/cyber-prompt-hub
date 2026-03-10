import streamlit as st
import json

st.set_page_config(page_title="CyberPrompt AI Hub", page_icon="🛡️", layout="wide")

# Dark Theme Customization
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: #e0e0e0; }
    .stCodeBlock { border: 1px solid #00ff41 !important; border-radius: 8px; }
    .st-expander { background-color: #161b22 !important; border: 1px solid #30363d !important; }
    h1, h2, h3 { color: #58a6ff; }
    </style>
    """, unsafe_allow_html=True)

# Load the full database
try:
    with open('prompts.json') as f:
        data = json.load(f)
except FileNotFoundError:
    st.error("Missing prompts.json file!")
    data = {"missions": []}

st.title("🛡️ CyberPrompt AI Hub")
st.markdown("### Advanced AI Framework for Cybersecurity Operations")
st.write(f"Showing {len(data['missions'])} professional security missions.")

# Sidebar Navigation
st.sidebar.title("Mission Control")
categories = sorted(list(set(m['category'] for m in data['missions'])))
selected_cat = st.sidebar.selectbox("Choose a Security Domain", categories)

st.sidebar.markdown("---")
st.sidebar.write(f"👤 **Developer:** Abhijay")
st.sidebar.write("📍 *Calgary, AB*")

# Display Missions in the selected category
st.header(f"Domain: {selected_cat}")
missions = [m for m in data['missions'] if m['category'] == selected_cat]

# Two-column layout
cols = st.columns(2)
for i, m in enumerate(missions):
    with cols[i % 2]:
        with st.container():
            st.subheader(m['title'])
            st.caption(m['description'])
            
            st.markdown("**Target Prompt:**")
            st.code(m['prompt'], language="text")
            
            # THE DROPDOWN DETAILS
            with st.expander("🔍 Deep Dive: Why & How"):
                st.markdown(f"**🚩 The Threat (Why):**\n{m['why']}")
                st.markdown(f"**⚙️ AI Strategy (How):**\n{m['how']}")
            st.divider()

st.caption("© 2026 Abhijay - Cybersecurity Portfolio Project")
