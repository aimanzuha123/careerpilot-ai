# dashboard/app.py
"""
CareerPilot AI -- Phase 3 Premium Streamlit Dashboard

New Features:
  - Premium Modern Dark UI
  - ATS Dashboard
  - Plotly Charts for Market Trends & Gaps
  - Interview Prep Simulator
  - Interactive Career Roadmap
"""

import sys
import os
import sys
import os
import json
from typing import Optional

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from pipelines.core_pipeline import CorePipeline
from role_manager import RoleManager

# Provide fallback metadata since role_manager.py doesn't have it
ROLE_METADATA_FALLBACK = {
    "AI Engineer": {
        "icon": "🤖", "label": "AI Engineer", "color": "#6366f1",
        "hiring_trend": "High Growth", "avg_salary_usd": 145000,
        "description": "Building the future with AI and ML systems.",
        "seniority_path": ["Junior AI", "AI Engineer", "Senior AI Engineer", "AI Lead"],
        "daily_tools": ["Python", "PyTorch", "TensorFlow", "Docker"],
        "key_companies": ["OpenAI", "Google", "Meta", "Anthropic"]
    },
    "Data Analyst": {
        "icon": "📊", "label": "Data Analyst", "color": "#10b981",
        "hiring_trend": "Stable Demand", "avg_salary_usd": 85000,
        "description": "Extracting actionable insights from data.",
        "seniority_path": ["Junior Analyst", "Data Analyst", "Senior Analyst", "Analytics Manager"],
        "daily_tools": ["SQL", "Excel", "Tableau", "Python"],
        "key_companies": ["Amazon", "Uber", "Airbnb", "Banking"]
    },
    "DevOps Engineer": {
        "icon": "⚙️", "label": "DevOps", "color": "#f59e0b",
        "hiring_trend": "High Demand", "avg_salary_usd": 130000,
        "description": "Streamlining deployment and cloud infrastructure.",
        "seniority_path": ["Junior DevOps", "DevOps Engineer", "Senior DevOps", "Platform Lead"],
        "daily_tools": ["Docker", "Kubernetes", "AWS", "Terraform"],
        "key_companies": ["Netflix", "Stripe", "AWS", "Datadog"]
    },
    "Full Stack Developer": {
        "icon": "💻", "label": "Full Stack", "color": "#3b82f6",
        "hiring_trend": "Strong Demand", "avg_salary_usd": 115000,
        "description": "Building end-to-end web applications.",
        "seniority_path": ["Junior Dev", "Full Stack Dev", "Senior Dev", "Tech Lead"],
        "daily_tools": ["React", "Node.js", "TypeScript", "PostgreSQL"],
        "key_companies": ["Meta", "Atlassian", "Shopify", "Startups"]
    },
    "Cybersecurity Analyst": {
        "icon": "🛡️", "label": "Cybersecurity", "color": "#ef4444",
        "hiring_trend": "Growing", "avg_salary_usd": 105000,
        "description": "Protecting systems and networks from threats.",
        "seniority_path": ["Junior Analyst", "Security Analyst", "Senior Analyst", "CISO"],
        "daily_tools": ["Kali Linux", "Wireshark", "Splunk", "Python"],
        "key_companies": ["CrowdStrike", "Palantir", "Gov", "Banks"]
    }
}

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CareerPilot AI - Pro",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

:root {
  --bg:       #0a0a0b; --bg1: #121214; --bg2: #1c1c1f; --bg3: #27272a;
  --border:   #27272a; --border-hi: #3f3f46;
  --text:     #fafafa; --text-muted: #a1a1aa;
  --primary:  #6366f1; --primary-hover: #4f46e5;
  --success:  #10b981; --warning: #f59e0b; --danger: #ef4444; --info: #3b82f6;
  --radius:   12px;
}
.stApp { background:var(--bg); color:var(--text); font-family:'Inter', sans-serif; }
[data-testid="stSidebar"] { background:var(--bg1)!important; border-right:1px solid var(--border); }
.stButton>button {
  background:linear-gradient(135deg, var(--primary), var(--primary-hover))!important;
  color:#ffffff!important; border:none!important;
  font-family:'Inter', sans-serif!important; font-weight:600!important;
  border-radius:var(--radius)!important; letter-spacing:0.02em!important; padding:12px 24px!important;
  box-shadow: 0 4px 14px 0 rgba(99, 102, 241, 0.39)!important; transition: all 0.2s ease!important;
}
.stButton>button:hover { transform: translateY(-1px); box-shadow: 0 6px 20px rgba(99, 102, 241, 0.5)!important; }

