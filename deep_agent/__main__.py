"""Entry-point para execução via `python -m deep_agent`.

Mantém a execução centralizada na camada de apresentação.
"""

from deep_agent.presentation.cli import main


if __name__ == "__main__":
    raise SystemExit(main())
