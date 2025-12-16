"""Interface de linha de comando.

A apresentação é o composition root: lê entrada do usuário, imprime saída
e monta as dependências (adapters) para a camada de aplicação.
"""

from __future__ import annotations

import argparse
import uuid
from pathlib import Path

from dotenv import load_dotenv
from deepagents.backends import FilesystemBackend
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver

from deep_agent.application.agent.graph import create_agent
from deep_agent.application.agent.tools import build_tools
from deep_agent.infrastructure.web_search.tavily_adapter import TavilyWebSearchAdapter


def build_parser() -> argparse.ArgumentParser:
    """Constrói o parser de argumentos.

    Mantido em função separada para facilitar testes e evolução.
    """

    parser = argparse.ArgumentParser(prog="deep_agent")
    parser.add_argument(
        "--version",
        action="store_true",
        help="Exibe a versão e finaliza.",
    )
    parser.add_argument(
        "--model",
        default="gpt-4o-mini",
        help="Nome do modelo (ex.: gpt-4o-mini).",
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=0.0,
        help="Temperatura do modelo (0.0 a 2.0).",
    )
    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Desativa cores no terminal.",
    )
    parser.add_argument(
        "--disable-web-search",
        action="store_true",
        help="Desativa a ferramenta de busca na web (Tavily).",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    """Ponto de entrada do CLI."""

    parser = build_parser()
    args = parser.parse_args(argv)

    if args.version:
        # Mensagem em pt-br para facilitar suporte.
        print("deep_agent: estrutura inicializada")
        return 0

    load_dotenv()

    # Cores ficam restritas à apresentação.
    use_color = not bool(args.no_color)
    fore_green = ""
    fore_blue = ""
    fore_magenta = ""
    fore_yellow = ""
    fore_red = ""
    style_reset = ""
    if use_color:
        try:
            from colorama import Fore, Style, init as color_init

            color_init(autoreset=True)
            fore_green = Fore.GREEN
            fore_blue = Fore.BLUE
            fore_magenta = Fore.MAGENTA
            fore_yellow = Fore.YELLOW
            fore_red = Fore.RED
            style_reset = Style.RESET_ALL
        except Exception:
            use_color = False

    def paint(text: str, *, color: str = "") -> str:
        """Aplica cor no texto (quando habilitado)."""
        if not use_color or not color:
            return text
        return f"{color}{text}{style_reset}"

    # Montagem do modelo (provider externo) e ferramentas.
    llm = ChatOpenAI(model=str(args.model), temperature=float(args.temperature))

    tools = []
    if not args.disable_web_search:
        try:
            web_search = TavilyWebSearchAdapter()
            tools = build_tools(web_search=web_search)
        except Exception as exc:
            # Não falha o app inteiro se a chave não estiver configurada.
            print(paint(f"Aviso: busca na web desativada ({exc}).", color=fore_yellow))

    # Mantém estado (incluindo filesystem do agente) ao longo da sessão via checkpoints.
    checkpointer = MemorySaver()
    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}

    data_dir = (Path(__file__).resolve().parents[1] / "data").resolve()
    data_dir.mkdir(parents=True, exist_ok=True)
    backend = FilesystemBackend(root_dir=str(data_dir), virtual_mode=True)

    agent = create_agent(llm=llm, tools=tools, checkpointer=checkpointer, backend=backend)

    print(paint("=== DEEP AGENT (Ctrl+C para sair) ===", color=fore_green))
    print(paint(f"Pasta de arquivos do agente: {data_dir}", color=fore_yellow))

    while True:
        try:
            user_input = input(paint(">>> ", color=fore_blue))
            if user_input.strip().lower() in {"sair", "exit", "quit"}:
                break
            if not user_input.strip():
                continue

            print(paint("Processando...", color=fore_magenta))

            result = agent.invoke({"messages": [{"role": "user", "content": user_input}]}, config=config)
            messages = result.get("messages", []) if isinstance(result, dict) else []
            last_message = messages[-1] if messages else None

            final_content = ""
            if isinstance(last_message, dict):
                final_content = str(last_message.get("content") or "")
            else:
                final_content = str(getattr(last_message, "content", "") or "")

            if final_content:
                print(paint("=== Resposta Final ===", color=fore_green))
                print("-" * 50)
                print(final_content)
                print("-" * 50)
        except KeyboardInterrupt:
            print("\nEncerrando...")
            break
        except Exception as exc:
            print(paint(f"Erro: {exc}", color=fore_red))
            return 1

    return 0
