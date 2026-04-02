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

import streamlit as st

st.markdown("## 🤖 AI Security Prompt Generator (MXDR Edition)")

user_input = st.text_area(
    "Generate a cybersecurity investigation prompt",
    placeholder="Example: Create a threat hunting query for detecting suspicious PowerShell execution."
)

if st.button("Generate Security Prompt", key="generate_prompt"):
    if user_input:
        st.success("Suggested Prompt Structure")
        
        # Convert input to lowercase for keyword matching
        query = user_input.lower()
        
        # DYNAMIC ROUTING: Choose the template based on keywords
        
        # 1. Email & Phishing
        if any(word in query for word in ["phishing", "email", "spam", "inbox"]):
            generated_prompt = f"""You are an Expert Tier 3 SOC Analyst.
            
Task: {user_input}

Please analyze this scenario and provide:
1. Initial Access Vector analysis (Email headers, payloads, URLs)
2. Indicators of Compromise (Domains, IPs, Hashes) to extract
3. Microsoft Defender for Office 365 / Exchange KQL hunting queries
4. Containment strategy (e.g., ZAP, URL blocking, account resets)
"""
            
        # 2. Endpoint & Malware
        elif any(word in query for word in ["powershell", "endpoint", "malware", "process", "exe"]):
            generated_prompt = f"""You are a Senior Endpoint Detection and Response (EDR) Specialist.
            
Task: {user_input}

Please analyze this endpoint activity and provide:
1. MITRE ATT&CK Tactic & Technique mapping
2. Microsoft Defender for Endpoint (MDE) KQL hunting queries
3. Process tree analysis (Parent/Child relationships & Living off the Land binaries)
4. Memory/Live Response evidence collection steps
"""
            
        # 3. Identity & Access
        elif any(word in query for word in ["login", "mfa", "identity", "credential", "brute"]):
            generated_prompt = f"""You are a Cloud Identity Security Architect.
            
Task: {user_input}

Please evaluate this identity threat and provide:
1. Entra ID / Azure AD log analysis steps (Interactive vs. Non-Interactive sign-ins)
2. KQL queries for tracking Impossible Travel, MFA Fatigue, or Token Theft
3. Lateral movement risk assessment
4. Conditional Access policy recommendations to prevent recurrence
"""

        # 4. Cloud Infrastructure (Azure/AWS)
        elif any(word in query for word in ["azure", "cloud", "aws", "tenant", "storage", "vm"]):
            generated_prompt = f"""You are a Cloud Security Posture Management (CSPM) Lead.
            
Task: {user_input}

Please evaluate this cloud infrastructure event and provide:
1. Cloud Control Plane analysis (e.g., Azure Activity Logs, AWS CloudTrail)
2. Risk assessment for misconfigurations (e.g., Public S3 buckets, exposed NSGs)
3. Sentinel KQL queries to track identity privilege escalation within the tenant
4. Remediation steps using Azure CLI or PowerShell
"""

        # 5. Insider Threat & Data Loss
        elif any(word in query for word in ["insider", "usb", "download", "exfiltration", "purview"]):
            generated_prompt = f"""You are a Data Loss Prevention (DLP) and Insider Threat Investigator.
            
Task: {user_input}

Please analyze this potential data exfiltration event and provide:
1. Behavioral anomaly context (e.g., user resigning, unusual hours)
2. Microsoft Purview / Endpoint DLP log investigation steps
3. KQL queries to track large file archives (.zip, .rar) and external network transfers
4. Legal/HR escalation protocols and immediate access revocation steps
"""

        # 6. Ransomware Operations
        elif any(word in query for word in ["ransomware", "encrypt", "shadow copy", "crypto"]):
            generated_prompt = f"""You are a Major Incident Response Commander.
            
Task: {user_input}

Please analyze this high-severity ransomware event and provide:
1. Immediate containment and network isolation protocols
2. Hunting queries for Volume Shadow Copy deletion (`vssadmin`) and encryption binaries
3. Lateral movement tracking (SMB/RDP abuse)
4. Business Continuity / Disaster Recovery (BCDR) handoff recommendations
"""

        # 7. Fallback / General SOC
        else:
            generated_prompt = f"""You are a Senior Cyber Defender.
            
Task: {user_input}

Provide a comprehensive investigation plan including:
1. Threat context & potential business impact
2. Specific Microsoft Sentinel/EDR detection methodologies
3. Step-by-step investigation runbook
4. Immediate containment and remediation actions
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
