"""Pruebas de propiedades y verificación con un solucionador independiente (SciPy)."""

import random

import pytest

from plataforma_io.motor.transporte.noroeste import EsquinaNoroeste
from plataforma_io.motor.transporte.problema import ProblemaTransporte


def _problema_aleatorio(rng: random.Random) -> ProblemaTransporte:
    m, n = rng.randint(1, 6), rng.randint(1, 6)
    return ProblemaTransporte.desde_numeros(
        oferta=[rng.randint(1, 30) for _ in range(m)],
        demanda=[rng.randint(1, 30) for _ in range(n)],
        costos=[[rng.randint(0, 20) for _ in range(n)] for _ in range(m)],
    )


def test_propiedades_en_mil_problemas_aleatorios():
    rng = random.Random(2026)  # semilla fija: la prueba es reproducible
    for _ in range(1000):
        original = _problema_aleatorio(rng)
        balanceado = original.balancear()
        m, n = len(balanceado.oferta), len(balanceado.demanda)
        sol = EsquinaNoroeste(original).resolver()
        asig = sol.valores["asignaciones"]

        assert all(cantidad >= 0 for cantidad in asig.values())
        for i, oferta in enumerate(balanceado.oferta):
            assert sum(c for (a, _), c in asig.items() if a == i) == oferta
        for j, demanda in enumerate(balanceado.demanda):
            assert sum(c for (_, b), c in asig.items() if b == j) == demanda
        assert len(asig) == m + n - 1
        costo = sum(c * balanceado.costos[i][j] for (i, j), c in asig.items())
        assert sol.objetivo == costo
        assert len(sol.pasos) == len(asig) + 2


def test_el_costo_inicial_nunca_es_menor_que_el_optimo_de_scipy():
    linprog = pytest.importorskip("scipy.optimize").linprog
    rng = random.Random(7)
    for _ in range(50):
        original = _problema_aleatorio(rng)
        p = original.balancear()
        m, n = len(p.oferta), len(p.demanda)
        c = [float(p.costos[i][j]) for i in range(m) for j in range(n)]
        a_eq, b_eq = [], []
        for i in range(m):
            a_eq.append([1.0 if k // n == i else 0.0 for k in range(m * n)])
            b_eq.append(float(p.oferta[i]))
        for j in range(n):
            a_eq.append([1.0 if k % n == j else 0.0 for k in range(m * n)])
            b_eq.append(float(p.demanda[j]))
        optimo = linprog(c, A_eq=a_eq, b_eq=b_eq, bounds=(0, None), method="highs")
        assert optimo.success
        costo = EsquinaNoroeste(original).resolver().objetivo
        assert float(costo) >= optimo.fun - 1e-6


def test_propiedades_con_ofertas_y_demandas_en_cero():
    rng = random.Random(11)
    for _ in range(1000):
        m, n = rng.randint(1, 5), rng.randint(1, 5)
        oferta = [rng.randint(0, 9) for _ in range(m)]
        demanda = [rng.randint(0, 9) for _ in range(n)]
        if sum(oferta) == 0 or sum(demanda) == 0:
            continue
        original = ProblemaTransporte.desde_numeros(
            oferta, demanda, [[rng.randint(0, 9) for _ in range(n)] for _ in range(m)]
        )
        balanceado = original.balancear()
        asig = EsquinaNoroeste(original).resolver().valores["asignaciones"]
        for i, o in enumerate(balanceado.oferta):
            assert sum(c for (a, _), c in asig.items() if a == i) == o
        for j, d in enumerate(balanceado.demanda):
            assert sum(c for (_, b), c in asig.items() if b == j) == d
        assert all(c >= 0 for c in asig.values())
