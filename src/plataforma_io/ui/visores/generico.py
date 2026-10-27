"""Visor de respaldo: muestra el estado del paso como texto (sirve para depurar nuevos métodos)."""

from __future__ import annotations

from pprint import pformat

from PySide6.QtWidgets import QPlainTextEdit, QVBoxLayout

from plataforma_io.motor.modelos import Paso
from plataforma_io.ui.visores import Visor


class VisorGenerico(Visor):
    def __init__(self) -> None:
        super().__init__()
        self._texto = QPlainTextEdit()
        self._texto.setReadOnly(True)
        self._texto.setStyleSheet(
            'font-family: "JetBrains Mono", "Consolas", monospace; font-size: 13px;'
        )
        disposicion = QVBoxLayout(self)
        disposicion.setContentsMargins(0, 0, 0, 0)
        disposicion.addWidget(self._texto)

    def mostrar(self, paso: Paso) -> None:
        self._texto.setPlainText(pformat(paso.estado, width=90))
