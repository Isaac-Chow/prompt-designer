"""
    Phase 5 - Research Agent using Pydantic AI
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    In this file you will create the main ResearchAgent class that:
      - Uses Pydantic AI's Agent for structured LLM responses
      - Registers search tools (DuckDuckGo, ArXiv, PubMed) as Pydantic AI tools
      - Supports multiple prompt templates for comparison
      - Integrates Logfire for monitoring and tracing
"""


# TODO:
# Phase 5 — Imports
#
# > Import os for environment variables
# Reference: https://docs.python.org/3/library/os.html#os.getenv
#
# > Import time for measuring execution time
# Reference: https://docs.python.org/3/library/time.html#time.time
#
# > Import json for exporting sessions
# Reference: https://docs.python.org/3/library/json.html
#
# > Import datetime from the datetime module
# Reference: https://docs.python.org/3/library/datetime.html
#
# > Import Optional from typing
# Reference: https://docs.python.org/3/library/typing.html#typing.Optional
#
# > Import dataclass from dataclasses for creating the dependencies container
# Reference: https://docs.python.org/3/library/dataclasses.html
#
# > Import load_dotenv from dotenv to load .env files
# Reference: https://pypi.org/project/python-dotenv/
#
# > Import Agent and RunContext from pydantic_ai
# Reference: https://ai.pydantic.dev/agents/
# Reference: https://ai.pydantic.dev/tools/
#
# > Use a try/except to import logfire for optional monitoring
# Reference: https://logfire.pydantic.dev/docs/
#
# > Import the models: AgentResponse, QuerySession, SearchResult from models.py
# > Import the tools: get_search_tools, format_results from tools.py
# > Import PromptLoader from prompt_loader.py
# YOUR CODE STARTS HERE

import os
import time
import json
from datetime import datetime
from typing import Optional
from dataclasses import dataclass

from dotenv import load_dotenv
from pydantic_ai import Agent, RunContext

load_dotenv()

try:
    import logfire
    HAS_LOGFIRE = True
except ImportError:
    logfire = None
    HAS_LOGFIRE = False

from models import AgentResponse, QuerySession, SearchResult
from tools import get_search_tools, format_results
from prompt_loader import PromptLoader

# YOUR CODE ENDS HERE


# TODO:
# Task 1 — Create the ResearchDeps dataclass
#
# > Create a dataclass called ResearchDeps that acts as a dependency container
#   for the Pydantic AI agent. It will hold the search tools and current query.
# Reference: https://docs.python.org/3/library/dataclasses.html
# Reference: https://ai.pydantic.dev/dependencies/
#
# > Inside the dataclass, create the following fields:
#   - search_tools: dict  (the dictionary of search tool instances)
#   - query: str with a default of ""  (the current user query)
#   - max_results: int with a default of 5
# YOUR CODE STARTS HERE

@dataclass
class ResearchDeps:
    """Dependency container for the Pydantic AI agent."""
    search_tools: dict
    query: str = ""
    max_results: int = 5

# YOUR CODE ENDS HERE


# TODO:
# Task 2 — Create the Pydantic AI Agent with registered tools
#
# > Create an Agent instance called research_agent using Agent() with:
#   - model: 'openai:gpt-4o-mini' (default, can be overridden at runtime)
#   - deps_type: ResearchDeps
#   - result_type: AgentResponse
#   - system_prompt: A default system prompt string (this will be overridden per-query)
# Reference: https://ai.pydantic.dev/agents/#agent-class
# Reference: https://ai.pydantic.dev/agents/#system-prompts
#
# > Register a tool called search_web using the @research_agent.tool decorator
#   - The function should take ctx: RunContext[ResearchDeps] and query: str
#   - Inside, call ctx.deps.search_tools["web"].search(query)
#   - Format the results using format_results() and return the string
# Reference: https://ai.pydantic.dev/tools/#registering-tools
#
# > Register a tool called search_arxiv using @research_agent.tool
#   - Same pattern: use ctx.deps.search_tools["arxiv"].search(query)
# Reference: https://ai.pydantic.dev/tools/#registering-tools
#
# > Register a tool called search_pubmed using @research_agent.tool
#   - Same pattern: use ctx.deps.search_tools["pubmed"].search(query)
# Reference: https://ai.pydantic.dev/tools/#registering-tools
# YOUR CODE STARTS HERE

research_agent = Agent(
    'mistral:mistral-large-latest',
    deps_type=ResearchDeps,
    output_type=AgentResponse,
    system_prompt=(
        "You are an intelligent research agent. Answer questions using the provided "
        "search tools. Always provide references with unique URLs."
    ),
)


