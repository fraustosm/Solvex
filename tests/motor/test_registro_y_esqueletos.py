import pytest

from plataforma_io.motor.base import Metodo
from plataforma_io.motor.ejemplos import EJEMPLOS
from plataforma_io.motor.grafos.dijkstra import CaminoMasCorto
from plataforma_io.motor.grafos.modelo import Arista, Grafo
from plataforma_io.motor.lineal.problema import ProblemaLineal, Relacion
from plataforma_io.motor.lineal.simplex import Simplex
from plataforma_io.motor.registro import FAMILIAS, METODOS, metodos_por_familia
from plataforma_io.motor.transporte.problema import ProblemaTransporte


def test_todos_los_metodos_registrados_son_metodos_con_nombre():
    assert len(METODOS) == 9
    for clave, info in METODOS.items():
        assert info.clave == clave
        assert issubclass(info.clase, Metodo)
        assert info.nombre


def test_las_tres_familias_tienen_metodos():
    por_familia = metodos_por_familia()
    assert tuple(por_familia) == FAMILIAS
    assert all(por_familia[f] for f in FAMILIAS)


def test_los_metodos_implementados_tienen_ejemplo():
    for clave, info in METODOS.items():
        assert (clave in EJEMPLOS) == info.implementado


@pytest.mark.parametrize("clave", [c for c, i in METODOS.items() if not i.implementado])
def test_esqueletos_aun_no_implementados(clave):
    info = METODOS[clave]
    if info.familia == "Transporte":
        problema = ProblemaTransporte.desde_numeros([1], [1], [[1]])
    elif info.familia == "Programación lineal":
        problema = ProblemaLineal.desde_numeros(True, [1], [([1], "<=", 1)])
    else:
        problema = Grafo(("A", "B"), (Arista("A", "B", 1),))  # type: ignore[arg-type]
    with pytest.raises(NotImplementedError):
        info.clase(problema).resolver()


def test_validacion_de_lineal():
    p = ProblemaLineal.desde_numeros(True, [3, 5], [([1, 0], "<=", 4), ([1], "<=", 2)])
    errores = Simplex(p).validar()
    assert [e.campo for e in errores] == ["restriccion_2"]
    assert p.restricciones[0].relacion is Relacion.MENOR_IGUAL
    assert Simplex(ProblemaLineal.desde_numeros(True, [], [])).validar()


def test_validacion_de_grafos():
    malo = Grafo(("A", "A"), (Arista("A", "Z", 1),))  # type: ignore[arg-type]
    campos = [e.campo for e in CaminoMasCorto(malo).validar()]
    assert campos.count("nodos") == 1 and "aristas" in campos
    assert CaminoMasCorto(Grafo((), ())).validar()
