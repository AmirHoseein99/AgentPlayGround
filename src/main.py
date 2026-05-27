# ai.py
import sys
from rich import print
from llm.openrouter import OpenRouterAPI

def main():
    if len(sys.argv) < 2:
        print("[bold red]Usage:[/bold red] ai \"your prompt\"")
        return

    user_prompt = " ".join(sys.argv[1:])

    print("[cyan]Thinking...[/cyan]\n")

    try:
        openrouter_api = OpenRouterAPI()
        llm_response = openrouter_api.call_openrouter_api(user_prompt)
        result = openrouter_api.format_response(llm_response)
        print("[green]\n--- Response ---\n[/green]")
        print(result)
    except Exception as e:
        print(f"[red]Error:[/red] {e}")


if __name__ == "__main__":
    main()