@research_agent.tool
async def search_web(ctx: RunContext[ResearchDeps], query: str) -> str:
    """Search the web using DuckDuckGo for general information."""
    results = ctx.deps.search_tools["web"].search(query)
    return format_results(results)


@research_agent.tool
async def search_arxiv(ctx: RunContext[ResearchDeps], query: str) -> str:
    """Search ArXiv for academic and scientific papers."""
    results = ctx.deps.search_tools["arxiv"].search(query)
    return format_results(results)


@research_agent.tool
async def search_pubmed(ctx: RunContext[ResearchDeps], query: str) -> str:
    """Search PubMed for biomedical and life sciences literature."""
    results = ctx.deps.search_tools["pubmed"].search(query)
    return format_results(results)

# YOUR CODE ENDS HERE


# TODO:
# Task 3 — Create the setup_logfire helper function
#
# > Create a function called setup_logfire that configures Logfire monitoring
# Reference: https://logfire.pydantic.dev/docs/
#
# > Inside the function:
#   - Check if HAS_LOGFIRE is True and LOGFIRE_TOKEN is set in environment
#   - If so, call logfire.configure() to enable monitoring
#   - Call logfire.instrument_pydantic_ai() to trace all Pydantic AI agent calls
#   - Print a success message
#   - Wrap everything in try/except to gracefully handle errors
# Reference: https://logfire.pydantic.dev/docs/integrations/pydantic-ai/
# Reference: https://ai.pydantic.dev/logfire/
# YOUR CODE STARTS HERE

def setup_logfire() -> None:
    """Configure Logfire monitoring if available and token is set."""
    token = os.getenv("LOGFIRE_TOKEN")
    if token and HAS_LOGFIRE and logfire is not None:
        try:
            logfire.configure(token=token, service_name="prompt-designer")
            logfire.instrument_pydantic_ai()
            print("Logfire monitoring enabled.")
        except Exception as e:
            print(f"Logfire setup warning: {e}")

# YOUR CODE ENDS HERE


# TODO:
# Task 4 — Create the ResearchAgentRunner class
#
# > Create a class called ResearchAgentRunner that manages the agent lifecycle
# Reference: https://docs.python.org/3/tutorial/classes.html
#
# > Inside the class, create an __init__ method that takes:
#   - model: str with a default of "openai:gpt-4o-mini"
#   - max_search_results: int with a default of 5
# Reference: https://ai.pydantic.dev/agents/#agent-class
#
# > Inside __init__:
#   - Call load_dotenv() to load environment variables
#   - Call setup_logfire()
#   - Store self.model = model
#   - Create self.prompt_loader = PromptLoader()
#   - Create self.search_tools = get_search_tools(max_search_results)
#   - Create self.sessions: list[QuerySession] = []
#   - Store self.max_search_results = max_search_results
# Reference: https://pypi.org/project/python-dotenv/
#
# > Inside the class, create a method called list_prompts that returns list[str]
#   by delegating to self.prompt_loader.list_prompts()
#
# > Inside the class, create an async method called ask that takes:
#   - question: str
#   - prompt_name: str with default "structured"
# Reference: https://ai.pydantic.dev/agents/#running-agents
#
# > Inside the ask method:
#   - Record start_time = time.time()
#   - Load the prompt template using self.prompt_loader.load_prompt(prompt_name)
#   - Collect search results from all three tools (web, arxiv, pubmed)
#   - Format the combined results using format_results()
#   - Build the user prompt using prompt_template.format_user_prompt()
#   - Create a ResearchDeps instance with the search tools and query
#   - Call research_agent.run() with the user prompt and deps, using
#     model=self.model and override the system prompt from the template
#   - Create a QuerySession with the response data
#   - Append to self.sessions and return the session
# Reference: https://ai.pydantic.dev/agents/#running-agents
# Reference: https://ai.pydantic.dev/agents/#system-prompts
#
# > Inside the class, create a method called ask_sync that wraps the async ask
#   method for synchronous usage using asyncio.run()
# Reference: https://docs.python.org/3/library/asyncio-runner.html#asyncio.run
#
# > Inside the class, create a method called compare_prompts that takes:
#   - question: str
#   - prompt_names: Optional[list[str]] with default None
#   It should run ask() with each prompt and return a comparison dict
# Reference: https://docs.python.org/3/tutorial/datastructures.html#dictionaries
#
# > Inside the class, create a method called export_sessions that saves
#   all sessions to a JSON file
# Reference: https://docs.python.org/3/library/json.html#json.dump
#
# > Inside the class, create a method called print_response that pretty-prints
#   a QuerySession with the answer, key points, confidence, and references
# Reference: https://docs.python.org/3/library/functions.html#print
# YOUR CODE STARTS HERE

