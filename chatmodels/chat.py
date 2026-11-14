
from dotenv import load_dotenv
# from langchain.chat_models import init_chat_model

# Load API keys
load_dotenv()

# Initialize Groq model
# model = init_chat_model(
#     "groq:openai/gpt-oss-20b",
#     max_retries=1,
#     timeout=30
# )

# # Send prompt
# try:
#     print("Sending request to Groq...")

#     response = model.invoke("Explain about Generative AI")

#     print("\nGroq Response:")
#     print(response.content)

# except Exception as e:
#     print("\nGroq is unavailable.")
#     print("Error:", e)


# Using model class

from langchain_groq import ChatGroq

#Temperature value depends if you want more reasoning and logical answer then it should be close to  zero and if you want it to be more creative then it should be close to 1
model = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0.5,
    max_retries=2,
    max_tokens=900,
    timeout=30
)

# Send prompt
try:
    print("Sending request to Groq...")

    response = model.invoke("Explain about Generative AI")

    print("\nGroq Response:")
    print(response.content)

except Exception as e:
    print("\nGroq is unavailable.")
    print("Error:", e)