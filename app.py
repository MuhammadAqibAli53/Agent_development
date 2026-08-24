import os
import certifi
import requests
import streamlit as st

from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.tools import tool
from langchain.agents import create_agent


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="AI Agent",
    page_icon="🤖",
    layout="centered"
)


# ==========================================
# LOAD ENV VARIABLES
# ==========================================

os.environ["SSL_CERT_FILE"] = certifi.where()

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
WEATHERSTACK_API_KEY = os.getenv("WEATHERSTACK_API_KEY")


# ==========================================
# CHECK API KEYS
# ==========================================

if not GEMINI_API_KEY:
    st.error("GEMINI_API_KEY is missing from your .env file.")
    st.stop()

if not TAVILY_API_KEY:
    st.error("TAVILY_API_KEY is missing from your .env file.")
    st.stop()

if not WEATHERSTACK_API_KEY:
    st.error("WEATHERSTACK_API_KEY is missing from your .env file.")
    st.stop()


# ==========================================
# SEARCH TOOL
# ==========================================

search_tool = TavilySearchResults(
    max_results=2
)


# ==========================================
# WEATHER TOOL
# ==========================================

@tool
def get_weather_data(city: str) -> str:
    """
    Fetch current weather information for a city.
    """

    url = (
        f"https://api.weatherstack.com/current?"
        f"access_key={WEATHERSTACK_API_KEY}&query={city}"
    )

    response = requests.get(url)

    data = response.json()

    if "current" not in data:
        return f"Could not fetch weather data for {city}"

    return (
        f"City: {city}\n"
        f"Temperature: {data['current']['temperature']}°C\n"
        f"Weather: {data['current']['weather_descriptions'][0]}\n"
        f"Humidity: {data['current']['humidity']}%"
    )


# ==========================================
# LLM
# ==========================================

llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    google_api_key=GEMINI_API_KEY
)


# ==========================================
# TOOLS
# ==========================================

tools = [
    search_tool,
    get_weather_data
]


# ==========================================
# SYSTEM PROMPT
# ==========================================

system_prompt = """
You are a helpful AI assistant.

You have access to:

1. A web search tool for current information.
2. A weather tool for current weather information.

Use the weather tool when the user asks about weather.

Use the search tool when current information is needed.

Answer the user clearly and concisely.
"""


# ==========================================
# CREATE AGENT
# ==========================================

agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt=system_prompt
)


# ==========================================
# STREAMLIT USER INTERFACE
# ==========================================

st.title("🤖 AI Agent")

st.write(
    "Ask me a question. I can search the web and retrieve current weather information."
)


# ==========================================
# USER INPUT
# ==========================================

question = st.text_input(
    "Enter your question:",
    placeholder="e.g., Find the capital of Pakistan and then find its current weather."
)


# ==========================================
# ASK AGENT
# ==========================================

if st.button("Ask Agent"):

    if not question:
        st.warning("Please enter a question.")
    
    else:

        with st.spinner("🤔 Agent is thinking..."):

            try:

                response = agent.invoke({
                    "messages": [
                        {
                            "role": "user",
                            "content": question
                        }
                    ]
                })

                final_response = response["messages"][-1].content

                st.subheader("🤖 Agent Response")

                st.write(final_response)

            except Exception as e:

                st.error(f"An error occurred: {e}")