"""Método de las Dos Fases (pendiente: informe 4)."""

from __future__ import annotations

from plataforma_io.motor.lineal.simplex import Simplex
from plataforma_io.motor.modelos import Solucion


class DosFases(Simplex):

    nombre = "Dos Fases"

    def resolver(self) -> Solucion:
        raise NotImplementedError("Dos Fases se implementa en el informe 4.")
