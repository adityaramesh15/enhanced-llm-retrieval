# Confluence-Enhanced LLM Retrieval

## Overview

This project serves as a privacy-focused business productivity tool, using a company's Confluence Pages to enhance contextualized responses from LLMs. Using Retrieval-Augmented Generation (RAG) system and a locally hosted `Llama 3.1 8B` model through `Ollama`, the system utilized hybrid search (semantic and lexical) with powerful generative capabilities to deliver relevant and contextually aware responses by retrieving pertinent documents and integrating them into the model's generation process.

### Key Features

- **RAG Implementation**: Integrates Retrieval-Augmented Generation to improve the quality and relevance of generated responses by incorporating retrieved documents.
- **Optimized for Llama 3.1**: Uses the latest Llama 3.1 model to ensure high-quality text generation.
- **Hybrid Search Integration**: Employs lexical search using sparse vector embeddings and semantic search using dense vector embeddings through the `all-mpnet-base-v2` model.
- **Confluence API**: Seamlessly retrieves documents from Confluence, enhancing the knowledge base available for generation.
- **Efficient Query Handling**: Ensures minimal latency by avoiding redundant re-embedding processes, through a singleton-pattern, speeding up response times.

## Project Tree
```
enhanced-llm-retrieval/
├── hybrid_search/
│   ├── __init__.py
│   ├── confluence.py
│   ├── database.py
│   ├── embed.py
│   ├── search.py
│   ├── update.py
│   └── utils.py
├── rag_llm/
│   ├── __init__.py
│   ├── model.py
│   ├── rag.py
│   └── response.py
├── main.py
├── .gitignore
├── Dockerfile
├── License
├── README.md
└── requirments.txt
```

## Architecture

### High Level
![high level](./images/high-level.png)

### Low Level
![low level](./images/low-level.png)

## Prerequisites

Before installing and running the project, ensure you have the following:

- Python 3.8 or later
- Required Python packages (see `requirements.txt`)
- Pinecone DB instance and API key
- Confluence Space and API Key
- Ollama

## Getting Started

### Installation

1. **Clone the Repository**  
   First, clone the repository to your local machine:

   ```bash
   git clone https://github.com/adityaramesh15/enhanced-llm-retrieval
   ```

2. **Configuration**  
   Make sure to configure any necessary environment variables or settings, such as API keys for Pinecone Interaction and Confluence Data Retrieval.


### Running
Coming Soon!

## Usage
Coming Soon!

## Troubleshooting

If you encounter issues, please check the following:
- Ensure all dependencies are installed correctly.
- Verify API keys and configurations for external services.

## Limitations

Coming Soon!

## Future Plans

Coming Soon!

## Contribution Guidelines

I welcome contributions from the community! To contribute:

1. **Fork the Repository**: Start by forking the repository on GitHub.
2. **Create a New Branch**: Create a new branch for your feature or bug fix.
3. **Make Your Changes**: Implement your changes and commit them with clear, descriptive messages.
4. **Submit a Pull Request**: Once your changes are complete, submit a pull request with a detailed description of your changes.

Please ensure that your code adheres to the project's coding standards and includes appropriate tests where necessary. For significant changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

