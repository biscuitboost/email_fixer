import streamlit as st
from langchain import PromptTemplate
from langchain.llms import OpenAI

template = """
    Below is an email that may be poorly worded.
    Your goal is to:
    - Properly format the email
    - Convert the input text to a specified tone
    - Convert the input text to a specified language

    Here are some examples different Tones:
    - Formal: We went to Barcelona for the weekend. We have a lot of things to tell you.
    - Informal: Went to Barcelona for the weekend. Lots to tell you.  

    Please start the email with a warm introduction. Add the introduction if you need to.
    
    Below is the email, tone, and dialect:
    TONE: {tone}
    LANGUAGE: {dialect}
    EMAIL: {email}
    
    YOUR {dialect} RESPONSE:
"""

prompt = PromptTemplate(
    input_variables=["tone", "dialect", "email"],
    template=template,
)

def load_LLM(openai_api_key):
    """Logic for loading the chain you want to use should go here."""
    # Make sure your openai_api_key is set as an environment variable
    llm = OpenAI(temperature=.7, openai_api_key=openai_api_key)
    return llm

st.set_page_config(page_title="Email Enhancer", page_icon=":robot:")
st.header("Globalize Text")

col1, col2 = st.columns(2)

with col1:
    st.markdown("Introducing [App name], the perfect solution for anyone struggling with English grammar and writing. \
        Whether you're a non-native speaker, have limited proficiency, or just need some extra help, \
            our app offers a simple solution to elevate your writing skills. \
                With a few clicks, our app will analyze your message and provide well-written alternatives \
                    that are both formal and informal.")

with col2:
    st.markdown("\
*Improved communication: Our app helps bridge the communication gap by refining your message, making it easier to understand and more professional. \
*Time-saving: Save time and effort by having your email automatically re-written, preventing the need for manual editing and revision.\
*Increased confidence: With our app, you can feel more confident in your writing skills, knowing that your message is accurately conveyed and polished.\
*Competitive edge: Stand out from the crowd by creating highly professional messages that impress your recipients.")    

st.markdown("## Enter Your Email To Convert")

openai_api_key = st.secrets["OPENAPI_KEY"]

col1, col2 = st.columns(2)
with col1:
    option_tone = st.selectbox(
        'Which tone would you like your email to have?',
        ('Formal', 'Informal'))
    
with col2:
    option_dialect = st.selectbox(
        'Which English Dialect would you like?',
        ('American', 'British', 'Scots', 'Welsh', 'Cornish'))

def get_text():
    input_text = st.text_area(label="Email Input", label_visibility='collapsed', placeholder="Your Email...", key="email_input")
    return input_text

email_input = get_text()

if len(email_input.split(" ")) > 700:
    st.write("Please enter a shorter email. The maximum length is 700 words.")
    st.stop()

def update_text_with_example():
    print ("in updated")
    st.session_state.email_input = "Sally I am starts work at yours monday from dave"

st.button("*See An Example*", type='secondary', help="Click to see an example of the email you will be converting.", on_click=update_text_with_example)

st.markdown("### Your Converted Email:")

if email_input:
    llm = load_LLM(openai_api_key=openai_api_key)
    prompt_with_email = prompt.format(tone=option_tone, dialect=option_dialect, email=email_input)
    formatted_email = llm(prompt_with_email)
    st.write(formatted_email)
