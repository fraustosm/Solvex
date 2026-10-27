# Solvex

Plataforma de resolución de problemas en Investigación de Operaciones.

Aplicación de escritorio multiplataforma, desarrollada en Python, que resuelve y muestra paso a
paso seis métodos de Investigación de Operaciones: Simplex y Dos Fases, Vogel, Esquina Noroeste,
Camino más corto, Árbol de expansión mínima y Flujo máximo.

Proyecto de servicio social. Este repositorio es la base técnica descrita en el documento de
análisis, diseño y planeación (arquitectura en tres capas, modelo de pasos y plan de calidad).

## Estado actual (versión 0.1.0)

| Componente | Estado |
|---|---|
| Modelos (`Paso`, `Solucion`), clase abstracta `Metodo`, registro de métodos | Terminado |
| Esquina Noroeste (con balanceo y degeneración) | Terminado, con pruebas |
| Captura de datos de transporte (matriz editable, validación, balance en vivo, guardar y abrir) | Terminado, con pruebas |
| Persistencia en JSON | Terminado, con pruebas |
| Interfaz: inicio, captura, resolución, reproductor de pasos, visor de transporte | Funcional para la Esquina Noroeste con datos propios |
| Vogel, Simplex, Dos Fases, grafos | Esqueleto (`NotImplementedError`) |
| Captura de programación lineal y grafos, exportación a PDF, editor de grafos | Pendiente |

## Puesta en marcha en VS Code

Requiere Python 3.11 o superior.

Windows (PowerShell):

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -e ".[dev]"
```

macOS o Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e ".[dev]"
```

El paquete interno se llama `plataforma_io`; el nombre visible y del ejecutable es Solvex.

Después, en VS Code: abrir la carpeta, instalar las extensiones recomendadas, elegir el
intérprete `.venv` (Ctrl+Shift+P, «Python: Select Interpreter») y usar:

- F5, configuración «Plataforma IO (interfaz)», para ejecutar la aplicación.
- La vista de pruebas (matraz) o la tarea «Pruebas del motor» para ejecutar pytest.
- Las tareas «Lint», «Formatear» y «Tipos» (Terminal, Ejecutar tarea) antes de cada confirmación.

Desde la terminal: `python -m plataforma_io`, `pytest`, `ruff check .`, `mypy src/plataforma_io/motor`.

## Estructura

```text
src/plataforma_io/
  motor/        Algoritmos y modelo de pasos. NO depende de la interfaz.
    lineal/     Simplex y Dos Fases
    transporte/ Esquina Noroeste y Vogel
    grafos/     Camino más corto, árbol de expansión mínima y flujo máximo
  servicios/    Persistencia (JSON) y, más adelante, exportación
  ui/           PySide6: pantallas, visores, reproductor y hoja de estilos
tests/          Pruebas unitarias (motor, servicios) y de interfaz
docs/           Arquitectura y guía para agregar métodos
packaging/      Construcción del ejecutable
```

Regla de dependencias: `ui` puede importar `motor` y `servicios`; `servicios` puede importar
`motor`; `motor` no importa nada de las otras capas.

## Convenciones de calidad

PEP 8 con ruff (línea de 100 caracteres), anotaciones de tipo en el motor (mypy), cálculo exacto
con `fractions.Fraction`, cobertura mínima de 80 % en el motor, ramas cortas por funcionalidad y
mensajes de confirmación descriptivos. Una tarea está terminada cuando cumple su criterio de
aceptación, tiene pruebas aprobadas, pasa ruff y mypy, y la integración continua está en verde.

## Hoja de ruta por informe

- Informe 2: reproductor y captura de matrices (hechos); Esquina Noroeste (hecha) y Vogel.
- Informe 3: modelo de programación lineal, forma estándar y Simplex.
- Informe 4: Dos Fases, interpretación de resultados, región factible y exportación a PDF.
- Informe 5: modelo y editor de grafos; Dijkstra, Floyd-Warshall, Kruskal, Prim y Edmonds-Karp.
- Informe 6: integración, pruebas de sistema y usabilidad, instaladores y documentación.

Nota sobre el nombre: la aplicación se llama Solvex (nombre visible, ejecutable y comando `solvex`);
el paquete interno de Python conserva el nombre `plataforma_io`. Antes de publicar el paquete o el
repositorio, verificar que el nombre no genere confusión con productos o marcas existentes.

Licencia: FIM UAS.
