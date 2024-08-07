from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from pydantic import BaseModel
import os
import uvicorn

load_dotenv()

class Chat_input(BaseModel):
    input: str

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


llm = ChatGroq(
    model="llama-3.1-70b-versatile",
    temperature=0.5,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    api_key=os.getenv("GROQ_API_KEY"),
)

memory = ConversationBufferMemory(k=20, memory_key="chat_history", return_messages=True)


prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage(content="You are an expert in talking with humans. Human will provide you some input, reply to them with a proper answer."),
        MessagesPlaceholder(variable_name="chat_history"),
        HumanMessagePromptTemplate.from_template("{input}"),
    ]
)


chain = ConversationChain(
    prompt=prompt,
    llm=llm,
    memory=memory,
)

# Route for chat with history
@app.post("/chat")
async def chat(input: Chat_input):
    async def event_stream():
        try:
            async for event in chain.astream_events({"input": input.input}, version="v1"):
                if event["event"] == 'on_chat_model_stream':
                    yield event["data"]["chunk"].content
        except Exception as e:
            yield f"Error: {str(e)}"

    return StreamingResponse(event_stream(), media_type="text/event-stream")

# Route for simple Q&A without history
@app.post("/ask")
async def ask(input: Chat_input):
    async def event_stream():
        try:
            simple_prompt = ChatPromptTemplate.from_messages(
                [
                    SystemMessage(content="You are an expert in answering questions."),
                    HumanMessagePromptTemplate.from_template("{input}"),
                ]
            )
            
            simple_chain = simple_prompt | llm

            async for event in simple_chain.astream_events({"input": input.input}, version="v1"):
                if event["event"] == 'on_chat_model_stream':
                    yield event["data"]["chunk"].content
        except Exception as e:
            yield f"Error: {str(e)}"

    return StreamingResponse(event_stream(), media_type="text/event-stream")

