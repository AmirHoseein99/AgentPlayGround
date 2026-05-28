# ai.py
import sys
from rich import print

from llm.openrouter import OpenRouterAPI
from llm.prompt import SYSTEM_PROMPT
from llm.utils import stream_to_terminal


def main():
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
    ]

    openrouter_api = OpenRouterAPI()

    print("\n[cyan]AI Assistant ready — /exit to quit, /clear to reset[/cyan]\n")

    while True:
        print("\n[bold red]You:[/bold red]")
        user_message = input("      ")

        if user_message.strip().lower() == "/exit":
            print("\n[yellow]Exiting...[/yellow]")
            sys.exit(0)

        if user_message.strip().lower() == "/clear":
            messages = [{"role": "system", "content": SYSTEM_PROMPT}]
            print("\n[yellow]Conversation cleared.[/yellow]\n")
            continue

        messages.append({"role": "user", "content": user_message})

        try:
            print("\n[blue]⠋ Thinking...[/blue]\n")

            print("[bold green]Assistant:[/bold green]\n")
            print("─" * 50)

            assisstat_response = stream_to_terminal(
                openrouter_api=openrouter_api,
                messages=messages
            )
            messages.append({"role": "assistant", "content":assisstat_response})
            print("\n" + "─" * 50 + "\n")

        except Exception as e:
            print(f"\n[red]Error:[/red] {e}\n")


if __name__ == "__main__":
    main()