[data-testid="stTabContent"] { background:transparent!important; margin-top:20px; }
button[role="tab"] { font-family:'Inter', sans-serif!important; font-weight:500!important; color:var(--text-muted)!important; font-size:1.05rem!important; padding-bottom: 8px!important; }
button[role="tab"][aria-selected="true"] { color:var(--text)!important; border-bottom:3px solid var(--primary)!important; }
.stSelectbox label,.stSlider label,.stRadio label,.stFileUploader label,.stTextArea label { color:var(--text-muted)!important; font-size:0.9rem!important; font-weight:500!important; }
h1,h2,h3,h4,h5 { font-family:'Inter', sans-serif!important; font-weight:600!important; letter-spacing:-0.02em; }
hr { border-color:var(--border)!important; }

.card { background:var(--bg1); border:1px solid var(--border); border-radius:var(--radius); padding:24px; margin-bottom:16px; transition:all 0.2s ease; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06); }
.card:hover { border-color:var(--border-hi); transform: translateY(-2px); box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05); }

.hero { background:linear-gradient(135deg, #121214 0%, #1c1c1f 100%);
  border:1px solid var(--border); border-top:3px solid var(--primary); border-radius:16px;
  padding:36px; margin-bottom:32px; position:relative; overflow:hidden; }
.hero::after { content:''; position:absolute; top:-100px; right:-100px; width:300px; height:300px;
  background:radial-gradient(circle, rgba(99, 102, 241, 0.15) 0%, transparent 70%); pointer-events:none; }
.hero-title { font-size:2.4rem; color:var(--text); font-weight:700; margin:0 0 12px; letter-spacing:-0.03em; }
.hero-sub { color:var(--text-muted); font-size:1.1rem; max-width: 600px; line-height:1.5; }
.hero-badges { margin-top:20px; display:flex; gap:10px; flex-wrap:wrap; }

.badge { background:rgba(255,255,255,0.05); border:1px solid rgba(255,255,255,0.1); color:var(--text);
  padding:6px 12px; border-radius:20px; font-size:0.8rem; font-weight:500; font-family:'JetBrains Mono', monospace; }
.badge-primary { background:rgba(99, 102, 241, 0.1); border-color:rgba(99, 102, 241, 0.3); color:#818cf8; }
.badge-success { background:rgba(16, 185, 129, 0.1); border-color:rgba(16, 185, 129, 0.3); color:#34d399; }
.badge-warning { background:rgba(245, 158, 11, 0.1); border-color:rgba(245, 158, 11, 0.3); color:#fbbf24; }
.badge-danger { background:rgba(239, 68, 68, 0.1); border-color:rgba(239, 68, 68, 0.3); color:#f87171; }

.sk-row { display:flex; align-items:center; padding:10px 0; border-bottom:1px solid var(--border); }
.sk-row:last-child { border:none; }
.sk-rank { font-family:'JetBrains Mono', monospace; font-size:0.75rem; color:var(--text-muted); width:32px; flex-shrink:0; }
.sk-name { font-size:0.9rem; color:var(--text); width:180px; flex-shrink:0; font-weight:500; }
.sk-bar  { flex:1; background:var(--bg2); border-radius:6px; height:8px; margin:0 16px; overflow:hidden; }
.sk-fill { height:100%; border-radius:6px; transition: width 1s ease-in-out; }
.sk-freq { font-family:'JetBrains Mono', monospace; font-size:0.75rem; color:var(--text-muted); width:60px; text-align:right; }

.gap-row { display:flex; align-items:center; padding:12px 0; border-bottom:1px solid var(--border); }
.gap-row:last-child { border:none; }
.gap-idx { font-family:'JetBrains Mono', monospace; width:32px; font-size:0.75rem; color:var(--text-muted); flex-shrink:0; }
.gap-name { flex:1; font-size:0.95rem; color:var(--text); font-weight:600; }
.gap-cat  { font-size:0.8rem; color:var(--text-muted); width:160px; }
.gap-fr   { font-family:'JetBrains Mono', monospace; font-size:0.8rem; color:var(--text-muted); width:60px; text-align:right; }

.chip-match { display:inline-block; background:rgba(16, 185, 129, 0.1); border:1px solid rgba(16, 185, 129, 0.2);
  color:#34d399; padding:6px 12px; border-radius:20px; font-size:0.85rem; font-weight:500; margin:4px; box-shadow: 0 1px 2px rgba(0,0,0,0.1); }
.chip-gap { display:inline-block; background:rgba(239, 68, 68, 0.1); border:1px solid rgba(239, 68, 68, 0.2);
  color:#f87171; padding:6px 12px; border-radius:20px; font-size:0.85rem; font-weight:500; margin:4px; box-shadow: 0 1px 2px rgba(0,0,0,0.1); }

.wk-card { background:var(--bg1); border:1px solid var(--border); border-radius:var(--radius); padding:24px; margin-bottom:20px; position: relative; overflow: hidden; }
.wk-card::before { content: ''; position: absolute; left: 0; top: 0; bottom: 0; width: 4px; background: var(--primary); }
.wk-hdr  { display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:16px; }
.wk-num  { font-family:'JetBrains Mono', monospace; color:var(--primary); font-size:0.85rem; font-weight:600; letter-spacing:0.05em; }
.wk-theme { font-size:1.1rem; font-weight:600; color:var(--text); margin-top:4px; }
.wk-date  { font-size:0.85rem; color:var(--text-muted); margin-top:4px; }
.wk-hrs   { background:rgba(255,255,255,0.05); border:1px solid rgba(255,255,255,0.1); color:var(--text);
  padding:4px 12px; border-radius:20px; font-family:'JetBrains Mono', monospace; font-size:0.8rem; font-weight:500; }
.tk-row   { display:flex; align-items:center; padding:12px 10px; border-radius: 8px; margin-bottom: 4px; font-size:0.95rem; transition: background 0.2s; }
.tk-row:hover { background: var(--bg2); }
.tk-hrs   { background:rgba(59, 130, 246, 0.1); border:1px solid rgba(59, 130, 246, 0.2); color:#60a5fa;
  font-family:'JetBrains Mono', monospace; font-size:0.8rem; padding:4px 10px; border-radius:6px;
  margin-right:16px; flex-shrink:0; min-width:44px; text-align:center; font-weight:600; }
.tk-name  { flex:1; color:var(--text); font-weight:500; }
.tk-gap   { background:rgba(239, 68, 68, 0.1); border:1px solid rgba(239, 68, 68, 0.2); color:#f87171;
  font-size:0.75rem; font-weight:600; padding:2px 8px; border-radius:6px; margin-right:12px; flex-shrink:0; letter-spacing:0.05em; }
.tk-plat  { color:var(--text-muted); font-size:0.85rem; text-align:right; font-weight:500; }
.info-box { background:rgba(59, 130, 246, 0.05); border:1px solid rgba(59, 130, 246, 0.2); border-left:4px solid #3b82f6; border-radius:8px;
  padding:16px 20px; font-size:0.95rem; color:#e0f2fe; line-height:1.5; }
.score-val   { font-family:'JetBrains Mono', monospace; font-size:3.5rem; font-weight:700; line-height:1; letter-spacing:-0.02em; }
.score-label { font-size:0.85rem; color:var(--text-muted); text-transform:uppercase; letter-spacing:0.1em; margin-top:8px; font-weight:600; }
</style>
""", unsafe_allow_html=True)


# ── Helpers ───────────────────────────────────────────────────────────────────
@st.cache_data(ttl=120, show_spinner=False)
def run_pipeline_cached(role, level, hours, resume_bytes, resume_filename, resume_text):
    p = CorePipeline(role_type=role, skill_level=level, hours_per_week=hours, top_n_skills=20)
    return p.run(resume_bytes=resume_bytes, resume_filename=resume_filename, resume_text=resume_text)

def score_color(s):
    return ("#10b981" if s >= 70 else "#f59e0b" if s >= 40 else "#ef4444")

def demand_color(d):
    return {"HIGH": "#ef4444", "MEDIUM": "#f59e0b", "LOW": "#10b981"}.get(d, "var(--text-muted)")

def skill_bar(rank, skill, freq, max_freq, color="#3b82f6"):
    pct = int((freq / max_freq) * 100) if max_freq else 0
    st.markdown(f"""<div class="sk-row">
      <span class="sk-rank">#{rank:02d}</span>
      <span class="sk-name">{skill.title()}</span>
      <div class="sk-bar"><div class="sk-fill" style="width:{pct}%;background:{color};"></div></div>
      <span class="sk-freq">{freq}x</span></div>""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""<div style="text-align:center;padding:20px 0 30px;">
      <div style="font-size:2rem; margin-bottom: 8px;">🚀</div>
      <div style="font-family:'Inter', sans-serif;font-size:1.5rem;color:#ffffff;font-weight:700;letter-spacing:-0.03em;">CareerPilot</div>
      <div style="font-size:0.85rem;color:#6b7a96;margin-top:4px;font-weight:500;letter-spacing:0.05em;text-transform:uppercase;">Pro Edition</div>
    </div>""", unsafe_allow_html=True)

    st.markdown("### Profile Settings")
    rm_inst = RoleManager()
    roles = rm_inst.get_roles() if hasattr(rm_inst, "get_roles") else ["AI/ML Engineer", "Data Scientist", "Data Analyst", "Data Engineer", "Software Engineer"]
    
    role_type = st.selectbox("Target Role", roles, index=0)
    
    # Get metadata, fallback to generic if not found
    meta = ROLE_METADATA_FALLBACK.get(role_type, {
        "icon": "💼", "label": role_type, "color": "#6366f1",
        "hiring_trend": "Stable Demand", "avg_salary_usd": 100000,
        "description": f"Professional in {role_type}.",
        "seniority_path": ["Junior", "Mid-Level", "Senior", "Lead"],
        "daily_tools": ["Python", "SQL", "Git"],
        "key_companies": ["Tech Companies", "Startups", "Enterprise"]
    })
    
    col1, col2 = st.columns(2)
    with col1:
        skill_level = st.radio("Level", ["Beginner", "Intermediate", "Advanced"], index=1)
    with col2:
        hours_per_week = st.slider("Hours / Week", 3.0, 25.0, 10.0, 1.0)
    
    st.markdown("---")
    st.markdown("### ATS Resume Upload")
    resume_mode = st.radio("Input Format", ["Upload PDF", "Paste Text", "No Resume"], index=2, horizontal=True)

    resume_bytes: Optional[bytes] = None
    resume_filename = "resume.pdf"
    resume_text_input: Optional[str] = None

    if resume_mode == "Upload PDF":
        uploaded = st.file_uploader("", type=["pdf"], label_visibility="collapsed")
        if uploaded:
            resume_bytes = uploaded.read()
            resume_filename = uploaded.name
            st.success(f"ATS Ready: {uploaded.name}")
    elif resume_mode == "Paste Text":
        resume_text_input = st.text_area(
            "", height=150, label_visibility="collapsed",
            placeholder="Paste your resume text here for ATS parsing..."
        )

    st.markdown("<br>", unsafe_allow_html=True)
    run_btn = st.button("Generate Strategy", use_container_width=True)

    st.markdown("""<div style="margin-top: 40px; padding: 16px; background: rgba(255,255,255,0.03); border-radius: 12px; border: 1px solid rgba(255,255,255,0.05);">
        <div style="font-size:0.75rem; color:#a1a1aa; text-transform:uppercase; letter-spacing:0.05em; font-weight:600; margin-bottom:8px;">Features Unlocked</div>
        <div style="font-size:0.85rem; color:#d4d4d8; line-height:1.8;">
            <div style="display:flex; align-items:center; gap:8px;">✨ ATS Scoring Engine</div>
            <div style="display:flex; align-items:center; gap:8px;">📊 Market Charts</div>
            <div style="display:flex; align-items:center; gap:8px;">🗺️ Interactive Roadmap</div>
            <div style="display:flex; align-items:center; gap:8px;">🗣️ Interview Simulator</div>
        </div>
    </div>""", unsafe_allow_html=True)


# ── Pipeline execution ────────────────────────────────────────────────────────
effective_text = resume_text_input if resume_mode == "Paste Text" else None

if "result" not in st.session_state or run_btn:
    with st.spinner("Analyzing job market & extracting insights..."):
        try:
            result = run_pipeline_cached(
                role_type, skill_level.lower(), hours_per_week,
                resume_bytes, resume_filename, effective_text
            )
            st.session_state["result"] = result
        except Exception as e:
            st.error(f"Execution Error: {e}")
            st.stop()

result = st.session_state.get("result", {})
if not result:
    st.info("👋 Welcome! Configure your profile on the left and click **Generate Strategy** to begin.")
    st.stop()

has_resume = result.get("has_resume", False)
plan       = result.get("plan", {})
ra         = result.get("resume_analysis")
# Use our fallback meta instead of role_ctx to prevent crashing if RoleManager was basic
role_ctx   = result.get("role_context", {})
data_stats = result.get("data_stats", {})
top_skills = result.get("top_skills", [])

# ── Hero Section ──────────────────────────────────────────────────────────────
resume_badge = '<span class="badge badge-success">📄 ATS Parsed</span>' if has_resume else ""
plan_badge   = f'<span class="badge badge-primary">{"🎯 Personalized Path" if plan.get("gap_driven") else "📈 Market Path"}</span>'
st.markdown(f"""
<div class="hero">
  <div class="hero-title">Welcome to your Career Command Center.</div>
  <div class="hero-sub">AI-driven market insights and personalized upskilling roadmaps for ambitious professionals. Optimized for <b>{role_type}</b>.</div>
  <div class="hero-badges">
    <span class="badge">{meta['icon']} {role_type}</span>
    <span class="badge">Lv. {skill_level}</span>
    {resume_badge}
    {plan_badge}
  </div>
</div>
""", unsafe_allow_html=True)

# ── Global Metrics ────────────────────────────────────────────────────────────
m1, m2, m3, m4 = st.columns(4)
with m1: 
    st.metric("Live Market Data", f"{data_stats.get('total_jobs',0):,} Jobs", delta="Market Volume", delta_color="normal")
with m2: 
    st.metric("Skill Taxonomy", result.get("skill_summary",{}).get("total_unique_skills",0), "Core Competencies")
if ra and isinstance(ra, dict):
    with m3:
        st.metric("ATS Match Score", f"{ra.get('match_score', 0):.1f}%", f"{len(ra.get('matched_skills', []))} Matches", delta_color="normal")
    with m4:
        st.metric("Critical Gaps", len(ra.get("gap_skills", [])), "Immediate Focus Areas", delta_color="inverse")
else:
    with m3: st.metric("ATS Match Score", "N/A", "Upload Resume")
    with m4: st.metric("Critical Gaps", "N/A", "Upload Resume")

st.markdown("<br>", unsafe_allow_html=True)

# ── Main Tabs ─────────────────────────────────────────────────────────────────
t1, t2, t3, t4, t5 = st.tabs([
    "🎭 Role Intelligence", 
    "📊 Market & Charts", 
    "📄 ATS Dashboard", 
    "🗺️ Career Roadmap",
    "🗣️ Interview Prep"
])

# ══════ TAB 1: ROLE INTELLIGENCE ═════════════════════════════════════════════
with t1:
    col_main, col_side = st.columns([2, 1])
    # Fallback applied from meta above
    act = meta

    with col_main:
        st.markdown(f"""<div class="card" style="border-left: 4px solid {act['color']};">
          <div style="font-size:2.5rem; margin-bottom: 12px;">{act['icon']}</div>
          <h2 style="margin:0 0 8px 0; color:#fff;">{act['label']}</h2>
          <p style="font-size:1.05rem; color:var(--text-muted); line-height:1.6;">{act['description']}</p>
          <div style="display:flex; gap: 24px; margin-top:24px;">
            <div>
              <div style="font-size:0.8rem; color:var(--text-muted); text-transform:uppercase;">Est. Salary</div>
              <div style="font-size:1.5rem; font-weight:700; color:{act['color']};">${act.get('avg_salary_usd', 0):,}</div>
            </div>
            <div>
              <div style="font-size:0.8rem; color:var(--text-muted); text-transform:uppercase;">Demand Trend</div>
              <div style="font-size:1.5rem; font-weight:700; color:#fff;">{act.get('hiring_trend', 'Unknown')}</div>
            </div>
          </div>
        </div>""", unsafe_allow_html=True)
        
        path = act.get("seniority_path", [])
        st.markdown("### Corporate Ladder")
        steps_html = "".join([f"""
            <div style="display:flex; align-items:center; gap:16px; margin-bottom:12px;">
                <div style="background:rgba(255,255,255,0.05); border-radius:50%; width:32px; height:32px; display:flex; align-items:center; justify-content:center; font-weight:600; color:var(--text-muted);">{i+1}</div>
                <div style="font-size:1.1rem; font-weight: {'600' if i==1 else '400'}; color: {'#fff' if i==1 else 'var(--text-muted)'};">{p}</div>
            </div>
        """ for i, p in enumerate(path)])
        st.markdown(f'<div class="card">{steps_html}</div>', unsafe_allow_html=True)

    with col_side:
        st.markdown("### Essential Tools")
        tools_html = "".join(f'<span class="badge" style="margin:0 8px 8px 0; display:inline-block;">{t}</span>' for t in act.get("daily_tools",[]))
        st.markdown(f'<div class="card">{tools_html}</div>', unsafe_allow_html=True)
        
        st.markdown("### Top Employers")
        co_html = "".join(f'<div style="padding:10px 0; border-bottom:1px solid var(--border); font-weight:500;">🏢 {co}</div>' for co in act.get("key_companies",[]))
        st.markdown(f'<div class="card">{co_html}</div>', unsafe_allow_html=True)

# ══════ TAB 2: MARKET & CHARTS ═══════════════════════════════════════════════
with t2:
    st.markdown("### Market Skill Demand")
    if top_skills:
        df_skills = pd.DataFrame(top_skills[:15])
        df_skills['skill'] = df_skills['skill'].str.title()
        
        c1, c2 = st.columns([1.5, 1])
        
        with c1:
            fig = px.bar(df_skills, x='frequency', y='skill', orientation='h',
                         color='frequency', color_continuous_scale='Purples',
                         template='plotly_dark')
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                yaxis={'categoryorder':'total ascending', 'title': ''},
                xaxis={'title': 'Job Postings Mentioning Skill'},
                margin=dict(l=0, r=0, t=20, b=0),
                height=450
            )
            st.plotly_chart(fig, use_container_width=True)
            
        with c2:
            st.markdown("#### Demand Distribution")
            cats = result.get("skills_by_category", {})
            if cats:
                cat_counts = [{"Category": k.replace('_',' ').title(), "Count": len(v)} for k, v in cats.items()]
                df_cats = pd.DataFrame(cat_counts)
                fig_pie = px.pie(df_cats, values='Count', names='Category', hole=0.7,
                                template='plotly_dark', color_discrete_sequence=px.colors.qualitative.Pastel)
                fig_pie.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                    margin=dict(l=0, r=0, t=10, b=10),
                    height=450, showlegend=False
                )
                fig_pie.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig_pie, use_container_width=True)

# ══════ TAB 3: ATS DASHBOARD ═════════════════════════════════════════════════
with t3:
    if not has_resume:
        st.warning("Upload a PDF resume in the sidebar to activate the ATS Dashboard.")
    else:
        st.markdown("### Applicant Tracking System (ATS) Scan")
        s_color = score_color(ra["match_score"])
        
        st.markdown(f"""
        <div class="card" style="display:flex; justify-content:space-between; align-items:center; border-left: 6px solid {s_color};">
            <div>
                <div style="color:var(--text-muted); font-weight:600; letter-spacing:0.05em; margin-bottom:8px;">OVERALL MATCH SCORE</div>
                <div style="font-size:3rem; font-weight:800; color:{s_color}; line-height:1;">{ra['match_score']:.1f}%</div>
            </div>
            <div style="text-align:right;">
                <div style="color:var(--text-muted); margin-bottom:8px;">Resume Parsed: <b>{ra['resume_source']}</b></div>
                <div style="display:flex; gap: 16px;">
                    <div><b style="color:#10b981;">{len(ra['matched_skills'])}</b> Hits</div>
                    <div><b style="color:#ef4444;">{len(ra['gap_skills'])}</b> Misses</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        
        with c1:
            st.markdown("#### ✅ ATS Hits (Matched Skills)")
            if ra["matched_skills"]:
                chips = "".join(f'<span class="chip-match">{s.title()}</span>' for s in ra["matched_skills"])
                st.markdown(f'<div>{chips}</div>', unsafe_allow_html=True)
            else:
                st.info("No matching high-demand skills found in this resume.")
                
        with c2:
            st.markdown("#### ❌ ATS Misses (Skill Gaps)")
            if ra["gap_skills"]:
                df_gaps = pd.DataFrame(ra["gap_skills"][:10])
                df_gaps['skill'] = df_gaps['skill'].str.title()
                
                # Plotly radar or bar chart for gaps
                fig = px.bar(df_gaps, x='frequency', y='skill', orientation='h',
                             color='demand_level',
                             color_discrete_map={"HIGH": "#ef4444", "MEDIUM": "#f59e0b", "LOW": "#10b981"},
                             template='plotly_dark', title="Top Missing Skills (By Market Demand)")
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                    yaxis={'categoryorder':'total ascending', 'title': ''}, xaxis={'title':'Demand Frequency'},
                    height=350, margin=dict(l=0, r=0, t=40, b=0)
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.success("No significant gaps found!")

# ══════ TAB 4: CAREER ROADMAP ════════════════════════════════════════════════
with t4:
    st.markdown("### Interactive Learning Roadmap")
    if plan.get("gap_driven"):
        st.info("🎯 This roadmap is dynamically generated to close your specific ATS misses.")
    
    st.markdown(f'<p style="color:var(--text-muted);">Recommended Commitment: <b>{hours_per_week}h / week</b></p>', unsafe_allow_html=True)
    
    for week in plan.get("weeks", []):
        st.markdown(f"""
        <div class="wk-card">
            <div class="wk-hdr">
                <div>
                    <div class="wk-num">WEEK {week['week_number']}</div>
                    <div class="wk-theme">{week['theme']}</div>
                </div>
                <div class="wk-hrs">{week['total_hours']} Hours</div>
            </div>
            <div style="margin-top: 16px;">
        """, unsafe_allow_html=True)
        
        for task in week["tasks"]:
            badge = '<span class="tk-gap">TARGET GAP</span>' if task.get("is_gap") else ""
            st.markdown(f"""
                <div class="tk-row">
                    <div class="tk-hrs">{task['hours']}h</div>
                    {badge}
                    <div class="tk-name">{task['skill'].title()}</div>
                    <div class="tk-plat">{task['platform']}</div>
                </div>
            """, unsafe_allow_html=True)
            
        st.markdown("</div></div>", unsafe_allow_html=True)

# ══════ TAB 5: INTERVIEW PREP ════════════════════════════════════════════════
with t5:
    st.markdown("### 🗣️ Technical Interview Simulator")
    st.markdown("Practice questions tailored to your gaps and role expectations.")
    
    # Generate mock questions based on top skills / gaps
    skills_to_test = []
    if ra and ra.get("gap_skills"):
        skills_to_test = [s['skill'].title() for s in ra["gap_skills"][:3]]
    elif top_skills:
        skills_to_test = [s['skill'].title() for s in top_skills[:3]]
        
    if skills_to_test:
        c1, c2 = st.columns([1, 2])
        test_skill = c1.radio("Select Topic", skills_to_test)
        
        with c2:
            st.markdown(f"#### Behavioral & Technical Prep: {test_skill}")
            
            with st.expander("Q1: Technical Overview", expanded=True):
                st.markdown(f"**How would you explain the core concepts of {test_skill} to a non-technical stakeholder?**")
                st.markdown("*Hint: Focus on business value, efficiency, and real-world analogies rather than deep technical jargon.*")
                st.text_area("Your Answer", height=100, key=f"q1_{test_skill}")
                
            with st.expander("Q2: Problem Solving"):
                st.markdown(f"**Describe a scenario where you had to troubleshoot a challenging issue related to {test_skill}. How did you resolve it?**")
                st.markdown("*Hint: Use the STAR method (Situation, Task, Action, Result).*")
                st.text_area("Your Answer", height=100, key=f"q2_{test_skill}")
                
            with st.expander("Q3: Market Context"):
                st.markdown(f"**Why do you think {test_skill} is currently in such high demand for {role_type} roles?**")
                st.markdown("*Hint: Mention scalability, modern architecture, or industry trends.*")
                st.text_area("Your Answer", height=100, key=f"q3_{test_skill}")
                
            st.button("Submit Answers & Get AI Feedback", type="primary")

    else:
        st.info("Run the pipeline first to generate interview questions.")

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("<br><hr>", unsafe_allow_html=True)
st.markdown("""<div style="text-align:center;padding:20px 0;font-size:0.85rem;color:var(--text-muted);font-weight:500;">
  CareerPilot AI Pro · Premium Dashboard<br>
  Built with Streamlit & Plotly
</div>""", unsafe_allow_html=True)
