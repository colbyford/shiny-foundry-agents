# ------------------------------------------------------------------------------------
# A basic Shiny Chat example powered by OpenAI running on Azure.
# To run it, you'll need a deployed model and API key from Microsoft Foundry.
# ------------------------------------------------------------------------------------
import os

# from dotenv import load_dotenv
from app_utils import load_dotenv
from openai import AzureOpenAI, OpenAI

from shiny.express import ui

## Load environment variables from .env file
load_dotenv()

## Check that .env variables are set
print("FOUNDRY_API_KEY:", os.getenv("FOUNDRY_API_KEY") is not None)
print("FOUNDRY_ENDPOINT:", os.getenv("FOUNDRY_ENDPOINT") is not None)
print("FOUNDRY_DEPLOYMENT_NAME:", os.getenv("FOUNDRY_DEPLOYMENT_NAME") is not None)

llm = AzureOpenAI(
    api_key=os.getenv("FOUNDRY_API_KEY"),
    api_version="2024-02-01",
    azure_endpoint=os.getenv("FOUNDRY_ENDPOINT"),
)

# llm = OpenAI(
#     base_url=os.getenv("FOUNDRY_ENDPOINT"),
#     api_key=os.getenv("FOUNDRY_API_KEY")
# )

deployment_name = os.getenv("FOUNDRY_DEPLOYMENT_NAME")

## Set some Shiny page options
ui.page_opts(
    title="Welcome to Foundry Agent Chat",
    fillable=True,
    fillable_mobile=True,
)

## Create a chat instance, with an initial message
chat = ui.Chat(
    id="chat",
    messages=[
        {"content": "Hello! How can I help you today?", "role": "assistant"},
    ],
)

## Display the chat
chat.ui()


## Define a callback to run when the user submits a message
@chat.on_user_submit
async def _():
    ## Get messages currently in the chat
    messages = chat.messages(format="openai")
    ## Create a response message stream
    response = llm.chat.completions.create(
        model=deployment_name,
        messages=messages,
        stream=True,
    )
    ## Append the response stream into the chat
    await chat.append_message_stream(response)
