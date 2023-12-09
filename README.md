# Teach Assistant 引擎

Teach Assistant (TA) 引擎结合了多样化文档数据的导入及向量数据库管理与OpenAI的先进技术，极大地增强了您私有数据的搜索和处理能力。

## 核心特性
- **多格式兼容性**：支持 JSON、TXT、MD 和 PDF 等多种文件格式的导入。
- **高效向量检索**：提供强大的向量数据搜索功能。
- **流畅对话交互**：支持连续的对话式交互体验。

## 快速安装
安装 TA 引擎极为便捷。仅需执行以下全局安装命令：

```bash
pip install -e .
```

## 环境配置步骤

### 步骤一：设置环境变量

1. **创建 `.env` 文件**：首先，将 `.env.example` 文件复制为一个新的 `.env` 文件。可在终端中使用以下命令实现：

    ```bash
    cp .env.example .env
    ```

2. **配置 OpenAI 密钥**：在 `.env` 文件中填入您的 OpenAI 密钥。
   - 可在 [AGI 课堂手册](https://a.agiclass.ai) 查找 OpenAI API 密钥的获取方法。
   - 在 `OPENAI_API_KEY` 后填入您的密钥。

    示例：

    ```env
    OPENAI_API_KEY='您的OpenAI密钥'
    ```

### 步骤二：获取 Weaviate 数据库配置

1. **注册 Weaviate**：访问 [Weaviate官网](https://console.weaviate.cloud/)，注册账户并登录，创建免费的向量数据库。

2. **配置数据库信息**：获取 `WEAVIATE_URL` 和 `WEAVIATE_API_KEY` 并填写至 `.env` 文件。

    注意：免费服务有效期限为 14 天。

### 步骤三：导入数据

使用以下命令将数据导入 TA 引擎：

```bash
ta import --path data
```

### 步骤四：启动 Web 服务

通过以下命令启动本地 Web 服务：

```bash
python server/web.py
```

服务将在本地端口 http://127.0.0.1:7860 上运行。

## 额外说明

- 配置 `BYPASS_AUTH=1` 环境变量，可在不使用 LDAP 权限的情况下运行程序。