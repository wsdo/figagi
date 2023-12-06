<!--
 * @Author: yuyingtao yuyingtao@agiclas.cn
 * @Date: 2023-06-18 00:15:59
 * @LastEditors: yuyingtao yuyingtao@agiclass.ai
 * @LastEditTime: 2023-07-02 14:14:37
 * @Description: 
-->
# 爬取公众号所有文章链接

1. 登录[公众号后台](https://mp.weixin.qq.com/)
    1. 新建一篇文章
    2. 打开浏览器 Developer Tools
    3. 点「超链接」
    4. 「选择其他公众号」
    5. 输入公众号名，回车，选中公众号
    6. 在 Devtools 的 Network 中找到 `appmsg` 请求
    7. 记下参数里的 `fakeid` 和 `token`
    8. 记下请求 Header 里的 Cookie
2. 创建 .env 文件，填入上面的参数

```bash
COOKIE="..."
FAKEID="..."
TOKEN="..."
BEGIN="..." # 用于在限流后进行续传的字段，对应上面所述的 appmsg 链接中的 begin 字段
```

3. 运行 `scrapy crawl wx_article_list -o wx_article_list.json --output-format=json`，所有文章标题和链接会存入 `wx_article_list.json` 文件中。

# 爬取文章内容

## 爬取单篇文章

运行下面命令将指定 url 的文章内容爬取，并存入 `wx_article.json`：

 ```bash
 scrapy crawl wx_article -a url="https://mp.weixin.qq.com/......" -o wx_article.json --output-format=json
 ```

 ## 爬取 json 文件中的所有文章

```bash
scrapy crawl wx_article -a json="wx_article_list.json" -o wx_article.json --output-format=json
```

## 爬取文章后上传到 ai 助手
在上述的爬取文章内容时，在 `.env` 中设置 `SERVER_TOKEN=...`，即可在爬取到文章时，自动上传到 AI 助手

