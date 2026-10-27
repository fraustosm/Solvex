"""Visores: interpretan ``Paso.estado`` y lo dibujan según la familia de métodos."""

from __future__ import annotations

from PySide6.QtWidgets import QWidget

from plataforma_io.motor.modelos import Paso
from plataforma_io.motor.registro import FAMILIA_TRANSPORTE


class Visor(QWidget):
    """Contrato de un visor: recibe un paso y lo muestra."""

    def mostrar(self, paso: Paso) -> None:  # pragma: no cover - interfaz
        raise NotImplementedError


def crear_visor(familia: str) -> Visor:
    """Devuelve el visor de la familia. TODO: visores de programación lineal y de grafos."""
    from plataforma_io.ui.visores.generico import VisorGenerico
    from plataforma_io.ui.visores.transporte import VisorTransporte

    if familia == FAMILIA_TRANSPORTE:
        return VisorTransporte()
    return VisorGenerico()
