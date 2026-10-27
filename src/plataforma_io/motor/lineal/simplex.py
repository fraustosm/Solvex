"""Método Simplex (pendiente: informe 3)."""

from __future__ import annotations

from plataforma_io.motor.base import Metodo
from plataforma_io.motor.lineal.problema import ProblemaLineal
from plataforma_io.motor.modelos import ErrorValidacion, Solucion


class Simplex(Metodo):
    """TODO

    1. Convertir a forma estándar (holgura, exceso; minimizar = maximizar el negativo).
    2. Construir la tabla con ``Fraction`` y registrar un ``Paso`` por tabla.
    3. Elegir variable entrante (regla de Dantzig) y saliente (razón mínima); pivotear.
    4. Detectar no acotamiento, degeneración y óptimos alternativos; usar la regla de Bland
       como salvaguarda contra el ciclado.
    """

    nombre = "Método Simplex"
    problema: ProblemaLineal

    def validar(self) -> list[ErrorValidacion]:
        p = self.problema
        errores: list[ErrorValidacion] = []
        if p.n_variables == 0:
            errores.append(ErrorValidacion("objetivo", "Se requiere al menos una variable."))
        for k, r in enumerate(p.restricciones, start=1):
            if len(r.coeficientes) != p.n_variables:
                errores.append(
                    ErrorValidacion(
                        f"restriccion_{k}",
                        f"La restricción {k} debe tener {p.n_variables} coeficientes.",
                    )
                )
        return errores

    def resolver(self) -> Solucion:
        raise NotImplementedError("El Simplex se implementa en el informe 3.")
