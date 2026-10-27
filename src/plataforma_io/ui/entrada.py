"""Lectura y validación de los datos que el usuario escribe (sin dependencia de Qt)."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from fractions import Fraction

from plataforma_io.motor.modelos import a_fraccion, suma
from plataforma_io.motor.transporte.problema import ProblemaTransporte


@dataclass(frozen=True)
class ErrorCelda:
    """Error de captura asociado a una celda de la tabla (fila y columna base 0)."""

    fila: int
    columna: int
    mensaje: str


def interpretar_numero(texto: str) -> Fraction:
    """Convierte lo escrito a fracción exacta: acepta 5, -2, 2.5, 2,5 y 5/2.

    Lanza ``ValueError`` si el texto está vacío o no es un número finito.
    """
    limpio = texto.strip().replace(",", ".")
    if not limpio:
        raise ValueError("vacío")
    try:
        return a_fraccion(limpio)
    except (ValueError, ZeroDivisionError) as exc:
        raise ValueError("no es un número") from exc


def leer_problema(
    textos: Sequence[Sequence[str]],
) -> tuple[ProblemaTransporte | None, list[ErrorCelda]]:
    """Construye un problema de transporte a partir de la tabla de captura.

    ``textos`` tiene (m + 1) filas y (n + 1) columnas: los costos ocupan las primeras m filas y
    n columnas; la última columna es la oferta de cada origen y la última fila es la demanda de
    cada destino. Devuelve ``(problema, [])`` o ``(None, errores)``.
    """
    m, n = len(textos) - 1, len(textos[0]) - 1
    errores: list[ErrorCelda] = []

    def leer(i: int, j: int, nombre: str, *, no_negativo: bool = False) -> Fraction | None:
        try:
            valor = interpretar_numero(textos[i][j])
        except ValueError:
            errores.append(
                ErrorCelda(i, j, f"{nombre}: escriba un número (por ejemplo 5, 2.5 o 5/2).")
            )
            return None
        if no_negativo and valor < 0:
            errores.append(ErrorCelda(i, j, f"{nombre}: no puede ser negativo."))
            return None
        return valor

    costos = [[leer(i, j, f"Costo de O{i + 1} a D{j + 1}") for j in range(n)] for i in range(m)]
    oferta = [leer(i, n, f"Oferta de O{i + 1}", no_negativo=True) for i in range(m)]
    demanda = [leer(m, j, f"Demanda de D{j + 1}", no_negativo=True) for j in range(n)]
    if errores:
        return None, errores

    problema = ProblemaTransporte.desde_numeros(
        [x for x in oferta if x is not None],
        [x for x in demanda if x is not None],
        [[x for x in fila if x is not None] for fila in costos],
    )
    if suma(problema.oferta) == 0:
        errores.append(ErrorCelda(0, n, "La oferta total debe ser mayor que cero."))
    if suma(problema.demanda) == 0:
        errores.append(ErrorCelda(m, 0, "La demanda total debe ser mayor que cero."))
    if errores:
        return None, errores
    return problema, []
