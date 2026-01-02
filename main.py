"""Main example for Pydantic Deep Agents with chutes.ai provider."""

import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv
from pydantic_deep import create_deep_agent, DeepAgentDeps, StateBackend

# Load environment variables
load_dotenv()


async def main():
    """Run example code generation with chutes.ai."""
    
    # Get model configuration from environment
    model = os.getenv("CHUTES_MODEL", "openai:gpt-4")
    
    print(f"🚀 Initializing Pydantic Deep Agent with chutes.ai")
    print(f"📦 Model: {model}\n")
    
    # Create agent with chutes.ai configuration
    agent = create_deep_agent(
        model=model,
        instructions="""You are an expert Python developer specializing in clean, 
        production-ready code. When generating code:
        
        - Use type hints for all function signatures
        - Include comprehensive docstrings (Google style)
        - Follow PEP 8 and modern Python best practices
        - Write modular, testable code with single responsibility
        - Include proper error handling with specific exceptions
        - Add logging where appropriate
        - Consider edge cases and input validation
        
        Always explain your approach and decisions.
        """,
    )
    
    # Create dependencies with in-memory backend
    deps = DeepAgentDeps(backend=StateBackend())
    
    # Example 1: Simple code generation
    print("\n" + "="*70)
    print("Example 1: Data Validation Module")
    print("="*70 + "\n")
    
    result = await agent.run(
        """Create a Python module called 'validators.py' that includes:
        
        1. A User model using Pydantic with:
           - email: must be valid email format
           - age: must be between 13 and 120
           - username: alphanumeric, 3-20 characters
           
        2. A function to validate a list of user dictionaries
           - Returns list of validated User objects
           - Collects and reports all validation errors
           
        3. Include comprehensive docstrings
        4. Add example usage in if __name__ == "__main__" block
        """,
        deps=deps,
    )
    
    print("\n📝 Agent Response:")
    print(result.output)
    
    # Example 2: Multi-file project
    print("\n" + "="*70)
    print("Example 2: REST API with Flask")
    print("="*70 + "\n")
    
    result = await agent.run(
        """Create a simple Flask REST API for a todo list application:
        
        1. Create 'app.py' with:
           - Flask app setup
           - CRUD endpoints for todos (GET, POST, PUT, DELETE)
           - In-memory storage (list)
           - Proper error handling and status codes
           
        2. Create 'models.py' with:
           - Todo Pydantic model (id, title, completed, created_at)
           
        3. Create 'requirements.txt' with dependencies
        
        4. Create 'README.md' with:
           - Setup instructions
           - API endpoint documentation
           - Example curl commands
        """,
        deps=deps,
        message_history=result.all_messages,  # Continue conversation
    )
    
    print("\n📝 Agent Response:")
    print(result.output)
    
    # Show created files
    print("\n" + "="*70)
    print("📁 Created Files:")
    print("="*70 + "\n")
    
    files = deps.backend.lsinfo("/")
    for file_info in files:
        icon = "📁" if file_info["is_dir"] else "📄"
        print(f"{icon} {file_info['path']}")
    
    print("\n✅ Examples completed!")
    print("\nNext steps:")
    print("1. Check the created files using the backend")
    print("2. Try with FilesystemBackend for persistent storage")
    print("3. Explore subagents for code review")
    print("4. Add human-in-the-loop approval for sensitive operations")


if __name__ == "__main__":
    asyncio.run(main())
