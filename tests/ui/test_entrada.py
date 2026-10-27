from fractions import Fraction

import pytest

from plataforma_io.ui.entrada import interpretar_numero, leer_problema


@pytest.mark.parametrize(
    ("texto", "esperado"),
    [
        ("5", Fraction(5)),
        ("  -2 ", Fraction(-2)),
        ("2.5", Fraction(5, 2)),
        ("2,5", Fraction(5, 2)),
        ("5/2", Fraction(5, 2)),
        ("0", Fraction(0)),
    ],
)
def test_interpretar_numero_acepta_enteros_decimales_y_fracciones(texto, esperado):
    assert interpretar_numero(texto) == esperado


@pytest.mark.parametrize("texto", ["", "   ", "abc", "5/0", "1..2", "nan", "inf", "3 4"])
def test_interpretar_numero_rechaza_entradas_invalidas(texto):
    with pytest.raises(ValueError):
        interpretar_numero(texto)


def test_leer_problema_valido():
    textos = [["1", "2", "5"], ["3", "4", "5"], ["4", "6", ""]]
    problema, errores = leer_problema(textos)
    assert errores == []
    assert problema is not None
    assert problema.oferta == (5, 5)
    assert problema.demanda == (4, 6)
    assert problema.costos == ((1, 2), (3, 4))


def test_leer_problema_acepta_fracciones_y_decimales():
    textos = [["1.5", "2/3", "1,5"], ["0", "0", "1.5"], ["1.5", "1.5", ""]]
    problema, errores = leer_problema(textos)
    assert errores == [] and problema is not None
    assert problema.costos[0] == (Fraction(3, 2), Fraction(2, 3))
    assert problema.oferta == (Fraction(3, 2), Fraction(3, 2))


def test_leer_problema_senala_cada_celda_con_error():
    textos = [["", "x", "5"], ["3", "4", "-1"], ["4", "", ""]]
    problema, errores = leer_problema(textos)
    assert problema is None
    celdas = {(e.fila, e.columna) for e in errores}
    assert celdas == {(0, 0), (0, 1), (1, 2), (2, 1)}
    mensajes = " ".join(e.mensaje for e in errores)
    assert "Costo de O1 a D1" in mensajes
    assert "Oferta de O2" in mensajes and "negativo" in mensajes
    assert "Demanda de D2" in mensajes


def test_leer_problema_exige_totales_positivos():
    textos = [["1", "0"], ["0", ""]]
    problema, errores = leer_problema(textos)
    assert problema is None
    assert len(errores) == 2
    assert all("mayor que cero" in e.mensaje for e in errores)
