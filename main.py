import constants
import response_body_generator
from scrape.scrape_chi_awe_org import ScrapeChiAWE
from get_image import get_image

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
"""
Setup the Streamlit app
Streamlit is the host for this app
The following code is based on this example https://blog.streamlit.io/langchain-tutorial-2-build-a-blog-outline-generator-app-in-25-lines-of-code/ 
The set_page_config method above needs to be at the top of the script to work properly. Even before any line comments.
"""
"""
Scrape all of the Chi-AWE websites to get the most relevant, up-to-date content.
"""
def scrape_all_websites():
    """
    Scrape all of the chi-AWE websites
    """
    scraped_text_dict = {}
    
    for website in constants.ALL_CHI_AWE_WEBSITES:
        scraper = ScrapeChiAWE(website)
        next_scrape = scraper.get_content()
        next_scrape_dict = dict(next_scrape)
        scraped_text_dict.update(next_scrape_dict)

    # with open(constants.SCRAPED_JSON, "w") as outfile:
    #    json.dump(scraped_text_dict, outfile)
    
    with open(constants.SCRAPED_TEXT,'w+') as f:
        f.write(str(scraped_text_dict))

def generate_image(openai_api_key, image_topics_string):
    response = get_image(openai_api_key, image_topics_string)
    return st.info(response)

def generate_response(openai_api_key, person, topic, ask, secondary_ask, initiative):
    generator = response_body_generator.ResponseBodyGenerator(openai_api_key, person, topic, ask, secondary_ask, initiative)
    response = generator.generate()
    return st.info(response)

openai_api_key = st.sidebar.text_input('OpenAI API Key', type='password')

with st.form('myform'):
  person = st.text_input('Provide a list of adjectives/pronouns describing the demographics of the target audience, ie: age, ethnicity, gender, occupation:', '')
  topic = st.text_input('What topic do you want to generate a blog post for? Topics include: pageantry, fashion, AAPI:', '')
  ask = st.text_input('What is the specific thing you want to ask of the blog post reader? Asks include: donate, volunteer, sponsor:', '')
  initiative = st.text_input('What specific chi-awe program/initiative/department are you asking the reader to support?:', '')
  secondary_ask = st.text_input('What is the secondary thing you would want to ask of the blog post reader if they cannot commit to the first ask? ie: attend an upcoming event, sign up for the email list')
  scrape_requested = st.form_submit_button('Scrape')
  image_requested = st.form_submit_button('Generate Image')
  blog_requested = st.form_submit_button('Request Blog')
  # Smoke test for whether the user is providing a valid OpenAi API Key
  if not openai_api_key.startswith('sk-'):
    st.warning('Please enter your OpenAI API key!', icon='⚠')
  if scrape_requested:
    scrape_all_websites()
  if image_requested:
    image_topics = [topic, initiative]
    image_topics_string = ''.join(image_topics)
    generate_image(openai_api_key, image_topics_string) 
  if blog_requested and openai_api_key.startswith('sk-'):
    generate_response(openai_api_key, person, topic, ask, secondary_ask, initiative)
    # os.remove(constants.SCRAPED_TEXT_FILENAME)

if __name__ == '__main__':
    scrape_all_websites()
