"""P01: pantalla de inicio con los métodos agrupados por familia."""

from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget

from plataforma_io import NOMBRE_APP
from plataforma_io.motor.registro import metodos_por_familia

DESCRIPCIONES = {
    "Programación lineal": "Maximizar o minimizar con restricciones",
    "Transporte": "Solución inicial de costo mínimo",
    "Redes y grafos": "Dibuje su red y resuélvala",
}


class PantallaInicio(QWidget):
    metodo_elegido = Signal(str)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("pantalla")
        raiz = QVBoxLayout(self)
        raiz.setContentsMargins(0, 0, 0, 0)
        raiz.setSpacing(0)

        barra = QFrame()
        barra.setObjectName("barra")
        barra.setFixedHeight(56)
        disposicion_barra = QHBoxLayout(barra)
        disposicion_barra.setContentsMargins(20, 0, 20, 0)
        titulo_app = QLabel(NOMBRE_APP)
        titulo_app.setProperty("rol", "subtitulo")
        disposicion_barra.addWidget(titulo_app)
        disposicion_barra.addStretch(1)
        raiz.addWidget(barra)

        cuerpo = QVBoxLayout()
        cuerpo.setContentsMargins(28, 24, 28, 24)
        cuerpo.setSpacing(6)
        titulo = QLabel("¿Qué método desea resolver?")
        titulo.setProperty("rol", "titulo")
        subtitulo = QLabel("Elija un método y recorra la solución paso a paso.")
        subtitulo.setProperty("rol", "secundario")
        cuerpo.addWidget(titulo)
        cuerpo.addWidget(subtitulo)

        tarjetas = QHBoxLayout()
        tarjetas.setSpacing(14)
        for familia, metodos in metodos_por_familia().items():
            tarjetas.addWidget(self._tarjeta(familia, metodos))
        cuerpo.addSpacing(12)
        cuerpo.addLayout(tarjetas)
        cuerpo.addStretch(1)
        raiz.addLayout(cuerpo, 1)

    def _tarjeta(self, familia: str, metodos: list) -> QFrame:  # type: ignore[type-arg]
        tarjeta = QFrame()
        tarjeta.setObjectName("tarjeta")
        disposicion = QVBoxLayout(tarjeta)
        disposicion.setContentsMargins(16, 16, 16, 16)
        disposicion.setSpacing(8)
        nombre = QLabel(familia)
        nombre.setProperty("rol", "subtitulo")
        descripcion = QLabel(DESCRIPCIONES.get(familia, ""))
        descripcion.setProperty("rol", "secundario")
        disposicion.addWidget(nombre)
        disposicion.addWidget(descripcion)
        for info in metodos:
            texto = info.nombre if info.implementado else f"{info.nombre} (próximamente)"
            boton = QPushButton(texto)
            boton.setObjectName(f"metodo_{info.clave}")
            boton.clicked.connect(lambda _=False, c=info.clave: self.metodo_elegido.emit(c))
            disposicion.addWidget(boton)
        disposicion.addStretch(1)
        return tarjeta
