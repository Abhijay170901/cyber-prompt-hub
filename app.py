import streamlit as st
import json

# Page config
st.set_page_config(page_title="CyberPrompt AI Hub", page_icon="🛡️")

# Custom CSS for a professional look
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMarkdown { color: #fafafa; }
    </style>
    """, unsafe_allow_html=True)

# Load Prompts
with open('prompts.json') as f:
    data = json.load(f)

st.title("🛡️ CyberPrompt AI Hub")
st.sidebar.header("Mission Control")
category = st.sidebar.selectbox("Select a Domain", list(set(m['category'] for m in data['missions'])))

st.subheader(f"Domain: {category}")

# Filter and display prompts
for m in data['missions']:
    if m['category'] == category:
        with st.expander(f"🚀 {m['title']}"):
            st.write(m['description'])
            st.info(m['prompt'])
            if st.button("Copy to Clipboard", key=m['title']):
                st.write("Copied!")

st.sidebar.markdown("---")
st.sidebar.write("👤 **Developed by Abhijay Nair**")