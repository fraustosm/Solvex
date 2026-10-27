"""Variables de diseño (Anexo B) y hoja de estilos de Qt."""

from __future__ import annotations

COLORES = {
    "primario": "#1F4E8C",
    "texto": "#1F2933",
    "texto_secundario": "#52606D",
    "fondo": "#F4F6F9",
    "superficie": "#FFFFFF",
    "borde": "#D5DCE5",
    "exito": "#2F6B3A",
    "error": "#B42318",
    "advertencia_fondo": "#FFF1CC",
    "advertencia_texto": "#7A4B00",
    # Estados de visualización
    "pivote_fila": "#DCE9F8",
    "pivote_elemento": "#F5B041",
    "asignada": "#D5EBD9",
    "descartado": "#6B7280",
    "agotada": "#EEF1F5",
}


def hoja_estilos() -> str:
    c = COLORES
    return f"""
QWidget {{
    font-family: "Inter", "Segoe UI", "Helvetica Neue", Arial, sans-serif;
    font-size: 14px;
    color: {c["texto"]};
}}
QMainWindow, QStackedWidget, QWidget#pantalla {{ background: {c["fondo"]}; }}
QFrame#barra {{ background: {c["superficie"]}; border-bottom: 1px solid {c["borde"]}; }}
QFrame#panel, QFrame#tarjeta {{
    background: {c["superficie"]};
    border: 1px solid {c["borde"]};
    border-radius: 8px;
}}
QWidget#reproductor {{ background: {c["superficie"]}; border-top: 1px solid {c["borde"]}; }}
QLabel {{ background: transparent; }}
QLabel#aviso {{
    background: {c["advertencia_fondo"]};
    color: {c["advertencia_texto"]};
    padding: 8px 16px;
    border-bottom: 1px solid #F0D58A;
}}
QTableWidget QLineEdit {{ border: 2px solid {c["primario"]}; padding: 2px; }}
QLabel[rol="titulo"] {{ font-size: 20px; font-weight: 500; }}
QLabel[rol="subtitulo"] {{ font-size: 15px; font-weight: 500; }}
QLabel[rol="secundario"] {{ color: {c["texto_secundario"]}; font-size: 12px; }}
QPushButton {{
    background: {c["superficie"]};
    border: 1px solid {c["borde"]};
    border-radius: 6px;
    padding: 6px 12px;
    min-height: 20px;
}}
QPushButton:hover {{ border-color: {c["primario"]}; }}
QPushButton:focus {{ border: 2px solid {c["primario"]}; }}
QPushButton:disabled {{ color: {c["descartado"]}; background: {c["agotada"]}; }}
QPushButton[primario="true"] {{
    background: {c["primario"]};
    color: white;
    border-color: {c["primario"]};
    font-weight: 500;
}}
QListWidget, QTableWidget, QPlainTextEdit {{
    background: {c["superficie"]};
    border: 1px solid {c["borde"]};
    border-radius: 6px;
}}
QListWidget::item:selected {{ background: {c["pivote_fila"]}; color: {c["texto"]}; }}
QHeaderView::section {{
    background: {c["agotada"]};
    border: 1px solid {c["borde"]};
    padding: 4px;
    font-weight: 500;
}}
QSlider::groove:horizontal {{ height: 6px; background: {c["borde"]}; border-radius: 3px; }}
QSlider::sub-page:horizontal {{ background: {c["primario"]}; border-radius: 3px; }}
QSlider::handle:horizontal {{
    background: {c["primario"]};
    width: 16px;
    margin: -5px 0;
    border-radius: 8px;
    border: 2px solid white;
}}
"""
