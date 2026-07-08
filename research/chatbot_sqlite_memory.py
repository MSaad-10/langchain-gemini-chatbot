import os
import sqlite3
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage

load_dotenv()

#  Database Setup 
# To store the memory.db file in the current directory (/research) where chatbot_sqlite_memory.py is located
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(CURRENT_DIR, "chat_memory.db")

SESSION_ID = "default_user_session"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Inserts a single message into the database
def save_message(session_id, role, content):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO messages (session_id, role, content) VALUES (?, ?, ?)",
        (session_id, role, content)
    )
    conn.commit()
    conn.close()

# Fetches history and formats it for LangChain
def load_history(session_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT role, content FROM messages WHERE session_id = ? ORDER BY id ASC", 
        (session_id,)
    )
    rows = cursor.fetchall()
    conn.close()

    # Convert SQL rows back into LangChain message objects
    history = []
    for role, content in rows:
        if role == "user":
            history.append(HumanMessage(content=content))
        elif role == "ai":
            history.append(AIMessage(content=content))
    return history


# Chatbot Execution 
init_db()
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)

print("Custom SQLite Chatbot initialized! Type 'exit' to end.\n")

while True:
    user_input = input("User: ")
    if user_input.strip().lower() == 'exit':
        break

    save_message(SESSION_ID, "user", user_input)

    current_chat_history = load_history(SESSION_ID)

    response = llm.invoke(current_chat_history)

    save_message(SESSION_ID, "ai", response.content)

    print(f'\nAI: {response.content}\n')