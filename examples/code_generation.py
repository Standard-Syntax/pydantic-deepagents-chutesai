"""Simple code generation example with chutes.ai."""

import asyncio
import os
from dotenv import load_dotenv
from pydantic_deep import create_deep_agent, DeepAgentDeps, FilesystemBackend

load_dotenv()


async def main():
    """Generate a Python data analysis module."""
    
    # Use filesystem backend for persistent storage
    backend = FilesystemBackend("./workspace", virtual_mode=False)
    deps = DeepAgentDeps(backend=backend)
    
    agent = create_deep_agent(
        model=os.getenv("CHUTES_MODEL", "openai:gpt-4"),
        instructions="""You are a data science expert. Generate production-ready 
        Python code with proper error handling, type hints, and documentation.""",
    )
    
    result = await agent.run(
        """Create a data analysis module 'src/analytics.py' that:
        
        1. Loads CSV data from a file path
        2. Performs basic statistical analysis (mean, median, std dev)
        3. Detects outliers using IQR method
        4. Generates a summary report
        5. Includes proper logging
        6. Has comprehensive error handling
        
        Also create:
        - requirements.txt with needed packages
        - README.md with usage examples
        - tests/test_analytics.py with unit tests
        """,
        deps=deps,
    )
    
    print(result.output)
    print("\nFiles created in ./workspace/")


if __name__ == "__main__":
    asyncio.run(main())
