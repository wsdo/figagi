import os
import gradio as gr
customJS = ''
externalScripts = ''
customCSS = ''
GradioTemplateResponseOriginal = gr.routes.templates.TemplateResponse


# 获取脚本所在目录的路径
script_dir = os.path.dirname(__file__)

# 动态拼接路径
# custom_js_file_path = os.path.join(script_dir, "assets", "custom.js")
# custom_js_file_path = os.path.join(script_dir, "assets", "custom.js")

with open(os.path.join(script_dir, "assets", "custom.js"), "r", encoding="utf-8") as f, \
    open(os.path.join(script_dir, "assets", "external-scripts.js"), "r", encoding="utf-8") as f1:
    customJS = f.read()
    externalScripts = f1.read()

with open(os.path.join(script_dir, "assets", "custom.css"), "r", encoding="utf-8") as f:
    customCSS = f.read()

def reload_javascript():
    js = f'<script>{customJS}</script><script async>{externalScripts}</script>'
    def template_response(*args, **kwargs):
        res = GradioTemplateResponseOriginal(*args, **kwargs)
        res.body = res.body.replace(b'</html>', f'{js}</html>'.encode("utf8"))
        res.init_headers()
        return res

    gr.routes.templates.TemplateResponse = template_response

small_and_beautiful_theme = gr.themes.Soft(
    primary_hue=gr.themes.Color(
        c50="rgba(2, 193, 96, 0.1)",
        c100="rgba(2, 193, 96, 0.2)",
        c200="#02C160",
        c300="rgba(2, 193, 96, 0.32)",
        c400="rgba(2, 193, 96, 0.32)",
        c500="rgba(2, 193, 96, 1.0)",
        c600="rgba(2, 193, 96, 1.0)",
        c700="rgba(2, 193, 96, 0.32)",
        c800="rgba(2, 193, 96, 0.32)",
        c900="#02C160",
        c950="#02C160",
    ),
    secondary_hue=gr.themes.Color(
        c50="#576b95",
        c100="#576b95",
        c200="#576b95",
        c300="#576b95",
        c400="#576b95",
        c500="#576b95",
        c600="#576b95",
        c700="#576b95",
        c800="#576b95",
        c900="#576b95",
        c950="#576b95",
    ),
    neutral_hue=gr.themes.Color(
        name="gray",
        c50="#f9fafb",
        c100="#f3f4f6",
        c200="#e5e7eb",
        c300="#d1d5db",
        c400="#B2B2B2",
        c500="#808080",
        c600="#636363",
        c700="#515151",
        c800="#393939",
        c900="#272727",
        c950="#171717",
    ),
    radius_size=gr.themes.sizes.radius_sm,
).set(
    button_primary_background_fill="#06AE56",
    button_primary_background_fill_dark="#06AE56",
    button_primary_background_fill_hover="#07C863",
    button_primary_border_color="#06AE56",
    button_primary_border_color_dark="#06AE56",
    button_primary_text_color="#FFFFFF",
    button_primary_text_color_dark="#FFFFFF",
    button_secondary_background_fill="#F2F2F2",
    button_secondary_background_fill_dark="#2B2B2B",
    button_secondary_text_color="#393939",
    button_secondary_text_color_dark="#FFFFFF",
    # background_fill_primary="#F7F7F7",
    # background_fill_primary_dark="#1F1F1F",
    block_title_text_color="*primary_500",
    block_title_background_fill="*primary_100",
    input_background_fill="#F6F6F6",
)