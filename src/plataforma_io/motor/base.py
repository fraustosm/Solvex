"""Clase abstracta común a todos los métodos."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, ClassVar

from plataforma_io.motor.modelos import ErrorValidacion, Paso, Solucion


class ProblemaInvalido(ValueError):
    """Se lanza al resolver un problema que no pasó la validación."""

    def __init__(self, errores: list[ErrorValidacion]) -> None:
        self.errores = errores
        super().__init__("; ".join(f"{e.campo}: {e.mensaje}" for e in errores))


class Metodo(ABC):
    """Contrato de un método: validar, resolver y exponer sus pasos."""

    nombre: ClassVar[str]

    def __init__(self, problema: Any) -> None:
        self.problema = problema

    @abstractmethod
    def validar(self) -> list[ErrorValidacion]:
        """Devuelve la lista de errores de captura (vacía si el problema es válido)."""

    @abstractmethod
    def resolver(self) -> Solucion:
        """Resuelve el problema generando un ``Paso`` por cada operación relevante."""

    def pasos(self) -> list[Paso]:
        return self.resolver().pasos

    def _exigir_valido(self) -> None:
        errores = self.validar()
        if errores:
            raise ProblemaInvalido(errores)
