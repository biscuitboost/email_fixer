import streamlit as st
from langchain import PromptTemplate
from langchain.llms import OpenAI


template = """
    Below is an email from me that may be poorly worded.
    Your goal is to:
    - Properly format the email
    - Convert the input text to a specified tone
    - Convert the input text to a specified dialect
 
    Please start the email with a warm introduction.
    
    Below is the email, tone, and dialect:
    TONE: {tone}
    DIALECT: {dialect}
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
st.header("Email Fixer")

col1, col2 = st.columns(2)

with col1:
    st.markdown("\
Introducing **Email Fixer**, the perfect solution for anyone struggling with English grammar and writing. \n\nWhether you're a non-native speaker, have limited proficiency, or just need some extra help, our app offers a simple solution to elevate your writing skills. \n\nWith a few clicks, our app will analyze your email and provide well-written alternatives that are either formal and informal.")

with col2:
    st.markdown("- **Improved communication:** Our app helps bridge the communication gap by refining your email, making it easier to understand and more professional.\n \
- **Time-saving:** Save time and effort by having your email automatically re-written, preventing the need for manual editing and revision. \n \
- **Increased confidence:** With our app, you can feel more confident in your writing skills, knowing that your email is accurately conveyed and polished. \n \
- **Competitive edge:** Stand out from the crowd by creating highly professional emails that impress your recipients.")    

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
        ('British English', 'American English', 'Scots', 'Welsh', 'Cornish'))

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

st.button("*See An Example*", 
          type='secondary', 
          help="Click to see an example of the email you will be converting.", 
          on_click=update_text_with_example)


st.markdown("### Your Converted Email:")

if email_input:
    llm = load_LLM(openai_api_key=openai_api_key)
    prompt_with_email = prompt.format(tone=option_tone, dialect=option_dialect, email=email_input)
    formatted_email = llm(prompt_with_email)
    st.write(formatted_email)

    # add option to copy to clipboard
    if st.button("Copy to Clipboard"):
        if "button_id" not in st.session_state:
            st.session_state.button_id = 0
        button_id = st.session_state.button_id + 1
        st.session_state.button_id = button_id
        copy_button_html = """
        <button id="copy-button-{button_id:}" onclick="copyText()">Copy Email</button>
        <script>
            function copyText() {
                var copyText = document.getElementById("formatted-email");
                copyText.select();
                copyText.setSelectionRange(0, 99999);
                document.execCommand("copy");
                var button = document.getElementById("copy-button-{button_id:}");
                button.innerText = "Copied!";
            }
        </script>
        """.format(button_id=button_id)
        st.markdown(copy_button_html, unsafe_allow_html=True)
        st.text_area("Formatted Email", value=formatted_email, key="formatted-email")
    
