"""Lógica del reproductor de pasos, sin dependencia de Qt (se prueba sin interfaz)."""

from __future__ import annotations


class ControladorPasos:
    def __init__(self, total: int = 0) -> None:
        self.total = total
        self.indice = 0

    def establecer_total(self, total: int) -> None:
        self.total = max(total, 0)
        self.indice = 0

    @property
    def hay_pasos(self) -> bool:
        return self.total > 0

    @property
    def al_inicio(self) -> bool:
        return self.indice <= 0

    @property
    def al_final(self) -> bool:
        return self.indice >= self.total - 1

    def ir_a(self, indice: int) -> bool:
        """Salta al paso indicado (acotado al rango válido). Devuelve ``True`` si cambió."""
        if not self.hay_pasos:
            return False
        nuevo = max(0, min(indice, self.total - 1))
        if nuevo == self.indice:
            return False
        self.indice = nuevo
        return True

    def siguiente(self) -> bool:
        return self.ir_a(self.indice + 1)

    def anterior(self) -> bool:
        return self.ir_a(self.indice - 1)

    def inicio(self) -> bool:
        return self.ir_a(0)

    def final(self) -> bool:
        return self.ir_a(self.total - 1)

    @property
    def etiqueta(self) -> str:
        if not self.hay_pasos:
            return "Sin pasos"
        return f"Paso {self.indice + 1} de {self.total}"
