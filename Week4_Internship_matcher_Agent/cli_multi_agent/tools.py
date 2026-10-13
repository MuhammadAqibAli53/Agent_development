from datetime import datetime
from pathlib import Path

from langchain.tools import tool
from langchain_tavily import TavilySearch


BASE_DIR = Path(__file__).resolve().parents[1]
RESUME_PATH = BASE_DIR / "resume.txt"


# Tool 1: Read the resume
@tool
def read_resume() -> dict:
    """Read the student's resume from resume.txt."""
    try:
        text = RESUME_PATH.read_text(encoding="utf-8-sig").strip()
        if not text:
            return {"error": "resume.txt is empty. Add your resume first."}
        return {"resume_text": text}
    except (OSError, UnicodeError):
        return {"error": "Cannot read resume.txt. Check its location and encoding."}


# Tool 2: Search for internships
@tool
def search_internships(query: str) -> dict:
    """Search internship listings using role and location, never personal details."""
    try:
        search = TavilySearch(
            max_results=5,
            topic="general",
            search_depth="basic",
            include_raw_content=True,
        )
        return search.invoke({"query": query})
    except Exception:
        return {"error": "Search failed. Check your Tavily key and connection."}


# Tool 3: Calculate the skill match

@tool
def match_skills(resume_skills: list[str], required_skills: list[str]) -> dict:
    """Compare resume skills with required skills and calculate a match percentage."""

    resume = {skill.strip().lower() for skill in resume_skills if skill.strip()}
    required = {skill.strip().lower() for skill in required_skills if skill.strip()}

    if not required:
        return {
            "match_percentage": None,
            "matched_skills": [],
            "missing_skills": [],
            "note": "No explicit required skills available; cannot calculate a score.",
        }

    matched = sorted(resume & required)
    missing = sorted(required - resume)
    score = round(len(matched) / len(required) * 100, 1)

    return {
        "match_percentage": score,
        "matched_skills": matched,
        "missing_skills": missing,
        "note": "Missing means not evidenced in the resume. Not a hiring probability.",
    }


# Tool 4: Save the final report
@tool
def save_shortlist(content: str) -> dict:
    """Save the internship report as a Markdown file."""
    if not content.strip():
        return {"error": "Cannot save an empty shortlist."}
    try:
        folder = BASE_DIR / "shortlists"
        folder.mkdir(exist_ok=True)
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        path = folder / f"internship_shortlist_{stamp}.md"
        path.write_text(content, encoding="utf-8")
        return {"saved_to": str(path)}
    except OSError:
        return {"error": "Could not save the shortlist. Check folder permissions."}
  