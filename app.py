import streamlit as st
import os
from langchain_groq import ChatGroq
from langchain_community.tools.tavily_search import TavilySearchResults

# --- 1. SETTINGS & BRANDING ---
st.set_page_config(page_title="Padosi AI", page_icon="🏠", layout="wide")

# SAHI LOGO LINK
LOGO_URL = "https://raw.githubusercontent.com/shivamverma55/padosi-AI/main/logo.png.png" 

# Custom CSS matching your Logo Colors (Navy Blue & Green)
st.markdown(f"""
    <style>
    .main {{ background-color: #f8f9fa; }}
    .stButton>button {{
        background-color: #32CD32; /* Lime Green from logo */
        color: white;
        border-radius: 8px;
        border: none;
        height: 3em;
        width: 100%;
        font-weight: bold;
    }}
    .stButton>button:hover {{ background-color: #002147; color: white; }}
    .report-card {{
        background-color: white;
        padding: 30px;
        border-radius: 15px;
        border-top: 10px solid #002147; /* Navy Blue from logo */
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
    }}
    [data-testid="stMetricValue"] {{ color: #002147; font-weight: bold; }}
    </style>
    """, unsafe_allow_html=True)

# --- 2. SIDEBAR ---
with st.sidebar:
    st.image(LOGO_URL, use_container_width=True)
    st.markdown("---")
    st.markdown("### 🛠️ Services")
    st.write("✅ Neighborhood Audit")
    st.write("✅ Safety Verification")
    st.write("✅ Future Growth Intel")
    st.markdown("---")
    st.info("Padosi AI helps you verify a locality before you buy your dream home.")

# --- 3. MAIN UI ---
st.title("🏙️ Padosi AI")
st.markdown("#### *Smart data for smarter home-buying decisions.*")

locality = st.text_input("Enter Locality Name (e.g. Rohini Sector 10, GK-2, Dwarka Sector 1):")

if st.button("Generate Intelligence Report"):
    if not locality:
        st.warning("Please enter a locality name.")
    else:
        with st.spinner(f"🕵️ Padosi AI is analyzing {locality}..."):
            try:
                # API Keys from Secrets
                os.environ["TAVILY_API_KEY"] = st.secrets["TAVILY_API_KEY"]
                os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]
                
                # AI Research
                search = TavilySearchResults(k=3)
                search_results = search.run(f"locality liveability report {locality} Delhi safety water aqi future infra")
                
                llm = ChatGroq(model_name="llama-3.3-70b-versatile", temperature=0)
                
                prompt = f"""
                You are a senior Real Estate Consultant. Based on: {search_results}
                Write a detailed report for {locality}, Delhi.
                
                Structure:
                1. EXECUTIVE SUMMARY (2 sentences)
                2. SCORECARD (Approximate scores out of 10 for Safety, Utilities, Connectivity, Future Growth)
                3. DETAILED ANALYSIS (Safety, Environment, Utility, Growth)
                4. PROS & CONS (Bullet points)
                5. EXPERT RECOMMENDATION
                """
                
                response = llm.invoke(prompt)
                
                # --- 4. DISPLAY RESULTS ---
                st.markdown("---")
                st.markdown(f"<div class='report-card'>", unsafe_allow_html=True)
                st.header(f"📍 Locality Intelligence: {locality}")
                
                # Professional Metrics Row
                m1, m2, m3, m4 = st.columns(4)
                m1.metric("🛡️ Safety", "7.5/10")
                m2.metric("🚇 Connectivity", "9.2/10")
                m3.metric("🌿 Environment", "6.4/10")
                m4.metric("📈 Growth", "8.0/10")
                
                st.markdown("---")
                st.markdown(response.content)
                st.markdown("</div>", unsafe_allow_html=True)
                
                # Call to Action
                st.markdown("### 📞 Interested in this locality?")
                col_btn1, col_btn2 = st.columns(2)
                with col_btn1:
                    st.button("Get Expert Legal Consultation")
                with col_btn2:
                    st.button("Download Full PDF Report (Premium)")
                    
            except Exception as e:
                st.error(f"Error: {e}")

st.markdown("---")
st.caption("© 2024 Padosi AI | Transparent Urban Intelligence")
