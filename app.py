import streamlit as st
from langchain_groq import ChatGroq
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import AIMessage, HumanMessage
import os

st.set_page_config(page_title="Italy Study Advisor AI", page_icon="🇮🇹", layout="wide")

st.title("🇮🇹 Italy Study Advisor")
st.subheader("Your Personal AI Guide for Bachelor's & Master's in Italy")

# ===================== API KEYS =====================
os.environ["GROQ_API_KEY"] = "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"
os.environ["TAVILY_API_KEY"] = "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"

# ===================== LLM + TOOLS =====================
@st.cache_resource
def get_agent():
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.3, max_tokens=1024)

    search_tool = TavilySearchResults(max_results=4)

    tools = [search_tool]

    system_prompt = """You are an expert, friendly, and highly knowledgeable Italian Education Consultant.
    You help students (especially from India and other countries) apply for Bachelor's and Master's programs in Italy.

    Key topics you cover:
    - Top universities (Politecnico di Milano, University of Bologna, Sapienza Rome, Padova, etc.)
    - Application process, deadlines, required documents
    - Pre-enrollment on Universitaly portal
    - Student Visa (Type D) procedure
    - Scholarships (DSU, Invest Your Talent, university merit scholarships)
    - Cost of living, accommodation, part-time work
    - Student life & cultural adaptation tips
    - Personalized university & program recommendations

    Always be accurate. Use tools for latest deadlines. Give encouraging and practical advice."""

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    agent = create_tool_calling_agent(llm, tools, prompt)
    return AgentExecutor(agent=agent, tools=tools, verbose=False)

agent_executor = get_agent()

# ===================== SESSION =====================
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Namaste! 👋 I'm your dedicated Italy Study Advisor AI.\n\nHow can I help you today? You can ask about universities, applications, visas, scholarships, or get personalized recommendations."}
    ]

# ===================== CHAT UI =====================
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Type your question here... (e.g., Best universities for Computer Science in Italy)"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking... ⚡ Groq is fast"):
            response = agent_executor.invoke({
                "input": prompt,
                "chat_history": [
                    HumanMessage(content=m["content"]) if m["role"] == "user" else AIMessage(content=m["content"])
                    for m in st.session_state.messages[:-1]
                ]
            })
            answer = response["output"]
            st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})

# ===================== SIDEBAR =====================
with st.sidebar:
    st.header("🇮🇹 Quick Info")
    st.markdown("""
    **Top Universities (2026):**
    - Politecnico di Milano
    - University of Bologna
    - Sapienza University of Rome
    - University of Padova
    - Politecnico di Torino
    """)
    
    st.divider()
    st.markdown("**Useful Links**")
    st.markdown("[Universitaly Portal](https://www.universitaly.it)")
    st.markdown("[Study in Italy](https://studyinitaly.esteri.it)")
    st.markdown("[Visa Portal](https://vistoperitalia.esteri.it)")

    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

    st.caption("Powered by **Groq + Tavily**")
