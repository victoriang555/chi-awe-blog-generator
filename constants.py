
MODEL_NAME='text-curie-001'
TITLE = 'AAPI Women in {topic} - The Community Service, Sisterhood, and Empowerment'
TOPIC = 'topic'
PERSON = 'person'
ASK = 'ask'
INITIATIVE = 'initiative'
SECONDARY_ASK = 'secondary-ask'
NEXT_READ = 'next-read'
NEXT_READ_TOPICS = 'next-read-topics'
ALTERNATIVE_READ = 'alternative-read'
ALTERNATIVE_READ_TOPICS = 'alternative-read-topics'

###### SCRAPED TEXT QUERIES ######
WEBSITE_SUMMARY_QUERY = "Summarize the Chicago Asian Women Empowerment non-profit organization mission and vision"

###### PARAGRAPH TEMPLATES ######
OPENING_PARAGRAPH_TEMPLATE = 'Generate a 1 paragraph explanation why {topic} is important and relevant. The reader is a {person} interested in empowering AAPI women and making friends in Chicago.'
PITCH_PARAGRAPH_TEMPLATE = 'As a {person} who is interested in {topic}, give 1 paragraph explaining why it is important support a non-profit organization.'
ASK_PARAGRAPH_TEMPLATE = 'As an engaged community member who is ready to support, give 1 paragraph telling me that I should {ask} {initiative}'
ALTERNATIVE_ASK_PARAGRAPH_TEMPLATE = 'As someone who cannot {ask} {initiative}, give 1 paragraph telling me that I should {secondary-ask}.'
NEXT_READ_PARAGRAPH_TEMPLATE = 'Since I have already learned a lot about {topic}, give 1 paragraph convincing me why I should read the following webpage: {next-read}, which discusses the following topics {next-read-topics}'
ALTERNATIVE_READ_PARAGRAPH_TEMPLATE = 'Since I have already learned a lot about {topic}, give 1 paragraph convincing me why I should read the following webpage: {alternative-read}, which discusses the following topics {alternative-read-topics}'

###### WEBSITE LINKS ########
CHI_AWE_WEBSITE = "https://www.chi-awe.org/"
MISS_ASIAN_CHICAGO_WEBSITE = "https://www.missasianchicago.info/"
MISS_CHINESE_CHICAGO_WEBSITE = "https://www.misschinesechicago.info/"
ASIAN_FASHION_SHOW_CHICAGO_WEBSITE = "https://www.chiasian.fashion/"
ALL_CHI_AWE_WEBSITES = [CHI_AWE_WEBSITE, MISS_ASIAN_CHICAGO_WEBSITE, MISS_CHINESE_CHICAGO_WEBSITE, ASIAN_FASHION_SHOW_CHICAGO_WEBSITE]

######## FILENAMES ########
SCRAPED_JSON = "website_text.json"
SCRAPED_TEXT = "website_text.txt"
SCRAPED_PARTICULAR_WEBSITE = "particular_website.json"