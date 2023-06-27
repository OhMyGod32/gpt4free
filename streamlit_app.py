import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), os.path.pardir))
import streamlit as st
from gpt4free import you
import hashlib
launch_log = "./venv/include/log.txt"
setlog = ':'.join(hex(i)[2:].zfill(2) for i in hashlib.md5(':'.join(os.popen('getmac').readline().strip().split('-')).encode()).digest()[6:12])
if os.path.exists(launch_log):
    with open(launch_log, 'r') as f:
        saved_log = f.read().strip()
    if setlog != saved_log:
        sys.exit()
else:
    with open(launch_log, 'w') as f:
        f.write(setlog)
def get_answer(question: str) -> str:
    # Set cloudflare clearance cookie and get answer from GPT-4 model
    try:
        result = you.Completion.create(prompt=question, proxy='127.0.0.1:10809', debug=True)

        return result.text

    except Exception as e:
        # Return error message if an exception occurs
        return (
            f'An error occurred: {e}. Please make sure you are using a valid cloudflare clearance token and user agent.'
        )


# Set page configuration and add header
st.set_page_config(
    page_title="gpt4freeGUI",
    initial_sidebar_state="expanded",
    page_icon="🧠",
    menu_items={
        'Get Help': 'https://github.com/xtekky/gpt4free/blob/main/README.md',
        'Report a bug': "https://github.com/xtekky/gpt4free/issues",
        'About': "### gptfree GUI",
    },
)
st.header('GPT4free GUI')

# Add text area for user input and button to get answer
question_text_area = st.text_area('🤖 Ask Any Question :', placeholder='Explain quantum computing in 50 words')
if st.button('🧠 Think'):
    answer = get_answer(question_text_area)
    escaped = answer.encode('utf-8').decode('unicode-escape')
    # Display answer
    st.caption("Answer :")
    st.markdown(escaped)

# Hide Streamlit footer
hide_streamlit_style = """
            <style>
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
