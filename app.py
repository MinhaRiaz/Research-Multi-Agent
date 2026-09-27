import os
import streamlit as st

# Streamlit Cloud secrets are loaded into the environment for the backend.
# This keeps the agent files independent from Streamlit.
if "GEMINI_API_KEY" in st.secrets:
    os.environ["GEMINI_API_KEY"] = st.secrets["GEMINI_API_KEY"]
if "SERPER_API_KEY" in st.secrets:
    os.environ["SERPER_API_KEY"] = st.secrets["SERPER_API_KEY"]

from research_team import run_research

st.set_page_config(
    page_title="ResearchForge AI",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
html, body, [class*="css"] { font-family: Inter, sans-serif; }
.stApp {
    background:
      radial-gradient(circle at 8% 8%, rgba(124,92,255,.20), transparent 27%),
      radial-gradient(circle at 92% 18%, rgba(0,210,255,.12), transparent 25%),
      linear-gradient(135deg,#07111f 0%,#0b1220 55%,#111827 100%);
    color:#f8fafc;
}
.block-container { max-width:1180px; padding-top:2.2rem; padding-bottom:3rem; }
.hero {
    padding:42px; border-radius:28px;
    background:linear-gradient(135deg,rgba(255,255,255,.09),rgba(255,255,255,.035));
    border:1px solid rgba(255,255,255,.10);
    box-shadow:0 24px 80px rgba(0,0,0,.28);
    backdrop-filter:blur(18px);
}
.badge {
    display:inline-block; padding:7px 12px; border-radius:999px;
    background:rgba(124,92,255,.16); border:1px solid rgba(124,92,255,.35);
    color:#c4b5fd; font-size:12px; font-weight:800; letter-spacing:.08em;
    text-transform:uppercase;
}
.hero h1 { font-size:clamp(2.4rem,5vw,4.8rem); line-height:1.02; margin:18px 0 14px; letter-spacing:-.055em; }
.hero p { color:#aab6c8; font-size:1.08rem; max-width:760px; line-height:1.7; }
.panel {
    margin-top:24px; padding:24px; border-radius:22px;
    background:rgba(255,255,255,.045); border:1px solid rgba(255,255,255,.08);
}
.agent-card {
    padding:18px; border-radius:18px; min-height:130px;
    background:rgba(255,255,255,.045); border:1px solid rgba(255,255,255,.07);
}
.agent-name { font-weight:800; font-size:.98rem; margin-top:8px; }
.agent-role { color:#94a3b8; font-size:.80rem; margin-top:6px; line-height:1.45; }
.muted { color:#94a3b8; }
.result {
    padding:30px; border-radius:24px;
    background:rgba(255,255,255,.055); border:1px solid rgba(255,255,255,.09);
}
div.stButton > button {
    width:100%; border:0; border-radius:14px; padding:.9rem 1rem;
    font-weight:800; color:white;
    background:linear-gradient(135deg,#7c5cff,#4f46e5);
    box-shadow:0 12px 30px rgba(99,82,220,.30);
}
div.stButton > button:hover { transform:translateY(-1px); }
.small-note { color:#64748b; font-size:.82rem; margin-top:16px; }
</style>
""", unsafe_allow_html=True)

AGENTS = [
    ("🧭", "Research Manager", "Understands the question and plans the research"),
    ("🌐", "Web Researcher", "Finds broad, current web evidence"),
    ("🎓", "Academic Researcher", "Focuses on papers and academic evidence"),
    ("🏢", "Industry Researcher", "Looks at companies, products and market applications"),
    ("✍️", "Research Synthesizer", "Verifies evidence and writes the final report"),
]

st.markdown("""
<div class="hero">
  <span class="badge">CrewAI · Gemini 3.8 Flash · Multi-Agent Research</span>
  <h1>ResearchForge AI</h1>
  <p>
    A specialized research team that plans, searches the web, investigates
    academic evidence, examines industry applications, then synthesizes the
    evidence into one structured research report.
  </p>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="panel">', unsafe_allow_html=True)
st.markdown("### 🎯 What do you want to research?")
topic = st.text_area(
    "Research topic",
    placeholder="Example: Impact of generative AI on software engineering",
    height=120,
    label_visibility="collapsed",
)
c1, c2 = st.columns([1, 1])
with c1:
    depth = st.selectbox("Research depth", ["Focused", "Detailed"], index=0)
with c2:
    st.markdown("**5-agent research team**")
    st.caption("Manager · Web · Academic · Industry · Synthesizer")
run = st.button("🚀 Start Research", use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("### ⚡ Team activity")

agent_status = []
cols = st.columns(5)
for i, (icon, name, role) in enumerate(AGENTS):
    with cols[i]:
        status = st.status(f"{icon} {name}", state="complete" if False else "running", expanded=False)
        status.update(label=f"{icon} {name} · Waiting", state="complete", expanded=False)
        agent_status.append(status)
        st.markdown(
            f'<div class="agent-card"><div style="font-size:1.45rem">{icon}</div>'
            f'<div class="agent-name">{name}</div><div class="agent-role">{role}</div></div>',
            unsafe_allow_html=True,
        )

if run:
    if not topic.strip():
        st.warning("Please enter a research topic first.")
    else:
        # Reset all visible status containers.
        for i, status in enumerate(agent_status):
            icon, name, _ = AGENTS[i]
            status.update(label=f"{icon} {name} · Waiting", state="complete", expanded=False)

        live = st.empty()

        def on_agent_start(index, message):
            for i, status in enumerate(agent_status):
                icon, name, _ = AGENTS[i]
                if i < index:
                    status.update(label=f"{icon} {name} · Complete", state="complete", expanded=False)
                elif i == index:
                    status.update(label=f"{icon} {name} · Working now", state="running", expanded=True)
                else:
                    status.update(label=f"{icon} {name} · Waiting", state="complete", expanded=False)
            live.info(f"**{AGENTS[index][0]} {AGENTS[index][1]} is working now** — {message}")

        try:
            report = run_research(topic.strip(), depth, on_agent_start)
            for i, status in enumerate(agent_status):
                icon, name, _ = AGENTS[i]
                status.update(label=f"{icon} {name} · Complete", state="complete", expanded=False)
            live.success("✅ All five research agents completed their work.")
            st.markdown("### 📑 Final research report")
            st.markdown('<div class="result">', unsafe_allow_html=True)
            st.markdown(report)
            st.markdown("</div>", unsafe_allow_html=True)
            st.download_button(
                "⬇️ Download report",
                data=report,
                file_name="research_report.md",
                mime="text/markdown",
                use_container_width=True,
            )
        except Exception as e:
            live.error(f"Research failed: {e}")
            st.exception(e)

st.markdown(
    '<div class="small-note">Review research outputs before using them for academic, professional, legal, financial or other high-stakes decisions.</div>',
    unsafe_allow_html=True,
)
