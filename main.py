import streamlit as st
import time
from langchain import PromptTemplate
from langchain.llms import OpenAI

##################
# Global Variables
##################
template = """
    Below is an email from me that may be poorly worded.
    Your goal is to:
    - Give a suggested email subject line.
    - Include an appropriate salutation.
    - Taylor the email according to TYPE.
    - Convert the input text to a specified TONE.
    - Convert the input text to a specified DIALECT.
    - End email with a conclusion and CTA if appropriate.
    - Properly format the email
 
    Below is the current email, suggested tone, and dialect:
    TYPE: {emailType}
    TONE: {tone}
    DIALECT: {dialect}
    EMAIL: {email}
    
    YOUR {dialect} RESPONSE:
"""

prompt = PromptTemplate(
    input_variables=["tone", "dialect", 'emailType', "email"],
    template=template,
)

##################
# Functions
##################
def load_LLM(openai_api_key):
    """Logic for loading the chain you want to use should go here."""
    # Make sure your openai_api_key is set as an environment variable
    llm = OpenAI(temperature=.7, openai_api_key=openai_api_key)
    return llm

def get_text():
    input_text = st.text_area(label="Email Input", label_visibility='collapsed', placeholder="Your Email...", key="email_input")
    return input_text

def update_text_with_example():
    print ("in updated")
    st.session_state.email_input = "Sally I am starts work at yours monday\nfrom dave"


##################
# Page Code
##################
st.set_page_config(
    page_title="Email Enhancer",
    page_icon=":robot:",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)


st.markdown("## Enter Your Email To Convert")

openai_api_key = st.secrets["OPENAPI_KEY"]

with st.sidebar:
    st.markdown("**Email Enhancer**")
    option_tone = st.selectbox(
        'Which tone would you like your email to have?',
        ('Professional 🤝', 'Friendly ✋'))
    option_dialect = st.selectbox(
        'Which English Dialect would you like?',
        ('British English 🇬🇧', 'American English 🇺🇸'))
    option_emailtype = st.selectbox(
        'What type of email are you sending?',
        ('Contractor to customer 👷', 'Office setting 🧑‍💼'))
        
        

#col1, col2, col3 = st.columns(3)
#with col1:
#    option_tone = st.selectbox(
#        'Which tone would you like your email to have?',
#        ('Professional 🤝', 'Friendly ✋'))
#    
#with col2:
#    option_dialect = st.selectbox(
#        'Which English Dialect would you like?',
#        ('British English 🇬🇧', 'American English 🇺🇸'))#
#
#with col3:
#    option_emailtype = st.selectbox(
#        'What type of email are you sending?',
#        ('Contractor to customer 👷', 'Office setting 🧑‍💼'))



email_input = get_text()
        

if len(email_input.split(" ")) > 700:
    st.warning("Please enter a shorter email. The maximum length is 700 words.")
    st.stop()


col1, col2, col3, col4 = st.columns(4)

with col2:
    st.button("*See An Example*", 
          type='secondary', 
          help="Click to see an example of the email you will be converting.", 
          on_click=update_text_with_example)
with col3:
    st.button("*Fix My Email*", 
          type='primary', 
          help="Click Fix Your Email", 
          on_click=update_text_with_example)


with st.container():
    if email_input:
        with st.spinner(text="In progress..."):
            llm = load_LLM(openai_api_key=openai_api_key)
            prompt_with_email = prompt.format(tone=option_tone, dialect=option_dialect, emailType=option_emailtype, email=email_input)
            formatted_email = llm(prompt_with_email)
            with st.container():
                st.markdown("### Your Converted Email:")
                st.info(formatted_email, icon="✉️")
        st.balloons()
    

st.markdown("## About Email Fixer")

col1, col2 = st.columns(2)        
with col1:
    st.markdown("\
Introducing **Email Fixer**, the perfect solution for anyone struggling with English grammar and writing. \n\nWhether you're a non-native speaker, have limited proficiency, or just need some extra help, our app offers a simple solution to elevate your writing skills. \n\nWith a few clicks, our app will analyze your email and provide well-written alternatives that are either formal and informal.")

with col2:
    st.markdown("- **Improved communication:** Our app helps bridge the communication gap by refining your email, making it easier to understand and more professional.\n \
- **Time-saving:** Save time and effort by having your email automatically re-written, preventing the need for manual editing and revision. \n \
- **Increased confidence:** With our app, you can feel more confident in your writing skills, knowing that your email is accurately conveyed and polished. \n \
- **Competitive edge:** Stand out from the crowd by creating highly professional emails that impress your recipients.")    
    
