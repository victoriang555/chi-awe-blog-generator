from scrape_chi_awe_org import ScrapeChiAWE
import constants

import json

def scrape(base_url):
    """
    Scrape a given website's text
    """
    scraper = ScrapeChiAWE(base_url=base_url)
    scraped_text_dict = scraper.get_content()
    return scraped_text_dict

def scrape_all_websites():
    """
    Scrape all of the chi-AWE websites
    """
    for website in constants.ALL_CHI_AWE_WEBSITES:
        scraped_text_dict = scrape(website)
        filename = "{}.txt".format(website)
        with open(filename, 'w') as file:
            file.write(json.dumps(scraped_text_dict))


