from dotenv import load_dotenv

load_dotenv() 

from langchain_groq import ChatGroq 
from langchain_core.prompts import ChatPromptTemplate


model = ChatGroq(model = "openai/gpt-oss-20b")
    
prompt = ChatPromptTemplate.from_messages([
    (
    "system",
        """You are an expert information extraction assistant. Extract key details from the user's text and present them in a clean, structured Markdown format.

Rules:
- Extract ONLY facts explicitly mentioned in the text. Do NOT add outside knowledge.
- If a detail is missing from the text, write "Not mentioned".
- Keep the Quick Summary concise (1–2 sentences max).

Use this exact output layout:

\n🎬 Extracted Details

- Movie Name:
- Release Year: 
- Director:
- Genre: 
- Cast: 
- Music Credits: 
- Ratings: 
- Key Themes & Highlights:

\n📝 Quick Summary

\n[Write a crisp 1–2 sentence summary here]""",
),
(
    "human",
    "Extract the key information and summarize this"
    " paragraph:\n\n{paragraph}",
)
])

para = input("Give your paragraph here :")

final_prompt = prompt.invoke(
    {"paragraph":para}
)


response = model.invoke(final_prompt)

print(response.content)

