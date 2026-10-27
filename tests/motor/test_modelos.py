from fractions import Fraction

import pytest

from plataforma_io.motor.modelos import Paso, a_fraccion, formatear


def test_a_fraccion_acepta_enteros_textos_y_decimales():
    assert a_fraccion(3) == Fraction(3)
    assert a_fraccion("7/2") == Fraction(7, 2)
    assert a_fraccion(0.1) == Fraction(1, 10)  # sin residuos de punto flotante
    assert a_fraccion(Fraction(1, 3)) == Fraction(1, 3)


@pytest.mark.parametrize(
    ("valor", "esperado"),
    [(Fraction(5), "5"), (Fraction(7, 2), "7/2"), (Fraction(-3, 4), "-3/4"), (Fraction(0), "0")],
)
def test_formatear(valor, esperado):
    assert formatear(valor) == esperado


def test_paso_es_inmutable():
    paso = Paso(1, "t", "e")
    with pytest.raises(AttributeError):
        paso.titulo = "otro"  # type: ignore[misc]
