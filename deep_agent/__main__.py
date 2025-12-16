"""Entry-point para execução via `python -m deep_agent`.

Mantém a execução centralizada na camada de apresentação.
"""

from __future__ import annotations

import sys

from deep_agent.presentation.cli import main as cli_main

def main() -> int:
    """Encaminha para o CLI (camada de apresentação)."""
    return int(cli_main(sys.argv[1:]))

if __name__ == "__main__":
    raise SystemExit(main())