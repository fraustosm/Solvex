"""Método de aproximación de Vogel (pendiente: informe 2)."""

from __future__ import annotations

from plataforma_io.motor.modelos import Solucion
from plataforma_io.motor.transporte.base import MetodoTransporte


class Vogel(MetodoTransporte):
    """TODO

    Algoritmo: en cada iteración calcular la penalización de cada fila y columna vigente (diferencia
    entre los dos costos menores), elegir la mayor (definir y documentar el criterio de desempate),
    asignar min(oferta, demanda) en la celda de menor costo de esa fila o columna, eliminar la fila
    o columna agotada y repetir. Generar un ``Paso`` por iteración usando ``estado_transporte`` y
    agregar al estado las claves ``penalizaciones_filas`` y ``penalizaciones_columnas``.
    """

    nombre = "Método de Vogel"

    def resolver(self) -> Solucion:
        raise NotImplementedError("Vogel se implementa en el informe 2.")
