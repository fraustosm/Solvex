"""Ventana principal: inicio, captura de datos y resolución paso a paso."""

from __future__ import annotations

from PySide6.QtWidgets import QMainWindow, QMessageBox, QStackedWidget

from plataforma_io import NOMBRE_APP, SUBTITULO_APP
from plataforma_io.motor.base import ProblemaInvalido
from plataforma_io.motor.registro import METODOS
from plataforma_io.motor.transporte.problema import ProblemaTransporte
from plataforma_io.ui.pantallas.captura_transporte import PantallaCapturaTransporte
from plataforma_io.ui.pantallas.inicio import PantallaInicio
from plataforma_io.ui.pantallas.resolucion import PantallaResolucion


class VentanaPrincipal(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle(f"{NOMBRE_APP} · {SUBTITULO_APP}")
        self.setMinimumSize(1024, 700)
        self.resize(1280, 800)

        self.inicio = PantallaInicio()
        self.captura = PantallaCapturaTransporte()
        self.resolucion = PantallaResolucion()
        self._pila = QStackedWidget()
        for pantalla in (self.inicio, self.captura, self.resolucion):
            self._pila.addWidget(pantalla)
        self.setCentralWidget(self._pila)
        self._clave_actual = ""

        self.inicio.metodo_elegido.connect(self.abrir_metodo)
        self.captura.regresar.connect(self.mostrar_inicio)
        self.captura.resolver_solicitado.connect(self._resolver_transporte)
        self.resolucion.regresar.connect(self.mostrar_inicio)
        self.resolucion.editar_datos.connect(self._volver_a_captura)

    def mostrar_inicio(self) -> None:
        self.resolucion.reproductor.detener()
        self._pila.setCurrentWidget(self.inicio)

    def _volver_a_captura(self) -> None:
        self.resolucion.reproductor.detener()
        self._pila.setCurrentWidget(self.captura)

    def abrir_metodo(self, clave: str) -> None:
        info = METODOS[clave]
        if not info.implementado:
            QMessageBox.information(
                self,
                "En desarrollo",
                f"El método «{info.nombre}» se implementará en una etapa posterior del proyecto.",
            )
            return
        self._clave_actual = clave
        self.captura.configurar(clave, info.nombre)
        self._pila.setCurrentWidget(self.captura)

    def _resolver_transporte(self, problema: ProblemaTransporte) -> None:
        info = METODOS[self._clave_actual]
        try:
            solucion = info.clase(problema).resolver()
        except ProblemaInvalido as exc:
            self.captura.mostrar_error("\n".join(e.mensaje for e in exc.errores))
            return
        self.resolucion.cargar(f"{info.familia} · {info.nombre}", info.familia, solucion)
        self._pila.setCurrentWidget(self.resolucion)
