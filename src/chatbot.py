import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.chat_message_histories import SQLChatMessageHistory


load_dotenv()


# === Setup FastAPI Application === 
app = FastAPI(
    title="LangChain Gemini API",
    description="A conversational AI backend with persistent SQLite memory.",
    version="1.0.0"
)


# === Data Validation Models ===
# This is what user must send to the API 
class ChatRequest(BaseModel):
    session_id: str
    message: str

# This is what API will send back
class ChatResponse(BaseModel):
    response: str


llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)


# === Database PATH ===
# fetching the PATH of chatbot.py file
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
# making the PATH for chat_memory.db file 
DB_PATH = os.path.join(CURRENT_DIR, "chat_memory.db")
db_connection = f"sqlite:///{DB_PATH}"


# === API Endpoints ===
@app.get("/")
async def root():
    ''' simple check to ensure the server is running '''
    return {"status": "online", "message": "FastAPI Chatbot Server is running!"}

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        # load memory
        memory = SQLChatMessageHistory(
            session_id = request.session_id,
            connection = db_connection
        )

        # save incoming user message to database
        memory.add_user_message(request.message)

        # ask Gemini to generate a response on full history
        ai_reponse = llm.invoke(memory.messages)

        # save AI's response to database
        memory.add_ai_message(ai_reponse.content)

        # return clean response to user
        return ChatResponse(response=ai_reponse.content)

    except:
        raise HTTPException(status_code=500, detail=str(0))