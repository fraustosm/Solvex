"""Modelo de grafo."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction


@dataclass(frozen=True)
class Arista:
    origen: str
    destino: str
    peso: Fraction  # peso, distancia o capacidad según el método


@dataclass(frozen=True)
class Grafo:
    nodos: tuple[str, ...]
    aristas: tuple[Arista, ...]
    dirigido: bool = False
