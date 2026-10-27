"""Camino más corto (Floyd-Warshall) (pendiente: informe 5)."""

from __future__ import annotations

from plataforma_io.motor.grafos.base import MetodoGrafo
from plataforma_io.motor.modelos import Solucion


class FloydWarshall(MetodoGrafo):
    """TODO 

    Matriz de distancias; un Paso por nodo intermedio k.
    """

    nombre = "Camino más corto (Floyd-Warshall)"

    def resolver(self) -> Solucion:
        raise NotImplementedError(
            "Camino más corto (Floyd-Warshall) se implementa en el informe 5."
        )
