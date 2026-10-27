"""Base común de los métodos sobre grafos."""

from __future__ import annotations

from plataforma_io.motor.base import Metodo
from plataforma_io.motor.grafos.modelo import Grafo
from plataforma_io.motor.modelos import ErrorValidacion


class MetodoGrafo(Metodo):
    problema: Grafo

    def validar(self) -> list[ErrorValidacion]:
        g = self.problema
        errores: list[ErrorValidacion] = []
        if not g.nodos:
            errores.append(ErrorValidacion("nodos", "El grafo debe tener al menos un nodo."))
        if len(set(g.nodos)) != len(g.nodos):
            errores.append(ErrorValidacion("nodos", "Los nombres de los nodos deben ser únicos."))
        conocidos = set(g.nodos)
        for a in g.aristas:
            if a.origen not in conocidos or a.destino not in conocidos:
                errores.append(
                    ErrorValidacion(
                        "aristas", f"La arista {a.origen}-{a.destino} usa un nodo inexistente."
                    )
                )
        return errores
