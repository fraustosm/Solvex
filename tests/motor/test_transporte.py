from fractions import Fraction

import pytest

from plataforma_io.motor.base import ProblemaInvalido
from plataforma_io.motor.ejemplos import transporte_clasico
from plataforma_io.motor.modelos import TipoSolucion
from plataforma_io.motor.transporte.noroeste import EsquinaNoroeste
from plataforma_io.motor.transporte.problema import ProblemaTransporte


def test_balanceo_agrega_destino_ficticio_cuando_sobra_oferta():
    p = ProblemaTransporte.desde_numeros([20, 30], [10, 10, 10], [[1, 2, 3], [4, 5, 6]])
    b = p.balancear()
    assert b.ficticio_destino and not b.ficticio_origen
    assert b.demanda == (10, 10, 10, 20)
    assert all(fila[-1] == 0 for fila in b.costos)
    assert b.balanceado


def test_balanceo_agrega_origen_ficticio_cuando_sobra_demanda():
    p = ProblemaTransporte.desde_numeros([10], [6, 8], [[1, 2]])
    b = p.balancear()
    assert b.ficticio_origen and not b.ficticio_destino
    assert b.oferta == (10, 4)
    assert b.costos[-1] == (0, 0)


def test_balanceo_no_cambia_un_problema_balanceado():
    p = transporte_clasico()
    assert p.balanceado
    assert p.balancear() is p


def test_noroeste_ejemplo_clasico():
    sol = EsquinaNoroeste(transporte_clasico()).resolver()
    assert sol.tipo == TipoSolucion.BASICA_FACTIBLE
    assert sol.valores["asignaciones"] == {
        (0, 0): 5,
        (0, 1): 10,
        (1, 1): 5,
        (1, 2): 15,
        (1, 3): 5,
        (2, 3): 10,
    }
    assert sol.valores["celdas_basicas"] == 3 + 4 - 1
    assert sol.valores["degenerada"] is False
    assert sol.objetivo == 500  # 5*10 + 10*0 + 5*7 + 15*9 + 5*20 + 10*18


def test_noroeste_desbalanceado_y_degenerado():
    p = ProblemaTransporte.desde_numeros([20, 30], [10, 10, 10], [[1, 2, 3], [4, 5, 6]])
    sol = EsquinaNoroeste(p).resolver()
    assert sol.valores["ficticio_destino"] is True
    assert sol.valores["degenerada"] is True
    assert sol.valores["asignaciones"][(1, 1)] == 0
    assert sol.valores["celdas_basicas"] == 2 + 4 - 1
    assert sol.objetivo == 90
    assert sol.mensajes  # advierte la degeneración


def test_noroeste_conserva_oferta_y_demanda():
    sol = EsquinaNoroeste(transporte_clasico()).resolver()
    asig = sol.valores["asignaciones"]
    p = transporte_clasico()
    for i, oferta in enumerate(p.oferta):
        assert sum(c for (a, _), c in asig.items() if a == i) == oferta
    for j, demanda in enumerate(p.demanda):
        assert sum(c for (_, b), c in asig.items() if b == j) == demanda


def test_noroeste_acepta_fracciones():
    p = ProblemaTransporte.desde_numeros(["5/2", "5/2"], [3, 2], [[1, 2], [3, 4]])
    sol = EsquinaNoroeste(p).resolver()
    assert sol.objetivo == Fraction(5, 2) * 1 + Fraction(1, 2) * 3 + 2 * 4


def test_pasos_consecutivos_con_inicio_y_resumen():
    pasos = EsquinaNoroeste(transporte_clasico()).resolver().pasos
    assert [p.indice for p in pasos] == list(range(1, len(pasos) + 1))
    assert pasos[0].titulo == "Datos del problema"
    assert pasos[-1].titulo == "Resumen"
    assert pasos[-1].estado["costo_total"] == 500
    assert all(p.explicacion for p in pasos)
    # cada paso de asignación resalta exactamente una celda
    assert all(len(p.resaltados) == 1 for p in pasos[1:-1])


def test_pasos_no_comparten_estado_mutable():
    pasos = EsquinaNoroeste(transporte_clasico()).resolver().pasos
    assert len(pasos[1].estado["asignaciones"]) == 1
    assert len(pasos[2].estado["asignaciones"]) == 2


@pytest.mark.parametrize(
    ("oferta", "demanda", "costos", "campo"),
    [
        ([], [1], [], "problema"),
        ([1], [1], [[1, 2]], "costos"),
        ([-1], [1], [[1]], "oferta"),
        ([1], [-1], [[1]], "demanda"),
    ],
)
def test_validacion(oferta, demanda, costos, campo):
    metodo = EsquinaNoroeste(ProblemaTransporte.desde_numeros(oferta, demanda, costos))
    assert campo in {e.campo for e in metodo.validar()}
    with pytest.raises(ProblemaInvalido):
        metodo.resolver()


def test_problema_a_dict_y_desde_dict():
    p = ProblemaTransporte.desde_numeros(["5/2", 3], [1, "9/2"], [[1, 2], [3, "1/2"]])
    assert ProblemaTransporte.desde_dict(p.a_dict()) == p


def test_noroeste_con_sobra_de_demanda_agrega_origen_ficticio():
    p = ProblemaTransporte.desde_numeros([10], [6, 8], [[1, 2]])
    metodo = EsquinaNoroeste(p)
    sol = metodo.resolver()
    assert sol.valores["ficticio_origen"] is True
    assert sol.valores["asignaciones"] == {(0, 0): 6, (0, 1): 4, (1, 1): 4}
    assert sol.objetivo == 6 * 1 + 4 * 2 + 4 * 0
    assert "origen ficticio" in sol.pasos[0].explicacion
    assert len(metodo.pasos()) == len(sol.pasos)
