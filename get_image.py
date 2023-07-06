import openai

###### Below are some of the iterations of the prompt before we figured out the best way to phrase the prompt #######

# prompt_1 = "The image should represent following values - " + topics + ". The image must meet following criteria - image must be a cartoon or a sketch of Asian American Women, - image must contain English text. - consider images from following as source (#AAPIWomen #AsianAmericanPower #StopAAPIHate #womenempowerment #womensupportingwomen #womeninbusiness #girlpower #selflov #womenempoweringwomen #feminism #womenpower #womeninspiringwomen #feminist #girlboss #strongwomen #bossbabe #empowerment #empoweringwomen #womenentrepreneurs)"

# prompt_2 = "The image should represent following values - " + topics + ". The image must meet following criteria - image must be a cartoon or a sketch of Asian American Women, - image must contain English text."

# prompt_3 = "An Asian American Woman doing community service."
# prompt_4 = "A colored pencil drawing of Asian American Women doing community service."
# prompt_5 = "A beautiful painting of Asian American Women Dancing"

def get_image(key, adj_of_image_type, type_of_image, adj_of_objects, objects_in_image, verb_of_objects):
    '''function returns an artificailly generated image specific to passed topics
    inputs - 
        key - Open API key, 
        topics - string representation of interested topic. Example - "asian, women, empowerment" etc.
    output - Image URL 
    '''
    PROMPT = "A " + adj_of_image_type + type_of_image + "of" + adj_of_objects +  objects_in_image + verb_of_objects
    openai.api_key = key

    response = openai.Image.create(
        prompt=PROMPT,
        n=1,
        size="256x256", #can be changed to 512x512, 1024x1024
    )
    print(response["data"][0]["url"]);
    return response["data"][0]["url"]
