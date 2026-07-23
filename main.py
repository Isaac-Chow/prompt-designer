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
import asyncio
from agent import ResearchAgentRunner

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
async def interactive_mode():
    """Run the Prompt Designer agent in interactive mode."""
    print("\n" + "=" * 55)
    print("  Prompt Designer — Pydantic AI Research Agent")
    print("=" * 55)

    try:
        runner = ResearchAgentRunner()
        print(f"Initialized with model: {runner.model}")
    except Exception as e:
        print(f"Error initializing agent: {e}")
        print("Make sure MISTRAL_API_KEY is set in your .env file.")
        return

    print(f"\nAvailable prompts: {', '.join(runner.list_prompts())}")
    print("\nCommands:")
    print("  ask <prompt> <question>  — Ask with specific prompt")
    print("  compare <question>       — Compare all prompts")
    print("  prompts                  — List prompt templates")
    print("  export                   — Export sessions to JSON")
    print("  quit                     — Exit")

    while True:
        try:
            user_input = input("\n> ").strip()

            if not user_input:
                continue

            if user_input.lower() == "quit":
                print("Goodbye!")
                break

            elif user_input.lower() == "prompts":
                for name in runner.list_prompts():
                    info = runner.prompt_loader.get_prompt_info(name)
                    print(f"  - {name} (v{info['version']}, {info['system_prompt_length']} chars)")

            elif user_input.lower() == "export":
                runner.export_sessions()

            elif user_input.lower().startswith("compare "):
                question = user_input[8:].strip()
                if question:
                    print(f"\nComparing all prompts on: '{question}'")
                    results = await runner.compare_prompts(question)
                    print("\nCOMPARISON RESULTS:")
                    for comp in results['comparisons']:
                        status = "OK" if comp['success'] else "FAIL"
                        refs = comp.get('num_references', 0)
                        time_s = comp.get('execution_time', 0)
                        conf = comp.get('confidence', 'n/a')
                        print(f"  [{status}] {comp['prompt']}: {refs} refs, "
                              f"confidence={conf}, {time_s:.2f}s")
                else:
                    print("Usage: compare <question>")

            elif user_input.lower().startswith("ask "):
                parts = user_input[4:].strip().split(' ', 1)
                if len(parts) == 2:
                    prompt_name, question = parts
                    if prompt_name in runner.list_prompts():
                        session = await runner.ask(question, prompt_name)
                        runner.print_response(session)
                    else:
                        print(f"Unknown prompt: {prompt_name}")
                        print(f"Available: {', '.join(runner.list_prompts())}")
                else:
                    print("Usage: ask <prompt_name> <question>")

            else:
                # Default: treat as question using "structured" prompt
                session = await runner.ask(user_input, "structured")
                runner.print_response(session)

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")


# YOUR CODE ENDS HERE


# TODO:
# Task 2 — Create the main entry point
#
# > Add an if __name__ == "__main__" block that calls asyncio.run(interactive_mode())
# Reference: https://docs.python.org/3/library/asyncio-runner.html#asyncio.run
# Reference: https://docs.python.org/3/library/__main__.html
# YOUR CODE STARTS HERE
if __name__ == "__main__":
    asyncio.run(interactive_mode())

# YOUR CODE ENDS HERE
