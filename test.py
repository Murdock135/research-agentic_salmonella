import os
import torch
from transformers import pipeline
from huggingface_hub import login
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv, find_dotenv

# Load environment variables
load_dotenv(find_dotenv())
hf_token = os.getenv("HF_TOKEN")

# Login to Hugging Face (optional but recommended for gated models)
if hf_token:
    login(token=hf_token)

try:
    # Instantiate model with explicit token
    llm = HuggingFaceEndpoint(
        repo_id="mistralai/Mistral-7B-Instruct-v0.3",
        huggingfacehub_api_token=hf_token,
        task="text-generation",
        max_new_tokens=512,
        do_sample=False,
        repetition_penalty=1.03,
    )

except Exception as e:
    print(f"An error occurred: {e}")

chat_model = ChatHuggingFace(llm=llm)

# Invoke model
messages = [
    SystemMessage(content="You're a helpful assistant"),
    HumanMessage(
        content="What happens when an unstoppable force meets an immovable object?"
    ),
]

ai_msg = chat_model.invoke(messages)
print(ai_msg.content)


