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

agiaid_engine = RetrieverEngine()

app = FastAPI()

# 允许的源列表，用于配置 CORS
origins = [
    "http://localhost:3001",
    "http://localhost:3000",
    "http://localhost:6000",
]

# 添加 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 基础目录路径，用于文件服务等
BASE_DIR = Path(__file__).resolve().parent


class QueryPayload(BaseModel):
    query: str

class OpenAIPayload(BaseModel):
    messages: object

# 查询接口，接收查询请求并返回结果
@app.post("/api/query")
async def query(payload: QueryPayload):
    try:
        # 使用检索引擎进行查询
        system_msg, results = agiaid_engine.query(payload.query)
        msg.good(f"Succesfully processed query: {payload.query}")

        # 返回成功的响应
        return JSONResponse(
            content={
                "system": system_msg,
                "documents": results,
            }
        )
    except Exception as e:
        # 异常处理
        msg.fail(f"Query failed")
        print(e)
        return JSONResponse(
            content={
                "system": f"Something went wrong! {str(e)}",
                "documents": [],
            }
        )

# OpenAI 聊天完成接口
@app.post("/v1/chat/completions")
async def create_chat_completion(payload: OpenAIPayload):
    try:
        # 使用检索引擎处理 OpenAI 请求
        results = agiaid_engine.openai_query(payload.messages)
        msg.good(f"Succesfully processed query: {payload.messages}")
        return results
    
    except Exception as e:
        # 异常处理
        msg.fail(f"Query failed")
        print(e)
        return JSONResponse(
            content={
                "system": f"Something went wrong! {str(e)}",
                "documents": [],
            }
        )
