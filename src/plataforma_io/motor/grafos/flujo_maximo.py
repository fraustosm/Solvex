"""Flujo máximo (Edmonds-Karp) (pendiente: informe 5)."""

from __future__ import annotations

from plataforma_io.motor.grafos.base import MetodoGrafo
from plataforma_io.motor.modelos import Solucion


class FlujoMaximo(MetodoGrafo):
    """TODO 

    Red residual; caminos aumentantes por búsqueda en anchura; corte mínimo al terminar.
    """

    nombre = "Flujo máximo (Edmonds-Karp)"

    def resolver(self) -> Solucion:
        raise NotImplementedError("Flujo máximo (Edmonds-Karp) se implementa en el informe 5.")
