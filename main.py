"""
    Phase 6 - Main Entry Point for the Prompt Designer Agent
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    In this file you will create the interactive command loop that
    lets you test different prompts, compare them, and export results.
"""


# TODO:
# Phase 6 — Imports
#
# > Import asyncio for running async functions
# Reference: https://docs.python.org/3/library/asyncio.html
#
# > Import ResearchAgentRunner from agent.py
# Reference: https://docs.python.org/3/tutorial/modules.html
# YOUR CODE STARTS HERE


# YOUR CODE ENDS HERE


# TODO:
# Task 1 — Create the interactive_mode async function
#
# > Create an async function called interactive_mode that takes no parameters
# Reference: https://docs.python.org/3/library/asyncio-task.html#coroutines
#
# > Inside the function, print a welcome banner with the app name
#
# > Inside the function, create a ResearchAgentRunner instance
#   Wrap this in a try/except to catch initialization errors (e.g., missing API keys)
# Reference: https://ai.pydantic.dev/agents/
#
# > Inside the function, print the available prompts and commands:
#   - ask <prompt> <question>  — Ask with a specific prompt template
#   - compare <question>       — Compare all prompts on one question
#   - prompts                  — List available prompt templates
#   - export                   — Export all sessions to JSON
#   - quit                     — Exit the program
#
# > Inside the function, create a while True loop that:
#   - Gets user input with input("\n> ").strip()
#   - Handles empty input (continue)
#   - Handles "quit" command (break)
#   - Handles "prompts" command: list all prompt names with their version info
#   - Handles "export" command: call runner.export_sessions()
#   - Handles "compare <question>": call await runner.compare_prompts(question)
#     and print the comparison results
#   - Handles "ask <prompt> <question>": call await runner.ask(question, prompt_name)
#     and call runner.print_response(session)
#   - Default: treat entire input as a question using the "structured" prompt
#   - Wrap in try/except for KeyboardInterrupt and general Exception
# Reference: https://docs.python.org/3/library/functions.html#input
# Reference: https://docs.python.org/3/reference/compound_stmts.html#the-while-statement
# YOUR CODE STARTS HERE


# YOUR CODE ENDS HERE


# TODO:
# Task 2 — Create the main entry point
#
# > Add an if __name__ == "__main__" block that calls asyncio.run(interactive_mode())
# Reference: https://docs.python.org/3/library/asyncio-runner.html#asyncio.run
# Reference: https://docs.python.org/3/library/__main__.html
# YOUR CODE STARTS HERE


# YOUR CODE ENDS HERE
