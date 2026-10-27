"""Árbol de expansión mínima (Prim) (pendiente: informe 5)."""

from __future__ import annotations

from plataforma_io.motor.grafos.base import MetodoGrafo
from plataforma_io.motor.modelos import Solucion


class Prim(MetodoGrafo):
    """TODO 

    Crecer el árbol desde un nodo inicial eligiendo la arista mínima de corte.
    """

    nombre = "Árbol de expansión mínima (Prim)"

    def resolver(self) -> Solucion:
        raise NotImplementedError("Árbol de expansión mínima (Prim) se implementa en el informe 5.")
