import json

import pytest

from plataforma_io.motor.transporte.problema import ProblemaTransporte
from plataforma_io.servicios.persistencia import ArchivoInvalido, abrir_problema, guardar_problema


def test_ida_y_vuelta_con_fracciones(tmp_path):
    problema = ProblemaTransporte.desde_numeros(["5/2", 3], [1, "9/2"], [[1, 2], [3, "1/2"]])
    ruta = tmp_path / "p.ioproblema"
    guardar_problema(ruta, "noroeste", problema.a_dict())
    metodo, datos = abrir_problema(ruta)
    assert metodo == "noroeste"
    assert ProblemaTransporte.desde_dict(datos) == problema


def test_archivo_inexistente_o_corrupto(tmp_path):
    with pytest.raises(ArchivoInvalido):
        abrir_problema(tmp_path / "no_existe.ioproblema")
    roto = tmp_path / "roto.ioproblema"
    roto.write_text("{ esto no es json", encoding="utf-8")
    with pytest.raises(ArchivoInvalido):
        abrir_problema(roto)


def test_formato_incompleto_o_version_distinta(tmp_path):
    incompleto = tmp_path / "a.ioproblema"
    incompleto.write_text(json.dumps({"metodo": "x"}), encoding="utf-8")
    with pytest.raises(ArchivoInvalido, match="no contiene"):
        abrir_problema(incompleto)
    futuro = tmp_path / "b.ioproblema"
    futuro.write_text(json.dumps({"version": 99, "metodo": "x", "datos": {}}), encoding="utf-8")
    with pytest.raises(ArchivoInvalido, match="Versión"):
        abrir_problema(futuro)
