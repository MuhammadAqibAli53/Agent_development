"""The interface: collect input, show tool activity, and display the answer."""
import os
from pathlib import Path

import openai
import streamlit as st
from langgraph.errors import GraphRecursionError
from First_Simple_Langchain_Agent.internship_agent_cmd import build_agent

st.set_page_config(page_title="Internship Matcher", page_icon="🎓", layout="centered")
st.title("🎓 Internship Matcher")
st.write("Explore your skills, compare a job, or find internships. The agent chooses which tools to use.")

examples = {
    "1. Understand my resume": "Summarize the technical skills in my resume and suggest two suitable internship roles. Do not search the web or calculate a match score.",
    "2. Find and compare internships": "Find up to two current Python internships in Lahore, Pakistan. Compare their stated required skills with my resume and show matched skills, missing skills, and a match percentage when requirements are available.",
}

with st.sidebar:
    st.header("Three available tools")
    st.markdown("**Read resume** — your entered text\n\n**Web search** — current listings\n\n**Match skills** — a Python calculation")
    st.caption("Score = matched required skills ÷ total required skills × 100.")
    st.caption("Missing means not evidenced in the resume. It is not a hiring probability.")
    st.caption("Each request starts fresh. Your resume is sent to OpenAI only if the agent reads it.")

# Read the starter text for editing; this is UI setup, not an agent tool call.
resume_path = Path(__file__).resolve().parent / "resume.txt"
try:
    default_resume = resume_path.read_text(encoding="utf-8-sig") if resume_path.exists() else ""
except (OSError, UnicodeError):
    default_resume = ""

resume = st.text_area("Your resume — paste or edit plain text", value=default_resume, height=180)
choice = st.selectbox("Choose a demo, then edit the question if you like", list(examples))
question = st.text_area("Your question", value=examples[choice], key=choice, height=110)

if st.button("Ask agent", type="primary"):
    st.session_state.pop("answer", None)
    st.session_state["tools_used"] = []
    if not question.strip():
        st.warning("Enter a question first.")
    elif not os.getenv("OPENAI_API_KEY") or not os.getenv("TAVILY_API_KEY"):
        st.error("Add OPENAI_API_KEY and TAVILY_API_KEY to the .env file beside app.py.")
    else:
        with st.status("Waiting for OpenAI...", expanded=True) as status:
            try:
                agent = build_agent(resume)
                # These are actual agent events, not a predefined tool sequence.
                for update in agent.stream(
                    {"messages": [{"role": "user", "content": question}]},
                    config={"recursion_limit": 16}, stream_mode="updates",
                ):
                    for step in update.values():
                        for message in step.get("messages", []):
                            if message.type == "ai":
                                for call in message.tool_calls:
                                    st.write("Selected tool:", call["name"])
                                if not message.tool_calls and message.content:
                                    st.session_state["answer"] = message.content
                            elif message.type == "tool":
                                st.session_state["tools_used"].append(message.name)
                                st.write("Tool returned:", message.name)
                                if getattr(message, "status", "") == "error":
                                    st.warning("This tool returned an error; the agent will receive it.")
                                status.update(label="Waiting for OpenAI...")
                if st.session_state.get("answer"):
                    status.update(label="Answer ready", state="complete", expanded=False)
                else:
                    status.update(label="No final answer returned. Please try again.", state="error")
            except Exception as error:
                if isinstance(error, openai.AuthenticationError):
                    detail = "Check OPENAI_API_KEY in .env, then restart Streamlit."
                elif isinstance(error, openai.RateLimitError):
                    detail = "OpenAI rate limit or API quota reached. Check your API usage and billing."
                elif isinstance(error, openai.APIConnectionError):
                    detail = "OpenAI connection failed or timed out. Please try again later."
                elif isinstance(error, GraphRecursionError):
                    detail = "Step limit reached. Try a simpler question or one internship."
                else:
                    detail = f"Request failed ({type(error).__name__}). Check the API service and configuration."
                st.error(detail)
                status.update(label="Request stopped", state="error")

# Keep the completed answer visible when Download triggers a page rerun.
if st.session_state.get("answer"):
    st.subheader("Answer")
    st.markdown(st.session_state["answer"])
    used = st.session_state.get("tools_used", [])
    st.caption("Actual tool calls: " + (" → ".join(used) if used else "None — direct model answer"))
    st.download_button("Download answer", st.session_state["answer"], "internship_answer.md", "text/markdown")
