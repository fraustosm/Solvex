"""Plantilla de resolución (Anexo B, B.7): común a los seis métodos."""

from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from plataforma_io.motor.modelos import Solucion
from plataforma_io.ui.visores import Visor, crear_visor
from plataforma_io.ui.widgets.reproductor import ReproductorPasos


class PantallaResolucion(QWidget):
    regresar = Signal()
    editar_datos = Signal()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("pantalla")
        self._solucion: Solucion | None = None
        self._visores: dict[str, Visor] = {}

        raiz = QVBoxLayout(self)
        raiz.setContentsMargins(0, 0, 0, 0)
        raiz.setSpacing(0)

        # Barra superior (56 px)
        barra = QFrame()
        barra.setObjectName("barra")
        barra.setFixedHeight(56)
        fila = QHBoxLayout(barra)
        fila.setContentsMargins(16, 0, 16, 0)
        self._btn_regresar = QPushButton("← Inicio")
        self._btn_regresar.clicked.connect(self.regresar.emit)
        self._btn_editar = QPushButton("Editar datos")
        self._btn_editar.clicked.connect(self.editar_datos.emit)
        self._titulo = QLabel()
        self._titulo.setProperty("rol", "titulo")
        fila.addWidget(self._btn_regresar)
        fila.addWidget(self._titulo, 1)
        fila.addWidget(self._btn_editar)
        raiz.addWidget(barra)

        self._aviso = QLabel()
        self._aviso.setObjectName("aviso")
        self._aviso.setWordWrap(True)
        self._aviso.hide()
        raiz.addWidget(self._aviso)

        # Cuerpo: panel de pasos (izquierda) + visualización y explicación (centro)
        cuerpo = QHBoxLayout()
        cuerpo.setContentsMargins(12, 12, 12, 12)
        cuerpo.setSpacing(12)

        panel_pasos = QFrame()
        panel_pasos.setObjectName("panel")
        panel_pasos.setFixedWidth(280)
        lp = QVBoxLayout(panel_pasos)
        etiqueta_pasos = QLabel("Pasos")
        etiqueta_pasos.setProperty("rol", "secundario")
        self._lista = QListWidget()
        self._lista.currentRowChanged.connect(self._fila_elegida)
        lp.addWidget(etiqueta_pasos)
        lp.addWidget(self._lista, 1)
        cuerpo.addWidget(panel_pasos)

        centro = QVBoxLayout()
        centro.setSpacing(12)
        self._pila = QStackedWidget()
        centro.addWidget(self._pila, 1)

        panel_explicacion = QFrame()
        panel_explicacion.setObjectName("panel")
        panel_explicacion.setFixedHeight(160)
        le = QVBoxLayout(panel_explicacion)
        self._titulo_paso = QLabel()
        self._titulo_paso.setProperty("rol", "subtitulo")
        self._explicacion = QLabel()
        self._explicacion.setWordWrap(True)
        self._explicacion.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        le.addWidget(self._titulo_paso)
        le.addWidget(self._explicacion, 1)
        centro.addWidget(panel_explicacion)
        cuerpo.addLayout(centro, 1)
        raiz.addLayout(cuerpo, 1)

        self._reproductor = ReproductorPasos()
        self._reproductor.paso_cambiado.connect(self._mostrar_paso)
        raiz.addWidget(self._reproductor)

    @property
    def reproductor(self) -> ReproductorPasos:
        return self._reproductor

    def cargar(self, titulo: str, familia: str, solucion: Solucion) -> None:
        self._solucion = solucion
        self._titulo.setText(titulo)
        self._aviso.setText(" ".join(solucion.mensajes))
        self._aviso.setVisible(bool(solucion.mensajes))
        visor = self._visores.get(familia)
        if visor is None:
            visor = crear_visor(familia)
            self._visores[familia] = visor
            self._pila.addWidget(visor)
        self._pila.setCurrentWidget(visor)
        self._lista.blockSignals(True)
        self._lista.clear()
        self._lista.addItems([f"{p.indice}. {p.titulo}" for p in solucion.pasos])
        self._lista.blockSignals(False)
        self._reproductor.cargar(len(solucion.pasos))

    def _fila_elegida(self, fila: int) -> None:
        if fila >= 0:
            self._reproductor.ir_a(fila)

    def _mostrar_paso(self, indice: int) -> None:
        if self._solucion is None:
            return
        paso = self._solucion.pasos[indice]
        self._lista.blockSignals(True)
        self._lista.setCurrentRow(indice)
        self._lista.blockSignals(False)
        self._titulo_paso.setText(f"Paso {paso.indice}: {paso.titulo}")
        self._explicacion.setText(paso.explicacion)
        visor = self._pila.currentWidget()
        if isinstance(visor, Visor):
            visor.mostrar(paso)
