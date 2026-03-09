"""streamlit UI for the AI-powered credit bureau assistant.

run with: streamlit run app.py
"""

import json
import streamlit as st

from agent import CreditCheckAgent

# --- page config ---
st.set_page_config(
    page_title="AI Credit Bureau Assistant",
    layout="wide",
)

# --- session state ---
if "agent" not in st.session_state:
    st.session_state.agent = CreditCheckAgent()
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "tool_calls" not in st.session_state:
    st.session_state.tool_calls = []

# --- sidebar ---
with st.sidebar:
    st.title("Credit Bureau Assistant")
    st.caption("AI-powered credit analysis")
    st.divider()

    # tool call log
    if st.session_state.tool_calls:
        st.subheader("Tools Called")
        for i, tc in enumerate(st.session_state.tool_calls):
            with st.expander(f"{tc['tool']}", expanded=False):
                st.markdown("**Input:**")
                st.json(tc["input"])
                st.markdown("**Output:**")
                st.json(tc["output"])

    st.divider()

    if st.button("New Session", use_container_width=True):
        st.session_state.agent.reset()
        st.session_state.chat_history = []
        st.session_state.tool_calls = []
        st.rerun()

    st.divider()
    st.caption(
        "AI-assisted analysis only. This is not a credit decision. "
        "All data is synthetic."
    )

# --- main area ---
st.title("AI Credit Bureau Assistant")
st.markdown(
    "> Paste or type customer details below. The AI agent will extract the "
    "data, run the appropriate credit checks, and provide a summary."
)
st.markdown("---")

# --- disclaimer ---
st.info(
    "**Disclaimer:** This is an AI-assisted analysis tool. All outputs are "
    "advisory only and do not constitute a credit decision. All data shown "
    "is synthetic for demonstration purposes."
)

# --- chat history ---
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("tool_calls"):
            with st.expander("View tool calls and raw data", expanded=False):
                for tc in msg["tool_calls"]:
                    st.markdown(f"**{tc['tool']}**")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("*Input:*")
                        st.json(tc["input"])
                    with col2:
                        st.markdown("*Output:*")
                        st.json(tc["output"])


# --- chat input ---
if prompt := st.chat_input("Enter customer details or ask a question..."):
    # display user message
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # process through agent
    with st.chat_message("assistant"):
        with st.spinner("Analysing..."):
            try:
                result = st.session_state.agent.process_message(prompt)
            except Exception as e:
                result = {
                    "response": f"**Error:** {e}\n\nPlease check that your "
                    "ANTHROPIC_API_KEY is set in the .env file.",
                    "tool_calls": [],
                }

        st.markdown(result["response"])

        if result["tool_calls"]:
            with st.expander("View tool calls and raw data", expanded=False):
                for tc in result["tool_calls"]:
                    st.markdown(f"**{tc['tool']}**")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("*Input:*")
                        st.json(tc["input"])
                    with col2:
                        st.markdown("*Output:*")
                        st.json(tc["output"])

    # save to history
    st.session_state.chat_history.append(
        {
            "role": "assistant",
            "content": result["response"],
            "tool_calls": result["tool_calls"],
        }
    )

    # update sidebar tool calls
    st.session_state.tool_calls.extend(result["tool_calls"])