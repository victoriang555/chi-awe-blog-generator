import openai

def get_image(key, topics):
    PROMPT = "The image should represent following values - " + topics + ". The image must meet following criteria - image must be a cartoon or a sketch, - image must not contain any text. - consider images from following as source (#womenempowerment #womensupportingwomen #women #womeninbusiness #love #girlpower #selflove #motivation #womenempoweringwomen #fashion #feminism #womenpower #womeninspiringwomen #entrepreneur #feminist #selfcare #girlboss #strongwomen #inspiration #bossbabe #loveyourself #beauty #woman #empowerment #empoweringwomen #instagood #instagram #smallbusiness #womenentrepreneurs #girls)"
    openai.api_key = key

    response = openai.Image.create(
        prompt=PROMPT,
        n=1,
        size="256x256", #can be changed to 512x512, 1024x1024
    )
    print(response["data"][0]["url"]);
    return response["data"][0]["url"]

#getImage("<open api key>", "asian, women, empowerment, beauty, pagent")
