"""Portas (interfaces) da camada de aplicação.

As portas definem contratos que a infraestrutura implementa, permitindo trocar
provedores externos sem acoplar o domínio/aplicação a SDKs específicos.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True, slots=True)
class WebSearchResult:
    """Resultado normalizado de uma busca na web."""

    title: str
    url: str
    content: str | None = None


class WebSearchPort(Protocol):
    """Contrato para busca na web.

    Implementações concretas (ex.: Tavily) devem viver na infraestrutura.
    """

    def search(self, query: str, *, max_results: int = 5) -> list[WebSearchResult]:
        """Executa uma busca e retorna resultados normalizados."""

