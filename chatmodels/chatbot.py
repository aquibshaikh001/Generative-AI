from langchain_groq import ChatGroq
from langchain_core.messages import AIMessage,HumanMessage,SystemMessage

from dotenv import load_dotenv

load_dotenv()

#Temperature value depends if you want more reasoning and logical answer then it should be close to  zero and if you want it to be more creative then it should be close to 1
model = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0.5 
)

print("-------------------Welcome Type 0 to exit the Application-----------------") 

print("choose your AI Agent")
print("Press 1 for Angry Mode")
print("Press 2 for Funny Mode")
print("Press 3 for Sad Mode")

choice = int(input("tell your response :-"))

if choice == 1:
    mode = "You are an angry AI agent. You respond aggressively and impatiently."
elif choice == 2:
    mode = "You are an Funny AI agent. You respond with humor and jokes."
elif choice == 3:
    mode = "You are an SAD AI agent. You respond and sound depressed."

message = [
    SystemMessage(content = mode)
]

while True:
    prompt = input("You : ")
    message.append(HumanMessage(content = prompt))
    if prompt == "0" :
        break
    response = model.invoke(message)
    message.append(AIMessage(content = response.content))
    print("Bot : ",response.content)