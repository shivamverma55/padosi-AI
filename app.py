import streamlit as st
import os
from langchain_groq import ChatGroq
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.agents import create_react_agent, AgentExecutor
from langchain_core.prompts import PromptTemplate

# --- 1. SETTINGS & BRANDING ---
st.set_page_config(page_title="Padosi AI", page_icon="🏠")

# API Keys
os.environ["TAVILY_API_KEY"] = "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"
os.environ["GROQ_API_KEY"] = "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"

# UI
st.title("🏙️ Padosi AI")
st.write("Delhi Neighborhood Intelligence (Fixed Version)")

locality = st.text_input("Enter Locality Name (e.g. Rohini, Dwarka, GK):")

if st.button("Generate Report"):
    if not locality:
        st.error("Locality name toh daalo bhai!")
    else:
        with st.spinner("Analyzing data..."):
            try:
                # LLM Setup
                llm = ChatGroq(model_name="llama-3.3-70b-versatile", temperature=0)
                
                # Tools Setup
                search = TavilySearchResults(k=3)
                tools = [search]

                # Modern ReAct Prompt
                template = """Answer the following questions as best you can. You have access to the following tools:
                {tools}

                Use the following format:
                Question: the input question you must answer
                Thought: you should always think about what to do
                Action: the action to take, should be one of [{tool_names}]
                Action Input: the input to the action
                Observation: the result of the action
                ... (this Thought/Action/Action Input/Observation can repeat N times)
                Thought: I now know the final answer
                Final Answer: the final answer to the original input question

                Begin!
                Question: {input}
                Thought: {agent_scratchpad}"""

                prompt = PromptTemplate.from_template(template)

                # Create the Agent (Simplified)
                agent = create_react_agent(llm, tools, prompt)
                
                # Agent Executor
                agent_executor = AgentExecutor(
                    agent=agent, 
                    tools=tools, 
                    verbose=True, 
                    handle_parsing_errors=True
                )

                # Execution
                query = f"Provide a liveability report for {locality}, Delhi covering Safety, AQI, and Future Infra."
                result = agent_executor.invoke({"input": query})

                st.success("Report Ready!")
                st.markdown(result["output"])

            except Exception as e:
                st.error(f"Error logic: {e}")

st.caption("Padosi AI | Powered by Groq & Tavily")