# Import System Libraries
import time

# Import Third-party Libraries
import streamlit as st
from langchain import PromptTemplate
from langchain.llms import OpenAI

##################
# Global Variables
##################
openai_api_key = st.secrets["OPENAPI_KEY"]

template = """\
    Below is an email from me that may be poorly worded.
    Your goal is to:
    - Give a suggested email subject line.
    - Include an appropriate salutation.
    - Tailor the email according to TYPE.
    - Convert the input text to a specified TONE.
    - Convert the input text to a specified DIALECT.
    - End email with a conclusion and CTA if appropriate.
    - Properly format the email.

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
    llm = OpenAI(temperature=.7, openai_api_key=openai_api_key)
    return llm

def get_input_email():
    input_email = st.text_area(label="Email Input", label_visibility='collapsed', placeholder="Your Email...", key="email_input")
    return input_email

def update_email_with_example():
    st.session_state.email_input = "Sally I am starts work at yours monday\nfrom dave"

def llm_call(option_tone, option_dialect, option_emailtype):
    llm = load_LLM(openai_api_key=openai_api_key)
    prompt_with_email = prompt.format(tone=option_tone, dialect=option_dialect, emailType=option_emailtype, email=email_input)
    formatted_email = llm(prompt_with_email)
    return formatted_email

# Check if the button was clicked
def button_clicked():
    if 'button_click' not in st.session_state:
        st.session_state.button_click = False
    return st.session_state.button_click

##################
# Page Code
##################
st.set_page_config(
    page_title="Email Enhancer",
    page_icon=":robot:",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("## Enter Your Email To Convert")

with st.sidebar:
    st.markdown("## Email Enhancer")
    option_tone = st.selectbox(
        'Which tone would you like your email to have?',
        ('Professional 🤝', 'Friendly ✋'))
    option_dialect = st.selectbox(
        'Which English Dialect would you like?',
        ('British English 🇬🇧', 'American English 🇺🇸'))
    option_emailtype = st.selectbox(
        'What type of email are you sending?',
        ('Contractor to customer 👷', 'Office setting 🧑‍💼'))

email_input = get_input_email()
if len(email_input.split(" ")) > 700:
    st.warning("Please enter a shorter email. The maximum length is 700 words.")
    st.stop()

col1, col2, col3, col4 = st.columns(4)
with col2:
    if st.button("*See An Example*", type='secondary', help="Click to see an example of the email you will be converting."):
        update_email_with_example()
with col3:
    if st.button("*Fix My Email*", type='primary', help="Click Fix Your Email"):
        st.session_state.button_click = True

with st.container():
    if email_input and button_clicked():
        with st.spinner(text="In progress..."):
            llm = load_LLM(openai_api_key=openai_api_key)
            prompt_with_email = prompt.format(tone=option_tone, dialect=option_dialect, emailType=option_emailtype, email=email_input)
            formatted_email = llm(prompt_with_email)
            st.markdown("### Your Converted Email:")
            st.info(formatted_email, icon="✉️")
        st.balloons()

about_email_fixer = """\
## About Email Fixer

Introducing **Email Fixer**, the perfect solution for anyone struggling with English grammar and writing. \n\nWhether you're a non-native speaker, have limited proficiency, or just need some extra help, our app offers a simple solution to elevate your writing skills. \n\nWith a few clicks, our app will analyze your email and provide well-written alternatives that are either formal and informal.
"""

benefits_text = """\
- **Improved communication:** Our app helps bridge the communication gap by refining your email,-making it easier to understand and more professional.\n 
- **Time-saving:** Save time and effort by having your email automatically rewritten, preventing the need for manual editing and revision. \n 
- **Increased confidence:** With our app, you can feel more confident in your writing skills, knowing that your email is accurately conveyed and polished. \n 
- **Competitive edge:** Stand out from the crowd by creating highly professional emails that impress your recipients.
"""    
        
st.markdown(about_email_fixer)

col1, col2 = st.columns(2)        
with col1:
    st.markdown(about_email_fixer)

with col2:
    st.markdown(benefits_text)
