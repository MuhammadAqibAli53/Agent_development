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