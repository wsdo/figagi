# FigAGI Engine

The FigAGI (fa) engine integrates multi-document data import functionality and vector database management, combined with the capabilities of the OpenAI model, enhancing the search for private data.

## Core Features
- **Multi-Format Compatibility**: Supports the import of various file formats including JSON, TXT, MD, and PDF.
- **Efficient Vector Retrieval**: Provides powerful vector data search functionality.
- **Smooth Conversational Interaction**: Supports continuous conversational interaction experience.

## Quick Installation
Install `ta` as a global command:

```bash
pip install -e .
```

## Environment Configuration Steps

### Step One: Set Environment Variables

1. **Create `.env` File**: First, copy the `.env.example` file to a new `.env` file. This can be done in the terminal using the following command:

    ```bash
    cp .env.example .env
    ```

2. **Configure OpenAI Key**: Enter your OpenAI key in the `.env` file.
   - The method for obtaining the OpenAI API key can be found in the [AGI Classroom Manual](https://a.agiclass.ai).
   - Enter your key after `OPENAI_API_KEY`.

    Example:

    ```env
    OPENAI_API_KEY='Your OpenAI Key'
    ```

### Step Two: Obtain Weaviate Database Configuration

1. **Register with Weaviate**: Visit the [Weaviate website](https://console.weaviate.cloud/), register an account, and log in to create a free vector database.

2. **Configure Database Information**: Obtain `WEAVIATE_URL` and `WEAVIATE_API_KEY` and fill them in the `.env` file.

    Note: The free service is valid for 14 days.

### Step Three: Import Data

Use the following command to import data into the TA engine:

```bash
ta import --path data
```

### Step Four: Start Web Service

Start the local web service with the following command:

```bash
python server/web.py
```

The service will run on the local port http://127.0.0.1:7860.

## Additional Information

- Configure the `BYPASS_AUTH=1` environment variable to run the program without using LDAP authentication.