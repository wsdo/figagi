'''
Author: yuyingtao yuyingtao@agiclas.cn
Date: 2023-06-25 16:38:12
LastEditors: yuyingtao yuyingtao@agiclas.cn
LastEditTime: 2023-07-01 00:12:59
Description: 
'''
from typing import List, Dict
from pydantic import BaseModel
from datetime import datetime
import secrets

from fastapi import FastAPI, HTTPException, Depends, Request, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from ai_assistant.server_common.server_response import ServerResponse
from ai_assistant.common.service_common import dict_model
from ai_assistant.server_common.models.content import ContentModel, CreateContentModel, UpdateContentModel
from ai_assistant.server_common.models.common_resp import CommonResp, create_success_resp

from ai_assistant.content_manager.es_content_service import EsContentService
from ai_assistant.content_manager.es_big_text_service import EsBigTextService
from ai_assistant.app.LangChainService import LangChainService
from ai_assistant.config.config import config
from ai_assistant.content_manager.content import Content
from ai_assistant.server_common.models.user import UserModel
from ai_assistant.authentication.ldap_authectication import ldap_auth
from ai_assistant.utils.logger import create_logger
from ai_assistant.utils.str_utils import tract_prefix

from ai_assistant.utils.object import copyObjToObj

from ai_assistant.app.app_service import AppService


logger = create_logger('serverapp')

langchain_service = LangChainService(config=config, temperature=0.9)
bt_service = EsBigTextService(es_url=config.ES_URL, es_index=config.DB_BIG_TEXT)
content_service = EsContentService(big_text_service=bt_service, es_url=config.ES_URL, es_index=config.DB_CONTENT)
app_service = AppService(config, content_service=content_service, langchain_service=langchain_service)

tokens: Dict[str, UserModel]  = {}
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", auto_error=False)

app = FastAPI()

no_auth_paths = [
    '/api/login',
    '/api/a/',
    '/docs',
    '/openapi.json',
]

app.add_middleware(CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = datetime.now()
    response = await call_next(request)
    process_time = datetime.now() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

@app.middleware("auth")
async def check_auth(request: Request, call_next):
    path: str = request.url.path
    no_auth = False
    for na_path in no_auth_paths:
        if (path.startswith(na_path)):
            no_auth = True
            break
    if (no_auth or request.method == 'OPTIONS'):
        return await call_next(request)
    
    token = await oauth2_scheme(request=request)
    if (not token or (token not in tokens)):
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={ 'message': 'auth invalid', 'success': False, 'code': '401' }, headers={"WWW-Authenticate": "Bearer"})
    user = tokens.get(token)
    request.state.user = user

    return await call_next(request)

class SearchContentParam(BaseModel):
    lastId: str | None

@app.post('/api/contents')
async def search_contents(param: SearchContentParam) -> CommonResp[List[ContentModel]] :
    ret = content_service.search_contents_paged(last_id=param.lastId, size=1000)
    resp = []
    for v in ret:
        resp.append(vars(v))
    
    return create_success_resp(resp)

@app.get('/api/content/{id}')
async def get_content(id) -> CommonResp[ContentModel]:
    c = content_service.get_by_id(id) 

    if (not c): 
        raise HTTPException(status_code=404, detail='内容不存在')

    return create_success_resp(vars(c)) 

@app.delete('/api/content/{id}')
async def delete_content(id) -> CommonResp[bool]:
    c = content_service.delete(id) 
    return create_success_resp(True) 

@app.post('/api/content')
async def add_content(item: CreateContentModel) -> ContentModel:
    c = Content()
    copyObjToObj(item, c)
    newC = content_service.create(c, item.big_text)

    return create_success_resp(vars(newC)) 

@app.put('/api/content')
async def update_content(item: UpdateContentModel) -> CommonResp[bool]:
    c = Content()
    logger.info('update_content item: %s', vars(item))
    logger.info('update_content c: %s', vars(c))
    copyObjToObj(item, c)

    logger.info('update_content after copy c: %s', vars(c))
    content_service.update(c)

    return create_success_resp(True)

class LoginOutputModel(BaseModel):
    access_token: str

@app.get('/api/currentUser')
def get_current_user(request: Request):
    return create_success_resp(request.state.user)

# @app.put()
# def vector_content():
#     pass
    
class CrawlWxPlatformIn(BaseModel):
    fake_id: str
    token: str
    cookie: str
    category: str

class CrawlWxPlatformOut(BaseModel):
    success: int
    failed: int
    duplicated: int

@app.post('/api/crawl_wx_platform')
def crawl_wx_platform(input: CrawlWxPlatformIn) -> CommonResp[CrawlWxPlatformOut]:
    return app_service.crawl_wx_platform(fake_id=input.fake_id, token=input.token, cookie=input.cookie, category=input.category)

@app.post("/api/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    username, password = form_data.username, form_data.password
    if (config.BYPASS_AUTH or ldap_auth(username=username, password=password)):
        token = secrets.token_urlsafe(64)
        tokens[token] = { "username": username }
        response = JSONResponse(content=create_success_resp({"access_token": token}))
        response.set_cookie(
            key="access-token",
            value=token,
            httponly=True,
            samesite="none",
            secure=True,
        )
        response.set_cookie(
            key="access-token-unsecure", value=token, httponly=True
        )
        return response
    else:
        raise HTTPException(status_code=400, detail="Incorrect credentials.")

class CheckCreateContentOut(BaseModel):
    isCreated: bool
    content: ContentModel

class CheckCreateContentIn(CreateContentModel):
    token: str
    big_text: str

@app.post('/api/a/check_create_content')
def check_create_content(item: CheckCreateContentIn) -> CommonResp[CheckCreateContentOut]:
    if item.token != config.SERVER_TOKEN:
        raise HTTPException(status_code=400, detail="Invalid token")
    c = Content()
    copyObjToObj(item, c)

    ret = content_service.checkAndCreate(c, item.big_text)
    retDic = {
        "isCreated": ret[0],
        "content": vars(ret[1]),
    }

    
    return create_success_resp(retDic) 