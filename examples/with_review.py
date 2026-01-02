"""Example demonstrating human-in-the-loop code review workflow."""

import asyncio
import os
from dotenv import load_dotenv
from pydantic_deep import create_deep_agent, DeepAgentDeps, StateBackend
from pydantic import BaseModel

load_dotenv()


class CodeReview(BaseModel):
    """Structured output for code review."""
    files_created: list[str]
    security_issues: list[str]
    performance_issues: list[str]
    style_issues: list[str]
    recommendations: list[str]
    overall_score: int  # 1-10
    ready_for_production: bool


async def main():
    """Generate code with automated review and approval workflow."""
    
    deps = DeepAgentDeps(backend=StateBackend())
    
    # Step 1: Generate code with structured output
    agent = create_deep_agent(
        model=os.getenv("CHUTES_MODEL", "openai:gpt-4"),
        output_type=CodeReview,
        instructions="""You are a code generation and review expert.
        Generate code and provide comprehensive review.""",
    )
    
    print("Step 1: Generating code...\n")
    
    result = await agent.run(
        """Create a REST API endpoint handler for user management:
        
        1. Create 'handlers/users.py' with:
           - GET /users - list users with pagination
           - GET /users/{id} - get user by ID
           - POST /users - create user
           - PUT /users/{id} - update user
           - DELETE /users/{id} - delete user
        
        2. Include input validation
        3. Add error handling
        4. Implement rate limiting
        
        After creating the code, perform a comprehensive review and return
        structured analysis including security, performance, and style issues.
        """,
        deps=deps,
    )
    
    review = result.output
    
    print("="*70)
    print("Code Review Results:")
    print("="*70)
    print(f"\nFiles Created: {', '.join(review.files_created)}")
    print(f"\nOverall Score: {review.overall_score}/10")
    print(f"Production Ready: {'✅ Yes' if review.ready_for_production else '❌ No'}")
    
    if review.security_issues:
        print("\n🔒 Security Issues:")
        for issue in review.security_issues:
            print(f"  - {issue}")
    
    if review.performance_issues:
        print("\n⚡ Performance Issues:")
        for issue in review.performance_issues:
            print(f"  - {issue}")
    
    if review.style_issues:
        print("\n🎨 Style Issues:")
        for issue in review.style_issues:
            print(f"  - {issue}")
    
    if review.recommendations:
        print("\n💡 Recommendations:")
        for rec in review.recommendations:
            print(f"  - {rec}")
    
    # Step 2: If not production ready, improve the code
    if not review.ready_for_production:
        print("\n" + "="*70)
        print("Step 2: Improving code based on review...")
        print("="*70 + "\n")
        
        # Create a new agent for improvements (no structured output)
        improvement_agent = create_deep_agent(
            model=os.getenv("CHUTES_MODEL", "openai:gpt-4"),
        )
        
        improvement_prompt = f"""Based on the code review, fix the following issues:
        
        Security Issues:
        {chr(10).join(f'- {issue}' for issue in review.security_issues)}
        
        Performance Issues:
        {chr(10).join(f'- {issue}' for issue in review.performance_issues)}
        
        Style Issues:
        {chr(10).join(f'- {issue}' for issue in review.style_issues)}
        
        Implement all recommendations:
        {chr(10).join(f'- {rec}' for rec in review.recommendations)}
        
        Update the files and verify all issues are resolved.
        """
        
        improvement_result = await improvement_agent.run(
            improvement_prompt,
            deps=deps,
            message_history=result.all_messages,
        )
        
        print(improvement_result.output)
    else:
        print("\n✅ Code is production ready!")
    
    # Show final files
    print("\n" + "="*70)
    print("Final Files:")
    print("="*70)
    files = deps.backend.lsinfo("/")
    for file_info in files:
        print(f"  {file_info['path']}")


if __name__ == "__main__":
    asyncio.run(main())
