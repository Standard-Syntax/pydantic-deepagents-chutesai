# Copilot Instructions for Pydantic Deep Agents (chutes.ai)

This repository provides a Pydantic Deep Agents framework configured for the chutes.ai provider, enabling autonomous Python code generation with planning, filesystem operations, and subagent delegation.

## Project Overview

- **Framework**: Pydantic Deep Agents with Pydantic AI
- **Provider**: chutes.ai (OpenAI-compatible API)
- **Language**: Python 3.10+
- **Package Manager**: uv (recommended) or pip
- **Key Features**: Planning, filesystem operations, subagent delegation, skills system, multiple backends

## Python Coding Standards

### General Guidelines

- **Python Version**: Target Python 3.10+ features
- **Style Guide**: Follow PEP 8 strictly
- **Line Length**: Maximum 100 characters (configured in pyproject.toml)
- **Type Hints**: Always use type hints for all function signatures and return types
- **Docstrings**: Use Google-style docstrings for all public functions, classes, and modules
- **Imports**: Use ruff's import sorting (configured in pyproject.toml)

### Type Hints

```python
# Always include type hints
def process_data(input_data: list[str], max_items: int = 10) -> dict[str, Any]:
    """Process input data and return results."""
    ...

# Use Pydantic models for structured data
from pydantic import BaseModel

class UserConfig(BaseModel):
    email: str
    age: int
    username: str
```

### Docstrings

Use Google-style docstrings consistently:

```python
def validate_users(user_dicts: list[dict]) -> list[User]:
    """Validate a list of user dictionaries.

    Args:
        user_dicts: List of dictionaries containing user data.

    Returns:
        List of validated User model instances.

    Raises:
        ValidationError: If any user data is invalid.
    """
    ...
```

### Error Handling

- Use specific exception types, not bare `except:`
- Create custom exception hierarchies when appropriate
- Include context in exception messages
- Use context managers (`with` statements) for resource management

```python
# Good
try:
    result = process_file(path)
except FileNotFoundError as e:
    logger.error(f"File not found: {path}", exc_info=True)
    raise

# Bad
try:
    result = process_file(path)
except:
    pass
```

## Pydantic Deep Agents Conventions

### Agent Creation

Always use `create_deep_agent` with clear, specific instructions:

```python
from pydantic_deep import create_deep_agent, DeepAgentDeps, StateBackend

agent = create_deep_agent(
    model=os.getenv("CHUTES_MODEL", "openai:gpt-4"),
    instructions="""Clear, specific instructions about the agent's role
    and expected behavior. Include coding standards and conventions.""",
)
```

### Dependencies and Backends

- **StateBackend**: Use for in-memory operations (testing, demos)
- **FilesystemBackend**: Use for persistent file generation
- **DockerSandbox**: Use for isolated code execution (requires optional dependency)

```python
# In-memory
deps = DeepAgentDeps(backend=StateBackend())

# Persistent filesystem
from pydantic_deep import FilesystemBackend
deps = DeepAgentDeps(backend=FilesystemBackend("./workspace", virtual_mode=False))
```

### Subagents

When using subagents, provide clear, focused instructions:

```python
from pydantic_deep import SubAgentConfig

subagents = [
    SubAgentConfig(
        name="code-reviewer",
        description="Reviews code for quality, security, and best practices",
        instructions="""Specific review criteria and focus areas...""",
    ),
]
```

## Skills System

### Creating Skills

Skills are defined in Markdown files with frontmatter in the `skills/` directory:

```markdown
---
name: skill-name
description: Brief description of the skill
tags: [tag1, tag2, tag3]
version: 1.0.0
author: standard-syntax
---

# Skill Name

Detailed skill content and guidelines...
```

### Skills Directory Structure

```
skills/
├── skill-name/
│   └── SKILL.md
└── another-skill/
    └── SKILL.md
```

### Loading Skills

```python
agent = create_deep_agent(
    skill_directories=[
        {"path": "./skills", "recursive": True}
    ],
)
```

## Testing

### Running Tests

```bash
# Run all tests
uv run pytest

# Run specific test file
uv run pytest tests/test_example.py

# Run with coverage
uv run pytest --cov=src
```

### Test Structure

- Place tests in `tests/` directory
- Use `pytest` framework (configured for async support)
- Follow naming convention: `test_*.py` for files, `test_*` for functions
- Use `pytest-asyncio` for async tests (asyncio_mode set to "auto")

### Writing Tests

```python
import pytest
from pydantic_deep import create_deep_agent, DeepAgentDeps, StateBackend

@pytest.mark.asyncio
async def test_agent_creation():
    """Test basic agent creation and execution."""
    agent = create_deep_agent(model="openai:gpt-4")
    deps = DeepAgentDeps(backend=StateBackend())
    
    result = await agent.run("Simple task", deps=deps)
    assert result.output is not None
```

## Code Quality Tools

### Linting and Formatting

```bash
# Format code
uv run ruff format

# Check and fix linting issues
uv run ruff check --fix

# Check without fixing
uv run ruff check
```

### Type Checking

