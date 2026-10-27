"""Modelo de un problema de transporte."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, replace
from fractions import Fraction
from typing import Any

from plataforma_io.motor.modelos import a_fraccion, suma


@dataclass(frozen=True)
class ProblemaTransporte:
    oferta: tuple[Fraction, ...]
    demanda: tuple[Fraction, ...]
    costos: tuple[tuple[Fraction, ...], ...]
    ficticio_origen: bool = False
    ficticio_destino: bool = False

    @classmethod
    def desde_numeros(
        cls,
        oferta: Sequence[Any],
        demanda: Sequence[Any],
        costos: Sequence[Sequence[Any]],
    ) -> ProblemaTransporte:
        return cls(
            oferta=tuple(a_fraccion(x) for x in oferta),
            demanda=tuple(a_fraccion(x) for x in demanda),
            costos=tuple(tuple(a_fraccion(x) for x in fila) for fila in costos),
        )

    @property
    def balanceado(self) -> bool:
        return suma(self.oferta) == suma(self.demanda)

    def balancear(self) -> ProblemaTransporte:
        """Agrega un destino u origen ficticio (costos nulos) si oferta y demanda difieren."""
        total_oferta, total_demanda = suma(self.oferta), suma(self.demanda)
        if total_oferta == total_demanda:
            return self
        if total_oferta > total_demanda:
            return replace(
                self,
                demanda=(*self.demanda, total_oferta - total_demanda),
                costos=tuple((*fila, Fraction(0)) for fila in self.costos),
                ficticio_destino=True,
            )
        return replace(
            self,
            oferta=(*self.oferta, total_demanda - total_oferta),
            costos=(*self.costos, tuple(Fraction(0) for _ in self.demanda)),
            ficticio_origen=True,
        )

    def a_dict(self) -> dict[str, Any]:
        """Representación serializable (fracciones como texto) para guardar en JSON."""
        return {
            "oferta": [str(x) for x in self.oferta],
            "demanda": [str(x) for x in self.demanda],
            "costos": [[str(x) for x in fila] for fila in self.costos],
        }

    @classmethod
    def desde_dict(cls, datos: dict[str, Any]) -> ProblemaTransporte:
        return cls.desde_numeros(datos["oferta"], datos["demanda"], datos["costos"])
