Creating Simple Langchain Agent
Some Conda Commands
Conda deactivate
conda remove -n simplelangagent --all -y     // to uninstall all packages from a conda environment
Start: 
1.	Create README.md file
2.	Open anaconda prompt and there run this command to create conda environment to install all dependencies into that environment.
conda create -n simplelangagent python=3.11 -y

3.	Now activate the environment
conda activate simplelangagent
4.	Now go to project root folder
cd /d "D:\UET Courses\Agent Based Modeling\Lecture Codes\Week3-Simple_Langchain_Agent"
5.	Now make requirements.txt in project in vscode and add all intallations in it. 
6.	Now in anaconda prompt run this command
pip install -r requirements.txt
7.	Add the environment to Jupyter. Since I am using VS Code/Jupyter notebooks:
python -m ipykernel install --user --name simplelangagent --display-name "simple_lang_agent"
8.	Now create a .env file in your project and add all API keys in it.
9.	Choose created environment kernal. 
10.	Start writing code
After Code writing, Now we will make a streamlit user interface for our code..
1.	For this first create a app.py file and copy all code into that. 
2.	Now generate streamlit interface via chatgpt.
3.	Now run streamlit from ur environment using anaconda. (streamlit was already installed as it was in my requirements.txt. if it is not there then first add it in requirements.txt and then install first)
4.	Go to anaconda and activate environment
conda activate simplelangagent
5.	Now go to project root folder
cd /d "D:\UET Courses\Agent Based Modeling\Lecture Codes\Week3-Simple_Langchain_Agent"

6.	Now run app using this command in anaconda
streamlit run app.py
Now upload project on github
1.	First of all, make .gitignore file in project. Because we dont want to expose our API keys publically.
2.	Now make a repository in github and then in that go to code and copy url. 
3.	Open anaconda, activate environment and go to project root path, now initialize git
git init
4.	Now check git status
git status
5.	Now add files to git using
git add . and check git status to see whether files added or not
Note: set these if not already done  before next step of commit git config --global user.name "Your Name"   and git config --global user.email "your-email@example.com"
6.	Now commit code to local git
git commit -m "Initial commit - LangChain agent"
7.	Now add this to remote gitrepositort created in github. And add copied url here
git remote add origin https://github.com/Amnawajid/First_Simple_Langchain_Agent.git
(to check connection run git remote -v)
8.	Change your branch from master to main
git branch -M main
9.	Push your project to GitHub
git push -u origin main
10.	Done
For future changes to add to git just run these 
git add .
git commit -m "description of change"
git push -u origin main




