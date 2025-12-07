import streamlit as st
import pandas as pd
import plotly.express as px
from database import init_db, read_jobs_df, add_job_to_db, count_skills

# ---------------------------
# Streamlit Page Config
# ---------------------------
st.set_page_config(page_title="Job Skills Analyzer 💼", page_icon="💜", layout="wide")

# ---------------------------
# Custom CSS (Fixed Sidebar Button)
# ---------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');

html, body, [class*="st-"], .main {
    font-family: 'Poppins', sans-serif;
    background-color: #F7F8FF;
}

/* Hide sidebar collapse button completely */
button[kind="header"] {
    display: none !important;
}

/* Alternative: Style it if you want to keep it */
button[kind="header"] {
    background-color: transparent !important;
    border: none !important;
    color: #6C63FF !important;
}

button[kind="header"]:hover {
    background-color: #f1f0ff !important;
}

/* Hide material icon text */
span[data-testid="stHeaderActionElements"] span {
    display: none !important;
}

/* Hide any keyboard arrow text */
span[class*="material-icons"] {
    font-size: 0 !important;
}

span[class*="material-icons"]::before {
    content: "☰";
    font-size: 20px;
    font-family: 'Poppins', sans-serif;
}

/* Remove default grey divider */
div[data-testid="stSidebar"] {
    border-right: none !important;
    position: relative;
    background-color: #FAFBFF;
}

