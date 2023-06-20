
import requests
from bs4 import BeautifulSoup


class ScrapeChiAWE:
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
      response = requests.get(url)
      soup = BeautifulSoup(response.content, 'html.parser')
      scrape_class_dict[(k, url)] = soup.find_all("div", {"class": scrape_class})
      scrape_text_dict[(k, url)] = [x.get_text() for x in scrape_class_dict[(k, url)]]

    return scrape_text_dict
