import streamlit as st
import os
import re
from langchain_groq import ChatGroq
from langchain_community.tools.tavily_search import TavilySearchResults

# --- CONFIG ---
st.set_page_config(page_title="Padosi AI", page_icon="🏠", layout="wide")

LOGO_URL = "https://raw.githubusercontent.com/shivamverma55/padosi-AI/main/logo.png.png"

# --- STYLE ---
st.markdown("""
<style>
.main { background-color: #f5f7fa; }

.stButton>button {
    background-color: #32CD32;
    color: white;
    border-radius: 10px;
    height: 3em;
    font-weight: bold;
}

.stButton>button:hover {
    background-color: #002147;
}

.report-card {
    background-color: white;
    padding: 30px;
    border-radius: 15px;
    border-top: 8px solid #002147;
    box-shadow: 0 10px 25px rgba(0,0,0,0.08);
}
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.image(LOGO_URL, use_container_width=True)
    st.markdown("### 🛠️ Services")
    st.write("✅ Neighborhood Audit")
    st.write("✅ Safety Check")
    st.write("✅ Growth Insights")

# --- TITLE ---
st.title("🏙️ Padosi AI")
st.caption("Smart data for smarter property decisions")

locality = st.text_input("Enter Locality")

# --- SCORE EXTRACTOR ---
def extract_scores(text):
    scores = {"Safety": "-", "Connectivity": "-", "Environment": "-", "Growth": "-"}

    patterns = {
        "Safety": r"Safety[:\s\-]*([0-9]+\/10)",
        "Connectivity": r"Connectivity[:\s\-]*([0-9]+\/10)",
        "Environment": r"Environment[:\s\-]*([0-9]+\/10)",
        "Growth": r"Growth[:\s\-]*([0-9]+\/10)"
    }

    for key in scores:
        match = re.search(patterns[key], text, re.IGNORECASE)
        if match:
            scores[key] = match.group(1)

    return scores

# --- MAIN BUTTON ---
if st.button("Generate Report"):
    if not locality:
        st.warning("Enter locality name first")
    else:
        with st.spinner("Analyzing locality..."):

            try:
                os.environ["TAVILY_API_KEY"] = st.secrets["TAVILY_API_KEY"]
                os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]

                # --- SEARCH ---
                search = TavilySearchResults(k=5)
                search_data = search.run(
                    f"{locality} Delhi crime safety AQI water supply metro connectivity infrastructure future development"
                )

                # --- LLM ---
                llm = ChatGroq(
                    model_name="llama-3.3-70b-versatile",
                    temperature=0
                )

                # --- STRICT PROMPT ---
                prompt = f"""
You are a strict real estate analyst.

RAW DATA:
{search_data}

IMPORTANT:
Return output EXACTLY in this format. Do NOT change format.

SCORECARD:
Safety: 7/10
Connectivity: 8/10
Environment: 6/10
Growth: 8/10

EXECUTIVE SUMMARY:
Write 2 lines only.

DETAILED ANALYSIS:
- Safety:
- Connectivity:
- Environment:
- Growth:

PROS:
- Point 1
- Point 2

CONS:
- Point 1
- Point 2

FINAL VERDICT:
Clear yes or no with reason.
"""

                response = llm.invoke(prompt)
                report = response.content

                scores = extract_scores(report)

                # --- OUTPUT ---
                st.markdown("---")
                st.markdown("<div class='report-card'>", unsafe_allow_html=True)

                st.header(f"📍 {locality}")

                col1, col2, col3, col4 = st.columns(4)
                col1.metric("🛡️ Safety", scores["Safety"])
                col2.metric("🚇 Connectivity", scores["Connectivity"])
                col3.metric("🌿 Environment", scores["Environment"])
                col4.metric("📈 Growth", scores["Growth"])

                st.markdown("---")
                st.markdown(report)

                st.markdown("</div>", unsafe_allow_html=True)

                # DEBUG (remove later)
                with st.expander("🔍 Debug Output"):
                    st.write(report)

            except Exception as e:
                st.error(f"Error: {e}")

st.markdown("---")
st.caption("© Padosi AI")
