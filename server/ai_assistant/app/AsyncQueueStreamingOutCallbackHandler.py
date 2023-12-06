'''
Author: yuyingtao yuyingtao@agiclass.ai
Date: 2023-07-03 20:52:19
LastEditors: yuyingtao yuyingtao@agiclas.cn
LastEditTime: 2023-07-04 01:19:41
Description: 
'''
from typing import Optional, Any, Dict, List
from queue import Queue
from uuid import UUID
from langchain.callbacks.base import AsyncCallbackHandler

class AsyncQueueStreamingOutCallbackHandler(AsyncCallbackHandler):
    def __init__(self, q: Queue):

        self.q = q

    async def on_llm_new_token(
        self,
        token: str,
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        **kwargs: Any,
    ) -> None:
        self.q.put(token)

    async def on_chain_start(
        self,
        serialized: Dict[str, Any],
        inputs: Dict[str, Any],
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> None:
        """Run when chain starts running."""
        pass