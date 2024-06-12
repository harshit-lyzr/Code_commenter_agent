import streamlit as st
from lyzr_automata.ai_models.openai import OpenAIModel
from lyzr_automata import Agent, Task
from lyzr_automata.pipelines.linear_sync_pipeline import LinearSyncPipeline
from PIL import Image
from lyzr_automata.tasks.task_literals import InputType, OutputType

st.set_page_config(
    page_title="Lyzr Code Comment Generator",
    layout="centered",  # or "wide"
    initial_sidebar_state="auto",
    page_icon="lyzr-logo-cut.png",
)

api = st.sidebar.text_input("Enter Your OPENAI API KEY HERE", type="password")

st.markdown(
    """
    <style>
    .app-header { visibility: hidden; }
    .css-18e3th9 { padding-top: 0; padding-bottom: 0; }
    .css-1d391kg { padding-top: 1rem; padding-right: 1rem; padding-bottom: 1rem; padding-left: 1rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

image = Image.open("lyzr-logo.png")
st.image(image, width=150)

# App title and introduction
st.title("Lyzr Code Comment Generator👩🏼‍💻")
st.sidebar.markdown("## Welcome to the Lyzr Code Comment Generator!")
st.sidebar.markdown(
    "This App Harnesses power of Lyzr Automata to Generate Comments for Your Code classes and Functions. You Need to input Your Code and this app add Comments to your code.")

if api:
    openai_model = OpenAIModel(
        api_key=api,
        parameters={
            "model": "gpt-4-turbo-preview",
            "temperature": 0.2,
            "max_tokens": 1500,
        },
    )
else:
    st.sidebar.error("Please Enter Your OPENAI API KEY")


def code_commenter(code_snippet):
    code_comment_agent = Agent(
        prompt_persona="you are a seasoned software engineer with a wealth of experience in writing, reviewing, and improving code",
        role="Software Engineer",
    )

    code_comment_task = Task(
        name="Code Commenting Task",
        output_type=OutputType.TEXT,
        input_type=InputType.TEXT,
        model=openai_model,
        agent=code_comment_agent,
        log_output=True,
        instructions=f"""You are tasked with generating comments for a given piece of code. 
        Your comments should be clear, concise, and informative, providing insight into the functionality and purpose of each section of code. 
        You should strive to explain the logic behind the code, highlight any important features or techniques used, and offer suggestions for improvement if applicable. 
        Your goal is to help readers understand the code more easily and to promote good coding practices through your comments.

        Code: {code_snippet}
        """,
    )

    output = LinearSyncPipeline(
        name="Generate Comment",
        completion_message="Comment Generated!",
        tasks=[
            code_comment_task
        ],
    ).run()
    return output[0]['task_output']


code = st.text_area("Enter Code", height=300)

if st.button("Convert"):
    solution = code_commenter(code)
    st.markdown(solution)
