"""Nós do grafo do agente.

Cada nó deve ser pequeno, testável e com dependências injetadas.
"""

import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import ToolMessage
from colorama import Fore, Style

