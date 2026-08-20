import streamlit as st
import time

# 1. Page Configuration
st.set_page_config(
    page_title="AutoSec Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Custom CSS for Modern Dark Theme & Sleek Styling
st.markdown("""
    <style>
    /* Dark Theme Base Colors */
    .stApp {
        background-color: #0f172a;
        color: #f8fafc;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #1e293b;
        border-right: 1px solid #334155;
    }
    
    /* Terminal Output Box Styling */
    .terminal-box {
        background-color: #020617;
        border: 1px solid #334155;
        border-radius: 8px;
        padding: 1rem;
        font-family: 'Courier New', Courier, monospace;
        color: #38bdf8;
        min-height: 220px;
        white-space: pre-wrap;
    }
    
    /* Custom Styling for Streamlit Buttons */
    .stButton>button {
        background-color: #3b82f6;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1.25rem;
        font-weight: 600;
        width: 100%;
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        background-color: #2563eb;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Sidebar Navigation Menu
with st.sidebar:
    st.title("🛡️ AutoSec")
    st.caption("AI-Assisted Security Platform")
    st.markdown("---")
    
    menu_selection = st.radio(
        "Navigation",
        options=["🎯 Penetrate!", "📊 Reports", "⚙️ Settings", "ℹ️ About"],
        index=0,
        label_visibility="collapsed"
    )

# 4. Main Panel Logic Based on Sidebar Choice
if menu_selection == "🎯 Penetrate!":
    st.title("Target Execution Panel")
    st.write("Configure target parameters for security assessment.")
    
    st.markdown("---")
    
    # Target Input Section
    col1, col2 = st.columns([3, 1], vertical_alignment="bottom")
    
    with col1:
        target_ip = st.text_input(
            "Target IP Address or Range", 
            placeholder="e.g., 192.168.56.101",
            help="Enter the IP address of your isolated target VM."
        )
        
    with col2:
        confirm_btn = st.button("🚀 Confirm & Run")

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Console Output Area
    st.subheader("Console Output")
    
    # Interactive Terminal State Simulation
    if "logs" not in st.session_state:
        st.session_state.logs = "[+] System initialized.\n[+] Awaiting target input..."

    if confirm_btn:
        if target_ip.strip():
            st.session_state.logs = f"[+] Target acquired: {target_ip}\n[+] Initializing Ollama LLM execution chain...\n[+] Handshake complete."
            st.success(f"Execution started for target: `{target_ip}`")
        else:
            st.warning("Please enter a valid IP address before proceeding.")

    # Render CSS Terminal
    st.markdown(f'<div class="terminal-box">{st.session_state.logs}</div>', unsafe_allow_html=True)

elif menu_selection == "📊 Reports":
    st.title("Assessment Reports")
    st.info("No prior execution reports found.")

elif menu_selection == "⚙️ Settings":
    st.title("Settings")
    st.text_input("Ollama Endpoint URL", value="http://localhost:11434")
    st.checkbox("Require manual confirmation before executing commands (Recommended)", value=True)

elif menu_selection == "ℹ️ About":
    st.title("About AutoSec")
    st.write("A local dashboard integration framework for security testing environments.")