"""Adapter Tavily para busca na web.

Mantém o SDK (tavily-python) restrito à infraestrutura, expondo apenas uma
saída normalizada para a camada de aplicação.
"""

from __future__ import annotations

import os

from tavily import TavilyClient
from tavily.errors import (
    BadRequestError,
    ForbiddenError,
    InvalidAPIKeyError,
    MissingAPIKeyError,
    TimeoutError,
    UsageLimitExceededError,
)

from deep_agent.application.agent.ports import WebSearchPort, WebSearchResult


class TavilyWebSearchAdapter(WebSearchPort):
    """Implementa `WebSearchPort` usando Tavily."""

    def __init__(self, api_key: str | None = None) -> None:
        resolved_key = api_key or os.getenv("TAVILY_API_KEY")
        if not resolved_key:
            raise RuntimeError("Variável de ambiente TAVILY_API_KEY não configurada.")

        self._client = TavilyClient(api_key=resolved_key)

    def search(self, query: str, *, max_results: int = 5) -> list[WebSearchResult]:
        try:
            response = self._client.search(
                query=query,
                max_results=max_results,
                search_depth="basic",
                include_answer=False,
                include_raw_content=False,
                include_images=False,
            )
        except MissingAPIKeyError as exc:
            raise RuntimeError(
                "Chave da Tavily ausente. Configure TAVILY_API_KEY."
            ) from exc
        except InvalidAPIKeyError as exc:
            raise RuntimeError("Chave da Tavily inválida. Verifique TAVILY_API_KEY.") from exc
        except UsageLimitExceededError as exc:
            raise RuntimeError(
                "Limite de uso da Tavily excedido. Verifique seu plano/quotas."
            ) from exc
        except BadRequestError as exc:
            raise RuntimeError(
                "Requisição inválida para a Tavily. Verifique os parâmetros da busca."
            ) from exc
        except ForbiddenError as exc:
            raise RuntimeError("Acesso negado pela Tavily para esta requisição.") from exc
        except TimeoutError as exc:
            raise RuntimeError("Tempo limite excedido ao consultar a Tavily.") from exc
        except Exception as exc:
            raise RuntimeError("Erro inesperado ao consultar a Tavily.") from exc

        items = response.get("results", []) if isinstance(response, dict) else []
        results: list[WebSearchResult] = []
        for item in items:
            if not isinstance(item, dict):
                continue
            results.append(
                WebSearchResult(
                    title=str(item.get("title", "") or ""),
                    url=str(item.get("url", "") or ""),
                    content=(
                        None
                        if item.get("content") is None
                        else str(item.get("content"))
                    ),
                )
            )
        return results

