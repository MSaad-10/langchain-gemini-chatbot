import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.chat_message_histories import SQLChatMessageHistory

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)

session_id = "default_user_session"

# fteching the PATH of chatbot.py
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
# making the PATH for chat_memory.db file 
DB_PATH = os.path.join(CURRENT_DIR, "chat_memory.db")

db_connection = f"sqlite:///{DB_PATH}"

memory = SQLChatMessageHistory(
    session_id = session_id,
    connection = db_connection
)

print("LangChain Chatbot with SQL Memory initialized! Type 'exit' to end.\n")   

while True:
    user_input = input("User: ")
    if user_input.strip().lower() == 'exit':
        break

    memory.add_user_message(user_input)
    response = llm.invoke(memory.messages)
    memory.add_ai_message(response.content)
    
    print(f'AI: {response.content}\n')