from typing import Dict, List, Any, Union, Optional
from uuid import UUID
from langchain.callbacks.base import BaseCallbackHandler

class TestingCallbackHandler(BaseCallbackHandler):
    def on_llm_start(
        self,
        serialized: Dict[str, Any],
    ) -> None:
        print('---------- on_llm_start \n')
        print(serialized)

    def on_chat_model_start(
        self,
        serialized: Dict[str, Any],
        messages,
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> Any:
        print('---------- on_chat_model_start \n')
        print(serialized, messages, tags)

    def on_llm_new_token(
        self,
        token: str,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
    ) -> None:
        print('---------- on_llm_new_token \n')
        print(token)

    def on_llm_end(
        self,
        response,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
    ) -> None:
        """Run when LLM ends running."""
        print('---------- on_llm_end \n')
        print(response)

    def on_llm_error(
        self,
        error: Union[Exception, KeyboardInterrupt],
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
    ) -> None:
        print('---------- on_llm_error \n')
        print(error)

    def on_chain_start(
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
        print('---------- on_chain_start \n')
        print(serialized, inputs, tags)

    def on_chain_end(
        self,
        outputs: Dict[str, Any],
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
    ) -> None:
        """Run when chain ends running."""
        print('---------- on_chain_end \n')
        print(outputs)

    def on_chain_error(
        self,
        error: Union[Exception, KeyboardInterrupt],
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
    ) -> None:
        """Run when chain errors."""
        print('---------- on_chain_error \n')
        print(error)

    def on_tool_start(
        self,
        serialized: Dict[str, Any],
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
    ) -> None:
        """Run when tool starts running."""
        print('---------- on_tool_start \n')
        print(serialized)

    def on_tool_end(
        self,
        output: str,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
    ) -> None:
        """Run when tool ends running."""
        print('---------- on_tool_end \n')
        print(output)

    def on_tool_error(
        self,
        error: Union[Exception, KeyboardInterrupt],
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
    ) -> None:
        """Run when tool errors."""
        print('---------- on_tool_error \n')
        print(error)

    def on_text(
        self,
        text: str,
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        **kwargs: Any,
    ) -> None:
        """Run on arbitrary text."""
        print('---------- on_text \n')
        print(text)

    def on_agent_action(
        self,
        action,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
    ) -> None:
        """Run on agent action."""
        print('---------- on_agent_action \n')

    def on_agent_finish(
        self,
        finish,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
    ) -> None:
        """Run on agent end."""
        print('---------- on_agent_finish \n')