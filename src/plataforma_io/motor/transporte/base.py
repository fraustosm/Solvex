"""Base común de los métodos de transporte."""

from __future__ import annotations

from fractions import Fraction

from plataforma_io.motor.base import Metodo
from plataforma_io.motor.modelos import ErrorValidacion, Paso, formatear, suma
from plataforma_io.motor.transporte.problema import ProblemaTransporte

Asignaciones = dict[tuple[int, int], Fraction]


class MetodoTransporte(Metodo):
    problema: ProblemaTransporte

    def validar(self) -> list[ErrorValidacion]:
        p = self.problema
        errores: list[ErrorValidacion] = []
        m, n = len(p.oferta), len(p.demanda)
        if m == 0 or n == 0:
            errores.append(
                ErrorValidacion("problema", "Se requiere al menos un origen y un destino.")
            )
            return errores
        if len(p.costos) != m or any(len(fila) != n for fila in p.costos):
            errores.append(
                ErrorValidacion(
                    "costos", f"La matriz de costos debe tener {m} filas y {n} columnas."
                )
            )
        if any(x < 0 for x in p.oferta):
            errores.append(ErrorValidacion("oferta", "La oferta no puede ser negativa."))
        if any(x < 0 for x in p.demanda):
            errores.append(ErrorValidacion("demanda", "La demanda no puede ser negativa."))
        return errores

    @staticmethod
    def costo_total(
        asignaciones: Asignaciones, costos: tuple[tuple[Fraction, ...], ...]
    ) -> Fraction:
        return suma(cant * costos[i][j] for (i, j), cant in asignaciones.items())

    @staticmethod
    def paso_datos(
        indice: int, original: ProblemaTransporte, balanceado: ProblemaTransporte
    ) -> Paso:
        total_oferta, total_demanda = suma(original.oferta), suma(original.demanda)
        if balanceado.ficticio_destino:
            extra = formatear(total_oferta - total_demanda)
            balance = (
                f"La oferta total ({formatear(total_oferta)}) es mayor que la demanda total "
                f"({formatear(total_demanda)}); se agrega un destino ficticio con costos nulos "
                f"y demanda {extra}."
            )
        elif balanceado.ficticio_origen:
            extra = formatear(total_demanda - total_oferta)
            balance = (
                f"La demanda total ({formatear(total_demanda)}) es mayor que la oferta total "
                f"({formatear(total_oferta)}); se agrega un origen ficticio con costos nulos "
                f"y oferta {extra}."
            )
        else:
            balance = (
                f"El problema está balanceado: oferta y demanda suman {formatear(total_oferta)}."
            )
        m, n = len(balanceado.oferta), len(balanceado.demanda)
        sufijo = (
            " (incluido el ficticio)"
            if (balanceado.ficticio_origen or balanceado.ficticio_destino)
            else ""
        )
        explicacion = f"Se tienen {m} orígenes y {n} destinos{sufijo}. {balance}"
        return Paso(
            indice=indice,
            titulo="Datos del problema",
            explicacion=explicacion,
            estado=estado_transporte(
                balanceado, {}, balanceado.oferta, balanceado.demanda, set(), set()
            ),
        )


def estado_transporte(
    problema: ProblemaTransporte,
    asignaciones: Asignaciones,
    oferta_restante: tuple[Fraction, ...] | list[Fraction],
    demanda_restante: tuple[Fraction, ...] | list[Fraction],
    filas_agotadas: set[int],
    columnas_agotadas: set[int],
) -> dict[str, object]:
    """Construye el diccionario de ``Paso.estado`` según la convención de transporte."""
    return {
        "costos": problema.costos,
        "oferta": problema.oferta,
        "demanda": problema.demanda,
        "asignaciones": dict(asignaciones),
        "oferta_restante": tuple(oferta_restante),
        "demanda_restante": tuple(demanda_restante),
        "filas_agotadas": frozenset(filas_agotadas),
        "columnas_agotadas": frozenset(columnas_agotadas),
        "ficticio_origen": problema.ficticio_origen,
        "ficticio_destino": problema.ficticio_destino,
    }
