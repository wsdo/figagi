import time
import gradio as gr
from dotenv import load_dotenv
load_dotenv()
from ui.gradio_utils import reload_javascript, customCSS, small_and_beautiful_theme
from ui.page_services.WebAppService import WebAppService
from ai_assistant.config.config import config 
from app.controllers.retrieval.RetrieverEngine import RetrieverEngine
agikb_engine = RetrieverEngine()

reload_javascript()
with gr.Blocks(css=customCSS, theme=small_and_beautiful_theme) as demo:
    user_question = gr.State("")
    with gr.Row():
        gr.HTML('AGI 助教', elem_id="app_title")
        status_display = gr.Markdown("status", elem_id="status_display")
    with gr.Row().style(equal_height=True):
        with gr.Column(scale=5):        
            with gr.Row():
                chatbot = gr.Chatbot(elem_id="chuanhu_chatbot").style(height="100%")

            with gr.Row():
                with gr.Column(min_width=225, scale=12):
                    user_input = gr.Textbox(
                        elem_id="user_input_tb",
                        show_label=False,
                        placeholder="在这里输入",
                        interactive=True
                    ).style(container=False)
                with gr.Column(min_width=42, scale=1):
                    submit_btn = gr.Button(value="", variant="primary", elem_id="submit_btn")
                    cancel_btn = gr.Button(value="", variant="secondary", visible=False, elem_id="cancel_btn")

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
                # accumulated_response += current_content
                # yield ('', accumulated_response)
                if current_content:
                    history.append(('system', current_content))
                    yield '', history

    def reset_input(input):
        return (
            '',
            input
        )

    # def predict(input, chatHistory):
    #     service = WebAppService(config=config)
    #     for _ in service.predict_yield(input, chatHistory):
    #         yield ('', chatHistory)
        
    def user(input, chatHistory):
        chatHistory.append(('user', input))
        return input, chatHistory

        
    submit_btn.click(fn=reset_input, 
                        inputs=[user_input], 
                        outputs=[user_input, user_question], 
                        queue=False).then(
                        fn=user, 
                        inputs=[user_question, chatbot], 
                        outputs=[user_question, chatbot]).then(
                            fn=slow_echo, 
                            inputs=[user_question, chatbot], 
                            outputs=[user_question, chatbot]
                        )
    user_input.submit(fn=reset_input, inputs=[user_input], outputs=[user_input, user_question], queue=False).then(fn=user, inputs=[user_question, chatbot], outputs=[user_question, chatbot]).then(fn=slow_echo, inputs=[user_question, chatbot], outputs=[user_question, chatbot])

    demo.queue()

if __name__ == "__main__":
    # demo.launch(root_path="/aid/",debug=True)
    demo.launch(debug=True)