/* Add clean thin divider */
div[data-testid="stSidebar"]::after {
    content: "";
    position: absolute;
    top: 0;
    right: 0;
    width: 2px;
    height: 100%;
    background: linear-gradient(180deg, #e5e5f7 0%, #d5d5f7 100%);
    border-radius: 10px;
}

/* Sidebar text + hover */
[data-testid="stSidebar"] label, 
[data-testid="stSidebar"] p, 
[data-testid="stSidebar"] h1 {
    color: #333 !important;
}

[data-testid="stSidebar"] [role="radiogroup"] > div {
    transition: all 0.2s ease;
    padding: 8px;
    border-radius: 8px;
}

[data-testid="stSidebar"] [role="radiogroup"] > div:hover {
    background-color: #f1f0ff;
    transform: translateX(3px);
}

/* Gradient Header */
h1 {
    background: linear-gradient(90deg, #6C63FF 0%, #836FFF 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-weight: 800;
    text-align: center;
    margin-bottom: 10px;
}

h2, h3 { 
    color: #4A46D5;
    font-weight: 600;
}

/* Cards */
.card {
    background-color: white;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    transition: 0.3s;
    margin-bottom: 15px;
}

.card:hover {
    box-shadow: 0 6px 20px rgba(108,99,255,0.25);
    transform: translateY(-2px);
}

/* Metrics */
[data-testid="stMetric"] {
    background-color: white;
    border-radius: 12px;
    padding: 15px;
    box-shadow: 0px 4px 12px rgba(108,99,255,0.1);
}

[data-testid="stMetric"] label {
    color: #666 !important;
    font-weight: 600;
}

[data-testid="stMetric"] [data-testid="stMetricValue"] {
    color: #6C63FF;
    font-weight: 700;
}

/* Buttons */
.stButton>button {
    background: linear-gradient(90deg, #6C63FF, #836FFF);
    color: white;
    border-radius: 10px;
    border: none;
    height: 3em;
    font-weight: 600;
    font-size: 16px;
    transition: all 0.3s ease;
    width: 100%;
}

.stButton>button:hover {
    transform: translateY(-2px);
    box-shadow: 0px 4px 15px rgba(108,99,255,0.3);
}

/* Text Inputs */
.stTextInput input, .stTextArea textarea {
    border-radius: 8px;
    border: 2px solid #e5e5f7;
    transition: border-color 0.3s ease;
}

.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: #6C63FF;
    box-shadow: 0 0 0 2px rgba(108,99,255,0.1);
}

/* Hide Streamlit branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ---------------------------
# Header
# ---------------------------
st.markdown("<h1>💼 Job Skills Analyzer</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#555; font-size: 1.1rem;'>Analyze, Add, and Visualize Job Skill Trends</p>", unsafe_allow_html=True)
st.markdown("<hr style='border: none; height: 2px; background: linear-gradient(90deg, transparent, #6C63FF, transparent); margin: 20px 0;'>", unsafe_allow_html=True)

# ---------------------------
# Sidebar
# ---------------------------
with st.sidebar:
    st.markdown("<div style='text-align: center; padding: 20px 0;'>", unsafe_allow_html=True)
    st.image("https://cdn-icons-png.flaticon.com/512/993/993685.png", width=100)
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.title("Navigation 🧭")

    menu = st.radio("Go to:", ["📊 Analyze Skills", "➕ Add Job", "📋 View Jobs"], label_visibility="collapsed")

    st.markdown("---")
    st.info("💡 Empowering you to discover what skills matter most!")
    st.markdown("<p style='text-align:center; color:#999; font-size: 0.85rem; margin-top: 20px;'>Made with 💜 by Akriti Bhardwaj</p>", unsafe_allow_html=True)

# ---------------------------
# Init DB
# ---------------------------
init_db()

# ---------------------------
# Pages
# ---------------------------
if menu == "➕ Add Job":
    st.header("Add a New Job Posting")
    
    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_html=True)

        with st.form("add_job_form", clear_on_submit=True):
            title = st.text_input("Job Title", placeholder="e.g., Senior Data Analyst")
            col1, col2 = st.columns(2)
            company = col1.text_input("Company Name", placeholder="e.g., Google")
            location = col2.text_input("Location", placeholder="e.g., Remote")
            description = st.text_area("Job Description", height=200, placeholder="Enter the full job description here...")
            submitted = st.form_submit_button("✨ Add Job")

            if submitted:
                if not title.strip():
                    st.warning("⚠️ Please enter a job title.")
                elif not description.strip():
                    st.warning("⚠️ Please enter a job description.")
                else:
                    add_job_to_db(title, company, location, description)
                    st.success("✅ Job added successfully!")
                    st.balloons()

        st.markdown("</div>", unsafe_allow_html=True)

elif menu == "📋 View Jobs":
    st.header("All Job Postings")
    df = read_jobs_df()

    search_term = st.text_input("🔍 Search by title, company, or description:", placeholder="Type to search...")

    if search_term:
        mask = (
            df['title'].str.contains(search_term, case=False, na=False) |
            df['company'].str.contains(search_term, case=False, na=False) |
            df['job_description'].str.contains(search_term, case=False, na=False)
        )
        df_filtered = df[mask]
    else:
        df_filtered = df

    st.markdown(f"<p style='color:#666; margin: 10px 0;'>Showing <b>{len(df_filtered)}</b> of <b>{len(df)}</b> jobs</p>", unsafe_allow_html=True)

    if not df_filtered.empty:
        for _, row in df_filtered.iterrows():
            st.markdown(f"""
            <div class='card'>
                <h3 style='color:#6C63FF; margin-bottom: 8px;'>{row['title']}</h3>
                <p style='color:#666; font-size: 0.95rem; margin-bottom: 12px;'>
                    <b>🏢 {row['company']}</b> · 📍 {row['location']}
                </p>
                <p style='color:#333; line-height: 1.6;'>{row['job_description'][:300]}{'...' if len(row['job_description']) > 300 else ''}</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("🔍 No jobs found matching your criteria!")

elif menu == "📊 Analyze Skills":
    st.header("Skill Frequency Analysis")
    df = read_jobs_df()

    st.markdown("### 📈 Key Metrics")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Jobs Analyzed", len(df), delta="📊")
    top_skill_placeholder = col2.empty()
    avg_placeholder = col3.empty()

    st.markdown("---")
    st.markdown("### ⚙️ Select Skills to Analyze")

    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        skill_input = st.text_area(
            "Enter skills (comma-separated):",
            "Python, SQL, Excel, Tableau, Power BI, Machine Learning, HTML, JavaScript, pandas, React, AWS, Azure",
            height=100
        )
        st.markdown("</div>", unsafe_allow_html=True)

    user_skills = [s.strip() for s in skill_input.split(",") if s.strip()]

    if df.empty:
        st.info("📭 No jobs in database. Please add some jobs first.")
    else:
        skill_df = count_skills(df, user_skills)

        if not skill_df.empty and skill_df["Count"].sum() > 0:
            top_skill_placeholder.metric("Top Skill", skill_df.iloc[0]["Skill"], delta="🏆")
            avg_placeholder.metric("Avg. Skills / Job", f"{skill_df['Count'].sum() / len(df):.2f}", delta="📊")

            st.subheader("📊 Skill Frequency Chart")

            fig = px.bar(
                skill_df, x="Skill", y="Count", text="Count",
                color="Count", color_continuous_scale="Purp",
                title="Most In-Demand Skills"
            )

            fig.update_traces(textposition="outside", marker_line_width=0)
            fig.update_layout(
                showlegend=False, 
                font_family="Poppins",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                title_font_size=20,
                title_font_color='#4A46D5',
                xaxis_title="Skills",
                yaxis_title="Frequency"
            )

            st.plotly_chart(fig, use_container_width=True)
            
            # Show data table
            with st.expander("📋 View Detailed Data"):
                st.dataframe(skill_df, use_container_width=True)
        else:
            st.info("🔍 No skills detected in job descriptions. Try adding jobs or modifying your skill list.")