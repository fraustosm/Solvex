"""Ejemplos predefinidos (RF-03). También sirven como casos de referencia en las pruebas."""

from __future__ import annotations

from collections.abc import Callable

from plataforma_io.motor.base import Metodo
from plataforma_io.motor.transporte.noroeste import EsquinaNoroeste
from plataforma_io.motor.transporte.problema import ProblemaTransporte


def transporte_clasico() -> ProblemaTransporte:
    """3 orígenes y 4 destinos, balanceado (oferta y demanda suman 50)."""
    return ProblemaTransporte.desde_numeros(
        oferta=[15, 25, 10],
        demanda=[5, 15, 15, 15],
        costos=[[10, 0, 20, 11], [12, 7, 9, 20], [0, 14, 16, 18]],
    )


EJEMPLOS: dict[str, Callable[[], Metodo]] = {
    "noroeste": lambda: EsquinaNoroeste(transporte_clasico()),
}
