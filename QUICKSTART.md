# Quick Start Guide

Get up and running with Pydantic Deep Agents + chutes.ai in under 5 minutes.

## 1. Clone and Install

```bash
# Clone the repository
gh repo clone Standard-Syntax/pydantic-deepagents-chutesai
cd pydantic-deepagents-chutesai

# Install with uv (recommended)
uv sync

# OR with pip
pip install -e .
```

## 2. Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit .env and add your chutes.ai API key
# If chutes.ai uses OpenAI-compatible API:
OPENAI_API_KEY=your-chutes-ai-api-key
OPENAI_BASE_URL=https://api.chutes.ai/v1
CHUTES_MODEL=gpt-4
```

## 3. Run Your First Example

```bash
# Run the main example
uv run python main.py

# OR with regular python
python main.py
```

This will:
- Create a data validation module
- Generate a Flask REST API
- Show all created files

## 4. Try More Examples

### Simple Code Generation

```bash
uv run python examples/code_generation.py
```

Generates a data analysis module with tests in `./workspace/`.

### Code Review with Subagents

```bash
uv run python examples/with_subagents.py
```

Demonstrates:
- Code generation
- Automated code review by subagent
- Test generation by subagent
- Documentation generation

### Structured Output with Review

```bash
uv run python examples/with_review.py
```

Shows:
- Type-safe structured output
- Automated code quality assessment
- Iterative improvement based on review

### Docker Sandbox (Isolated Execution)

```bash
# Install Docker support
uv add pydantic-deep[sandbox]

# Run sandbox example
uv run python examples/docker_sandbox.py
```

## 5. Create Your Own Agent

Create a new file `my_agent.py`:

```python
import asyncio
import os
from dotenv import load_dotenv
from pydantic_deep import create_deep_agent, DeepAgentDeps, StateBackend

load_dotenv()

async def main():
    # Create agent
    agent = create_deep_agent(
        model=os.getenv("CHUTES_MODEL", "openai:gpt-4"),
        instructions="You are a helpful Python coding assistant.",
    )
    
    # Create dependencies
    deps = DeepAgentDeps(backend=StateBackend())
    
    # Run agent
    result = await agent.run(
        "Create a simple calculator module with add, subtract, multiply, divide functions",
        deps=deps,
    )
    
    print(result.output)

if __name__ == "__main__":
    asyncio.run(main())
```

Run it:

```bash
uv run python my_agent.py
```

## Common Use Cases

### Generate API Endpoint

```python
result = await agent.run(
    """Create a FastAPI endpoint for user registration:
    - Email validation
    - Password strength checking
    - Hash password with bcrypt
    - Return JWT token
    - Include error handling
    """,
    deps=deps,
)
```

### Generate Tests

```python
result = await agent.run(
    """Review the code in src/auth.py and create comprehensive 
    pytest tests in tests/test_auth.py covering:
    - Happy path scenarios
    - Edge cases
    - Error conditions
    - Security validations
    """,
    deps=deps,
)
```

### Refactor Code

```python
result = await agent.run(
    """Refactor src/legacy.py to:
    - Add type hints
    - Extract functions with single responsibility
    - Add comprehensive docstrings
    - Improve error handling
    - Add logging
    - Follow PEP 8
    """,
    deps=deps,
)
```

### Generate Documentation

```python
result = await agent.run(
    """Create API documentation for the endpoints in src/api.py:
    - OpenAPI/Swagger spec
    - README with usage examples
    - Include curl examples
    - Document all parameters and responses
    """,
    deps=deps,
)
```

## Key Features to Explore

### 1. Persistent Storage

```python
from pydantic_deep import FilesystemBackend

backend = FilesystemBackend("./my-project", virtual_mode=False)
deps = DeepAgentDeps(backend=backend)
# Files will be saved to ./my-project/
```

### 2. Subagents for Specialization

```python
from pydantic_deep import SubAgentConfig

agent = create_deep_agent(
    subagents=[
        SubAgentConfig(
            name="security-auditor",
            description="Security vulnerability scanner",
            instructions="Find and report security issues...",
        ),
    ],
)
```

### 3. Structured Output

```python
from pydantic import BaseModel

class CodeAnalysis(BaseModel):
    complexity: int
    issues: list[str]
    score: float

agent = create_deep_agent(output_type=CodeAnalysis)
result = await agent.run("Analyze src/app.py", deps=deps)
print(f"Complexity: {result.output.complexity}")
```

### 4. Skills System

```python
agent = create_deep_agent(
    skill_directories=[{"path": "./skills", "recursive": True}],
)
# Agent automatically discovers and uses skills in ./skills/
```

### 5. Human-in-the-Loop

```python
agent = create_deep_agent(
    interrupt_on={
        "execute": True,  # Approve shell commands
        "write_file": True,  # Approve file writes
    },
)
```

## Next Steps

1. ✅ **Read the full [README.md](README.md)** for detailed documentation
2. 📖 **Explore [examples/](examples/)** for more use cases
3. 🔧 **Customize agent instructions** for your specific needs
4. 🧠 **Create custom skills** in `skills/` directory
5. 🚀 **Build your own workflows** combining multiple agents

## Troubleshooting

### API Key Issues

```bash
# Verify environment variable is set
echo $OPENAI_API_KEY

# Or check .env file
cat .env
```

### Import Errors

```bash
# Ensure Python 3.10+
python --version

# Reinstall dependencies
uv sync --force
```

### Docker Issues (for sandbox)

```bash
# Check Docker is running
docker ps

# Pull Python image
docker pull python:3.12-slim
```

## Support

- 📚 [Pydantic Deep Agents Docs](https://github.com/vstorm-co/pydantic-deepagents)
- 🔧 [Pydantic AI Docs](https://ai.pydantic.dev/)
- 💬 [GitHub Issues](https://github.com/Standard-Syntax/pydantic-deepagents-chutesai/issues)

Happy coding! 🚀
