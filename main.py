import constants
import response_body_generator
from scrape.scrape_chi_awe_org import ScrapeChiAWE
from get_image import get_image
import prepare_text

import json

import streamlit as st

st.set_page_config(page_title="Chi-AWE Blog Post Generator App",
                   page_icon="chart_with_upwards_trend",
                   layout="wide",
                   initial_sidebar_state="expanded",
                   menu_items={
                      'Get Help': 'https://www.chi-awe.org/contact',
                      'Report a bug': 'https://www.chi-awe.org/contact',
                      'About': 'AI Hackathon project for Chi-AWE org. Source code here: https://github.com/victoriang555/chi-awe-blog-generator',
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

    with open(constants.SCRAPED_JSON, "w") as outfile:
       json.dump(scraped_text_dict, outfile)
    
    with open(constants.SCRAPED_TEXT,'w+') as f:
        f.write(str(scraped_text_dict))
    
    return st.info(scraped_text_dict)

def scrape_particular_website(website):
    scraper = ScrapeChiAWE(website)
    scraped_text_dict = scraper.get_content_for_specific_page(website)

def summarize_scraped_text(openai_api_key, filename):
    """Generate the paragraph that summarizes what the org does"""
    scraped_text = prepare_text.load_text(filename)
    texts = prepare_text.split_text(scraped_text=scraped_text)
    summary = prepare_text.docsearch(texts, openai_api_key)
    with open(constants.SCRAPED_PARTICULAR_WEBSITE, "w") as outfile:
       json.dump(scraped_text_dict, outfile)
    
    with open(constants.SCRAPED_TEXT,'w+') as f:
        f.write(str(scraped_text_dict))
    return st.info(summary)
    
def generate_org_summary(openai_api_key, webpage_url):
    """Generate the org summary paragraph"""
    # scraped_text = prepare_text.load_text(constants.SCRAPED_JSON, webpage_url)
    webpage_url_cleaned = webpage_url.replace("http://", "").replace("https://", "")
    scraped_text = prepare_text.load_json(constants.SCRAPED_PARTICULAR_WEBSITE,   webpage_url_cleaned)
    texts = prepare_text.split_text(scraped_text=scraped_text)
    docs = prepare_text.create_docs(texts)
    summarized_text = prepare_text.summarize(openai_api_key, docs)
    return st.info(summarized_text)
    
def generate_image(openai_api_key, image_topics_string):
    response = get_image(openai_api_key, image_topics_string)
    return st.info(response)

def generate_response(openai_api_key, person, topic, ask, secondary_ask, initiative, next_read, next_read_topics, alternative_read, alternative_read_topics):
    generator = response_body_generator.ResponseBodyGenerator(openai_api_key, person, topic, ask, secondary_ask, initiative, next_read, next_read_topics, alternative_read, alternative_read_topics)
    response = generator.generate()
    return st.info(response)

openai_api_key = st.sidebar.text_input('OpenAI API Key', type='password')

with st.form('myform'):
  person = st.text_input('Target Blog Post Reader Demographics - Provide a list of adjectives/pronouns describing the demographics of the target audience, ie: age, ethnicity, gender, occupation:', '')
  topic = st.text_input('Blog Post Topic - What topic do you want to generate a blog post for? Topics include: pageantry, fashion, AAPI:', '')
  ask = st.text_input('Primary Reader Ask - What is the specific thing you want to ask of the blog post reader? Asks include: donate, volunteer, sponsor:', '')
  initiative = st.text_input('Initiative - What specific chi-awe program/initiative/department are you asking the reader to support?:', '')
  secondary_ask = st.text_input('Secondary Reader Ask - What is the secondary thing you would want to ask of the blog post reader if they cannot commit to the first ask? ie: attend an upcoming event, sign up for the email list')
  next_read = st.text_input('Next Suggested Reading - What is the next page on the website or another chi-awe website you want to redirect the reader to once they are done reading this blog post?:', '')
  next_read_topics = st.text_input('Next Suggested Reading Keywords - Provide a list of the relevant topics of the next read:', '')
  alternative_read = st.text_input('Alternative Suggested Reading - What is an alternative webpage you want to redirect the reader to?', '')
  alternative_read_topics = st.text_input('Alternative Reading Keywords - Provide a list of the relevant topics of the alternative read:', '')
  particular_website_to_scrape = st.text_input('Webpage to Scrape - The full url of the Chi-AWE webpage we should scrape content from')
  scrape_requested = st.form_submit_button('Scrape')
  summary_requested = st.form_submit_button('Request Chi-AWE Summary')
  image_requested = st.form_submit_button('Generate Image')
  blog_requested = st.form_submit_button('Request Blog')
  org_summary_requested = st.form_submit_button('Request org summary')
  scrape_particular_webpage = st.form_submit_button("Scrape particular webpage")
  # Smoke test for whether the user is providing a valid OpenAi API Key
  if not openai_api_key.startswith('sk-'):
    st.warning('Please enter your OpenAI API key!', icon='⚠')
  if scrape_requested:
    scrape_all_websites()
  if summary_requested and openai_api_key.startswith('sk-'):
     summarize_scraped_text(openai_api_key, constants.SCRAPED_JSON)
  if image_requested:
    image_topics = [topic, initiative]
    image_topics_string = ''.join(image_topics)
    generate_image(openai_api_key, image_topics_string)
  if org_summary_requested:
     generate_org_summary(openai_api_key, particular_website_to_scrape) 
  if scrape_particular_webpage:
     scrape_particular_website(particular_website_to_scrape)
  if blog_requested and openai_api_key.startswith('sk-'):
    generate_response(openai_api_key, person, topic, ask, secondary_ask, initiative, next_read, next_read_topics, alternative_read, alternative_read_topics)
    # os.remove(constants.SCRAPED_TEXT_FILENAME)

if __name__ == '__main__':
    scrape_all_websites()
