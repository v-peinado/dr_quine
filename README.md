# Dr_Quine

## ¿Qué es un Quine?

Un **quine** es un programa informático que produce como salida una copia exacta de su propio código fuente, sin leer ningún archivo ni recibir entrada externa. Es un ejercicio de autorreferencia en programación que demuestra conceptos fundamentales de la teoría de la computación.

### Características de un Quine válido:
- ✅ Produce su propio código fuente como salida
- ❌ No puede leer archivos (incluido su propio archivo fuente)
- ❌ No puede usar argumentos de línea de comandos (argv/argc)
- ❌ No puede depender de entrada externa
- ✅ Debe ser un programa completo y funcional

## El Teorema de Recursión de Kleene

El **Teorema de Recursión de Kleene** (también conocido como Teorema del Punto Fijo) establece que:

> *Para cualquier función computable total f, existe un programa P tal que P y f(P) calculan la misma función.*


En términos simples, el teorema dice que si tienes una función f que transforma programas:

```
Para cualquier función f que transforme programas,
existe un programa P tal que:
P y f(P) hacen exactamente lo mismo
```

**Ejemplo concreto con quines:**
- f = "ejecutar el programa y obtener su salida"
- El teorema dice: existe un programa P tal que P = f(P)
- Es decir, existe un programa cuya salida es él mismo (¡un quine!)

Un quine es un punto fijo de la función "ejecutar e imprimir salida":
- Sea f la función que toma un programa P y devuelve su salida
- Un quine Q satisface: f(Q) = Q
- El programa y su salida son idénticos


## El Proyecto Dr_Quine

Este proyecto implementa tres quines diferentes, cada uno con características únicas:

### 1. **Colleen** - El Quine Clásico
- Imprime su código fuente en stdout
- Demuestra la técnica básica usando `printf` y format specifiers
- Incluye funciones y comentarios según requisitos
- [📖 Documentación detallada](docs/README_Colleen.md)

### 2. **Grace** - El Quine sin main
- Escribe su código en un archivo `Grace_kid.c`
- Se ejecuta mediante macros (sin función main declarada)
- Demuestra el uso creativo del preprocesador
- [📖 Documentación detallada](docs/README_Grace.md)

### 3. **Sully** - El Quine Autorreplicante
- Se replica a sí mismo con un contador decreciente
- Compila y ejecuta cada réplica automáticamente
- Demuestra autorreplicación con modificación
- [📖 Documentación detallada](docs/README_Sully.md)

## Autoreferencia

El mayor desafío al crear un quine es manejar la **autorreferencia sin recursión infinita**. Cuando intentamos que un programa imprima su propio código, nos encontramos con el problema del escape:

```c
// Si tenemos:
char *s = "char *s = ";
// ¿Cómo imprimimos las comillas dentro de s?
```

### Por Qué Printf Resuelve el Problema de la Autoreferencia

La función printf en C permite crear quines porque separa la plantilla del contenido:  
procesa una cadena de formato con especificadores (%s, %c, %d) y los sustituye por los argumentos proporcionados en una sola pasada, sin reinterpretar el resultado.  
Esto permite que una cadena se referencie a sí misma sin causar recursión infinita. El truco está en que la cadena contiene tanto su propia definición como las instrucciones para imprimirse:  
char *s = "char *s = %c%s%c; printf(s, 34, s, 34);";  
printf(s, 34, s, 34);.  
Cuando printf encuentra %s lo sustituye por la cadena completa, pero no vuelve a procesar los especificadores que aparecen en el contenido sustituido.  

Otros lenguajes ofrecen mecanismos similares mediante formateo de strings (funciones como format(), sprintf() que sustituyen marcadores en una plantilla:  
Python's "Hola %s" % nombre, Java's String.format()) o interpolación (inserción directa de expresiones dentro de strings que se evalúan al momento de ejecución:  
JavaScript's `Hola ${nombre}`, Ruby's "Hola #{nombre}").  
Ambos métodos comparten la característica clave: permiten que una cadena contenga referencias a variables que se sustituyen en tiempo de ejecución,  
incluyendo la posibilidad de que la cadena se referencie a sí misma. La diferencia principal es que el formateo usa funciones explícitas con marcadores,  
mientras que la interpolación embebe directamente las expresiones en la sintaxis del string.

#### 1. **Separación entre representación y contenido**

```c
char *s = "char *s = %c%s%c; printf(s, 34, s, 34);";
```

- La cadena `s` no contiene su propia definición literal completa
- Contiene un marcador `%s` que significa "aquí irá una cadena"
- El contenido real se proporciona como argumento durante la ejecución

#### 2. **El momento clave: la sustitución**

Cuando ejecutas:
```c
printf(s, 34, s, 34);
```

Printf hace esto:
1. Lee la cadena `s`: `"char *s = %c%s%c; printf(s, 34, s, 34);"`
2. Encuentra `%c` → sustituye por 34 → imprime `"`
3. Encuentra `%s` → sustituye por el contenido de `s` → imprime toda la cadena
4. Encuentra `%c` → sustituye por 34 → imprime `"`

#### 3. **No hay recursión, solo sustitución**

El punto crítico es que printf **no ejecuta código recursivamente**. Solo:
- Toma una cadena con marcadores
- Sustituye los marcadores por valores
- Imprime el resultado

#### 4. **La autoreferencia es indirecta**

```c
char *s = "algo %s algo";
printf(s, s);  // s se pasa como argumento a sí misma
```

- `s` no necesita contener literalmente todo su contenido
- Solo necesita un marcador `%s` donde irá su contenido
- En tiempo de ejecución, printf inserta el contenido de `s` en ese punto

## Compilación y Uso

```bash
cd C/
make                  # Compila todos los programas

# Ejecutar y verificar:
./Colleen > tmp.c && diff Colleen.c tmp.c
./Grace && diff Grace.c Grace_kid.c
./Sully && ls -la Sully_*
```
