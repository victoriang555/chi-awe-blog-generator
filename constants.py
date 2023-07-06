
MODEL_NAME='text-curie-001'
TITLE = 'AAPI Women in {topic} - The Community Service, Sisterhood, and Empowerment'
TOPIC = 'topic'
PERSON = 'person'
ASK = 'ask'
INITIATIVE = 'initiative'
SECONDARY_ASK = 'secondary-ask'
NEXT_READ = 'next-read'
NEXT_READ_SUMMARY = 'next-read-summary'
ALTERNATIVE_READ = 'alternative-read'
ALTERNATIVE_READ_SUMMARY = 'alternative-read-summary'
ORG_SUMMARY = 'org-summary'

###### SCRAPED TEXT QUERIES ######
WEBSITE_SUMMARY_QUERY = "Summarize the Chicago Asian Women Empowerment non-profit organization mission and vision"

###### PARAGRAPH TEMPLATES ######
OPENING_PARAGRAPH_TEMPLATE = 'As a {person} who is interested in empowering AAPI women and making friends in Chicago, give a 1 paragraph explanation of why {topic} is important and relevant.'
PITCH_PARAGRAPH_TEMPLATE = 'As a {person} who is interested in {topic}, give 1 paragraph explaining why it is important to support the organization that has the following description - {org-summary}'
ASK_PARAGRAPH_TEMPLATE = 'As an engaged community member who is ready to support, give 1 paragraph telling me that I should {ask} {initiative} of the organization with the following description - {org-summary}'
ALTERNATIVE_ASK_PARAGRAPH_TEMPLATE = 'As someone who cannot {ask} {initiative}, give 1 paragraph telling me that I should {secondary-ask}.'
NEXT_READ_PARAGRAPH_TEMPLATE = 'Since I have already learned a lot about {topic}, give 1 paragraph convincing me why I should read the following webpage: {next-read}, which is about the following - {next-read-summary}'
ALTERNATIVE_READ_PARAGRAPH_TEMPLATE = 'Since I have already learned a lot about {topic}, give 1 paragraph convincing me why I should read the following webpage: {alternative-read}, which is about the following - {alternative-read-summary}'

###### SQUARESPACE WEBSITES ########
MISS_ASIAN_CHICAGO_WEBSITE = "https://www.missasianchicago.info/"
MISS_CHINESE_CHICAGO_WEBSITE = "https://www.misschinesechicago.info/"
ASIAN_FASHION_SHOW_CHICAGO_WEBSITE = "https://www.chiasian.fashion/"
ALL_SQUARESPACE_WEBSITES = [MISS_ASIAN_CHICAGO_WEBSITE, MISS_CHINESE_CHICAGO_WEBSITE, ASIAN_FASHION_SHOW_CHICAGO_WEBSITE]

######## FILENAMES ########
SCRAPED_JSON = "website_text.json"
SCRAPED_TEXT = "website_text.txt"
SCRAPED_PARTICULAR_WEBSITE = "particular_website.json"
ORG_SUMMARY_SCRAPED_JSON = "org_summary_scrape.json"
ORG_SUMMARY_SCRAPED_TEXT = "org_summary_scrape.txt"
NEXT_READ_SCRAPED_TEXT = "next_read_text.txt"
ALTERNATIVE_READ_SCRAPED_TEXT = "alternative_read_text.txt"

####### OUR-VISION PAGE #######
OUR_VISION_PAGE = 'https://chi-awe.org/our-vision'
OUR_VISION_PAGE_ELEMENTS = ["#page-1", "#empower", "#amplify", "#build"]

####### COMMUNITY IMPACT PAGE ######
COMMUNITY_IMPACT_PAGE = 'https://chi-awe.org/community-impact'
COMMUNITY_IMPACT_PAGE_ELEMENTS = ["#home", "#page-2", "#page-3", "#page-4"]

######## COMMUNITY ENGAGEMENT PAGE #######
COMMUNITY_ENGAGEMENT_PAGE = 'https://chi-awe.org/community-engagement'
COMMUNITY_ENGAGEMENT_PAGE_ELEMENTS = ["#home", "#page-2", "#page-3", "#page-4", "#page-5", "#page-6"]

######## FEMALE VOICES PAGE #######
FEMALE_VOICES_PAGE = 'https://chi-awe.org/female-voices'
FEMALE_VOICES_PAGE_ELEMENTS = ["#home", "#page-2", "#page-3", "#page-4", "#page-5", "#page-6", "#page-7", "#page-8"]

######## SISTERHOOD PAGE ######
SISTERHOOD_PAGE = 'https://chi-awe.org/sisterhood'
SISTERHOOD_PAGE_ELEMENTS = ["#home", "#page-2", "#page-3", "#page-4", "#page-5", "#page-6"]

######## CANVA_CHI_AWE_PAGES ########
CANVA_CHI_AWE_PAGES = {OUR_VISION_PAGE: OUR_VISION_PAGE_ELEMENTS, 
                       COMMUNITY_IMPACT_PAGE: COMMUNITY_IMPACT_PAGE_ELEMENTS, 
                       COMMUNITY_ENGAGEMENT_PAGE: COMMUNITY_ENGAGEMENT_PAGE_ELEMENTS,
                       FEMALE_VOICES_PAGE: FEMALE_VOICES_PAGE_ELEMENTS,
                       SISTERHOOD_PAGE: SISTERHOOD_PAGE_ELEMENTS}
