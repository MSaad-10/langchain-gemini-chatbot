import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)
chat_history = []
print("LangChain Chatbot initialized! Type 'exit' to end.\n")

while True:
    user_input = input("User: ")
    if user_input.strip().lower() == 'exit':
        break

    chat_history.append(HumanMessage(content=user_input))
    response = llm.invoke(chat_history)
    chat_history.append(AIMessage(content=response.content))
    
    print(f'AI: {response.content}\n')