import streamlit as st
from langchain_groq import ChatGroq
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import AIMessage, HumanMessage
import os

st.set_page_config(page_title="Italy Study Advisor AI", page_icon="🇮🇹", layout="wide")

st.title("🇮🇹 Italy Study Advisor")
st.subheader("Your Personal AI Guide for Studying in Italy")

# ===================== API KEYS =====================
os.environ["GROQ_API_KEY"] = st.secrets.get("GROQ_API_KEY", "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")
os.environ["TAVILY_API_KEY"] = st.secrets.get("TAVILY_API_KEY", "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")

# ===================== LLM + TOOL =====================
@st.cache_resource
def get_llm_and_tool():
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.3, max_tokens=1024)
    search_tool = TavilySearchResults(max_results=3)
    return llm, search_tool

llm, search_tool = get_llm_and_tool()

# ===================== SESSION STATE =====================
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Namaste! 👋 I'm your Italy Study Advisor AI.\n\nAsk me anything about Bachelor's/Master's programs, universities, visa, scholarships, or get personalized recommendations."}
    ]

# ===================== CHAT UI =====================
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask anything about studying in Italy..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking... ⚡"):
            # Simple but effective agent-like behavior
            tool_result = ""
            if any(kw in prompt.lower() for kw in ["deadline", "latest", "current", "2026", "visa", "scholarship"]):
                tool_result = search_tool.invoke(prompt)
                context = f"\n\nLatest information from web:\n{tool_result}"
            else:
                context = ""

            full_prompt = f"""You are an expert Italy Education Consultant.
            {context}

            User Question: {prompt}
            Give a clear, helpful, and encouraging answer."""

            response = llm.invoke(full_prompt)
            answer = response.content
            
            st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})

# ===================== SIDEBAR =====================
with st.sidebar:
    st.header("🇮🇹 Quick Links")
    st.markdown("""
    - [Universitaly](https://www.universitaly.it)
    - [Study in Italy](https://studyinitaly.esteri.it)
    - [Visa Info](https://vistoperitalia.esteri.it)
    """)
    
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    st.caption("Powered by Groq + Tavily")
