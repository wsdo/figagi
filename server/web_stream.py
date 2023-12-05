import time
import gradio as gr
from dotenv import load_dotenv
load_dotenv()

from app.controllers.retrieval.RetrieverEngine import RetrieverEngine
agikb_engine = RetrieverEngine()

def generate_text(prompt):
    msg = [
        {
        "role": "system",
        "content": "\nYou are AI助教, a large language model trained by AGIClass."
        },
        {"role": "user","content": f"{prompt}"}
    ]

    results = agikb_engine.openai_query(msg)

    return results


def slow_echo(message, history):
    res = generate_text(message)
    accumulated_response = ''

    for chunk in res:
        # 检查 chunk 或其关键属性是否为 None
        if chunk is None or chunk.choices is None or chunk.choices[0].delta is None or chunk.choices[0].delta.content is None:
            break  # 如果是 None，则结束循环

        # 获取当前chunk的内容
        current_content = chunk.choices[0].delta.content

        if current_content is not None:  # 确保内容不是 None
            print(current_content)

            # 将当前chunk的内容合并
            accumulated_response += current_content

            yield accumulated_response
demo = gr.ChatInterface(slow_echo).queue()

if __name__ == "__main__":
    demo.launch(root_path="/aid")