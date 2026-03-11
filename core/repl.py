from prompt_toolkit import prompt
import os

from core.executor import run_command
from ai.ai_engine import ask_ai
from context.detector import detect_context
from core.os_detect import get_os
from safety.danger_detector import check_dangerous_command
from healing.error_agent import error_agent
from healing.file_ops import create_folder, create_file

# -------------------------------
# NEW IMPORTS (ghost suggestions)
# -------------------------------
from healing.ghost_suggest import GhostSuggest

ghost = GhostSuggest()


def start_terminal():

    while True:

        try:

            # -------------------------------
            # UPDATED PROMPT WITH SUGGESTION
            # -------------------------------
            user_input = prompt(
                f"{os.getcwd()} > ",
                auto_suggest=ghost
            ).strip()

            # -------------------------------
            # ACCEPT GHOST SUGGESTION ON ENTER
            # -------------------------------
            if not user_input:
                suggestion = None
                if hasattr(ghost, "get_next_command"):
                    suggestion = ghost.get_next_command()

                if suggestion:
                    user_input = suggestion
                    print(suggestion)
                else:
                    continue

            # Exit command
            if user_input.lower() == "exit":
                print("Exiting ShellMind...")
                break


            # =========================================================
            # AI MODE
            # =========================================================

            if user_input.lower().startswith("ai:"):

                query = user_input[3:].strip().lower()


                if query == "help":

                    print("""
ShellMind AI Commands

Error Agent:
ai: scan project
ai: create folder
ai: create file

""")

                    continue


                # -----------------------------------------------------
                # ERROR AGENT COMMANDS
                # -----------------------------------------------------

                if query == "scan project":

                    result = error_agent.cmd_scan(os.getcwd())
                    print(result)
                    continue


                if query == "show errors":

                    result = error_agent.cmd_show_errors(os.getcwd())
                    print(result)
                    continue

                if query == "create folder":

                    create_folder()
                    continue


                if query == "create file":

                    create_file()
                    continue

                if query == "explain errors":

                    result = error_agent.cmd_explain_errors()
                    print(result)
                    continue


                if query == "fix errors":

                    result = error_agent.cmd_fix_all(os.getcwd())
                    print(result)
                    continue


                if query.startswith("fix file"):

                    parts = query.split(" ", 2)

                    if len(parts) < 3:
                        print("Usage: ai: fix file <path>")
                        continue

                    filepath = parts[2]

                    result = error_agent.cmd_fix_file(filepath, os.getcwd())
                    print(result)
                    continue


                if query == "clear errors":

                    result = error_agent.cmd_clear_errors(os.getcwd())
                    print(result)
                    continue


                # -----------------------------------------------------
                # NORMAL AI COMMAND GENERATION
                # -----------------------------------------------------

                context = detect_context()
                os_type = get_os()

                command = ask_ai(query, context, os_type)

                if not command:
                    print("AI could not generate a command.")
                    continue

                print("\nAI Suggested Command:")
                print(f"  {command}")
                print("──────────────────────────────")

                # Check risk
                risk =check_dangerous_command(command)

                if risk == "HIGH":  
                    print("⚠ Warning: This command may be dangerous.")

                # Only suggest command, do not execute
                continue


            # =========================================================
            # NORMAL TERMINAL COMMANDS
            # =========================================================

            run_command(user_input)

            # -------------------------------
            # UPDATE GHOST SUGGESTION MEMORY
            # -------------------------------
            ghost.update_last_command(user_input)


        except KeyboardInterrupt:
            print("\nUse 'exit' to quit ShellMind.")