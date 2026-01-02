# Pydantic Deep Agents for chutes.ai

Pydantic Deep Agents framework configured for [chutes.ai](https://chutes.ai) provider - enabling autonomous Python code generation with planning, filesystem operations, and subagent delegation.

## Features

- **Planning**: Built-in todo list for task decomposition and tracking
- **Filesystem Operations**: Virtual and real filesystem with read, write, edit, grep, and glob support
- **Subagent Delegation**: Spawn specialized subagents for focused tasks (code review, testing, documentation)
- **Skills System**: Modular capability packages loaded on-demand
- **Multiple Backends**: StateBackend (in-memory), FilesystemBackend (persistent), DockerSandbox (isolated execution)
- **Structured Output**: Type-safe responses using Pydantic models
- **Human-in-the-Loop**: Built-in approval workflows for sensitive operations
- **Streaming Support**: Real-time output for long-running operations

## Installation

### Using uv (recommended)

```bash
# Clone the repository
gh repo clone Standard-Syntax/pydantic-deepagents-chutesai
cd pydantic-deepagents-chutesai

# Install with uv
uv sync
```

### Using pip

```bash
pip install -e .
```

### Optional: Docker Sandbox Support

For isolated code execution:

```bash
uv add pydantic-deep[sandbox]
# or
pip install -e .[sandbox]
```

## Configuration

### 1. Set up environment variables

```bash
cp .env.example .env
```

Edit `.env` and add your chutes.ai API credentials:

```bash
# If chutes.ai uses OpenAI-compatible API
OPENAI_API_KEY=your-chutes-ai-api-key
OPENAI_BASE_URL=https://api.chutes.ai/v1

# Model to use
CHUTES_MODEL=gpt-4  # or your chutes.ai model name
```

### 2. Verify Installation

```bash
uv run python main.py
```

## Usage

### Basic Python Code Generation

```python
import asyncio
from pydantic_deep import create_deep_agent, DeepAgentDeps, StateBackend
import os

async def main():
    # Create agent configured for chutes.ai
    agent = create_deep_agent(
        model=os.getenv("CHUTES_MODEL", "openai:gpt-4"),
        instructions="""You are an expert Python developer.
        When generating code:
        - Use type hints
        - Include comprehensive docstrings
        - Follow PEP 8 style guidelines
        - Write modular, testable code
        - Include error handling
        """,
    )
    
    # Create dependencies with in-memory storage
    deps = DeepAgentDeps(backend=StateBackend())
    
    # Generate Python code
    result = await agent.run(
        """Create a Python module for data validation that:
        1. Defines a User model with email and age validation
        2. Includes a function to validate a list of users
        3. Has comprehensive error handling
        4. Includes unit tests
        """,
        deps=deps,
    )
    
    print(result.output)

if __name__ == "__main__":
    asyncio.run(main())
```

### With Persistent Filesystem

```python
from pydantic_deep import FilesystemBackend

# Use real filesystem for persistent code generation
backend = FilesystemBackend("./workspace", virtual_mode=False)
deps = DeepAgentDeps(backend=backend)

result = await agent.run(
    "Create a Flask REST API with user CRUD operations",
    deps=deps,
)
```

### With Docker Sandbox (Isolated Execution)

```python
from pydantic_ai_backend import DockerSandbox

# Run code in isolated Docker container
backend = DockerSandbox(image="python:3.12-slim")
deps = DeepAgentDeps(backend=backend)

result = await agent.run(
    """Create and run a data analysis script that:
    1. Generates sample data
    2. Performs statistical analysis
    3. Executes the script to verify it works
    """,
    deps=deps,
)
```

### With Subagents for Code Review

```python
from pydantic_deep import SubAgentConfig

agent = create_deep_agent(
    model=os.getenv("CHUTES_MODEL", "openai:gpt-4"),
    subagents=[
        SubAgentConfig(
            name="code-reviewer",
            description="Reviews code for quality, security, and best practices",
            instructions="""You are an expert code reviewer.
            Review code for:
            - Security vulnerabilities
            - Performance issues
            - Code style and maintainability
            - Test coverage
            Provide specific, actionable feedback.
            """,
        ),
        SubAgentConfig(
            name="test-generator",
            description="Generates comprehensive unit tests",
            instructions="""You are a testing expert.
            Generate tests that:
            - Cover edge cases
            - Use pytest best practices
            - Include fixtures and mocks
            - Have clear assertions
            """,
        ),
    ],
)

result = await agent.run(
    """Create a user authentication module, then:
    1. Have the code-reviewer subagent review it
    2. Have the test-generator subagent create tests
    3. Implement any suggested improvements
    """,
    deps=deps,
)
```

### With Structured Output

```python
from pydantic import BaseModel

class CodeAnalysis(BaseModel):
    summary: str
    files_created: list[str]
    complexity_score: int
    recommendations: list[str]

agent = create_deep_agent(
    output_type=CodeAnalysis,
    model=os.getenv("CHUTES_MODEL", "openai:gpt-4"),
)

result = await agent.run(
    "Create a REST API and provide analysis",
    deps=deps,
)

# Type-safe access
print(f"Created {len(result.output.files_created)} files")
print(f"Complexity: {result.output.complexity_score}")
```

### With Human-in-the-Loop Approval

```python
agent = create_deep_agent(
    model=os.getenv("CHUTES_MODEL", "openai:gpt-4"),
    interrupt_on={
        "execute": True,  # Require approval for command execution
        "write_file": True,  # Require approval for file writes
    },
)

result = await agent.run(
    "Create a database migration script and run it",
    deps=deps,
)

# Review and approve/deny each action
if hasattr(result, "deferred_tool_calls"):
    for call in result.deferred_tool_calls:
        print(f"Tool: {call.tool_name}")
        print(f"Args: {call.args}")
        
        response = input("Approve? (y/n): ").lower()
        if response == 'y':
            call.approve()
        else:
            call.deny("Action not approved")
    
    # Resume with decisions
    result = await agent.run(
        result.get_decisions(),
        deps=deps,
        message_history=result.all_messages,
    )
```

## Project Structure

```
pydantic-deepagents-chutesai/
├── main.py                 # Main example
├── examples/               # Additional examples
│   ├── code_generation.py  # Code generation examples
│   ├── with_subagents.py   # Subagent delegation
│   └── with_review.py      # Code review workflow
├── skills/                 # Custom skill packages
│   └── code-review/        # Code review skill
│       └── SKILL.md
├── workspace/              # Generated code workspace
├── pyproject.toml          # Dependencies
├── .env                    # Environment configuration (create from .env.example)
└── README.md               # This file
```

## Chutes.ai Provider Configuration

### OpenAI-Compatible API

If chutes.ai provides an OpenAI-compatible endpoint:

```python
import os
from pydantic_ai.models.openai import OpenAIModel

model = OpenAIModel(
    model_name=os.getenv("CHUTES_MODEL"),
    base_url=os.getenv("OPENAI_BASE_URL"),
    api_key=os.getenv("OPENAI_API_KEY"),
)

agent = create_deep_agent(model=model)
```

### Custom Provider

If chutes.ai requires a custom provider, create a custom model wrapper:

```python
from pydantic_ai import Model
import httpx

class ChutesAIModel(Model):
    def __init__(self, api_key: str, base_url: str, model: str):
        self.api_key = api_key
        self.base_url = base_url
        self.model = model
    
    # Implement required Model protocol methods
    # See: https://ai.pydantic.dev/models/

agent = create_deep_agent(
    model=ChutesAIModel(
        api_key=os.getenv("CHUTES_API_KEY"),
        base_url=os.getenv("CHUTES_BASE_URL"),
        model=os.getenv("CHUTES_MODEL"),
    )
)
```

## Advanced Features

### Context Management with Summarization

```python
from pydantic_deep.processors import create_summarization_processor

processor = create_summarization_processor(
    trigger=("tokens", 100000),  # Summarize when reaching 100k tokens
    keep=("messages", 20),        # Keep last 20 messages
)

agent = create_deep_agent(
    model=os.getenv("CHUTES_MODEL", "openai:gpt-4"),
    history_processors=[processor],
)
```

### Skills System

Create reusable skills in `skills/` directory:

```markdown
<!-- skills/api-design/SKILL.md -->
---
name: api-design
description: RESTful API design best practices
tags: [api, rest, design]
version: 1.0.0
author: standard-syntax
---

# API Design Skill

When designing REST APIs:

1. Use proper HTTP methods (GET, POST, PUT, PATCH, DELETE)
2. Follow resource-based URL patterns
3. Implement pagination for list endpoints
4. Use appropriate status codes
5. Include comprehensive error responses
6. Version your API (e.g., /v1/)
7. Document with OpenAPI/Swagger
```

Load skills:

```python
agent = create_deep_agent(
    skill_directories=[
        {"path": "./skills", "recursive": True}
    ],
)
```

## Development

### Run Tests

```bash
uv run pytest
```

### Code Formatting

```bash
uv run ruff format
uv run ruff check --fix
```

### Type Checking

```bash
uv run pyright
```

## Resources

- [Pydantic Deep Agents Documentation](https://github.com/vstorm-co/pydantic-deepagents)
- [Pydantic AI Documentation](https://ai.pydantic.dev/)
- [chutes.ai Documentation](https://chutes.ai/docs)

## License

MIT License - see LICENSE for details.

## Contributing

Contributions welcome! Please open an issue or submit a pull request.
