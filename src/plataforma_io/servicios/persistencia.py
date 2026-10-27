"""Guardado y apertura de problemas en archivos JSON (RF-08)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

VERSION_FORMATO = 1
EXTENSION = ".ioproblema"


class ArchivoInvalido(ValueError):
    """El archivo no tiene el formato esperado o su versión no es compatible."""


def guardar_problema(ruta: str | Path, metodo: str, datos: dict[str, Any]) -> None:
    """Guarda ``datos`` (ya serializables) junto con la clave del método y la versión de formato."""
    contenido = {"version": VERSION_FORMATO, "metodo": metodo, "datos": datos}
    Path(ruta).write_text(json.dumps(contenido, ensure_ascii=False, indent=2), encoding="utf-8")


def abrir_problema(ruta: str | Path) -> tuple[str, dict[str, Any]]:
    """Devuelve ``(clave_del_metodo, datos)``; lanza ``ArchivoInvalido`` si el archivo no sirve."""
    try:
        contenido = json.loads(Path(ruta).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ArchivoInvalido(f"No se pudo leer el archivo: {exc}") from exc
    if not isinstance(contenido, dict) or {"version", "metodo", "datos"} - contenido.keys():
        raise ArchivoInvalido("El archivo no contiene un problema guardado.")
    if contenido["version"] != VERSION_FORMATO:
        raise ArchivoInvalido(f"Versión de formato no compatible: {contenido['version']}.")
    return str(contenido["metodo"]), dict(contenido["datos"])
