import streamlit as st 
from langchain import PromptTemplate
from langchain.llms import OpenAI

template = """
    Below is the name of industry. 
    Your goal is to: 
    -create engaging tweets for twitter about that industry
    -give the tweets a specified tone
    -create as many tweets as specified, where each tweet created is different

    Here the some examples of different tones for personal training industry: 
    -Formal: Embracing a lifestyle of health and fitness isn't just a personal decision, it's a journey that is best navigated with the guidance of experts. In the realm of #PersonalTraining, professionals leverage their knowledge and experience to tailor programs, setting the course for clients' long-lasting wellness. #FitnessIndustry #HealthAndWellness
    -Informal: Who said fitness has to be a solo journey? 😄 Personal trainers are here to make your #FitLife fun and achievable. Custom workouts, nutrition advice, and heaps of motivation - they've got it all covered! Let's smash those goals together! 💪 #PersonalTraining #HealthAndWellness
    -Motivational: Every journey towards health and fitness begins with a single step, and with the #PersonalTraining industry by your side, each step becomes easier. Harness the power of personalized training to conquer your goals and unveil the strongest, fittest version of YOU. #MondayMotivation #FitLife
    -Informative: The #PersonalTraining industry is an essential part of the health sector, offering personalized workout programs, nutrition guidance, and motivation. With a focus on individual goals and needs, personal trainers empower clients to make sustainable lifestyle changes for optimal health and fitness. #FitnessFacts #HealthAndWellness

    You can generate either 1, 2 , 3, 4, 5, or 10 tweets at once. 

    For extremely short tweets they should not exceed 5 words, for short tweets should not exceed more than 12, for medium it should not exceed 20 words, for long 28 words and extremely long not more than 35. 
    When asked to do more than one tweet make sure they vary in size but within the limitations set above. 

    Below is the industry, tone, number of tweets, and length of tweets: 
    Tone: {tone}
    Number of tweets: {number_tweet}
    Length of tweets: {length_tweets}
    Industry: {industry}

    YOUR RESPONSE:
"""

prompt = PromptTemplate(
    input_variables = ["tone", "number_tweet", "length_tweets", "industry"], 
    template = template, 
)

def load_LLM(openai_api_key): 
    """Logic for loading the chain you want to use should go here."""
    llm = OpenAI(temperature = .5, openai_api_key=openai_api_key)
    return llm

st.set_page_config(page_title = "Promo Parrot", page_icon =":robot")
st.image(image="promo parrot.png", width= 700)

col1, col2 = st.columns(2)

with col1: 
    st.markdown("""Promo Parrot is revolutionizing Twitter marketing by offering businesses an AI-powered solution that instantly crafts engaging tweets. \n\n Our platform allows users to customize their communication's tone and length, ensuring each message resonates with their audience and aligns perfectly with their brand ethos.""")
    
with col2: 
   st.markdown("""\n We're here to streamline your social media strategy, delivering instant, impactful, and personalized tweets at your command.""")

def get_api_key():
    input_text = st.text_input(label="OpenAI API Key ",  placeholder="Ex: sk-2twmA8tfCb8un4...", key="openai_api_key_input")
    return input_text

openai_api_key = get_api_key()

col3, col4, col5 = st.columns(3)
with col3: 
    option_tone = st.selectbox(
        "Which tone would you like your tweets to have?", 
        ("Formal", "Informal", "Motivational", "Informative")
    )
with col4:
    option_number_tweets = st.selectbox("How many tweets would you like to generate?", 
                         ("1", "2", "3", "4", "5", "10")
                         )
with col5:
    option_length = st.selectbox("What length would you like your tweets to be?", 
                         ("Extremely Short", "Short", "Medium", "Long", "Extremely Long"))

def get_text():
    input_text = st.text_area(label = "", placeholder = "Your Industry...", key = "industry_input")
    return input_text
    
st.markdown("### Which industry do you work in?")
industry_input = get_text()

st.markdown("### Your Tweets:")

if industry_input:
    if not openai_api_key: 
        st.warning('Please insert OpenAI API Key. Instructions [here](https://help.openai.com/en/articles/4936850-where-do-i-find-my-secret-api-key)', icon="⚠️")
        st.stop()
    
    llm = load_LLM(openai_api_key=openai_api_key)
    prompt = prompt.format(tone=option_tone, number_tweet = option_number_tweets, length_tweets = option_length, industry = industry_input)
    tweets = llm(prompt)
    st.write(tweets)