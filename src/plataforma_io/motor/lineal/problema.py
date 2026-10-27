"""Modelo de un problema de programación lineal."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from enum import StrEnum
from fractions import Fraction
from typing import Any

from plataforma_io.motor.modelos import a_fraccion


class Relacion(StrEnum):
    MENOR_IGUAL = "<="
    MAYOR_IGUAL = ">="
    IGUAL = "="


@dataclass(frozen=True)
class Restriccion:
    coeficientes: tuple[Fraction, ...]
    relacion: Relacion
    lado_derecho: Fraction


@dataclass(frozen=True)
class ProblemaLineal:
    maximizar: bool
    objetivo: tuple[Fraction, ...]
    restricciones: tuple[Restriccion, ...]

    @property
    def n_variables(self) -> int:
        return len(self.objetivo)

    @classmethod
    def desde_numeros(
        cls,
        maximizar: bool,
        objetivo: Sequence[Any],
        restricciones: Sequence[tuple[Sequence[Any], str, Any]],
    ) -> ProblemaLineal:
        return cls(
            maximizar=maximizar,
            objetivo=tuple(a_fraccion(x) for x in objetivo),
            restricciones=tuple(
                Restriccion(tuple(a_fraccion(x) for x in coef), Relacion(rel), a_fraccion(lado))
                for coef, rel, lado in restricciones
            ),
        )
