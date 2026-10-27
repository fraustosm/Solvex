"""Registro central de métodos: lo usa la interfaz para construir el menú."""

from __future__ import annotations

from dataclasses import dataclass

from plataforma_io.motor.base import Metodo
from plataforma_io.motor.grafos.dijkstra import CaminoMasCorto
from plataforma_io.motor.grafos.floyd_warshall import FloydWarshall
from plataforma_io.motor.grafos.flujo_maximo import FlujoMaximo
from plataforma_io.motor.grafos.kruskal import Kruskal
from plataforma_io.motor.grafos.prim import Prim
from plataforma_io.motor.lineal.dos_fases import DosFases
from plataforma_io.motor.lineal.simplex import Simplex
from plataforma_io.motor.transporte.noroeste import EsquinaNoroeste
from plataforma_io.motor.transporte.vogel import Vogel

FAMILIA_LINEAL = "Programación lineal"
FAMILIA_TRANSPORTE = "Transporte"
FAMILIA_GRAFOS = "Redes y grafos"
FAMILIAS = (FAMILIA_LINEAL, FAMILIA_TRANSPORTE, FAMILIA_GRAFOS)


@dataclass(frozen=True)
class InfoMetodo:
    clave: str
    familia: str
    clase: type[Metodo]
    implementado: bool = False

    @property
    def nombre(self) -> str:
        return self.clase.nombre


METODOS: dict[str, InfoMetodo] = {
    m.clave: m
    for m in (
        InfoMetodo("simplex", FAMILIA_LINEAL, Simplex),
        InfoMetodo("dos_fases", FAMILIA_LINEAL, DosFases),
        InfoMetodo("noroeste", FAMILIA_TRANSPORTE, EsquinaNoroeste, implementado=True),
        InfoMetodo("vogel", FAMILIA_TRANSPORTE, Vogel),
        InfoMetodo("dijkstra", FAMILIA_GRAFOS, CaminoMasCorto),
        InfoMetodo("floyd_warshall", FAMILIA_GRAFOS, FloydWarshall),
        InfoMetodo("kruskal", FAMILIA_GRAFOS, Kruskal),
        InfoMetodo("prim", FAMILIA_GRAFOS, Prim),
        InfoMetodo("flujo_maximo", FAMILIA_GRAFOS, FlujoMaximo),
    )
}


def metodos_por_familia() -> dict[str, list[InfoMetodo]]:
    return {f: [m for m in METODOS.values() if m.familia == f] for f in FAMILIAS}
