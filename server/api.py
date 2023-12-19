import os
from wasabi import msg
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from pydantic import BaseModel
from app.controllers.retrieval.RetrieverEngine import RetrieverEngine
from dotenv import load_dotenv
load_dotenv()

figagi_engine = RetrieverEngine()

app = FastAPI()

# List of allowed sources, used for configuring CORS
origins = [
    "http://localhost:6000",
]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Base directory path for file serving, etc.
BASE_DIR = Path(__file__).resolve().parent

class QueryPayload(BaseModel):
    query: str

class OpenAIPayload(BaseModel):
    message: object

# Query endpoint, receives query requests and returns results
@app.post("/api/query")
async def query(payload: QueryPayload):
    try:
        # Use retrieval engine to perform query
        system_msg, results = figagi_engine.query(payload.query)
        msg.good(f"Succesfully processed query: {payload.query}")

        # Return a successful response
        return JSONResponse(
            content={
                "system": system_msg,
                "documents": results,
            }
        )
    except Exception as e:
        # Exception handling
        msg.fail(f"Query failed")
        print(e)
        return JSONResponse(
            content={
                "system": f"Something went wrong! {str(e)}",
                "documents": [],
            }
        )

# OpenAI chat completion endpoint
@app.post("/v1/chat/completions")
async def create_chat_completion(payload: OpenAIPayload):
    try:
        # Process OpenAI request using retrieval engine
        msgx = [
            {
                "role": "system",
                "content": "\nYou are AI, a large language model trained by FigAGI."
            },
            {"role": "user","content": f"{payload.message}"}
        ]
        chat_history = [['user', '你好'], ['system', 'you are RAG chat bot']]
        # results = agikb_engine.openai_query(msg,chat_history)
    
        results = figagi_engine.api_openai_query(msgx,chat_history)
        msg.good(f"Succesfully processed query: {msg}")
        return results
    
    except Exception as e:
        # Exception handling
        msg.fail(f"Query failed")
        print(e)
        return JSONResponse(
            content={
                "system": f"Something went wrong! {str(e)}",
                "documents": [],
            }
        )
