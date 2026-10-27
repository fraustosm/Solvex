"""Visor de matrices de transporte (Esquina Noroeste y, próximamente, Vogel)."""

from __future__ import annotations

from fractions import Fraction

from PySide6.QtCore import Qt
from PySide6.QtGui import QBrush, QColor, QFont
from PySide6.QtWidgets import (
    QAbstractItemView,
    QHeaderView,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
)

from plataforma_io.motor.modelos import Paso, formatear
from plataforma_io.ui.estilos import COLORES
from plataforma_io.ui.visores import Visor


def _item(
    texto: str,
    *,
    fondo: str | None = None,
    color: str | None = None,
    negrita: bool = False,
) -> QTableWidgetItem:
    item = QTableWidgetItem(texto)
    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
    item.setFlags(Qt.ItemFlag.ItemIsEnabled)
    if fondo:
        item.setBackground(QBrush(QColor(fondo)))
    if color:
        item.setForeground(QBrush(QColor(color)))
    if negrita:
        fuente = QFont()
        fuente.setBold(True)
        item.setFont(fuente)
    return item


class VisorTransporte(Visor):
    """Matriz de costos con asignaciones; la última fila y columna muestran demanda y oferta."""

    def __init__(self) -> None:
        super().__init__()
        self._tabla = QTableWidget()
        self._tabla.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self._tabla.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self._tabla.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self._tabla.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        disposicion = QVBoxLayout(self)
        disposicion.setContentsMargins(0, 0, 0, 0)
        disposicion.addWidget(self._tabla)

    def mostrar(self, paso: Paso) -> None:
        e = paso.estado
        costos: tuple[tuple[Fraction, ...], ...] = e["costos"]
        m, n = len(costos), len(costos[0])
        asignaciones: dict[tuple[int, int], Fraction] = e["asignaciones"]
        filas_agotadas: frozenset[int] = e["filas_agotadas"]
        columnas_agotadas: frozenset[int] = e["columnas_agotadas"]
        resaltados = set(paso.resaltados)

        etiquetas_o = [
            f"O{i + 1}" + ("*" if e["ficticio_origen"] and i == m - 1 else "") for i in range(m)
        ]
        etiquetas_d = [
            f"D{j + 1}" + ("*" if e["ficticio_destino"] and j == n - 1 else "") for j in range(n)
        ]
        self._tabla.clear()
        self._tabla.setRowCount(m + 1)
        self._tabla.setColumnCount(n + 1)
        self._tabla.setVerticalHeaderLabels([*etiquetas_o, "Demanda"])
        self._tabla.setHorizontalHeaderLabels([*etiquetas_d, "Oferta"])

        for i in range(m):
            for j in range(n):
                costo = formatear(costos[i][j])
                asignada = asignaciones.get((i, j))
                if (i, j) in resaltados:
                    fondo, color = COLORES["pivote_elemento"], None
                elif asignada is not None:
                    fondo, color = COLORES["asignada"], None
                elif i in filas_agotadas or j in columnas_agotadas:
                    fondo, color = COLORES["agotada"], COLORES["descartado"]
                else:
                    fondo, color = None, None
                texto = (
                    f"{formatear(asignada)}\n(costo {costo})"
                    if asignada is not None
                    else f"costo {costo}"
                )
                self._tabla.setItem(
                    i, j, _item(texto, fondo=fondo, color=color, negrita=asignada is not None)
                )
        for i in range(m):
            restante, total = e["oferta_restante"][i], e["oferta"][i]
            self._tabla.setItem(
                i,
                n,
                _item(f"{formatear(restante)} de {formatear(total)}", fondo=COLORES["agotada"]),
            )
        for j in range(n):
            restante, total = e["demanda_restante"][j], e["demanda"][j]
            self._tabla.setItem(
                m,
                j,
                _item(f"{formatear(restante)} de {formatear(total)}", fondo=COLORES["agotada"]),
            )
        self._tabla.setItem(m, n, _item("", fondo=COLORES["agotada"]))
