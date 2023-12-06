'''
Author: moemoefish moemoefish@qq.com
Date: 2023-05-02 14:10:56
LastEditors: yuyingtao yuyingtao@agiclas.cn
LastEditTime: 2023-07-04 01:04:38
Description: 
'''
import os

import time
import gradio as gr
from ai_assistant.ui.gradio_utils import reload_javascript, customCSS, small_and_beautiful_theme
from ai_assistant.config.app_config import APP_TITLE
from ai_assistant.ui.page_services.WebAppService import WebAppService
from ai_assistant.config.config import config 

from ai_assistant.authentication.ldap_authectication import ldap_auth

def auth_user(username, password):
    if (config.BYPASS_AUTH): 
        return True
    
    return ldap_auth(username=username, password=password)

reload_javascript()

with gr.Blocks(css=customCSS, theme=small_and_beautiful_theme) as demo:
    user_question = gr.State("")
    with gr.Row():
        gr.HTML(APP_TITLE, elem_id="app_title")
        status_display = gr.Markdown("status", elem_id="status_display")

    # with gr.Row(elem_id="float_display"):
    #     user_info = gr.Markdown(value="getting user info...", elem_id="user_info")
    
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

    def reset_input(input):
        return (
            '',
            input
        )

    def predict(input, chatHistory):
        service = WebAppService(config=config)
        for _ in service.predict_yield(input, chatHistory):
            yield ('', chatHistory)
        
    def user(input, chatHistory):
        chatHistory.append((input, None))
        return (input, chatHistory)
        
    submit_btn.click(fn=reset_input, inputs=[user_input], outputs=[user_input, user_question], queue=False).then(fn=user, inputs=[user_question, chatbot], outputs=[user_question, chatbot]).then(fn=predict, inputs=[user_question, chatbot], outputs=[user_question, chatbot])
    user_input.submit(fn=reset_input, inputs=[user_input], outputs=[user_input, user_question], queue=False).then(fn=user, inputs=[user_question, chatbot], outputs=[user_question, chatbot]).then(fn=predict, inputs=[user_question, chatbot], outputs=[user_question, chatbot])

demo.queue(concurrency_count=20)
demo.title = APP_TITLE
demo.auth = auth_user

