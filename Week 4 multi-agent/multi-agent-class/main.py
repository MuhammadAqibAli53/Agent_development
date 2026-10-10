#### Code to test search tool  ####


#from src.tools.tools import web_search, scrape_url

# r=web_search.invoke("deep learning in healthcare")
# print(r)

#################################

#### Code to test scrape_url  tool  ####

# r=scrape_url.invoke("https://www.coursera.org/specializations/deep-learning-healthcare")
# print(r)

#################################


from src.pipelines.pipeline import run_research_pipeline


topic = "deep learning in healthcare"
run_research_pipeline(topic)