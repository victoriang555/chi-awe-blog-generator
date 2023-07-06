import constants
import response_body_generator
from scrape.scrape_chi_awe_org import ScrapeChiAWE
from scrape.scrape_chi_awe_org import scrape_all_canva_pages, scrape_specific_page
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

def scrape_all_websites():
    """
    Scrape all of the chi-AWE websites
    """
    scraped_text_dict = {}
    scraped_text_free = ""
    
    # Scrape 
    for website in constants.ALL_SQUARESPACE_WEBSITES:
        scraper = ScrapeChiAWE(website)
        next_scrape = scraper.get_content()
        next_scrape_free_text = scraper.get_content_free_text()
        next_scrape_dict = dict(next_scrape)
        scraped_text_dict.update(next_scrape_dict)
        scraped_text_free += next_scrape_free_text

    canva_website_scraped_text_dict, canva_website_scraped_text_free = scrape_all_canva_pages()
    scraped_text_free += canva_website_scraped_text_free
    scraped_text_dict.update(canva_website_scraped_text_dict)

    # Create json and text files specifically for the text for the org summary generation separately
    with open(constants.ORG_SUMMARY_SCRAPED_JSON, "w") as outfile:
       json.dump(canva_website_scraped_text_dict, outfile)
    with open(constants.ORG_SUMMARY_SCRAPED_TEXT,'w+') as f:
        f.write(str(canva_website_scraped_text_dict))

    # Create json and text files for all scraped text
    with open(constants.SCRAPED_JSON, "w") as outfile:
       json.dump(scraped_text_dict, outfile)
    
    with open(constants.SCRAPED_TEXT,'w+') as f:
        f.write(str(scraped_text_free))
    
    return st.info(scraped_text_dict)


openai_api_key = st.sidebar.text_input('OpenAI API Key', type='password')

with st.form('myform'):
  ###### Set user inputs in streamlit #######

  # Blog Post Inputs
  person = st.text_input('Target Blog Post Reader Demographics - Provide a list of adjectives/pronouns describing the demographics of the target audience, ie: age, ethnicity, gender, occupation:', '')
  
  topic = st.text_input('Blog Post Topic - What topic do you want to generate a blog post for? Topics include: pageantry, fashion, AAPI:', '')
  
  ask = st.text_input('Primary Reader Ask - What is the specific thing you want to ask of the blog post reader? Asks include: donate, volunteer, sponsor:', '')
  
  initiative = st.text_input('Initiative - What specific chi-awe program/initiative/department are you asking the reader to support?:', '')
  
  secondary_ask = st.text_input('Secondary Reader Ask - What is the secondary thing you would want to ask of the blog post reader if they cannot commit to the first ask? ie: attend an upcoming event, sign up for the email list')
  
  next_read = st.text_input('Next Suggested Reading - What is the next page on the chi-awe.org website you want to redirect the reader to once they are done reading this blog post?:', '')
  
  next_read_elements = st.text_input('Next Suggested Reading Page Sections - Provide a comma-separated list of the section names of the next read webpage. All items in the list should be prefixed with a hash. ie - #home, #page-1, #page-2:', '')
  
  alternative_read = st.text_input('Alternative Suggested Reading - What is an alternative chi-awe.org webpage you want to redirect the reader to?', '')
  
  alternative_read_elements = st.text_input('Alternative Suggested Reading Page Sections - Provide a comma-separated list of the section names of the alternative read webpage. All items in the list should be prefixed with a hash. ie - #home, #page-1, #page-2:', '')

  # Image Generator Inputs
  adj_of_image_type = st.text_input('Adjective for Image Type - What is the adjective you would use to describe the type of image? ie- beautiful, stunning, abstract, unique, retro, futuristic, surrealist:', '')
  
  type_of_image = st.text_input('Image Type - What type of image do you want to generate? ie- water color painting, oil painting, colored pencil sketch, black and white photo, 3d rendering, pencil sketch, pixel art:', '')

  adj_of_objects = st.text_input('Adjective of Objects - What adjectives (limit to 3) would you use to describe the objects in the image you want to generate? ie - cute, beautiful, unique, Asian-American, AAPI, gorgeous, stunning:', '')

  objects_in_image = st.text_input('Image Objects - What objects and/or types of people/animals do you want in the image? ie- women, dogs, community, basketball, gardening tools, food:', '')

  verb_of_objects = st.text_input('Verb of Objects - What is being done to the objects or what are the people/amimals doing? ie- volunteering, playing, working, protesting, cheering, supporting each other, doing nothing, relaxing:', '')

  # Streamlit buttons
  scrape_requested = st.form_submit_button('Re-Scrape All Chi-AWE Pages')
  image_requested = st.form_submit_button('Generate Image')
  blog_requested = st.form_submit_button('Generate Blog')
  org_summary_requested = st.form_submit_button('Generate org summary')

# Responses to user input through streamlit
  # Notify user if they need to use OpenAI API Key
  if not openai_api_key.startswith('sk-'):
    st.warning('Please enter your OpenAI API key!', icon='⚠')
  
  # Even though the service already scrapes upon loading and has scraped text saved in repo, user can request a re-scrape if they updated the website content
  if scrape_requested:
    scrape_all_websites()
  
  # Ensure user has provided all inputs before attempting to generate an image
  if image_requested and openai_api_key.startswith('sk-') and adj_of_image_type and type_of_image and adj_of_objects and    objects_in_image and verb_of_objects:
    response = get_image(openai_api_key, adj_of_image_type, type_of_image, adj_of_objects, objects_in_image, verb_of_objects)
    st.info(response)
  if org_summary_requested and openai_api_key.startswith('sk-'):
     summary = prepare_text.summarize_start_to_finish(constants.SCRAPED_TEXT, openai_api_key)
     st.info(summary)
    #  generate_org_summary(openai_api_key) 
  if blog_requested and openai_api_key.startswith('sk-'):
    # Generate a summary of Chi-AWE as an org
    org_summary = prepare_text.summarize_start_to_finish(constants.SCRAPED_TEXT, openai_api_key)

    # Scrape and summarize the suggested next read page content
    next_read_elements_list = next_read_elements.split(",")
    next_read_scraped_text = scrape_specific_page(next_read, next_read_elements_list)
    with open(constants.NEXT_READ_SCRAPED_TEXT,'w+') as f:
        f.write(next_read_scraped_text)
    next_read_summary = prepare_text.summarize_start_to_finish(constants.NEXT_READ_SCRAPED_TEXT, openai_api_key)

    # Scrape and summarize the suggested alternative read page content
    alternative_read_elements_list = alternative_read_elements.split(",")
    alternative_read_scraped_text = scrape_specific_page(alternative_read, alternative_read_elements_list)
    with open(constants.ALTERNATIVE_READ_SCRAPED_TEXT,'w+') as f:
        f.write(alternative_read_scraped_text)
    alternative_read_summary = prepare_text.summarize_start_to_finish(constants.ALTERNATIVE_READ_SCRAPED_TEXT, openai_api_key)

    # Generate the full blog
    generator = response_body_generator.ResponseBodyGenerator(openai_api_key, person, topic, ask, secondary_ask, initiative, next_read, alternative_read, org_summary, next_read_summary, alternative_read_summary)
    response = generator.generate()

    response["Chi-AWE Org Summary"] = org_summary
    st.info(response)

if __name__ == '__main__':
    scrape_all_websites()
    # scrape_all_pages()
