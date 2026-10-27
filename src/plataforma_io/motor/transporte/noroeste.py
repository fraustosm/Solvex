"""Método de la Esquina Noroeste."""

from __future__ import annotations

from fractions import Fraction

from plataforma_io.motor.modelos import Paso, Solucion, TipoSolucion, formatear
from plataforma_io.motor.transporte.base import (
    Asignaciones,
    MetodoTransporte,
    estado_transporte,
)


class EsquinaNoroeste(MetodoTransporte):
    """Solución básica factible inicial: se asigna desde la celda superior izquierda."""

    nombre = "Esquina Noroeste"

    def resolver(self) -> Solucion:
        self._exigir_valido()
        original = self.problema
        prob = original.balancear()
        m, n = len(prob.oferta), len(prob.demanda)
        oferta, demanda = list(prob.oferta), list(prob.demanda)
        asignaciones: Asignaciones = {}
        filas_agotadas: set[int] = set()
        columnas_agotadas: set[int] = set()
        pasos: list[Paso] = [self.paso_datos(1, original, prob)]

        i = j = 0
        while i < m and j < n:
            disponible, requerido = oferta[i], demanda[j]
            cantidad = min(disponible, requerido)
            celda = (i, j)
            asignaciones[celda] = cantidad
            oferta[i] -= cantidad
            demanda[j] -= cantidad
            agota_fila, agota_columna = oferta[i] == 0, demanda[j] == 0

            explicacion = (
                f"Esquina noroeste vigente: celda (O{i + 1}, D{j + 1}). Se asigna el mínimo entre "
                f"la oferta restante ({formatear(disponible)}) y la demanda restante "
                f"({formatear(requerido)}): {formatear(cantidad)} unidades."
            )
            if agota_fila and agota_columna:
                if i < m - 1:
                    filas_agotadas.add(i)
                    explicacion += (
                        f" Se agotan a la vez la oferta de O{i + 1} y la demanda de D{j + 1}; se "
                        "elimina solo la fila y la columna conserva demanda 0, por lo que la "
                        "siguiente asignación será 0 (solución degenerada)."
                    )
                    i += 1
                else:
                    filas_agotadas.add(i)
                    columnas_agotadas.add(j)
                    explicacion += " Se agotan la última oferta y la última demanda."
                    j += 1
            elif agota_fila:
                filas_agotadas.add(i)
                explicacion += f" Se agota la oferta de O{i + 1}; se pasa a la fila siguiente."
                i += 1
            else:
                columnas_agotadas.add(j)
                explicacion += (
                    f" Se satisface la demanda de D{j + 1}; se pasa a la columna siguiente."
                )
                j += 1

            pasos.append(
                Paso(
                    indice=len(pasos) + 1,
                    titulo=f"Asignar en (O{celda[0] + 1}, D{celda[1] + 1})",
                    explicacion=explicacion,
                    estado=estado_transporte(
                        prob, asignaciones, oferta, demanda, filas_agotadas, columnas_agotadas
                    ),
                    resaltados=(celda,),
                )
            )

        costo = self.costo_total(asignaciones, prob.costos)
        degenerada = any(cant == 0 for cant in asignaciones.values())
        terminos = " + ".join(
            f"{formatear(cant)}×{formatear(prob.costos[a][b])}"
            for (a, b), cant in asignaciones.items()
        )
        pasos.append(
            Paso(
                indice=len(pasos) + 1,
                titulo="Resumen",
                explicacion=(
                    f"Costo total = {terminos} = {formatear(costo)}. "
                    f"La solución tiene {len(asignaciones)} celdas básicas "
                    f"({m} + {n} − 1 = {m + n - 1})."
                ),
                estado={
                    **estado_transporte(
                        prob, asignaciones, oferta, demanda, filas_agotadas, columnas_agotadas
                    ),
                    "costo_total": costo,
                },
            )
        )

        mensajes = (
            ["La solución es degenerada: incluye una asignación igual a cero."]
            if degenerada
            else []
        )
        return Solucion(
            tipo=TipoSolucion.BASICA_FACTIBLE,
            valores={
                "asignaciones": dict(asignaciones),
                "celdas_basicas": len(asignaciones),
                "degenerada": degenerada,
                "ficticio_origen": prob.ficticio_origen,
                "ficticio_destino": prob.ficticio_destino,
            },
            objetivo=Fraction(costo),
            pasos=pasos,
            mensajes=mensajes,
        )