# model = 
class ResearchAgentRunner:
    """
    Manages the Pydantic AI research agent lifecycle.
    Supports multiple prompt templates, search tools, and prompt comparison.
    """

    def __init__(
        self,
        model: str = "mistral-medium-3-5",
        max_search_results: int = 5,
    ):
        load_dotenv()
        setup_logfire()
        self.model = model
        self.prompt_loader = PromptLoader()
        self.search_tools = get_search_tools(max_search_results)
        self.sessions: list[QuerySession] = []
        self.max_search_results = max_search_results

    def list_prompts(self) -> list[str]:
        """List all available prompt template names."""
        return self.prompt_loader.list_prompts()

    async def ask(
        self,
        question: str,
        prompt_name: str = "structured",
    ) -> QuerySession:
        """
        Ask a question using a specific prompt template and get a structured response.
        """
        start_time = time.time()

        prompt_template = self.prompt_loader.load_prompt(prompt_name)

        # Gather search results from all tools
        all_results: list[SearchResult] = []
        for tool_name, tool in self.search_tools.items():
            try:
                results = tool.search(question)
                all_results.extend(results)
            except Exception as e:
                print(f"Search error ({tool_name}): {e}")

        search_results_text = format_results(all_results)

        # Build the user prompt from the template
        user_prompt = prompt_template.format_user_prompt(
            question=question,
            search_results=search_results_text,
        )

        # Create dependencies for the agent
        deps = ResearchDeps(
            search_tools=self.search_tools,
            query=question,
            max_results=self.max_search_results,
        )

        try:
            # Run the Pydantic AI agent with the template's system prompt
            result = await research_agent.run(
                user_prompt,
                deps=deps,
                model=self.model,
                system_prompt=prompt_template.system_prompt,
            )

            session = QuerySession(
                question=question,
                prompt_used=prompt_name,
                model_used=self.model,
                response=result.data,
                search_results=all_results,
                execution_time_seconds=time.time() - start_time,
            )

        except Exception as e:
            session = QuerySession(
                question=question,
                prompt_used=prompt_name,
                model_used=self.model,
                raw_response=f"Error: {str(e)}",
                search_results=all_results,
                execution_time_seconds=time.time() - start_time,
            )

        self.sessions.append(session)
        return session

    def ask_sync(
        self,
        question: str,
        prompt_name: str = "structured",
    ) -> QuerySession:
        """Synchronous wrapper around the async ask method."""
        import asyncio
        return asyncio.run(self.ask(question, prompt_name))

    async def compare_prompts(
        self,
        question: str,
        prompt_names: Optional[list[str]] = None,
    ) -> dict:
        """
        Compare multiple prompt templates on the same question.
        Returns a dictionary with comparison results.
        """
        if prompt_names is None:
            prompt_names = self.list_prompts()

        results = {
            'question': question,
            'model': self.model,
            'timestamp': datetime.now().isoformat(),
            'comparisons': [],
        }

        for prompt_name in prompt_names:
            print(f"  Testing prompt: {prompt_name}...")
            session = await self.ask(question, prompt_name)

            comparison = {
                'prompt': prompt_name,
                'execution_time': session.execution_time_seconds,
                'success': session.response is not None,
            }

            if session.response:
                comparison['answer_length'] = len(session.response.answer)
                comparison['num_references'] = len(session.response.references)
                comparison['confidence'] = session.response.confidence
                comparison['reference_urls'] = [
                    ref.url for ref in session.response.references
                ]
            else:
                comparison['error'] = session.raw_response

            results['comparisons'].append(comparison)

        return results

    def export_sessions(self, filepath: str = "sessions.json") -> None:
        """Export all sessions to a JSON file for review."""
        data = [session.model_dump() for session in self.sessions]
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, default=str)
        print(f"Exported {len(self.sessions)} sessions to {filepath}")

    def print_response(self, session: QuerySession) -> None:
        """Pretty-print a session response."""
        print("\n" + "=" * 60)
        print(f"Question: {session.question}")
        print(f"Prompt: {session.prompt_used} | Model: {session.model_used}")
        print(f"Time: {session.execution_time_seconds:.2f}s")
        print("=" * 60)

        if session.response:
            print(f"\nANSWER:\n{session.response.answer}")
            print(f"\nConfidence: {session.response.confidence}")

            if session.response.key_points:
                print("\nKEY POINTS:")
                for point in session.response.key_points:
                    print(f"  - {point}")

            print("\nREFERENCES:")
            for i, ref in enumerate(session.response.references, 1):
                print(f"  [{i}] {ref.title}")
                print(f"      {ref.url}")
        else:
            print(f"\nError or raw response:\n{session.raw_response}")

        print("\n" + "=" * 60)

# YOUR CODE ENDS HERE
