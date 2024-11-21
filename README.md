# Overview

A Chrome extension that uses AI agents to help users negotiate the best deals.


<!-- [Website](https://contract-neg-system.streamlit.app/)

![UI](https://res.cloudinary.com/dfeirxlea/image/upload/v1731425753/portfolio/fsqjubnndrawnp9ezimq.png)

![Terminal](https://res.cloudinary.com/dfeirxlea/image/upload/v1731425419/portfolio/mytqa9jtu8yexf6oc0k8.png) -->


## Table of Contents
*generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [Table of Contents](#table-of-contents)
- [Overview](#overview-1)
- [Key Features](#key-features)
- [Technologies Used](#technologies-used)
- [Project Structure](#project-structure)
- [Setup](#setup)
- [Usage](#usage)
- [Development](#development)
- [Package Management](#package-management)
- [Customizing AI Agents](#customizing-ai-agents)
- [Modifying Prompts](#modifying-prompts)
- [Contributing](#contributing)
- [Troubleshooting](#troubleshooting)


## Overview

A Chrome extension that uses AI agents to help the user negotiate the best deals:

1. **Context & Goal Setting**:
   - From the chrome extention, ask users about their goals of the deal.
   - Use Pydantic to define the schema via models

2. **Negotiation Starts**:
   - Employ Llama 3.1 (running on Together AI) and call `/browse` API endpoint via FastAPI
   - Record the log on the negotiation.log to track the conversation

3. **User Interaction**:
   - Presents the seller's response and ask for a counter response.
   - Allows the buyer to choose whether to accept or renegotiate.

4. **Response Generation**:
   - Collect user input.
   - Passes the information back to Llama 3.1 on Together AI.
   - Generates response to the end user.

## Key Features

- Collect user inputs via Chrome extention
- Use Pydantic to build a schema and validate the inputs
- AI-driven context analysis & negotiation converation using Llama 3.1 on Together AI
- Call API via FastAPI and render response on the user-friendly interface
- Automated generation of response drafts using Llama 3.1


## Technologies Used
[data-doc-management]

   - Upstage: Converts natural language queries into SQL. In this project use Document Parser API to convert contracts to text format [Doc](https://console.upstage.ai/docs/getting-started/overview)
   - Chroma DB: Vector database for storing and querying standard contract clauses
   - SQLite: Database for storing application data

[ai-model-curation]

   - Together AI: Hosting Llama 3.1 for text processing, clause segmentation, and response generation

[deployment-framework]

   - Python: Primary programming language
   - Poetry: Backend build system and package installer/resolver [doc](https://python-poetry.org/docs/)
   - Pydantic: Data validation library for Python
   - Fast API: Web framework for building APIs based on standard Python type hints
   - Replit: Deploy Fast API on Replit server (See the `.replit` and `replit.nix` for its configuration.)


## Project Structure

```
.
frontend
backend
├── backend
│   └── __init__.py
│   └── api.py = connect with database
│   └── main.py = build fastAPI connection
├── Prompts
│   └── Browse.py
│   └── Negotiate.py
│   └── Validate.py
└── tests
│   └── __init__.py
│   └── test_endpoint.py: test connection to the browser endpoint
│   └── test_negotiation.py: test and log the negotiation process and outcome
├── pyproject.toml
└── poetry.lock
```

## Setup

1. Install the `poetry` package manager:
   ```
   curl -sSL https://install.python-poetry.org | python -
   poetry --version
   ```

2. Install dependencies on pyproject.toml:
   ```
   poetry install
   ```

3. Set up environment variables:
   Create a `.env` file in the project root and add the following:
   ```
   TOGETHER_API_KEY=your_together_api_key
   DATABASE_URL=your_database_url
   ```

## Usage

1. Test the negotiation process and outcome on terminal:
   ```
   poetry run neg
   ```
   The outcome will be recorded in the negotiation.log file.


2. In a separate terminal, test the connection to the client interface:
   ```
   poetry run client
   ```
   The results will be printed on your terminal.
   When you update the `main.py`, run this command to see if

   The backend will be available at `http://localhost:8000`.



## Development

### Package Management with poetry

- Add a package: `poetry add <package>`
- Remove a package: `poetry remove <package>`
- Run a command in the virtual environment: add a script to pyproject.toml, then `poetry run <command>`
- To reinstall all the package: after deleting poetry.lock file, run `poetry install`

[poetry cli](https://python-poetry.org/docs/cli/#add)



### Customizing AI Agents

To modify or add new AI agents, edit the `test_negotiation.py` file to test on the terminal, and/or edit the `main.py` file to apply the modification to the API.

### Modifying Prompts

Necessary prompts are stored in the `Prompts` folder. Add or modify the prompt accordingly.

(To avoid errors, we recommend adding a new prompt file to the Prompt folder.)


## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/your-amazing-feature`)
3. Commit your changes (`git commit -m 'Add your-amazing-feature'`)
4. Push to the branch (`git push origin feature/your-amazing-feature`)
5. Open a pull request



## Troubleshooting

Common issues and solutions:
- API key errors: Ensure all API keys in the `.env` file are correct and up to date.
- Database connection issues: Check if the Chroma DB is properly initialized and accessible.
- Memory errors: If processing large contracts, you may need to increase the available memory for the Python process.
- Issues related to the AI agents: Check the `negotiation.log` file for detailed error messages and stack traces.
