import streamlit as st
import os
import re
from langchain_groq import ChatGroq
from langchain_community.tools.tavily_search import TavilySearchResults

st.set_page_config(page_title="Padosi AI", layout="wide")

# --- MODERN UI CSS ---
st.markdown("""
<style>
body {
    background-color: #f6f7fb;
}

/* HERO INPUT */
.hero {
    text-align: center;
    padding: 40px 0;
}

.hero h1 {
    font-size: 42px;
    font-weight: 700;
}

/* CARD */
.card {
    background: white;
    padding: 25px;
    border-radius: 16px;
    box-shadow: 0 8px 30px rgba(0,0,0,0.05);
    margin-top: 20px;
}

/* SCORE GRID */
.metric-box {
    text-align: center;
    padding: 15px;
    border-radius: 12px;
    background: #f1f3f8;
}

/* BUTTON */
.stButton>button {
    background: #000;
    color: white;
    border-radius: 10px;
    height: 3em;
    font-weight: bold;
}

.stButton>button:hover {
    background: #333;
}
</style>
""", unsafe_allow_html=True)

# --- HERO ---
st.markdown("<div class='hero'><h1>🏙️ Padosi AI</h1><p>Know your locality before you invest</p></div>", unsafe_allow_html=True)

locality = st.text_input("Enter locality (e.g. Dwarka Sector 21)")

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

# --- BUTTON ---
if st.button("Analyze Locality"):

    with st.spinner("Analyzing data..."):

        try:
            os.environ["TAVILY_API_KEY"] = st.secrets["TAVILY_API_KEY"]
            os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]

            search = TavilySearchResults(k=5)
            data = search.run(
                f"{locality} Delhi crime AQI metro connectivity infrastructure property trends"
            )

            llm = ChatGroq(model_name="llama-3.3-70b-versatile", temperature=0)

            prompt = f"""
You are a real estate analyst.

DATA:
{data}

STRICT FORMAT:

SCORECARD:
Safety: 7/10
Connectivity: 8/10
Environment: 6/10
Growth: 8/10

SUMMARY:
2 lines.

PROS:
-

CONS:
-

VERDICT:
"""

            response = llm.invoke(prompt)
            report = response.content

            scores = extract_scores(report)

            # --- RESULT CARD ---
            st.markdown("<div class='card'>", unsafe_allow_html=True)

            st.subheader(f"📍 {locality}")

            # SCORE GRID
            c1, c2, c3, c4 = st.columns(4)
            c1.markdown(f"<div class='metric-box'>🛡️<br><b>{scores['Safety']}</b><br>Safety</div>", unsafe_allow_html=True)
            c2.markdown(f"<div class='metric-box'>🚇<br><b>{scores['Connectivity']}</b><br>Connectivity</div>", unsafe_allow_html=True)
            c3.markdown(f"<div class='metric-box'>🌿<br><b>{scores['Environment']}</b><br>Environment</div>", unsafe_allow_html=True)
            c4.markdown(f"<div class='metric-box'>📈<br><b>{scores['Growth']}</b><br>Growth</div>", unsafe_allow_html=True)

            st.markdown("---")

            st.markdown(report)

            st.markdown("</div>", unsafe_allow_html=True)

        except Exception as e:
            st.error(e)
