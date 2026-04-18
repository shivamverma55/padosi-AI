import streamlit as st
import os
from langchain_groq import ChatGroq
from langchain_community.tools.tavily_search import TavilySearchResults

# --- 1. SETTINGS ---
st.set_page_config(page_title="Padosi AI", page_icon="🏠")

# --- 2. API KEYS (Secrets se uthayega) ---
try:
    os.environ["TAVILY_API_KEY"] = st.secrets["TAVILY_API_KEY"]
    os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]
except:
    st.error("API Keys missing in Streamlit Secrets!")

# --- 3. UI ---
st.markdown("### *Kahan ghar lena hai? Humse pucho!*")
st.write("Delhi's Neighborhood Intelligence Auditor")

locality = st.text_input("Enter Locality Name (e.g. Rohini, Dwarka, GK):")

if st.button("Generate Report"):
    if not locality:
        st.error("Please enter a locality!")
    else:
        with st.spinner(f"Searching data for {locality}..."):
            try:
                # Direct Search
                search = TavilySearchResults(k=3)
                search_results = search.run(f"liveability report {locality} Delhi safety water power aqi")
                
                # LLM Analysis (Groq)
                llm = ChatGroq(model_name="llama-3.3-70b-versatile", temperature=0)
                
                prompt = f"""
                You are an expert urban planner. Based on these search results:
                {search_results}
                
                Write a detailed liveability report for {locality}, Delhi.
                Include:
                - Overall Score (out of 10)
                - Safety
                - Environment (AQI)
                - Utility (Water/Power)
                - Future Growth
                """
                
                response = llm.invoke(prompt)
                st.success("Report Ready!")
                st.markdown(response.content)
                
            except Exception as e:
                st.error(f"Error during analysis: {e}")

st.caption("Padosi AI | Live Version")
# Report aane ke baad ye columns dikhao
col1, col2, col3 = st.columns(3)
col1.metric("Liveability Score", "7.8/10", "Good")
col2.metric("Safety Index", "8.5/10", "High")
col3.metric("Air Quality", "150 AQI", "-20", delta_color="inverse")
