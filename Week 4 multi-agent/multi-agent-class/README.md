# Week4-Multi_Agent_ResearchSystem_Langchain
A powerful multi-agent research system built with LangChain that autonomously researches topics, gathers information, writes comprehensive reports, and evaluates their quality using AI-powered agents.
# 1- create and Clone the repository
Fisrt of all, create a repository at github and then copy code url and clone it in vs code.
For cloning open root folder in anaconda and write 
git clone https://github.com/Amnawajid/Week4-Multi_Agent_ResearchSystem_Langchain.git
Now go to project folder
 cd Week4-Multi_Agent_ResearchSystem_Langchain

# 2- Create Environment (Conda)
conda create -n multi_agent_langchain python=3.11 -y
conda activate multi_agent_langchain

# 3- Install Dependencies
pip install -r requirements.txt

# 4 preapare all folders in project
and commit changes in git hub for that run
$ git add . 
$ git commit -m "project setup and folders created"
$ git push origin main

# 5  Configure Environment Variables
Create a .env file in the project root:

add api keys i used Groq https://console.groq.com/keys and tavily

Now write tools code and check it... 

now write agents code

## Research workflow
Search Agent (Tavily / DuckDuckGo) -> Reader Agent -> Summarizer Chain -> Writer Chain -> Citation Agent -> Critic Chain.

The Citation Agent uses `citation_chain` in `src/agents/agents.py` to extract
references from the research sources cited in the report. It removes duplicate
URLs and formats a numbered References section without inventing missing metadata.
Both `main.py` and the Streamlit app run this step before the critic. References
are included in the final report and its Markdown download.

The Search Agent chooses between `web_search` (Tavily) and `duckduckgo_search`
(DuckDuckGo through the `ddgs` package). Tavily needs `TAVILY_API_KEY`;
DuckDuckGo does not need an API key. If one provider fails, the agent can try
the other. Neither provider is guaranteed to return results.

The Summarizer Chain condenses the Reader's scraped content before the Writer,
preserving source URLs, key facts, and limitations. The app also displays this
summary in an expandable panel. Original research is retained for citations
and review.

The Critic gives separate scores out of 10 for **accuracy**, **completeness**,
**clarity**, and **organization**, with a justification for each, strengths,
improvements, and a verdict. Accuracy is assessed against the supplied research.

## Run the completed assignment
From this project directory, install the updated dependencies and launch:

```bash
pip install -r requirements.txt
python main.py
python -m streamlit run app.py
```

Configure `GEMINI_API_KEY` (or `GOOGLE_API_KEY`) for the Gemini model and
`TAVILY_API_KEY` for Tavily in your local `.env` file.
