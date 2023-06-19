import constants
import response_body_generator
from scrape.scrape_chi_awe_org import ScrapeChiAWE

import os
import json

from langchain import PromptTemplate, FewShotPromptTemplate 
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from langchain.llms import OpenAI
from dotenv import load_dotenv
from langchain.prompts.example_selector import LengthBasedExampleSelector
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import LLMChain, ConversationChain, SimpleSequentialChain
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain import PromptTemplate

import streamlit as st

st.set_page_config(page_title="Chi-AWE Blog Post Generator App",
                   page_icon="chart_with_upwards_trend",
                   layout="wide",
                   initial_sidebar_state="expanded",
                   menu_items={
                      'Get Help': 'https://www.chi-awe.org/contact',
                      'Report a bug': 'https://www.chi-awe.org/contact',
                      'About': 'AI Hackathon project for Chi-AWE org'
                   })

def scrape_all_websites():
    """
    Scrape all of the chi-AWE websites
    """
    scraped_text_dict = {}
    
    for website in constants.ALL_CHI_AWE_WEBSITES:
        scraper = ScrapeChiAWE(website)
        next_scrape = scraper.get_content()
        scraped_text_dict.update(next_scrape)
    
    # filename = "website_text.txt"
    with open(constants.SCRAPED_TEXT_FILENAME,'w+') as f:
        f.write(str(scraped_text_dict))

"""
Setup the Streamlit app
"""
# Streamlit is the host for this app
# The following code is based on this example https://blog.streamlit.io/langchain-tutorial-2-build-a-blog-outline-generator-app-in-25-lines-of-code/ 

# st.title('Chi-AWE Blog Post Generator App')
openai_api_key = st.sidebar.text_input('OpenAI API Key', type='password')

# def generate_response(person, topic):
#   llm = OpenAI(model_name=constants.MODEL_NAME, openai_api_key=openai_api_key)
#   # Prompt
#   template = 'As a AAPI woman interested in empowering other women and making friends in Chicagoland, generate a blog post about {topic}.'
#   prompt = PromptTemplate(input_variables=['person','topic'], template=template)
#   prompt_query = prompt.format(persoUsing a list of a few words, describe what type of person you are, ie: age, ethnicity, gender, occupation=person, topic=topic)
#   # Run LLM model and print out response
#   response = llm(prompt_query)
#   return st.info(response)

def generate_response(openai_api_key, person, topic):
    generator = response_body_generator.ResponseBodyGenerator(openai_api_key, person, topic)
    response = generator.generate()
    return st.info(response)

with st.form('myform'):
  person = st.text_input('Using a list of a few words, describe what type of person you are, ie: age, ethnicity, gender, occupation:', '')
  topic = st.text_input('What topic do you want to generate a blog post for? Topics include: pageantry, fashion, AAPI:', '')
  scrape_requested = st.form_submit_button('Scrape')
  blog_requested = st.form_submit_button('Request Blog')
  # Smoke test for whether the user is providing a valid OpenAi API Key
  if not openai_api_key.startswith('sk-'):
    st.warning('Please enter your OpenAI API key!', icon='⚠')
  if scrape_requested:
    scrape_all_websites()
  if blog_requested and openai_api_key.startswith('sk-'):
    generate_response(openai_api_key, person, topic)
    os.remove(constants.SCRAPED_TEXT_FILENAME)

if __name__ == '__main__':
    # scrape(constants.CHI_AWE_WEBSITE)
    scrape_all_websites()
