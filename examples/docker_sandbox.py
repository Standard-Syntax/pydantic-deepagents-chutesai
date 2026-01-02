"""Example using Docker sandbox for isolated code execution."""

import asyncio
import os
from dotenv import load_dotenv

try:
    from pydantic_ai_backend import DockerSandbox
    from pydantic_deep import create_deep_agent, DeepAgentDeps
    DOCKER_AVAILABLE = True
except ImportError:
    DOCKER_AVAILABLE = False
    print("Docker sandbox not available. Install with: uv add pydantic-deep[sandbox]")

load_dotenv()


async def main():
    """Generate and execute code in isolated Docker container."""
    
    if not DOCKER_AVAILABLE:
        print("\nTo use Docker sandbox:")
        print("1. Install Docker: https://docs.docker.com/get-docker/")
        print("2. Install sandbox support: uv add pydantic-deep[sandbox]")
        print("3. Pull Python image: docker pull python:3.12-slim")
        return
    
    print("🐳 Initializing Docker Sandbox...\n")
    
    # Create Docker sandbox backend
    backend = DockerSandbox(
        image="python:3.12-slim",
        # Optional: mount volumes, set environment variables
        # volumes={"/host/path": {"bind": "/container/path", "mode": "rw"}},
        # environment={"DEBUG": "1"},
    )
    
    deps = DeepAgentDeps(backend=backend)
    
    agent = create_deep_agent(
        model=os.getenv("CHUTES_MODEL", "openai:gpt-4"),
        instructions="""You are a Python developer with access to an isolated 
        Docker container. You can safely execute code and install packages.
        Always verify code works by running it.""",
    )
    
    print("Example 1: Data Processing Script")
    print("="*70 + "\n")
    
    result = await agent.run(
        """Create a Python script that:
        
        1. Generates random sample data (100 records)
        2. Performs statistical analysis:
           - Calculate mean, median, std deviation
           - Find outliers using IQR method
        3. Saves results to 'analysis_results.txt'
        4. EXECUTE the script to verify it works
        5. Show the output
        
        Use only Python standard library (no pip installs for this example).
        """,
        deps=deps,
    )
    
    print(result.output)
    
    print("\n" + "="*70)
    print("Example 2: Package Installation and Usage")
    print("="*70 + "\n")
    
    result = await agent.run(
        """Create and execute a script that:
        
        1. Installs 'requests' package (pip install requests)
        2. Makes an API call to httpbin.org/json
        3. Parses the JSON response
        4. Saves results to 'api_results.json'
        5. Execute the script and show results
        
        Remember: You're in a Docker container, so you can safely install packages!
        """,
        deps=deps,
        message_history=result.all_messages,
    )
    
    print(result.output)
    
    print("\n" + "="*70)
    print("Example 3: Error Handling and Debugging")
    print("="*70 + "\n")
    
    result = await agent.run(
        """Create a script that demonstrates error handling:
        
        1. Try to read a non-existent file
        2. Catch the FileNotFoundError
        3. Create the file with sample content
        4. Read it successfully
        5. Execute the script to show it works
        
        Show both the code and execution output.
        """,
        deps=deps,
        message_history=result.all_messages,
    )
    
    print(result.output)
    
    # Show files created in sandbox
    print("\n" + "="*70)
    print("Files in Docker Container:")
    print("="*70)
    files = deps.backend.lsinfo("/")
    for file_info in files:
        print(f"  {file_info['path']}")
    
    print("\n✅ All examples completed!")
    print("\nDocker sandbox provides:")
    print("  - Isolated execution environment")
    print("  - Safe package installation")
    print("  - Code execution with shell commands")
    print("  - Clean separation from host system")


if __name__ == "__main__":
    if DOCKER_AVAILABLE:
        asyncio.run(main())
    else:
        print("Please install Docker sandbox support first.")
