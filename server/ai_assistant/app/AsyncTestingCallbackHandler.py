'''
Author: yuyingtao yuyingtao@agiclass.ai
Date: 2023-07-03 20:57:41
LastEditors: yuyingtao yuyingtao@agiclass.ai
LastEditTime: 2023-07-03 21:11:08
Description: 
'''
from typing import Dict, List, Any, Union
from langchain.callbacks.base import AsyncCallbackHandler

class AsyncTestinCallbackHander(AsyncCallbackHandler):
    async def on_llm_start(
        self,
        serialized: Dict[str, Any],
    ) -> None:
        print('---------- on_llm_start \n')
        print(serialized)

    async def on_chat_model_start(
        self,
        serialized: Dict[str, Any],
    ) -> Any:
        print('---------- on_chat_model_start \n')
        print(serialized)

    async def on_llm_new_token(
        self,
        token: str,
    ) -> None:
        print('---------- on_llm_new_token \n')
        print(token)

    async def on_llm_end(
        self,
        response,
    ) -> None:
        """Run when LLM ends running."""
        print('---------- on_llm_end \n')
        print(response)

    async def on_llm_error(
        self,
        error: Union[Exception, KeyboardInterrupt],
    ) -> None:
        print('---------- on_llm_error \n')
        print(error)

    async def on_chain_start(
        self,
        serialized: Dict[str, Any],
    ) -> None:
        """Run when chain starts running."""
        print('---------- on_chain_start \n')
        print(serialized)

    async def on_chain_end(
        self,
        outputs: Dict[str, Any],
    ) -> None:
        """Run when chain ends running."""
        print('---------- on_chain_end \n')
        print(outputs)

    async def on_chain_error(
        self,
        error: Union[Exception, KeyboardInterrupt],
    ) -> None:
        """Run when chain errors."""
        print('---------- on_chain_error \n')
        print(error)

    async def on_tool_start(
        self,
        serialized: Dict[str, Any],
    ) -> None:
        """Run when tool starts running."""
        print('---------- on_tool_start \n')
        print(serialized)

    async def on_tool_end(
        self,
        output: str,
    ) -> None:
        """Run when tool ends running."""
        print('---------- on_tool_end \n')
        print(output)

    async def on_tool_error(
        self,
        error: Union[Exception, KeyboardInterrupt],
    ) -> None:
        """Run when tool errors."""
        print('---------- on_tool_error \n')
        print(error)

    async def on_text(
        self,
        text: str,
    ) -> None:
        """Run on arbitrary text."""
        print('---------- on_text \n')
        print(text)

    async def on_agent_action(
        self,
    ) -> None:
        """Run on agent action."""
        print('---------- on_agent_action \n')

    async def on_agent_finish(
        self,
    ) -> None:
        """Run on agent end."""
        print('---------- on_agent_finish \n')
    