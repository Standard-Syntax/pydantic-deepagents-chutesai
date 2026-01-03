"""Foundational structure for multi-agent code generation system.

This module provides the core workflow orchestration for a multi-agent code
generation system using pydantic_deep agents. It defines the state management
structure and initialization logic for the workflow.
"""

import asyncio
import os

from dotenv import load_dotenv
from pydantic import BaseModel, Field
from pydantic_deep import (
    DeepAgentDeps,
    StateBackend,
    create_deep_agent,
)

# Load environment variables
load_dotenv()


class WorkflowState(BaseModel):
    """Tracks the state of the code generation workflow.

    This model maintains all the critical information about a code generation
    workflow execution, including the original request, task decomposition,
    implementation progress, and review feedback.

    Attributes:
        user_request: The original user specification or requirement.
        tasks: List of decomposed subtasks derived from the user request.
        implementation_status: Mapping of task identifiers to their current status.
        files_generated: List of file paths that have been generated during workflow.
        review_feedback: Collection of feedback items from code review processes.
        iteration_count: Current number of refinement iterations completed.
        max_iterations: Maximum allowed refinement iterations (default: 3).
    """

    user_request: str
    tasks: list[str]
    implementation_status: dict[str, str]
    files_generated: list[str]
    review_feedback: list[str]
    iteration_count: int
    max_iterations: int = Field(default=3)


def initialize_orchestrator():
    """Initialize and configure the Orchestrator Agent.

    Creates an orchestrator agent configured with the necessary toolsets and
    instructions for coordinating the multi-agent code generation workflow.

    Returns:
        Configured deep agent instance ready to coordinate workflow execution.
    """
    model = os.getenv("CHUTES_MODEL", "openai:gpt-4.1")

    orchestrator = create_deep_agent(
        model=model,
        instructions=(
            "You are an Orchestrator Agent responsible for coordinating a "
            "code generation workflow. Your role is to:\n"
            "1. Receive and validate user requests/specifications\n"
            "2. Coordinate task decomposition\n"
            "3. Monitor implementation progress\n"
            "4. Coordinate code review\n"
            "5. Decide when to iterate or exit based on review feedback\n"
            "6. Maintain workflow state throughout the process\n"
            "Always provide clear status updates and reasoning for decisions."
        ),
        include_todo=True,
        include_filesystem=True,
        include_subagents=True,
    )

    return orchestrator


async def main() -> None:
    """Initialize and run the multi-agent code generation workflow.

    This function sets up the foundational components for the code generation
    workflow including the state backend, dependencies, and initial workflow state.
    It initializes the orchestrator agent and processes a sample user request.
    """
    try:
        # Initialize the state backend for managing workflow state
        deps = DeepAgentDeps(backend=StateBackend())

        # Define sample user request
        user_request = (
            "Create a Python module for calculating Fibonacci numbers "
            "with proper error handling and type hints"
        )

        # Set up the workflow state object with initial values
        workflow_state = WorkflowState(
            user_request=user_request,
            tasks=[],
            implementation_status={},
            files_generated=[],
            review_feedback=[],
            iteration_count=0,
            max_iterations=3,
        )

        # Print welcome message indicating system initialization
        print("🚀 Multi-Agent Code Generation System Initialized")
        print("=" * 70)
        print(f"✓ State Backend: {type(deps.backend).__name__}")
        print(f"✓ Workflow State: {type(workflow_state).__name__}")
        print(f"✓ Max Iterations: {workflow_state.max_iterations}")
        print("=" * 70)
        print("\n🔧 Initializing Orchestrator Agent...\n")

        # Initialize orchestrator agent
        orchestrator = initialize_orchestrator()
        model_name = os.getenv("CHUTES_MODEL", "openai:gpt-4.1")
        print(f"✓ Orchestrator Agent initialized with model: {model_name}")

        # Call orchestrator agent with the user request
        print("\n" + "=" * 70)
        print("📋 Processing User Request")
        print("=" * 70)
        print(f"Request: {user_request}\n")

        orchestrator_prompt = (
            f"Process this user request and initialize the workflow: {user_request}"
        )

        result = await orchestrator.run(
            orchestrator_prompt,
            deps=deps,
        )

        # Print orchestrator's response
        print("\n" + "=" * 70)
        print("🤖 Orchestrator Response")
        print("=" * 70)
        print(result.output)

        # Log workflow state after orchestrator initialization
        print("\n" + "=" * 70)
        print("📊 Workflow State After Initialization")
        print("=" * 70)
        print(f"User Request: {workflow_state.user_request}")
        print(f"Tasks: {workflow_state.tasks}")
        print(f"Implementation Status: {workflow_state.implementation_status}")
        print(f"Files Generated: {workflow_state.files_generated}")
        print(f"Review Feedback: {workflow_state.review_feedback}")
        print(f"Iteration Count: {workflow_state.iteration_count}")
        print(f"Max Iterations: {workflow_state.max_iterations}")
        print("=" * 70)
        print("\n✅ Orchestrator initialization complete!\n")

    except Exception as e:
        print(f"\n❌ Error during workflow execution: {e}")
        print(f"Error type: {type(e).__name__}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
