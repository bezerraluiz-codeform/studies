"""Fábrica do agente (camada de aplicação).

Nesta refatoração, a orquestração do agente passa a usar a biblioteca oficial
`deepagents`, conforme a documentação da LangChain.

Responsabilidades deste módulo:
- Expor uma função pura de montagem do agente, recebendo dependências via injeção.
- Não fazer I/O (input/print), nem ler variáveis de ambiente.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from deepagents import create_deep_agent
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.tools import BaseTool

ToolLike = BaseTool | Callable[..., Any]

DEFAULT_SYSTEM_PROMPT_PT_BR = """Você é um assistente de IA prestativo.

Regras obrigatórias:
- Responda em pt-br.
- Quando gerar CÓDIGO, use nomes em inglês (variáveis, funções, classes, métodos).
- Quando gerar COMENTÁRIOS/documentação no código, escreva em português.
- Mensagens de LOG e textos de erro devem estar em português.

Planejamento:
- Para tarefas complexas, use a ferramenta `write_todos` para decompor passos e acompanhar progresso.

Ferramentas:
- Se precisar de informação atual, use `web_search` (quando disponível).
- Quando uma ferramenta retornar muitos dados, use o filesystem do agente para armazenar resultados e mantenha a resposta concisa.

Filesystem (pasta do projeto):
- Quando o usuário pedir para "salvar" ou "criar arquivo", use `write_file` e salve no filesystem do agente.
- Use caminhos absolutos começando com `/` (ex.: `/relatorio.md`). A aplicação está configurada para mapear isso para a pasta `deep_agent/data` no disco.
- Se o usuário pedir para salvar no "desktop", explique que por segurança você só pode salvar na pasta de dados do projeto e salve lá mesmo.
""".strip()


def create_agent(
    *,
    llm: BaseChatModel | str,
    tools: list[ToolLike] | None = None,
    system_prompt: str | None = None,
    backend: Any | None = None,
    store: Any | None = None,
    checkpointer: Any | None = None,
    subagents: Any | None = None,
):
    """Cria um Deep Agent compilado usando `deepagents.create_deep_agent`.

    O composition root (camada de apresentação) deve injetar `llm` e `tools`.
    """

    return create_deep_agent(
        model=llm,
        tools=list(tools or []),
        system_prompt=system_prompt or DEFAULT_SYSTEM_PROMPT_PT_BR,
        backend=backend,
        store=store,
        checkpointer=checkpointer,
        subagents=subagents,
    )


__all__ = ["create_agent", "DEFAULT_SYSTEM_PROMPT_PT_BR"]
