import constants
import response_body_generator
from main import scrape_all_websites

import os

import streamlit as st

"""
Setup the Streamlit app
"""
# Streamlit is the host for this app
# The following code is based on this example https://blog.streamlit.io/langchain-tutorial-2-build-a-blog-outline-generator-app-in-25-lines-of-code/ 
st.set_page_config(page_title ="Chi-AWE Blog Post Generator App")
st.title('Chi-AWE Blog Post Generator App')
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
