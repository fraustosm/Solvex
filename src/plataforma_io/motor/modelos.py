"""Modelos de datos compartidos por todos los métodos."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass, field
from enum import StrEnum
from fractions import Fraction
from typing import Any


def a_fraccion(valor: int | float | str | Fraction) -> Fraction:
    """Convierte un número a fracción exacta (los ``float`` se interpretan por su forma decimal)."""
    if isinstance(valor, Fraction):
        return valor
    if isinstance(valor, float):
        return Fraction(str(valor))
    return Fraction(valor)


def suma(valores: Iterable[Fraction]) -> Fraction:
    """Suma de fracciones; devuelve siempre ``Fraction`` (incluso con una lista vacía)."""
    return sum(valores, Fraction(0))


def formatear(valor: Fraction) -> str:
    """Muestra una fracción como entero (``5``) o como cociente (``7/2``)."""
    if valor.denominator == 1:
        return str(valor.numerator)
    return f"{valor.numerator}/{valor.denominator}"


class TipoSolucion(StrEnum):
    OPTIMA = "optima"
    BASICA_FACTIBLE = "basica_factible"
    INFACTIBLE = "infactible"
    NO_ACOTADA = "no_acotada"
    CAMINO = "camino"
    ARBOL = "arbol"
    FLUJO = "flujo"


@dataclass(frozen=True)
class ErrorValidacion:
    """Error de captura: ``campo`` identifica dónde se origina y ``mensaje`` cómo corregirlo."""

    campo: str
    mensaje: str


@dataclass(frozen=True)
class Paso:
    """Un instante de la resolución, listo para ser reproducido por la interfaz."""

    indice: int
    titulo: str
    explicacion: str
    estado: dict[str, Any] = field(default_factory=dict)
    resaltados: tuple[Any, ...] = ()


@dataclass
class Solucion:
    tipo: TipoSolucion
    valores: dict[str, Any]
    objetivo: Fraction | None
    pasos: list[Paso]
    mensajes: list[str] = field(default_factory=list)
