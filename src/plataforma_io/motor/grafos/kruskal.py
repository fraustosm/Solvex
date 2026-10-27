"""Árbol de expansión mínima (Kruskal) (pendiente: informe 5)."""

from __future__ import annotations

from plataforma_io.motor.grafos.base import MetodoGrafo
from plataforma_io.motor.modelos import Solucion


class Kruskal(MetodoGrafo):
    """TODO 

    Ordenar aristas por peso; aceptar o descartar con unión-búsqueda; un Paso por arista.
    """

    nombre = "Árbol de expansión mínima (Kruskal)"

    def resolver(self) -> Solucion:
        raise NotImplementedError(
            "Árbol de expansión mínima (Kruskal) se implementa en el informe 5."
        )
