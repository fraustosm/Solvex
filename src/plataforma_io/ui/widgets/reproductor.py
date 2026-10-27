"""Barra del reproductor de pasos (componente común a los seis métodos)."""

from __future__ import annotations

from collections.abc import Callable

from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSlider,
    QStyle,
    QWidget,
)

from plataforma_io.ui.controlador import ControladorPasos

VELOCIDADES_MS = {"0,5×": 2000, "1×": 1000, "2×": 500}


class ReproductorPasos(QWidget):
    """Emite ``paso_cambiado(indice)`` cada vez que cambia el paso actual."""

    paso_cambiado = Signal(int)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("reproductor")
        self.setFixedHeight(56)
        self._ctl = ControladorPasos()
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._avanzar_automatico)

        SP = QStyle.StandardPixmap
        self._btn_inicio = self._boton(SP.SP_MediaSkipBackward, "Ir al inicio", self.ir_al_inicio)
        self._btn_anterior = self._boton(SP.SP_MediaSeekBackward, "Paso anterior", self.anterior)
        self._btn_play = self._boton(SP.SP_MediaPlay, "Reproducir", self.alternar_reproduccion)
        self._btn_siguiente = self._boton(SP.SP_MediaSeekForward, "Paso siguiente", self.siguiente)
        self._btn_final = self._boton(SP.SP_MediaSkipForward, "Ir al final", self.ir_al_final)

        self._slider = QSlider(Qt.Orientation.Horizontal)
        self._slider.setAccessibleName("Selector de paso")
        self._slider.valueChanged.connect(self.ir_a)
        self._etiqueta = QLabel("Sin pasos")
        self._etiqueta.setMinimumWidth(110)
        self._etiqueta.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self._velocidad = QComboBox()
        self._velocidad.setAccessibleName("Velocidad de reproducción")
        self._velocidad.addItems(list(VELOCIDADES_MS))
        self._velocidad.setCurrentText("1×")
        self._velocidad.currentTextChanged.connect(self._cambiar_velocidad)

        disposicion = QHBoxLayout(self)
        disposicion.setContentsMargins(14, 0, 14, 0)
        disposicion.setSpacing(8)
        for w in (
            self._btn_inicio,
            self._btn_anterior,
            self._btn_play,
            self._btn_siguiente,
            self._btn_final,
        ):
            disposicion.addWidget(w)
        disposicion.addWidget(self._slider, 1)
        disposicion.addWidget(self._etiqueta)
        disposicion.addWidget(self._velocidad)
        self._sincronizar()

    # -- construcción
    def _boton(
        self, icono: QStyle.StandardPixmap, ayuda: str, accion: Callable[[], object]
    ) -> QPushButton:
        boton = QPushButton()
        boton.setIcon(self.style().standardIcon(icono))
        boton.setToolTip(ayuda)
        boton.setAccessibleName(ayuda)
        boton.setFixedSize(34, 34)
        boton.clicked.connect(lambda: accion())
        return boton

    # -- API pública
    @property
    def indice(self) -> int:
        return self._ctl.indice

    def cargar(self, total: int) -> None:
        self.detener()
        self._ctl.establecer_total(total)
        self._slider.blockSignals(True)
        self._slider.setRange(0, max(total - 1, 0))
        self._slider.blockSignals(False)
        self._sincronizar()
        if self._ctl.hay_pasos:
            self.paso_cambiado.emit(0)

    def ir_a(self, indice: int) -> None:
        if self._ctl.ir_a(indice):
            self._sincronizar()
            self.paso_cambiado.emit(self._ctl.indice)

    def siguiente(self) -> None:
        self.ir_a(self._ctl.indice + 1)

    def anterior(self) -> None:
        self.ir_a(self._ctl.indice - 1)

    def ir_al_inicio(self) -> None:
        self.ir_a(0)

    def ir_al_final(self) -> None:
        self.ir_a(self._ctl.total - 1)

    def alternar_reproduccion(self) -> None:
        if self._timer.isActive():
            self.detener()
            return
        if not self._ctl.hay_pasos:
            return
        if self._ctl.al_final:
            self.ir_al_inicio()
        self._timer.start(VELOCIDADES_MS[self._velocidad.currentText()])
        self._btn_play.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPause))
        self._btn_play.setToolTip("Pausar")

    def detener(self) -> None:
        self._timer.stop()
        self._btn_play.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay))
        self._btn_play.setToolTip("Reproducir")

    # -- internos
    def _avanzar_automatico(self) -> None:
        if self._ctl.al_final:
            self.detener()
            return
        self.siguiente()
        if self._ctl.al_final:
            self.detener()

    def _cambiar_velocidad(self, texto: str) -> None:
        if self._timer.isActive():
            self._timer.start(VELOCIDADES_MS[texto])

    def _sincronizar(self) -> None:
        self._slider.blockSignals(True)
        self._slider.setValue(self._ctl.indice)
        self._slider.blockSignals(False)
        self._etiqueta.setText(self._ctl.etiqueta)
        hay = self._ctl.hay_pasos
        for w in (self._btn_inicio, self._btn_anterior):
            w.setEnabled(hay and not self._ctl.al_inicio)
        for w in (self._btn_siguiente, self._btn_final):
            w.setEnabled(hay and not self._ctl.al_final)
        self._btn_play.setEnabled(hay)
        self._slider.setEnabled(hay)
