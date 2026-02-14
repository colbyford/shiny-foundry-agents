## ------------------------------------------------------------------
## A basic Shiny Chat example powered by a Microsoft Foundry Agent.
## ------------------------------------------------------------------

import os
from app_utils import load_dotenv
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider 
from shiny.express import ui

## Load environment variables from .env file (for local testing)
load_dotenv()

## Create connection to Foundry Agent using AsyncOpenAI client and Azure credentials
client = OpenAI(
    api_key=get_bearer_token_provider(DefaultAzureCredential(), "https://ai.azure.com/.default"),
    base_url=os.getenv("FOUNDRY_ENDPOINT"),
    default_query = {"api-version": "2025-11-15-preview"}
    )

## Set some Shiny page options
ui.page_opts(
    title="Microsoft Foundry - Real Estate Agent 🏡",
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
    response = client.responses.create( 
        input=messages,
        stream=True
        ) 
    ## Stream the response tokens into the chat as they arrive
    async def stream_tokens():
        for chunk in response:
            if chunk.type == "response.output_text.delta":
                yield chunk.delta

    await chat.append_message_stream(stream_tokens())

