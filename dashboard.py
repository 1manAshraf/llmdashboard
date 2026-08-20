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
# CSS
# ============================================================

st.markdown("""
<style>

.stApp {
    background-color: #0f172a;
    color: #f8fafc;
}

[data-testid="stSidebar"] {
    background-color: #1e293b;
    border-right: 1px solid #334155;
}

.terminal-box {
    background-color: #020617;
    border: 1px solid #334155;
    border-radius: 8px;
    padding: 1rem;
    font-family: 'Courier New', Courier, monospace;
    color: #38bdf8;
    min-height: 300px;
    white-space: pre-wrap;
    overflow-y: auto;
}

.stButton>button {
    background-color: #3b82f6;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 0.5rem 1.25rem;
    font-weight: 600;
    width: 100%;
}

.stButton>button:hover {
    background-color: #2563eb;
    color: white;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# SESSION STATE
# ============================================================

if "logs" not in st.session_state:
    st.session_state.logs = (
        "[+] System initialized.\n"
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
        [
            "🎯 Penetrate!",
            "📊 Reports",
            "⚙️ Settings",
            "ℹ️ About"
        ],
        label_visibility="collapsed"
    )


# ============================================================
# PENETRATION PAGE
# ============================================================

if menu_selection == "🎯 Penetrate!":

    st.title("Target Execution Panel")

    st.write(
        "Configure a target for your authorized security "
        "assessment laboratory."
    )

    st.markdown("---")

    col1, col2 = st.columns(
        [3, 1],
        vertical_alignment="bottom"
    )

    with col1:

        target_ip = st.text_input(
            "Target IP Address",
            placeholder="e.g. 192.168.56.101",
            help="Enter the IP address of your isolated lab target."
        )

    with col2:

        confirm_btn = st.button(
            "🚀 Confirm & Run",
            disabled=st.session_state.running
        )

    st.markdown("<br>", unsafe_allow_html=True)

    st.subheader("Console Output")

    # ========================================================
    # RUN AGENT
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
            )

            # Placeholder that will display updates.
            terminal_placeholder = st.empty()

            def dashboard_log(message):

                st.session_state.logs += (
                    str(message) + "\n"
                )

                safe_logs = html.escape(
                    st.session_state.logs
                )

                terminal_placeholder.markdown(
                    f"""
                    <div class="terminal-box">
                    {safe_logs}
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
                    "Assessment completed successfully."
                )

            except Exception as e:

                dashboard_log(
                    f"[ERROR] {str(e)}"
                )

                st.error(
                    f"Agent execution failed: {str(e)}"
                )

            finally:

                st.session_state.running = False

    # ========================================================
    # TERMINAL DISPLAY
    # ========================================================

    safe_logs = html.escape(
        st.session_state.logs
    )

    st.markdown(
        f"""
        <div class="terminal-box">
        {safe_logs}
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# REPORTS
# ============================================================

elif menu_selection == "📊 Reports":

    st.title("Assessment Reports")

    if st.session_state.report:

        st.success("Latest assessment report")

        st.text_area(
            "Report",
            value=st.session_state.report,
            height=600
        )

        if st.session_state.filename:

            st.caption(
                f"Saved to: {st.session_state.filename}"
            )

    else:

        st.info(
            "No assessment reports available yet."
        )


# ============================================================
# SETTINGS
# ============================================================

elif menu_selection == "⚙️ Settings":

    st.title("Settings")

    st.text_input(
        "Ollama Endpoint",
        value="http://localhost:11434"
    )

    st.checkbox(
        "Require manual confirmation before executing commands",
        value=True
    )


# ============================================================
# ABOUT
# ============================================================

elif menu_selection == "ℹ️ About":

    st.title("About AutoSec")

    st.write(
        "AutoSec is a local AI-assisted security assessment "
        "dashboard designed for authorized laboratory environments."
    )
