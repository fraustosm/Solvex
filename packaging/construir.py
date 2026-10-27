"""Construye el ejecutable de la aplicación con PyInstaller.

Uso:  python packaging/construir.py

El resultado queda en la carpeta ``dist/``. Es la base de la prueba de empaquetado
multiplataforma (riesgo R2); los instaladores nativos se definen en el informe 6.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent


def main() -> int:
    comando = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--noconfirm",
        "--clean",
        "--windowed",
        "--name",
        "Solvex",
        "--paths",
        str(RAIZ / "src"),
        "--distpath",
        str(RAIZ / "dist"),
        "--workpath",
        str(RAIZ / "build"),
        "--specpath",
        str(RAIZ / "build"),
        str(RAIZ / "src" / "plataforma_io" / "__main__.py"),
    ]
    print("Ejecutando:", " ".join(comando))
    return subprocess.call(comando)


if __name__ == "__main__":
    raise SystemExit(main())
