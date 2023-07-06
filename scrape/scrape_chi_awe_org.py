
import requests
from bs4 import BeautifulSoup
import time
from requests_html import HTMLSession
import constants


session = HTMLSession()

def scrape_all_canva_pages():
  all_page_text_free = ""
  all_page_text_dict = {}
  for page, page_elements in constants.CANVA_CHI_AWE_PAGES.items():
    page_text = scrape_specific_page(page, page_elements)
    all_page_text_free += page_text
    all_page_text_dict[page] = [page_text]

  return all_page_text_dict, all_page_text_free

def scrape_specific_page(page, page_elements):
  page_text = ""
  r = session.get(page)
  for element in page_elements:
    section = r.html.find(element, first=True)
    page_text+=section.text
  return page_text

class ScrapeChiAWE:
  """Can be used to scrape websites that are hosted by Squarespace"""
  def __init__(self, base_url) -> None:
    self.base_url = base_url

  def get_embedded_hyperlinks(self):
    # make request to the base website
    response = requests.get(self.base_url)

    # Create a BeautifulSoup object to parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all anchor tags containing hyperlinks
    anchors = soup.find_all('a')

    # Extract the hyperlink and associated text
    embedded_hyperlinks_list = []
    for anchor in anchors:
        link = anchor.get('href')
        text = anchor.get_text()
        if link:
            embedded_hyperlinks_list.append({'text': text, 'link': link})

    return embedded_hyperlinks_list

  def get_chi_awe_hyperlinks(self, embedded_hyperlinks_list):
    chi_awe_hyperlinks_dict = {}
    for d in embedded_hyperlinks_list:
      text = d['text'].strip()
      hyperlink = d['link']
      if hyperlink[0] == '/':
        chi_awe_hyperlinks_dict[text] = self.base_url + hyperlink[1:]
    return chi_awe_hyperlinks_dict

  def get_content(self, scrape_class = "sqs-html-content"):
    embedded_hyperlinks_list = self.get_embedded_hyperlinks()
    chi_awe_hyperlinks_dict = self.get_chi_awe_hyperlinks(embedded_hyperlinks_list)

    scrape_class_dict = {}
    scrape_text_dict = {}

    for k, url in chi_awe_hyperlinks_dict.items():
      time.sleep(1)
      response = requests.get(url)
      soup = BeautifulSoup(response.content, 'html.parser')
      scrape_class_dict[url] = soup.find_all("div", {"class": scrape_class})
      scrape_text_dict[url.replace("http://", "").replace("https://", "")] = [x.get_text() for x in scrape_class_dict[url]]
  
    return scrape_text_dict
  
  def get_content_free_text(self, scrape_class = "sqs-html-content"):
    embedded_hyperlinks_list = self.get_embedded_hyperlinks()
    chi_awe_hyperlinks_dict = self.get_chi_awe_hyperlinks(embedded_hyperlinks_list)
    
    scrape_class_dict = {}
    full_text = ""
    for k, url in chi_awe_hyperlinks_dict.items():
      time.sleep(1)
      response = requests.get(url)
      soup = BeautifulSoup(response.content, 'html.parser')
      scrape_class_dict[url] = soup.find_all("div", {"class": scrape_class})
      for x in scrape_class_dict[url]:
        text = x.get_text()
        full_text += text
  
    return full_text
    
  def get_content_for_specific_page(self, scrape_class = "sqs-html-content"):
    # Notice that we're using the base url without scraping links from the base url
    scrape_class_dict = {}
    scrape_text_dict = {}

    response = requests.get(self.base_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    scrape_class_dict[self.base_url] = soup.find_all("div", {"class": scrape_class})
    scrape_text_dict[self.base_url.replace("http://", "").replace("https://", "")] = [x.get_text() for x in scrape_class_dict[self.base_url]]
    # scrape_class_dict[self.base_url.replace("http://", "").replace("https://", "")] = soup.find_all("div", {"class": scrape_class})
    
    return scrape_class_dict
  
    # URL = "https://realpython.github.io/fake-jobs/"
    # page = requests.get(URL)
    # soup = BeautifulSoup(page.content, "html.parser")
    # results = soup.find(id=scrape_class)
    # job_elements = results.find_all("div", class_="card-content")
    # embedded_hyperlinks_list = self.get_embedded_hyperlinks()
    # chi_awe_hyperlinks_dict = self.get_chi_awe_hyperlinks(embedded_hyperlinks_list)

    # scrape_class_dict = {}
    # scrape_text_dict = {}

    # for k, url in chi_awe_hyperlinks_dict.items():
    #   response = requests.get(url)
    #   soup = BeautifulSoup(response.content, 'html.parser')
    #   scrape_class_dict[url] = soup.find_all("div", {"class": scrape_class})
    #   scrape_text_dict[url.replace("http://", "").replace("https://", "")] = [x.get_text() for x in scrape_class_dict[url]][0]

    # return scrape_text_dict
