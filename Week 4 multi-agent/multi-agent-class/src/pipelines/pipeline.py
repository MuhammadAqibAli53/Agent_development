from pathlib import Path
import sys

# Allow running this file directly from the IDE or any working directory.
if __name__ == "__main__" and not __package__:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.agents.agents import build_search_agent, build_reader_agent, summarizer_chain, writer_chain, citation_chain, critic_chain

def run_research_pipeline(topic : str) -> dict:

    state = {}

    #search agent working 
    print("\n"+" ="*50)
    print("step 1 - search agent is working ...")
    print("="*50)

    search_agent = build_search_agent()
    search_result = search_agent.invoke({
        "messages" : [("user", f"Find recent, reliable and detailed information about: {topic}")]
    })
    state["search_results"] = search_result['messages'][-1].content

    print("\n search result ",state['search_results'])


    #step 2 - reader agent 
    print("\n"+" ="*50)
    print("step 2 - Reader agent is scraping top resources ...")
    print("="*50)

    reader_agent = build_reader_agent()
    reader_result = reader_agent.invoke({
        "messages": [("user",
            f"Based on the following search results about '{topic}', "
            f"pick the most relevant URL and scrape it for deeper content.\n\n"
            f"Search Results:\n{state['search_results']}"
        )]
    })

    state['scraped_content'] = reader_result['messages'][-1].content

    print("\nscraped content: \n", state['scraped_content'])


    # step 3 - summarizer chain
    print("\nstep 3 - Summarizer is condensing scraped content ...")
    state["summary"] = summarizer_chain.invoke({
        "topic": topic,
        "content": state["scraped_content"]
    })
    print("\nResearch summary\n", state["summary"])

    #step 4 - writer chain 

    print("\n"+" ="*50)
    print("step 4 - Writer is drafting the report ...")
    print("="*50)

    research_combined = (
        f"SEARCH RESULTS : \n {state['search_results']} \n\n"
        f"SUMMARIZED CONTENT : \n {state['summary']}"
    )

    state["report"] = writer_chain.invoke({
        "topic" : topic,
        "research" : research_combined
    })

    source_research = (
        f"SEARCH RESULTS:\n{state['search_results']}\n\n"
        f"SCRAPED CONTENT:\n{state['scraped_content']}"
    )

    # step 5 - citation agent
    print("\nstep 5 - Citation Agent is formatting references ...")
    state["citations"] = citation_chain.invoke({
        "research": source_research,
        "report": state["report"]
    })
    state["report"] += "\n\n" + state["citations"]

    print("\n Final Report\n",state['report'])


    #critic report 

    print("\n"+" ="*50)
    print("step 6 - critic is reviewing the report ")
    print("="*50)

    state["feedback"] = critic_chain.invoke({
        "report":state['report'],
        "research": source_research
    })

    print("\n critic report \n", state['feedback'])

    return state
