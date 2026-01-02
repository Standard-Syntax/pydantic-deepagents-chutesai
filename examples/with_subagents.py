"""Example using subagents for specialized tasks."""

import asyncio
import os
from dotenv import load_dotenv
from pydantic_deep import (
    create_deep_agent,
    DeepAgentDeps,
    StateBackend,
    SubAgentConfig,
)

load_dotenv()


async def main():
    """Demonstrate code generation with subagent review and testing."""
    
    deps = DeepAgentDeps(backend=StateBackend())
    
    # Create agent with specialized subagents
    agent = create_deep_agent(
        model=os.getenv("CHUTES_MODEL", "openai:gpt-4"),
        instructions="You are a senior Python developer.",
        subagents=[
            SubAgentConfig(
                name="code-reviewer",
                description="Expert code reviewer focusing on quality and security",
                instructions="""Review code for:
                - Security vulnerabilities (SQL injection, XSS, etc.)
                - Performance bottlenecks
                - Code style violations (PEP 8)
                - Missing error handling
                - Type safety issues
                - Documentation gaps
                
                Provide specific, actionable feedback with examples.
                """,
            ),
            SubAgentConfig(
                name="test-generator",
                description="Generates comprehensive pytest test suites",
                instructions="""Generate pytest tests that:
                - Cover happy path and edge cases
                - Use fixtures for setup/teardown
                - Include parametrize for multiple test cases
                - Mock external dependencies
                - Have clear, descriptive names
                - Include docstrings explaining what's being tested
                
                Aim for >90% code coverage.
                """,
            ),
            SubAgentConfig(
                name="doc-writer",
                description="Creates comprehensive documentation",
                instructions="""Write documentation that includes:
                - Clear overview and purpose
                - Installation instructions
                - Usage examples with code snippets
                - API reference
                - Common pitfalls and troubleshooting
                - Contributing guidelines
                
                Use Markdown with proper formatting.
                """,
            ),
        ],
    )
    
    # Multi-step workflow with subagents
    result = await agent.run(
        """Build a user authentication system with the following workflow:
        
        1. Create 'auth.py' with:
           - User registration with password hashing
           - Login with JWT token generation
           - Password reset functionality
           - Email verification
        
        2. Use the 'code-reviewer' subagent to review the implementation
        
        3. Based on review feedback, improve the code
        
        4. Use the 'test-generator' subagent to create comprehensive tests
        
        5. Use the 'doc-writer' subagent to create README.md
        
        6. Create requirements.txt
        
        Complete all steps in order and report the final status.
        """,
        deps=deps,
    )
    
    print("\n" + "="*70)
    print("Final Output:")
    print("="*70)
    print(result.output)
    
    # Show files created
    print("\n" + "="*70)
    print("Files Created:")
    print("="*70)
    files = deps.backend.lsinfo("/")
    for file_info in files:
        print(f"  {'[DIR]' if file_info['is_dir'] else '[FILE]'} {file_info['path']}")


if __name__ == "__main__":
    asyncio.run(main())
