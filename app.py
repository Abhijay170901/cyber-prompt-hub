import streamlit as st
import json

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="AI-SecOps Prompt Intelligence Platform",
    page_icon="🛡️",
    layout="wide"
)

# ---------------------------------------------------
# DARK SECURITY THEME
# ---------------------------------------------------

st.markdown("""
<style>

.stApp {
    background-color:#0b0e14;
    color:#e6edf3;
}

h1,h2,h3 {
    color:#58a6ff;
}

.stCodeBlock {
    border:1px solid #00ff41;
    border-radius:8px;
}

.metric {
    color:#00ff41;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# TITLE
# ---------------------------------------------------

st.title("🛡️ AI-SecOps Prompt Intelligence Platform")

st.subheader(
    "AI-Assisted Cybersecurity Operations for Threat Detection, Incident Response, and Secure Development"
)

st.write(
"""
This platform provides **structured AI prompts for cybersecurity analysts**, covering:

- Threat Detection  
- Incident Response  
- DevSecOps  
- Phishing Investigation  
- Security Governance
"""
)

# ---------------------------------------------------
# LOAD DATABASE
# ---------------------------------------------------

try:
    with open("prompts.json") as f:
        data = json.load(f)
except FileNotFoundError:
    st.error("prompts.json not found.")
    st.stop()

missions = data["missions"]

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

st.sidebar.title("🎯 Mission Control")

categories = sorted(set(m["category"] for m in missions))

selected_category = st.sidebar.selectbox(
    "Security Domain",
    ["All"] + categories
)

search_query = st.sidebar.text_input("🔎 Search Prompts")

mitre_set = sorted(set(
    technique
    for m in missions
    for technique in m.get("mitre", [])
))

selected_mitre = st.sidebar.selectbox(
    "MITRE ATT&CK Technique",
    ["All"] + mitre_set
)

st.sidebar.markdown("---")

st.sidebar.write("👤 **Developer:** Abhijay Nair")
st.sidebar.write("🛡️ Cybersecurity Portfolio Project")
st.sidebar.write("📍 Calgary, Canada")

# ---------------------------------------------------
# FILTER MISSIONS
# ---------------------------------------------------

filtered = missions

if selected_category != "All":
    filtered = [m for m in filtered if m["category"] == selected_category]

if selected_mitre != "All":
    filtered = [m for m in filtered if selected_mitre in m.get("mitre", [])]

if search_query:
    filtered = [
        m for m in filtered
        if search_query.lower() in m["title"].lower()
        or search_query.lower() in m["description"].lower()
    ]

# ---------------------------------------------------
# DASHBOARD METRICS
# ---------------------------------------------------

st.markdown("### 📊 Security Mission Overview")

col1, col2, col3 = st.columns(3)

col1.metric("Total Missions", len(missions))
col2.metric("Filtered Results", len(filtered))
col3.metric("Security Domains", len(categories))

st.divider()

# ---------------------------------------------------
# DISPLAY MISSIONS
# ---------------------------------------------------

cols = st.columns(2)

for i, m in enumerate(filtered):

    with cols[i % 2]:

        st.subheader(m["title"])
        st.caption(m["description"])

        info1, info2, info3 = st.columns(3)

        info1.markdown(f"**Severity:** {m.get('severity','N/A')}")
        info2.markdown(f"**Difficulty:** {m.get('difficulty','N/A')}")
        info3.markdown(f"**Domain:** {m.get('domain','N/A')}")

        st.markdown("**Tags:** " + ", ".join(m.get("tags", [])))

        if m.get("mitre"):
            st.markdown("**MITRE ATT&CK:** " + ", ".join(m["mitre"]))

        st.markdown("### 🎯 Target Prompt")

        st.code(m["prompt"], language="text")

        # FIXED DOWNLOAD BUTTON
        st.download_button(
            label="📥 Download Prompt",
            data=m["prompt"],
            file_name=f"{m['title'].replace(' ', '_')}.txt",
            key=f"download_{i}"
        )

        with st.expander("🔍 Threat Intelligence Breakdown"):

            st.markdown("### 🚩 Why This Matters")
            st.write(m["why"])

            st.markdown("### ⚙️ AI Strategy")
            st.write(m["how"])

        st.divider()

# ---------------------------------------------------
# AI PROMPT GENERATOR
# ---------------------------------------------------

st.markdown("## 🤖 AI Security Prompt Generator")

user_input = st.text_area(
    "Generate a cybersecurity investigation prompt",
    placeholder="Example: Create a threat hunting query for detecting suspicious PowerShell execution."
)

if st.button("Generate Security Prompt", key="generate_prompt"):

    if user_input:

        st.success("Suggested Prompt Structure")

        generated_prompt = f"""
You are a senior SOC analyst.

Task:
{user_input}

Provide:

1. Threat context
2. Detection methodology
3. MITRE ATT&CK mapping
4. Investigation steps
5. Recommended remediation actions
"""

        st.code(generated_prompt)

# ---------------------------------------------------
# DOWNLOAD FULL DATABASE
# ---------------------------------------------------

st.divider()

st.download_button(
    "📂 Download Full Prompt Database",
    data=json.dumps(data, indent=2),
    file_name="cyberprompt_database.json",
    key="download_full_db"
)

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------

st.divider()

st.caption(
"© 2026 Abhijay Nair | AI-SecOps Prompt Intelligence Platform | Cybersecurity Portfolio Project"
)
