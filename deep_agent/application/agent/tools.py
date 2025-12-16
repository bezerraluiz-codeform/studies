"""Ferramentas (tools) usadas pelo agente.

Mantenha integrações externas na infraestrutura e injete aqui.
"""

from __future__ import annotations

from typing import Any

from langchain_core.tools import BaseTool, tool

from deep_agent.application.agent.ports import WebSearchPort


def build_tools(*, web_search: WebSearchPort) -> list[BaseTool]:
    """Monta a lista de tools do agente.

    A implementação concreta de busca (ex.: Tavily) deve ser injetada via porta,
    mantendo a camada de aplicação desacoplada de SDKs externos.
    """

    @tool("web_search")
    def web_search_tool(query: str, max_results: int = 5) -> list[dict[str, Any]]:
        """Pesquisa na web.

        Parâmetros:
            query: Termo/pergunta para pesquisa.
            max_results: Quantidade máxima de resultados.

        Retorno:
            Lista de resultados com `title`, `url` e `content` (quando disponível).
        """

        results = web_search.search(query, max_results=max_results)
        return [
            {"title": item.title, "url": item.url, "content": item.content}
            for item in results
        ]

    return [web_search_tool]

