"""P11: captura de un problema de transporte (Esquina Noroeste y Vogel)."""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QBrush, QColor
from PySide6.QtWidgets import (
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from plataforma_io.motor.ejemplos import transporte_clasico
from plataforma_io.motor.modelos import formatear, suma
from plataforma_io.motor.registro import FAMILIA_TRANSPORTE, METODOS
from plataforma_io.motor.transporte.problema import ProblemaTransporte
from plataforma_io.servicios.persistencia import (
    EXTENSION,
    ArchivoInvalido,
    abrir_problema,
    guardar_problema,
)
from plataforma_io.ui.entrada import ErrorCelda, interpretar_numero, leer_problema
from plataforma_io.ui.estilos import COLORES

MAXIMO = 10  # orígenes y destinos admitidos por la interfaz


class PantallaCapturaTransporte(QWidget):
    """Tabla editable: costos en el centro, oferta a la derecha y demanda abajo."""

    regresar = Signal()
    resolver_solicitado = Signal(object)  # ProblemaTransporte ya validado

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("pantalla")
        self._clave = "noroeste"
        self._en_carga = False

        raiz = QVBoxLayout(self)
        raiz.setContentsMargins(0, 0, 0, 0)
        raiz.setSpacing(0)

        barra = QFrame()
        barra.setObjectName("barra")
        barra.setFixedHeight(56)
        fila = QHBoxLayout(barra)
        fila.setContentsMargins(16, 0, 16, 0)
        self._btn_inicio = QPushButton("← Inicio")
        self._btn_inicio.clicked.connect(self.regresar.emit)
        self._titulo = QLabel()
        self._titulo.setProperty("rol", "titulo")
        self._btn_abrir = QPushButton("Abrir")
        self._btn_abrir.clicked.connect(self.abrir)
        self._btn_guardar = QPushButton("Guardar")
        self._btn_guardar.clicked.connect(self.guardar)
        fila.addWidget(self._btn_inicio)
        fila.addWidget(self._titulo, 1)
        fila.addWidget(self._btn_abrir)
        fila.addWidget(self._btn_guardar)
        raiz.addWidget(barra)

        panel = QFrame()
        panel.setObjectName("panel")
        cuerpo = QVBoxLayout(panel)
        cuerpo.setContentsMargins(16, 14, 16, 14)
        cuerpo.setSpacing(10)

        dimensiones = QHBoxLayout()
        self._origenes = self._spin()
        self._destinos = self._spin()
        dimensiones.addWidget(QLabel("Orígenes"))
        dimensiones.addWidget(self._origenes)
        dimensiones.addSpacing(16)
        dimensiones.addWidget(QLabel("Destinos"))
        dimensiones.addWidget(self._destinos)
        dimensiones.addStretch(1)
        ayuda = QLabel("Escriba números enteros, decimales o fracciones (5, 2.5, 5/2).")
        ayuda.setProperty("rol", "secundario")
        dimensiones.addWidget(ayuda)
        cuerpo.addLayout(dimensiones)

        self._tabla = QTableWidget()
        self._tabla.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self._tabla.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self._tabla.itemChanged.connect(self._al_editar)
        cuerpo.addWidget(self._tabla, 1)

        self._balance = QLabel()
        self._balance.setProperty("rol", "secundario")
        self._errores = QLabel()
        self._errores.setWordWrap(True)
        self._errores.setStyleSheet(f"color: {COLORES['error']};")
        self._errores.hide()
        cuerpo.addWidget(self._balance)
        cuerpo.addWidget(self._errores)

        contenedor = QVBoxLayout()
        contenedor.setContentsMargins(12, 12, 12, 8)
        contenedor.addWidget(panel, 1)
        raiz.addLayout(contenedor, 1)

        pie = QFrame()
        pie.setObjectName("barra")
        pie.setFixedHeight(56)
        fila_pie = QHBoxLayout(pie)
        fila_pie.setContentsMargins(16, 0, 16, 0)
        self._btn_ejemplo = QPushButton("Cargar ejemplo")
        self._btn_ejemplo.clicked.connect(self.cargar_ejemplo)
        self._btn_limpiar = QPushButton("Limpiar")
        self._btn_limpiar.clicked.connect(self.limpiar)
        self._btn_resolver = QPushButton("Resolver paso a paso")
        self._btn_resolver.setProperty("primario", True)
        self._btn_resolver.clicked.connect(self.resolver)
        fila_pie.addWidget(self._btn_ejemplo)
        fila_pie.addWidget(self._btn_limpiar)
        fila_pie.addStretch(1)
        fila_pie.addWidget(self._btn_resolver)
        raiz.addWidget(pie)

        self._origenes.valueChanged.connect(self._cambiar_dimensiones)
        self._destinos.valueChanged.connect(self._cambiar_dimensiones)
        self._construir_tabla(3, 3, {})

    # ------------------------------------------------------------------ API pública
    def configurar(self, clave: str, nombre: str) -> None:
        self._clave = clave
        self._titulo.setText(f"{FAMILIA_TRANSPORTE} · {nombre} · Captura")
        self._ocultar_error()

    @property
    def dimensiones(self) -> tuple[int, int]:
        return self._origenes.value(), self._destinos.value()

    def establecer_datos(self, problema: ProblemaTransporte) -> None:
        """Carga un problema en la tabla (ajusta orígenes y destinos)."""
        m, n = len(problema.oferta), len(problema.demanda)
        valores: dict[tuple[int, int], str] = {}
        for i in range(m):
            for j in range(n):
                valores[(i, j)] = formatear(problema.costos[i][j])
            valores[(i, n)] = formatear(problema.oferta[i])
        for j in range(n):
            valores[(m, j)] = formatear(problema.demanda[j])
        self._en_carga = True
        self._origenes.setValue(m)
        self._destinos.setValue(n)
        self._en_carga = False
        self._construir_tabla(m, n, valores)
        self._ocultar_error()

    def leer(self) -> tuple[ProblemaTransporte | None, list[ErrorCelda]]:
        return leer_problema(self._textos())

    def resolver(self) -> None:
        problema, errores = self.leer()
        self._marcar_errores(errores)
        if problema is None:
            return
        self._ocultar_error()
        self.resolver_solicitado.emit(problema)

    def cargar_ejemplo(self) -> None:
        self.establecer_datos(transporte_clasico())

    def limpiar(self) -> None:
        m, n = self.dimensiones
        self._construir_tabla(m, n, {})
        self._ocultar_error()

    def mostrar_error(self, mensaje: str) -> None:
        self._errores.setText(mensaje)
        self._errores.show()

    def guardar(self) -> None:
        problema, errores = self.leer()
        self._marcar_errores(errores)
        if problema is None:
            return
        ruta, _ = QFileDialog.getSaveFileName(
            self, "Guardar problema", "", f"Problema de Solvex (*{EXTENSION})"
        )
        if not ruta:
            return
        if not ruta.endswith(EXTENSION):
            ruta += EXTENSION
        try:
            guardar_problema(ruta, self._clave, problema.a_dict())
        except OSError as exc:
            self.mostrar_error(f"No se pudo guardar el archivo: {exc}")

    def abrir(self) -> None:
        ruta, _ = QFileDialog.getOpenFileName(
            self, "Abrir problema", "", f"Problema de Solvex (*{EXTENSION})"
        )
        if not ruta:
            return
        try:
            clave, datos = abrir_problema(Path(ruta))
            if clave not in METODOS or METODOS[clave].familia != FAMILIA_TRANSPORTE:
                raise ArchivoInvalido("El archivo no corresponde a un problema de transporte.")
            problema = ProblemaTransporte.desde_dict(datos)
        except (ArchivoInvalido, KeyError, ValueError, ZeroDivisionError) as exc:
            QMessageBox.warning(self, "No se pudo abrir", str(exc))
            return
        self.establecer_datos(problema)

    # ------------------------------------------------------------------ internos
    @staticmethod
    def _spin() -> QSpinBox:
        spin = QSpinBox()
        spin.setRange(1, MAXIMO)
        spin.setValue(3)
        return spin

    def _textos(self) -> list[list[str]]:
        t = self._tabla
        return [
            [(t.item(i, j).text() if t.item(i, j) else "") for j in range(t.columnCount())]
            for i in range(t.rowCount())
        ]

    def _rol(self, i: int, j: int, m: int, n: int) -> str:
        if i == m and j == n:
            return "esquina"
        if i == m or j == n:
            return "total"
        return "costo"

    def _construir_tabla(self, m: int, n: int, valores: dict[tuple[int, int], str]) -> None:
        t = self._tabla
        t.blockSignals(True)
        t.clear()
        t.setRowCount(m + 1)
        t.setColumnCount(n + 1)
        t.setVerticalHeaderLabels([*(f"O{i + 1}" for i in range(m)), "Demanda"])
        t.setHorizontalHeaderLabels([*(f"D{j + 1}" for j in range(n)), "Oferta"])
        for i in range(m + 1):
            for j in range(n + 1):
                item = QTableWidgetItem(valores.get((i, j), ""))
                rol = self._rol(i, j, m, n)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                if rol == "esquina":
                    item.setFlags(Qt.ItemFlag.NoItemFlags)
                if rol != "costo":
                    item.setBackground(QBrush(QColor(COLORES["agotada"])))
                t.setItem(i, j, item)
        t.blockSignals(False)
        self._actualizar_balance()

    def _cambiar_dimensiones(self) -> None:
        if self._en_carga:
            return
        m_viejo, n_viejo = self._tabla.rowCount() - 1, self._tabla.columnCount() - 1
        textos = self._textos()
        m, n = self.dimensiones
        valores: dict[tuple[int, int], str] = {}
        for i in range(min(m, m_viejo)):
            for j in range(min(n, n_viejo)):
                valores[(i, j)] = textos[i][j]
            valores[(i, n)] = textos[i][n_viejo]
        for j in range(min(n, n_viejo)):
            valores[(m, j)] = textos[m_viejo][j]
        self._construir_tabla(m, n, valores)
        self._ocultar_error()

    def _al_editar(self, item: QTableWidgetItem) -> None:
        m, n = self._tabla.rowCount() - 1, self._tabla.columnCount() - 1
        rol = self._rol(item.row(), item.column(), m, n)
        self._tabla.blockSignals(True)
        item.setBackground(QBrush(QColor("white" if rol == "costo" else COLORES["agotada"])))
        item.setForeground(QBrush(QColor(COLORES["texto"])))
        self._tabla.blockSignals(False)
        self._actualizar_balance()

    def _actualizar_balance(self) -> None:
        textos = self._textos()
        m, n = len(textos) - 1, len(textos[0]) - 1
        try:
            oferta = suma(interpretar_numero(textos[i][n]) for i in range(m))
            demanda = suma(interpretar_numero(textos[m][j]) for j in range(n))
        except ValueError:
            self._balance.setText("Complete la oferta y la demanda para ver el balance.")
            return
        base = f"Oferta total: {formatear(oferta)} · Demanda total: {formatear(demanda)} · "
        if oferta == demanda:
            self._balance.setText(base + "problema balanceado.")
        elif oferta > demanda:
            self._balance.setText(
                base + f"se agregará un destino ficticio con demanda {formatear(oferta - demanda)}."
            )
        else:
            self._balance.setText(
                base + f"se agregará un origen ficticio con oferta {formatear(demanda - oferta)}."
            )

    def _marcar_errores(self, errores: list[ErrorCelda]) -> None:
        t = self._tabla
        t.blockSignals(True)
        for e in errores:
            item = t.item(e.fila, e.columna)
            if item is not None:
                item.setBackground(QBrush(QColor("#FBE3E0")))
                item.setForeground(QBrush(QColor(COLORES["error"])))
        t.blockSignals(False)
        if not errores:
            self._ocultar_error()
            return
        lineas = [e.mensaje for e in errores[:5]]
        if len(errores) > 5:
            lineas.append(f"... y {len(errores) - 5} errores más.")
        self.mostrar_error("\n".join(lineas))

    def _ocultar_error(self) -> None:
        self._errores.clear()
        self._errores.hide()
