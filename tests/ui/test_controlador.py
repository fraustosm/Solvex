from plataforma_io.ui.controlador import ControladorPasos


def test_navegacion_basica():
    c = ControladorPasos(4)
    assert c.etiqueta == "Paso 1 de 4" and c.al_inicio and not c.al_final
    assert c.siguiente() and c.indice == 1
    assert c.final() and c.al_final and c.etiqueta == "Paso 4 de 4"
    assert not c.siguiente()  # no pasa del último
    assert c.anterior() and c.indice == 2
    assert c.inicio() and c.indice == 0
    assert not c.anterior()


def test_ir_a_se_acota_al_rango():
    c = ControladorPasos(3)
    assert c.ir_a(99) and c.indice == 2
    assert c.ir_a(-5) and c.indice == 0
    assert not c.ir_a(0)  # sin cambio


def test_sin_pasos():
    c = ControladorPasos()
    assert not c.hay_pasos and c.etiqueta == "Sin pasos"
    assert not c.siguiente() and not c.ir_a(0)
    c.establecer_total(2)
    assert c.hay_pasos and c.indice == 0
