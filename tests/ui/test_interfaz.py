"""Pruebas de humo de la interfaz (requieren PySide6; se ejecutan sin pantalla)."""

import os

import pytest

pytest.importorskip("PySide6")
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtWidgets import QApplication, QFileDialog, QMessageBox, QPushButton  # noqa: E402

from plataforma_io.motor.ejemplos import transporte_clasico  # noqa: E402
from plataforma_io.ui.estilos import hoja_estilos  # noqa: E402
from plataforma_io.ui.ventana_principal import VentanaPrincipal  # noqa: E402

pytestmark = pytest.mark.gui


@pytest.fixture(scope="module")
def app():
    instancia = QApplication.instance() or QApplication([])
    instancia.setStyleSheet(hoja_estilos())
    return instancia


@pytest.fixture
def ventana(app):
    v = VentanaPrincipal()
    yield v
    v.close()


def test_el_inicio_muestra_todos_los_metodos(ventana):
    botones = ventana.inicio.findChildren(QPushButton)
    assert len(botones) == 9


def test_abrir_noroeste_muestra_la_captura(ventana):
    ventana.abrir_metodo("noroeste")
    assert ventana._pila.currentWidget() is ventana.captura
    assert "Esquina Noroeste" in ventana.captura._titulo.text()


def test_resolver_el_ejemplo_y_recorrer_los_pasos(ventana):
    ventana.abrir_metodo("noroeste")
    ventana.captura.cargar_ejemplo()
    assert ventana.captura.dimensiones == (3, 4)
    ventana.captura.resolver()
    assert ventana._pila.currentWidget() is ventana.resolucion
    repro = ventana.resolucion.reproductor
    assert repro.indice == 0
    repro.siguiente()
    assert repro.indice == 1
    repro.ir_al_final()
    assert "Resumen" in ventana.resolucion._titulo_paso.text()
    assert "500" in ventana.resolucion._explicacion.text()
    ventana.mostrar_inicio()
    assert ventana._pila.currentWidget() is ventana.inicio


def test_resolver_con_datos_escritos_por_el_usuario(ventana):
    ventana.abrir_metodo("noroeste")
    ventana.captura.limpiar()
    ventana.captura._origenes.setValue(2)
    ventana.captura._destinos.setValue(3)
    tabla = ventana.captura._tabla
    datos = {
        (0, 0): "1",
        (0, 1): "2",
        (0, 2): "3",
        (0, 3): "20",
        (1, 0): "4",
        (1, 1): "5",
        (1, 2): "6",
        (1, 3): "30",
        (2, 0): "10",
        (2, 1): "10",
        (2, 2): "10",
    }
    for (i, j), texto in datos.items():
        tabla.item(i, j).setText(texto)
    assert "destino ficticio" in ventana.captura._balance.text()
    ventana.captura.resolver()
    assert ventana._pila.currentWidget() is ventana.resolucion
    ventana.resolucion.reproductor.ir_al_final()
    assert "90" in ventana.resolucion._explicacion.text()
    # el problema es degenerado: se muestra el aviso
    assert not ventana.resolucion._aviso.isHidden()
    assert "degenerada" in ventana.resolucion._aviso.text()
    # editar datos regresa a la captura sin perder lo escrito
    ventana.resolucion.editar_datos.emit()
    assert ventana._pila.currentWidget() is ventana.captura
    assert tabla.item(0, 0).text() == "1"


def test_datos_incompletos_no_navegan_y_marcan_los_errores(ventana):
    ventana.abrir_metodo("noroeste")
    ventana.captura.limpiar()
    ventana.captura.resolver()
    assert ventana._pila.currentWidget() is ventana.captura
    assert not ventana.captura._errores.isHidden()
    assert "escriba un número" in ventana.captura._errores.text()
    # corregir una celda quita su marca de error
    item = ventana.captura._tabla.item(0, 0)
    item.setText("7")
    assert item.background().color().name().lower() == "#ffffff"


def test_cambiar_dimensiones_conserva_lo_escrito(ventana):
    ventana.abrir_metodo("noroeste")
    ventana.captura.cargar_ejemplo()
    ventana.captura._destinos.setValue(5)
    tabla = ventana.captura._tabla
    assert tabla.columnCount() == 6
    assert tabla.item(0, 0).text() == "10"  # costo conservado
    assert tabla.item(0, 5).text() == "15"  # la oferta se movió a la nueva última columna
    assert tabla.item(0, 4).text() == ""  # destino nuevo, vacío


def test_guardar_y_abrir_un_problema(ventana, monkeypatch, tmp_path):
    ruta = tmp_path / "mi_problema.ioproblema"
    monkeypatch.setattr(QFileDialog, "getSaveFileName", lambda *a, **k: (str(ruta), ""))
    monkeypatch.setattr(QFileDialog, "getOpenFileName", lambda *a, **k: (str(ruta), ""))
    ventana.abrir_metodo("noroeste")
    ventana.captura.cargar_ejemplo()
    ventana.captura.guardar()
    assert ruta.exists()
    ventana.captura.limpiar()
    ventana.captura.abrir()
    problema, errores = ventana.captura.leer()
    assert errores == [] and problema == transporte_clasico()


def test_metodo_no_implementado_avisa_y_no_navega(ventana, monkeypatch):
    avisos = []
    monkeypatch.setattr(QMessageBox, "information", lambda *a, **k: avisos.append(a))
    ventana.abrir_metodo("simplex")
    assert avisos and ventana._pila.currentWidget() is ventana.inicio
