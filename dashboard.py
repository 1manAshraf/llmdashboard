import streamlit as st
import html

from agent import run_agent


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
# DARK CYBERSECURITY THEME
# ============================================================

st.markdown("""
<style>

/* =========================================================
   GLOBAL
   ========================================================= */

.stApp {
    background-color: #0b1120;
    color: #e2e8f0;
}

.main {
    background-color: #0b1120;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}


/* =========================================================
   SIDEBAR
   ========================================================= */

[data-testid="stSidebar"] {
    background-color: #111827;
    border-right: 1px solid #1e293b;
}

[data-testid="stSidebar"] * {
    color: #e2e8f0;
}

[data-testid="stSidebar"] hr {
    border-color: #334155;
}


/* =========================================================
   HEADINGS
   ========================================================= */

h1 {
    color: #f8fafc !important;
    font-weight: 700 !important;
}

h2 {
    color: #e2e8f0 !important;
}

h3 {
    color: #cbd5e1 !important;
}


/* =========================================================
   NORMAL TEXT
   ========================================================= */

p {
    color: #cbd5e1;
}


/* =========================================================
   INPUT BOX
   ========================================================= */

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


/* =========================================================
   BUTTON
   ========================================================= */

.stButton > button {
    background-color: #2563eb !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    min-height: 42px;
    transition: 0.2s;
}

.stButton > button:hover {
    background-color: #1d4ed8 !important;
    color: white !important;
    border: none !important;
}

.stButton > button:disabled {
    background-color: #334155 !important;
    color: #94a3b8 !important;
}


/* =========================================================
   TERMINAL
   ========================================================= */

.terminal-container {
    background-color: #020617;
    border: 1px solid #1e293b;
    border-radius: 10px;
    padding: 18px;
    margin-top: 10px;
    min-height: 320px;
    max-height: 500px;
    overflow-y: auto;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.35);
}

.terminal-header {
    color: #64748b;
    font-family: "Courier New", monospace;
    font-size: 13px;
    margin-bottom: 12px;
}

.terminal-content {
    color: #38bdf8;
    font-family: "Courier New", monospace;
    font-size: 14px;
    line-height: 1.6;
    white-space: pre-wrap;
}


/* =========================================================
   STATUS CARDS
   ========================================================= */

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
    font-size: 22px;
    font-weight: 700;
    margin-top: 5px;
}


/* =========================================================
   DIVIDERS
   ========================================================= */

hr {
    border-color: #1e293b !important;
}


/* =========================================================
   SELECT / RADIO
   ========================================================= */

[data-testid="stRadio"] label {
    color: #cbd5e1 !important;
}


/* =========================================================
   TEXT AREA
   ========================================================= */

.stTextArea textarea {
    background-color: #020617 !important;
    color: #cbd5e1 !important;
    border: 1px solid #334155 !important;
    font-family: "Courier New", monospace !important;
}


/* =========================================================
   INFO / SUCCESS / WARNING
   ========================================================= */

[data-testid="stAlert"] {
    border-radius: 8px;
}


/* =========================================================
   FOOTER
   ========================================================= */

.footer {
    text-align: center;
    color: #475569;
    font-size: 12px;
    margin-top: 40px;
    padding: 15px;
}

</style>
""", unsafe_allow_html=True)


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
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("🛡️ AutoSec")

    st.caption(
        "AI-Assisted Security Platform"
    )

    st.markdown("---")

    menu_selection = st.radio(
        "Navigation",
        options=[
            "🎯 Penetrate!",
            "📊 Reports",
            "⚙️ Settings",
            "ℹ️ About"
        ],
        index=0,
        label_visibility="collapsed"
    )

    st.markdown("---")

    st.markdown(
        """
        <div style="
            background-color:#020617;
            padding:12px;
            border-radius:8px;
            border:1px solid #1e293b;
        ">
            <div style="color:#64748b;font-size:12px;">
                SYSTEM STATUS
            </div>

            <div style="
                color:#22c55e;
                font-weight:600;
                margin-top:5px;
            ">
                ● ONLINE
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# PENETRATION PAGE
# ============================================================

if menu_selection == "🎯 Penetrate!":

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
            """
            <div class="status-card">
                <div class="status-title">
                    Agent
                </div>

                <div class="status-value">
                    🤖 AI Agent
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:

        status = (
            "RUNNING"
            if st.session_state.running
            else "READY"
        )

        st.markdown(
            f"""
            <div class="status-card">
                <div class="status-title">
                    Status
                </div>

                <div class="status-value">
                    {"🟢" if status == "READY" else "🟡"} {status}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:

        st.markdown(
            """
            <div class="status-card">
                <div class="status-title">
                    Engine
                </div>

                <div class="status-value">
                    Ollama
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


    st.markdown("---")


    # ========================================================
    # TARGET INPUT
    # ========================================================

    st.subheader("Target Configuration")

    col1, col2 = st.columns(
        [3, 1],
        vertical_alignment="bottom"
    )

    with col1:

        target_ip = st.text_input(
            "Target IP Address",
            placeholder="e.g. 192.168.56.101",
            help=(
                "Enter the IP address of your "
                "authorized isolated lab target."
            )
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


            # ------------------------------------------------
            # DASHBOARD LOG CALLBACK
            # ------------------------------------------------

            def dashboard_log(message):

                st.session_state.logs += (
                    str(message) + "\n"
                )

                safe_logs = html.escape(
                    st.session_state.logs
                )

                terminal_placeholder.markdown(
                    f"""
                    <div class="terminal-container">

                        <div class="terminal-header">
                            AutoSec Terminal
                        </div>

                        <div class="terminal-content">
                            {safe_logs}
                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True
                )


            try:

                dashboard_log(
                    "[+] Agent started."
                )

                report, filename = run_agent(
                    target,
                    max_iterations=3,
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
                    "Security assessment completed successfully."
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
    # TERMINAL OUTPUT
    # ========================================================

    safe_logs = html.escape(
        st.session_state.logs
    )

    st.markdown(
        f"""
        <div class="terminal-container">

            <div class="terminal-header">
                AutoSec Terminal
            </div>

            <div class="terminal-content">
                {safe_logs}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# REPORTS PAGE
# ============================================================

elif menu_selection == "📊 Reports":

    st.title("📊 Assessment Reports")

    st.write(
        "View the latest security assessment generated "
        "by the AutoSec analysis engine."
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
            "No assessment reports available yet. "
            "Run an assessment from the Penetrate page."
        )


# ============================================================
# SETTINGS PAGE
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
# ABOUT PAGE
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
        │
        ▼
     Agent
        │
   ┌────┴────┐
   ▼         ▼
Observer   Planner
   │         │
   └────┬────┘
        ▼
      Ollama
        │
        ▼
     Executor
        │
        ▼
   Lab Target
        │
        ▼
     Analyser
        │
        ▼
     Report
        """,
        language="text"
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        AutoSec • Local AI-Assisted Security Assessment Platform
    </div>
    """,
    unsafe_allow_html=True
)