```bash
# Run type checker
uv run pyright
```

### Ruff Configuration

- Line length: 100 characters
- Target: Python 3.10
- Selected rules: E (errors), F (pyflakes), I (isort), UP (pyupgrade), B (bugbear), SIM (simplify), Q (quotes)

## Environment Configuration

### Required Environment Variables

Create `.env` file from `.env.example`:

```bash
# chutes.ai API configuration
OPENAI_API_KEY=your-chutes-ai-api-key
OPENAI_BASE_URL=https://api.chutes.ai/v1

# Model to use (can be just model name or with provider prefix)
# The code will use "openai:gpt-4" as default if not set
CHUTES_MODEL=gpt-4
# or with provider prefix:
# CHUTES_MODEL=openai:gpt-4
```

### Loading Environment Variables

```python
from dotenv import load_dotenv
import os

load_dotenv()
model = os.getenv("CHUTES_MODEL", "openai:gpt-4")
```

## Project Structure

```
pydantic-deepagents-chutesai/
├── .github/                # GitHub configuration and workflows
│   └── copilot-instructions.md
├── examples/               # Example implementations
│   ├── code_generation.py
│   ├── with_subagents.py
│   ├── with_review.py
│   └── docker_sandbox.py
├── skills/                 # Custom skill packages
│   └── code-review/
│       └── SKILL.md
├── tests/                  # Test files (if added)
├── workspace/              # Generated code workspace (gitignored)
├── main.py                 # Main example entry point
├── code_gen_workflow.py    # Multi-agent workflow structure
├── pyproject.toml          # Project dependencies and config
├── .env.example            # Example environment variables
├── .gitignore              # Git ignore patterns
├── README.md               # Project documentation
└── LICENSE                 # MIT License
```

## Dependencies

### Core Dependencies

- `pydantic-deep>=0.2.9`: Deep agent framework
- `pydantic-ai>=0.1.0`: Pydantic AI library
- `pydantic>=2.0`: Data validation using Python type hints
- `httpx>=0.28.1`: HTTP client for API calls
- `python-dotenv>=1.0.0`: Environment variable management
- `rich>=13.0.0`: Terminal output formatting

### Dev Dependencies

- `pytest>=9.0.0`: Testing framework
- `pytest-asyncio>=0.23.0`: Async test support
- `ruff>=0.8.0`: Fast Python linter and formatter
- `pyright>=1.1.0`: Static type checker

### Optional Dependencies

- `pydantic-ai-backend[docker]>=0.0.3`: For DockerSandbox support (install with `pip install -e .[sandbox]` or `uv sync --extra sandbox`)

## Installation Commands

```bash
# Recommended: Using uv
uv sync

# Alternative: Using pip
pip install -e .

# With dev dependencies
pip install -e .[dev]

# With sandbox support (for DockerSandbox backend)
pip install -e .[sandbox]
# or with uv:
# uv sync --extra sandbox
```

## Best Practices

1. **Modular Code**: Keep functions focused and single-purpose
2. **Type Safety**: Use Pydantic models for data validation and structured output
3. **Error Handling**: Always handle errors gracefully with specific exceptions
4. **Logging**: Use Python's logging module for debugging (avoid print statements in production code)
5. **Testing**: Write tests for critical functionality
6. **Documentation**: Keep README and docstrings up to date
7. **Security**: Never commit `.env` files or API keys
8. **Resource Management**: Use context managers for file operations and connections
9. **Async/Await**: Use async functions properly with `asyncio.run()` or in async contexts
10. **Code Review**: Leverage the code-review skill for quality assurance

## Common Patterns

### Basic Agent Usage

```python
import asyncio
import os
from pydantic_deep import create_deep_agent, DeepAgentDeps, StateBackend

async def main():
    agent = create_deep_agent(
        model=os.getenv("CHUTES_MODEL", "openai:gpt-4"),
        instructions="You are an expert Python developer...",
    )
    
    deps = DeepAgentDeps(backend=StateBackend())
    
    result = await agent.run("Your task description", deps=deps)
    print(result.output)

if __name__ == "__main__":
    asyncio.run(main())
```

### Structured Output

```python
from pydantic import BaseModel

class CodeAnalysis(BaseModel):
    summary: str
    files_created: list[str]
    complexity_score: int

agent = create_deep_agent(
    output_type=CodeAnalysis,
    model=os.getenv("CHUTES_MODEL", "openai:gpt-4"),
)
```

### Conversation Continuation

```python
# First call
result1 = await agent.run("Create a module", deps=deps)

# Continue conversation with context
result2 = await agent.run(
    "Add tests to the module",
    deps=deps,
    message_history=result1.all_messages,
)
```

## Notes for Copilot

- When generating code, always include proper type hints and docstrings
- Follow the existing code style and patterns in the repository
- Use async/await patterns consistently
- Leverage Pydantic models for data validation
- Consider using subagents for complex, multi-step tasks
- Test with StateBackend first before using FilesystemBackend
- Reference the skills system for code review and quality assurance
- Keep the chutes.ai provider configuration in mind when working with model settings
