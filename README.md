# Dr_Quine

## ¿Qué es un Quine?

Un **quine** es un programa informático que produce como salida una copia exacta de su propio código fuente, sin leer ningún archivo ni recibir entrada externa. Es un ejercicio fascinante de autorreferencia en programación que demuestra conceptos fundamentales de la teoría de la computación.

### Características de un Quine válido:
- ✅ Produce su propio código fuente como salida
- ❌ No puede leer archivos (incluido su propio archivo fuente)
- ❌ No puede usar argumentos de línea de comandos (argv/argc)
- ❌ No puede depender de entrada externa
- ✅ Debe ser un programa completo y funcional

## El Teorema de Recursión de Kleene

El **Teorema de Recursión de Kleene** (también conocido como Teorema del Punto Fijo) establece que:

> *Para cualquier función computable f, existe un programa P tal que P y f(P) calculan la misma función.*

### Relación con los Quines

Los quines son una demostración práctica de este teorema:
- **P** = nuestro programa quine
- **f(P)** = la función que ejecuta P y obtiene su salida
- **Punto fijo**: P produce P cuando se ejecuta

En esencia, un quine encuentra el "punto fijo" donde el programa y su salida son idénticos.

## El Proyecto Dr_Quine

Este proyecto implementa tres quines diferentes, cada uno con características únicas:

### 1. **Colleen** - El Quine Clásico
- Imprime su código fuente en stdout
- Demuestra la técnica básica usando `printf` y format specifiers
- Incluye funciones y comentarios según requisitos

### 2. **Grace** - El Quine sin main
- Escribe su código en un archivo `Grace_kid.c`
- Se ejecuta mediante macros (sin función main declarada)
- Demuestra el uso creativo del preprocesador

### 3. **Sully** - El Quine Autorreplicante
- Se replica a sí mismo con un contador decreciente
- Compila y ejecuta cada réplica automáticamente
- Demuestra autorreplicación con modificación

## El Desafío Principal: El Problema del Escape

El mayor desafío al crear un quine es manejar la **autorreferencia sin recursión infinita**. Cuando intentamos que un programa imprima su propio código, nos encontramos con el problema del escape:

```c
// Si tenemos:
char *s = "char *s = ";
// ¿Cómo imprimimos las comillas dentro de s?
```

### La Solución: Format Specifiers

La solución elegante usa `printf` con especificadores de formato:

```c
char *s = "char *s = %c%s%c;";
printf(s, 34, s, 34);  // 34 = ASCII de "
```

Esto permite que la cadena contenga su propia definición con "huecos" que se rellenan dinámicamente.

## Estructura del Proyecto

```
Dr_Quine/
├── README.md          # Este archivo
└── C/                 # Implementaciones en C
    ├── Makefile      # Compila los tres programas
    ├── Colleen.c     # Quine clásico
    ├── Grace.c       # Quine con macros
    └── Sully.c       # Quine autorreplicante

```

## Compilación y Uso

```bash
cd C/
make                  # Compila todos los programas

# Ejecutar y verificar:
./Colleen > tmp.c && diff Colleen.c tmp.c
./Grace && diff Grace.c Grace_kid.c
./Sully && ls -la Sully_*
```

## Puntos Clave

1. **Autorreferencia sin recursión**: Usar datos para representar código
2. **Escape de caracteres**: Manejar comillas y caracteres especiales con ASCII
3. **Format specifiers posicionales**: `%1$c` permite reutilizar argumentos
4. **Macros del preprocesador**: Ejecutar código sin main declarado
5. **Metaprogramación**: Programas que generan y ejecutan otros programas

Este proyecto es una introducción perfecta a conceptos avanzados como puntos fijos, autorreplicación y las bases teóricas de los virus informáticos y programas automodificables.