"""Punto de entrada de la aplicación de escritorio."""

from __future__ import annotations

import sys
from collections.abc import Sequence

from PySide6.QtWidgets import QApplication

from plataforma_io import NOMBRE_APP
from plataforma_io.ui.estilos import hoja_estilos
from plataforma_io.ui.ventana_principal import VentanaPrincipal


def main(argv: Sequence[str] | None = None) -> int:
    app = QApplication(list(argv) if argv is not None else sys.argv)
    app.setApplicationName(NOMBRE_APP)
    app.setStyleSheet(hoja_estilos())
    ventana = VentanaPrincipal()
    ventana.show()
    return app.exec()
