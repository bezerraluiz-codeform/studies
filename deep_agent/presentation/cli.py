"""Interface de linha de comando.

Por enquanto é um esqueleto para manter a estrutura organizada.
"""

from __future__ import annotations

import argparse


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
    return parser


def main(argv: list[str] | None = None) -> int:
    """Ponto de entrada do CLI."""

    parser = build_parser()
    args = parser.parse_args(argv)

    if args.version:
        # Mensagem em pt-br para facilitar suporte.
        print("deep_agent: estrutura inicializada")
        return 0

    print("deep_agent: nada para executar ainda (apenas estrutura)")
    return 0
