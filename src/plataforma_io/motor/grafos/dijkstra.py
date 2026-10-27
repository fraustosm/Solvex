"""Camino más corto (Dijkstra) (pendiente: informe 5)."""

from __future__ import annotations

from plataforma_io.motor.grafos.base import MetodoGrafo
from plataforma_io.motor.modelos import Solucion


class CaminoMasCorto(MetodoGrafo):
    """TODO 

    Etiquetas de distancia y previo; hacer permanente el nodo pendiente de menor
    distancia; registrar un Paso por nodo permanente.
    """

    nombre = "Camino más corto (Dijkstra)"

    def resolver(self) -> Solucion:
        raise NotImplementedError("Camino más corto (Dijkstra) se implementa en el informe 5.")
