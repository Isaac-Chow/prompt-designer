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


# YOUR CODE ENDS HERE
