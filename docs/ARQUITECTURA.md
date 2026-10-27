# Arquitectura

## Capas

1. **Motor** (`plataforma_io.motor`): Python puro. Cada método recibe un problema y produce una
   `Solucion` con una lista de `Paso`. No conoce la interfaz ni Qt.
2. **Servicios** (`plataforma_io.servicios`): persistencia en archivos JSON y, más adelante,
   exportación a PDF o imagen.
3. **Presentación** (`plataforma_io.ui`): PySide6. Reproduce la lista de pasos; no contiene lógica
   matemática.

## Modelo de pasos

Un `Paso` contiene `indice`, `titulo`, `explicacion`, `estado` (diccionario con la estructura de
datos completa en ese instante) y `resaltados` (elementos que la interfaz debe destacar). La
interfaz no recalcula nada: el visor de cada familia interpreta las claves de `estado`.

Convención de claves de `estado` para transporte: `costos`, `oferta`, `demanda`, `asignaciones`
(diccionario `(fila, columna) -> cantidad`), `oferta_restante`, `demanda_restante`,
`filas_agotadas`, `columnas_agotadas`, `ficticio_origen`, `ficticio_destino`.

## Cómo agregar un método

1. Crear la clase en `motor/<familia>/`, heredando de la clase base de la familia (o de `Metodo`).
2. Implementar `validar()` (lista de `ErrorValidacion`) y `resolver()` (devuelve `Solucion`).
3. Generar un `Paso` por cada operación relevante, con título y explicación en español.
4. Registrarlo en `motor/registro.py` y, si ya funciona, agregar un ejemplo en `motor/ejemplos.py`.
5. Crear (o reutilizar) su visor en `ui/visores/` y asociarlo en `crear_visor`.
6. Escribir pruebas en `tests/motor/` con casos de referencia (bibliografía) y casos especiales.

## Captura de datos

La lectura y validación de lo que escribe el usuario está en `ui/entrada.py` (sin Qt, con pruebas
propias). Acepta enteros, decimales (con punto o coma) y fracciones, y devuelve errores por celda.
La pantalla `ui/pantallas/captura_transporte.py` solo dibuja la tabla y delega en ese módulo.
Para un método nuevo de otra familia, crear su pantalla de captura con el mismo patrón y
conectar su señal en `ventana_principal.py`.

## Aritmética exacta

Todos los datos numéricos se convierten con `a_fraccion` y se muestran con `formatear`. No usar
`float` en el motor, para que las tablas coincidan con las que se obtienen a mano.
