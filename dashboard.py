import streamlit as st
import html
import requests

from agent import run_agent


# ============================================================
# OLLAMA STATUS CHECK
# ============================================================

def check_ollama_status():
    try:
        response = requests.get(
            "http://127.0.0.1:11434/api/tags",
            timeout=3
        )

        if response.status_code == 200:
            data = response.json()
            models = data.get("models", [])

            model_available = any(
                model.get("name", "").startswith("llama3.2")
                for model in models
            )

            return True, model_available

        return False, False

    except requests.exceptions.RequestException:
        return False, False


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AutoSec Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# DARK THEME
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        background-color: #0b1120;
        color: #e2e8f0;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    /* SIDEBAR */

    [data-testid="stSidebar"] {
        background-color: #111827;
        border-right: 1px solid #1e293b;
    }

    [data-testid="stSidebar"] * {
        color: #e2e8f0;
    }

    /* HEADINGS */

    h1 {
        color: #f8fafc !important;
    }

    h2 {
        color: #e2e8f0 !important;
    }

    h3 {
        color: #cbd5e1 !important;
    }

    /* TEXT */

    p {
        color: #cbd5e1;
    }

    /* INPUT */

    .stTextInput label {
        color: #cbd5e1 !important;
        font-weight: 600;
    }

    .stTextInput input {
        background-color: #111827 !important;
        color: #f8fafc !important;
        border: 1px solid #334155 !important;
        border-radius: 8px !important;
    }

    .stTextInput input:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 1px #3b82f6 !important;
    }

    /* BUTTON */

    .stButton > button {
        background-color: #2563eb !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        min-height: 42px;
    }

    .stButton > button:hover {
        background-color: #1d4ed8 !important;
    }

    /* TERMINAL */

    .terminal-container {
        background-color: #020617;
        border: 1px solid #1e293b;
        border-radius: 10px;
        padding: 18px;
        margin-top: 10px;
        min-height: 320px;
        max-height: 500px;
        overflow-y: auto;
    }

    .terminal-header {
        color: #64748b;
        font-family: monospace;
        font-size: 13px;
        margin-bottom: 12px;
    }

    .terminal-content {
        color: #38bdf8;
        font-family: monospace;
        font-size: 14px;
        line-height: 1.6;
        white-space: pre-wrap;
    }

    /* STATUS CARD */

    .status-card {
        background-color: #111827;
        border: 1px solid #1e293b;
        border-radius: 10px;
        padding: 18px;
        margin-bottom: 15px;
    }

    .status-title {
        color: #64748b;
        font-size: 13px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .status-value {
        color: #f8fafc;
        font-size: 20px;
        font-weight: 700;
        margin-top: 5px;
    }

    /* FOOTER */

    .footer {
        text-align: center;
        color: #475569;
        font-size: 12px;
        margin-top: 40px;
        padding: 15px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SESSION STATE
# ============================================================

if "logs" not in st.session_state:
    st.session_state.logs = (
        "[+] AutoSec system initialized.\n"
        "[+] Agent status: READY\n"
        "[+] Awaiting target input..."
    )

if "report" not in st.session_state:
    st.session_state.report = None

if "filename" not in st.session_state:
    st.session_state.filename = None

if "running" not in st.session_state:
    st.session_state.running = False


# ============================================================
# CHECK OLLAMA
# ============================================================

ollama_online, llama_available = check_ollama_status()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("🛡️ AutoSec")
    st.caption("LLM-Integrated Security Platform")

    st.markdown("---")

    menu_selection = st.radio(
        "Navigation",
        [
            "🎯 Penetrate",
            "📊 Reports",
            "⚙️ Settings",
            "ℹ️ About"
        ],
        index=0,
        label_visibility="collapsed"
    )

    st.markdown("---")

    # ========================================================
    # SYSTEM STATUS
    # ========================================================

    if ollama_online:
        system_status = "🟢 ONLINE"
        system_message = "Ollama is reachable"
    else:
        system_status = "🔴 OFFLINE"
        system_message = "Ollama is not reachable"

    st.markdown(
        f"""
        <div style="
            background-color: #020617;
            padding: 14px;
            border-radius: 8px;
            border: 1px solid #1e293b;
            margin-bottom: 10px;
        ">

            <div style="
                color: #64748b;
                font-size: 12px;
            ">
                SYSTEM STATUS
            </div>

            <div style="
                color: #e2e8f0;
                font-weight: 600;
                margin-top: 8px;
            ">
                {system_status}
            </div>

            <div style="
                color: #64748b;
                font-size: 11px;
                margin-top: 5px;
            ">
                {system_message}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    # ========================================================
    # AI MODEL STATUS
    # ========================================================

    if ollama_online and llama_available:
        model_status = "🟢 LLAMA 3.2 AVAILABLE"
        model_color = "#22c55e"

    elif ollama_online:
        model_status = "🟡 MODEL NOT FOUND"
        model_color = "#f59e0b"

    else:
        model_status = "⚫ UNAVAILABLE"
        model_color = "#64748b"

    st.markdown(
        f"""
        <div style="
            background-color: #020617;
            padding: 14px;
            border-radius: 8px;
            border: 1px solid #1e293b;
        ">

            <div style="
                color: #64748b;
                font-size: 12px;
            ">
                AI MODEL
            </div>

            <div style="
                color: {model_color};
                font-weight: 600;
                margin-top: 8px;
            ">
                {model_status}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )
# ============================================================
# PENETRATE PAGE
# ============================================================

if menu_selection == "🎯 Penetrate":

    st.title("🎯 Target Execution Panel")

    st.write(
        "Configure a target for your authorized "
        "security assessment laboratory."
    )

    st.markdown("---")


    # ========================================================
    # STATUS CARDS
    # ========================================================

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(
            '<div class="status-card">'
            '<div class="status-title">AGENT</div>'
            '<div class="status-value">🤖 LLM Agent</div>'
            '</div>',
            unsafe_allow_html=True
        )

    with col2:

        if st.session_state.running:
            status_text = "🟡 RUNNING"
        else:
            status_text = "🟢 READY"

        st.markdown(
            '<div class="status-card">'
            '<div class="status-title">STATUS</div>'
            f'<div class="status-value">{status_text}</div>'
            '</div>',
            unsafe_allow_html=True
        )

    with col3:

        st.markdown(
            '<div class="status-card">'
            '<div class="status-title">ENGINE</div>'
            '<div class="status-value">Ollama</div>'
            '</div>',
            unsafe_allow_html=True
        )


    # ========================================================
    # TARGET CONFIGURATION
    # ========================================================

    st.markdown("---")

    st.subheader("Target Configuration")

    col1, col2 = st.columns(
        [3, 1],
        vertical_alignment="bottom"
    )

    with col1:

        target_ip = st.text_input(
            "Target IP Address",
            placeholder="e.g. 192.168.56.101",
            help="Enter the IP address of your authorized lab target."
        )

    with col2:

        confirm_btn = st.button(
            "🚀 START ASSESSMENT",
            disabled=st.session_state.running,
            use_container_width=True
        )


    # ========================================================
    # EXECUTION
    # ========================================================

    if confirm_btn:

        target = target_ip.strip()

        if not target:

            st.warning(
                "Please enter a target IP address."
            )

        else:

            st.session_state.running = True

            st.session_state.logs = (
                f"[+] Target acquired: {target}\n"
                "[+] Initializing AutoSec agent...\n"
                "[+] Preparing security assessment...\n"
            )

            terminal_placeholder = st.empty()


            # =================================================
            # DASHBOARD LOG FUNCTION
            # =================================================

            def dashboard_log(message):

                st.session_state.logs += (
                    str(message) + "\n"
                )

                safe_logs = html.escape(
                    st.session_state.logs
                )

                terminal_placeholder.markdown(
                    '<div class="terminal-container">'
                    '<div class="terminal-header">'
                    'AutoSec Terminal'
                    '</div>'
                    '<div class="terminal-content">'
                    f'{safe_logs}'
                    '</div>'
                    '</div>',
                    unsafe_allow_html=True
                )


            # =================================================
            # RUN AGENT
            # =================================================

            try:

                dashboard_log(
                    "[+] Agent started."
                )

                report, filename = run_agent(
                    target,
                    max_iterations=1,
                    log_callback=dashboard_log
                )

                st.session_state.report = report
                st.session_state.filename = filename

                dashboard_log(
                    "[+] Assessment completed."
                )

                dashboard_log(
                    f"[+] Report saved: {filename}"
                )

                st.success(
                    "Security assessment completed."
                )

            except Exception as e:

                dashboard_log(
                    "[ERROR] Agent execution failed."
                )

                dashboard_log(
                    f"[ERROR] {str(e)}"
                )

                st.error(
                    f"Agent error: {str(e)}"
                )

            finally:

                st.session_state.running = False


    # ========================================================
    # TERMINAL
    # ========================================================

    safe_logs = html.escape(
        st.session_state.logs
    )

    st.markdown(
        '<div class="terminal-container">'
        '<div class="terminal-header">'
        'AutoSec Terminal'
        '</div>'
        '<div class="terminal-content">'
        f'{safe_logs}'
        '</div>'
        '</div>',
        unsafe_allow_html=True
    )


# ============================================================
# REPORTS
# ============================================================

elif menu_selection == "📊 Reports":

    st.title("📊 Assessment Reports")

    st.write(
        "View the latest security assessment report."
    )

    st.markdown("---")

    if st.session_state.report:

        st.success(
            "Latest assessment report available."
        )

        st.text_area(
            "Generated Report",
            value=st.session_state.report,
            height=600
        )

        if st.session_state.filename:

            st.caption(
                f"Report file: {st.session_state.filename}"
            )

    else:

        st.info(
            "No assessment reports available yet."
        )


# ============================================================
# SETTINGS
# ============================================================

elif menu_selection == "⚙️ Settings":

    st.title("⚙️ Settings")

    st.write(
        "Configure the local AutoSec environment."
    )

    st.markdown("---")

    st.text_input(
        "Ollama Endpoint",
        value="http://127.0.0.1:11434"
    )

    st.text_input(
        "Ollama Model",
        value="llama3.2"
    )

    st.checkbox(
        "Require manual confirmation before executing commands",
        value=True
    )

    st.checkbox(
        "Enable execution logging",
        value=True
    )


# ============================================================
# ABOUT
# ============================================================

elif menu_selection == "ℹ️ About":

    st.title("ℹ️ About AutoSec")

    st.write(
        "AutoSec is a local AI-assisted security assessment "
        "dashboard designed for authorized laboratory environments."
    )

    st.markdown("---")

    st.subheader("Architecture")

    st.code(
        """
Streamlit Dashboard
        |
        v
     Agent
        |
   +----+----+
   |         |
   v         v
Observer   Planner
   |         |
   +----+----+
        |
        v
      Ollama
        |
        v
     Executor
        |
        v
    Lab Target
        |
        v
     Analyser
        |
        v
      Report
        """,
        language="text"
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    '<div class="footer">'
    'AutoSec • Local AI-Assisted Security Assessment Platform'
    '</div>',
    unsafe_allow_html=True
)
