"""Run with: python -m streamlit run internship_multi_agent_streamlit.py"""
import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

from cli_multi_agent.pipeline import run_internship_pipeline
from cli_multi_agent.tools import BASE_DIR, read_resume


# 1. Page setup
st.set_page_config(page_title="Multi-Agent Internship Matcher", page_icon="🎓", layout="wide")
load_dotenv(BASE_DIR / ".env")

st.title("Multi-Agent Internship Matcher")
st.caption("Find internships, compare your skills, and get a practical learning plan.")

columns = st.columns(3)
with columns[0]:
    st.subheader("1. Resume Analyzer")
    st.write("Extracts your skills, education, and project experience.")
with columns[1]:
    st.subheader("2. Search & Matching")
    st.write("Finds internships and compares their requirements with your skills.")
with columns[2]:
    st.subheader("3. Career Advisor")
    st.write("Creates the final report and a learning plan for missing skills.")


# 2. Preview the same resume used by the CLI tools.
with st.sidebar:
    st.header("Setup")
    st.write("Edit `resume.txt` in the project folder to update your resume.")
    st.write("Add `GEMINI_API_KEY` and `TAVILY_API_KEY` to the project's `.env` file.")
    st.caption("The resume is sent to Gemini. Tavily receives search keywords.")

resume = read_resume.invoke({})
with st.expander("Preview resume.txt"):
    if "error" in resume:
        st.warning(resume["error"])
    else:
        st.text(resume["resume_text"])


# 3. Collect the request and run the existing pipeline.
with st.form("internship_request"):
    request = st.text_area(
        "What internships are you looking for?",
        value="Find up to 3 Python internships in Lahore, Pakistan, suitable for my resume. Show missing required skills and a short learning plan.",
        height=110,
    )
    submitted = st.form_submit_button("Find internships", type="primary")

if submitted:
    # Remove old results so a failed new run cannot display an old report.
    st.session_state.pop("internship_results", None)
    if not request.strip():
        st.error("Enter an internship role and location.")
    elif "error" in resume:
        st.error(resume["error"])
    elif not os.getenv("GEMINI_API_KEY") or not os.getenv("TAVILY_API_KEY"):
        st.error("Add GEMINI_API_KEY and TAVILY_API_KEY to your .env file, then restart the app.")
    else:
        try:
            with st.spinner("The three agents are analyzing your resume, searching, and writing your report..."):
                results = run_internship_pipeline(request.strip())
            if results.get("error"):
                st.error(results["error"])
            elif not results.get("report", "").strip():
                st.error("No report was returned. Please try again.")
            else:
                st.session_state.internship_results = results
        except Exception as exc:
            st.error(
                f"The pipeline could not finish ({type(exc).__name__}). "
                "Check your API keys, model access, quota, and connection, then retry."
            )


# 4. Keep the results visible when Streamlit reruns (for example on download).
if "internship_results" in st.session_state:
    results = st.session_state.internship_results
    st.success("Your internship report is ready.")

    with st.expander("Agent 1: Candidate profile"):
        st.markdown(results.get("profile", "No profile returned."))
    with st.expander("Agent 2: Internship matches"):
        st.markdown(results.get("matches", "No matches returned."))

    st.subheader("Agent 3: Final report & learning plan")
    st.markdown(results["report"])

    if results.get("save_error"):
        st.warning("Local save failed: " + results["save_error"] + " You can still download the report below.")
    elif results.get("saved_to"):
        st.caption("Saved locally: " + results["saved_to"])

    filename = Path(results.get("saved_to", "internship_shortlist.md")).name
    st.download_button(
        "Download report (.md)",
        data=results["report"],
        file_name=filename,
        mime="text/markdown",
    )
