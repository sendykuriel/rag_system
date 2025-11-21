"""
Gestión de LLMs (modelos de lenguaje) para Greenpeace RAG.
"""

from typing import Any


class LLMManager:
    """Factory/Manager para instanciar LLMs soportados."""

    @staticmethod
    def create(provider: str, model: str, temperature: float = 0.7, num_ctx: int = 4096) -> Any:
        """
        Crea una instancia de LLM según el provider.

        Args:
            provider: Proveedor (p.ej. "ollama")
            model: Nombre del modelo
            temperature: Temperatura del LLM
            num_ctx: Tamaño del contexto

        Returns:
            Instancia de LLM compatible con LangChain
        """
        if provider == "ollama":
            from langchain_ollama import ChatOllama

            return ChatOllama(
                model=model,
                temperature=temperature,
                num_ctx=num_ctx,
            )

        raise ValueError(f"Provider {provider} not supported")


