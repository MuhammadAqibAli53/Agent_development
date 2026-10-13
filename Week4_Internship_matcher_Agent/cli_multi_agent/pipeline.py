
from dotenv import load_dotenv
import os
import certifi

from .agents import (
    build_model,
    build_resume_agent,
    build_search_matching_agent,
    build_report_agent
)

from .tools import BASE_DIR, read_resume, save_shortlist


# Gemini may return plain text or a list of content blocks.
def get_text(content):
    if isinstance(content, str):
        return content

    parts = []
    for block in content:
        if isinstance(block, str):
            parts.append(block)
        elif isinstance(block, dict) and block.get("type") == "text":
            parts.append(block.get("text", ""))
    return "\n".join(parts)


def run_internship_pipeline(request: str) -> dict:

    state = {}

    # Load API keys
    load_dotenv(BASE_DIR / ".env")
    os.environ.setdefault("SSL_CERT_FILE", certifi.where())

    llm = build_model()

    # Step 1 - Resume Analyzer Agent
    print("\n" + "="*50)
    print("Step 1 - Resume Analyzer Agent is working...")
    print("="*50)

    resume_agent = build_resume_agent(llm)

    resume_result = resume_agent.invoke({
        "messages": [("user",
            "Read my resume and extract my skills, education and projects."
        )]
    })

    state["profile"] = get_text(resume_result["messages"][-1].content)

    print("\nCandidate Profile:\n", state["profile"])


    # Step 2 - Internship Search and Matching Agent
    print("\n" + "="*50)
    print("Step 2 - Internship Search Agent is working...")
    print("="*50)

    search_agent = build_search_matching_agent(llm)

    search_result = search_agent.invoke({
        "messages": [("user",
            f"User Request:\n{request}\n\n"
            f"Candidate Profile:\n{state['profile']}\n\n"
            "Find suitable internships and match them with my skills."
        )]
    })

    state["matches"] = get_text(search_result["messages"][-1].content)

    print("\nInternship Matches:\n", state["matches"])


    # Step 3 - Career Advisor and Report Agent
    print("\n" + "="*50)
    print("Step 3 - Career Advisor Agent is working...")
    print("="*50)

    report_agent = build_report_agent(llm)

    report_result = report_agent.invoke({
        "messages": [("user",
            f"User Request:\n{request}\n\n"
            f"Candidate Profile:\n{state['profile']}\n\n"
            f"Internship Matches:\n{state['matches']}\n\n"
            "Create a final internship report with a short learning plan."
        )]
    })

    state["report"] = get_text(report_result["messages"][-1].content)

    print("\nFinal Internship Report:\n", state["report"])


    # Step 4 - Save Report
    print("\nStep 4 - Saving Report...")

    saved = save_shortlist.invoke({
        "content": state["report"]
    })

    if "error" in saved:
        state["save_error"] = saved["error"]
        return state

    state["saved_to"] = saved["saved_to"]

    print("\nReport saved to:", state["saved_to"])

    return state
