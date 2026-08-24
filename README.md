
Step-1:  Installation
conda create -n simplelangagent python=3.11 -y
conda activate simplelangagent
pip install -r requirements.txt
Configuration

Create a .env file at the repository root and add your API keys:

GENAI_API_KEY="your-openai-api-key"
TAVILY_API_KEY="your-tavily-api-key"
WEATHERSTACK_API_KEY="your-weatherstack-api-key"
Do not commit your .env file or secret keys to source control.

Run the Project
Use one of the Python entrypoints:

python app.py

Notebook Exploration
Open the  notebook for additional agent demos and experiments:
