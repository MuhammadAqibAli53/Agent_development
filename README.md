# AI Agent Development
### Tool-using agents · Multi-agent orchestration · Applied GenAI

A collection of Python projects that investigate how language-model agents reason over tasks, call external tools, retrieve information, and return structured, actionable outputs.

**Skills demonstrated:** Python · LangChain/LangGraph · LLM Orchestration · Tool Calling · Multi-Agent Design · Streamlit · Search Integration

## Featured engineering work

### 1. Internship Matching Agent
A Streamlit application that reads user-provided resume text, researches matching internship opportunities, and compares documented skills with job requirements.

- **Tools:** resume reader, online search, and deterministic skill matcher.
- **Skills shown:** agent tool design, typed outputs, external API integration, transparent scoring, and UI state management.
- **Design detail:** Required-skill overlap is calculated in Python; it is **not** presented as a hiring probability.
- **Implementations:** `Simple_langchain_agent/` and `Week4_Internship_matcher_Agent/`.

### 2. Multi-Agent Research System
A research workflow with complementary responsibilities:
```text
Topic -> Search -> Reader -> Summarizer -> Writer -> Citation -> Critic
```
- Combines online research and text processing into a report-generation pipeline.
- Includes citation deduplication and a critic with separate accuracy, completeness, clarity, and organization assessments.
- Uses Tavily and optional DuckDuckGo search paths as documented in the subproject.
- See `Week 4 multi-agent/multi-agent-class/`.

### 3. Multi-Agent Coursework
Additional applications and experiments under `Week 4 multi-agent/` explore multiple specialist roles and their coordination.

## Design principles practiced
| Engineering concern | Approach |
|---|---|
| External information | Tool-based web search rather than relying only on model memory |
| Deterministic calculations | Python skill comparison instead of LLM-invented percentages |
| Composable workflows | Separate responsibilities across agents/chains |
| User experience | Streamlit interfaces around the agent pipelines |
| API secrets | Environment variables instead of hard-coded credentials |
| Source quality | Citation handling and critique stages in the research project |

## Technologies
Python, LangChain, LangGraph, Streamlit, OpenAI/Gemini model integrations, Tavily, Groq (depending on subproject).

## How to explore
Each subdirectory is an **independent assignment or application** with its own dependencies and setup. Open the relevant folder and follow its README. Some applications require provider API keys, including `OPENAI_API_KEY`, `GEMINI_API_KEY`, and `TAVILY_API_KEY`.

## Scope
These are educational implementations and prototypes; live service availability, accuracy, and production-readiness have not been independently certified.

**Maintained by [Muhammad Aqib Ali](https://github.com/MuhammadAqibAli53).**
