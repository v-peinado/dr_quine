# Crear Sully - De Grace a auto-replicación

## Introducción

En este tutorial voy a crear Sully partiendo de Grace. Sully es un quine que se replica a sí mismo, compilándose y ejecutándose en cadena hasta llegar a 0.

## Paso 1: Entender los requisitos de Sully

Según el subject:
- El ejecutable se llama `Sully`
- Crea archivos `Sully_X.c` donde X es un entero
- Compila el archivo creado
- Ejecuta el programa compilado (solo si X >= 0)
- El entero decrementa en cada generación
- Empieza en 5

## Paso 2: Partir de Grace simplificado

Empiezo con una versión simplificada de Grace como base:

```c
#include <stdio.h>

int main() {
	int i = 5;
	FILE *f = fopen("Sully_5.c", "w");
	if(f) {
		char *s = "#include <stdio.h>%1$c%1$cint main() {%1$c%2$cint i = 5;%1$c%2$cFILE *f = fopen(%3$cSully_5.c%3$c, %3$cw%3$c);%1$c%2$cif(f) {%1$c%2$c%2$cchar *s = %3$c%4$s%3$c;%1$c%2$c%2$cfprintf(f, s, 10, 9, 34, s);%1$c%2$c%2$cfclose(f);%1$c%2$c}%1$c%2$creturn 0;%1$c}%1$c";
		fprintf(f, s, 10, 9, 34, s);
		fclose(f);
	}
	return 0;
}
```

Este código crea una copia idéntica, pero necesito hacerlo dinámico.

## Paso 3: Hacer el nombre de archivo dinámico

Uso `sprintf` para crear nombres de archivo basados en el valor de `i`:

```c
#include <stdio.h>

int main() {
	int i = 5;
	char filename[100];
	sprintf(filename, "Sully_%d.c", i);
	
	FILE *f = fopen(filename, "w");
	if(f) {
		char *s = "#include <stdio.h>%1$c%1$cint main() {%1$c%2$cint i = %5$d;%1$c%2$cchar filename[100];%1$c%2$csprintf(filename, %3$cSully_%%d.c%3$c, i);%1$c%2$c%1$c%2$cFILE *f = fopen(filename, %3$cw%3$c);%1$c%2$cif(f) {%1$c%2$c%2$cchar *s = %3$c%4$s%3$c;%1$c%2$c%2$cfprintf(f, s, 10, 9, 34, s, i);%1$c%2$c%2$cfclose(f);%1$c%2$c}%1$c%2$creturn 0;%1$c}%1$c";
		fprintf(f, s, 10, 9, 34, s, i);
		fclose(f);
	}
	return 0;
}
```

Nota: Uso `%5$d` para insertar el valor de `i` y `%%d` para escribir un `%d` literal en el string generado.

## Paso 4: Añadir compilación con system()

Necesito incluir `<stdlib.h>` para `system()`:

```c
#include <stdio.h>
#include <stdlib.h>

int main() {
	int i = 5;
	char filename[100];
	char compile[100];
	char exec[100];
	
	sprintf(filename, "Sully_%d.c", i);
	sprintf(compile, "gcc -Wall -Wextra -Werror %s -o Sully_%d", filename, i);
	sprintf(exec, "./Sully_%d", i);
	
	FILE *f = fopen(filename, "w");
	if(f) {
		char *s = "#include <stdio.h>%1$c#include <stdlib.h>%1$c%1$cint main() {%1$c%2$cint i = %5$d;%1$c%2$cchar filename[100];%1$c%2$cchar compile[100];%1$c%2$cchar exec[100];%1$c%2$c%1$c%2$csprintf(filename, %3$cSully_%%d.c%3$c, i);%1$c%2$csprintf(compile, %3$cgcc -Wall -Wextra -Werror %%s -o Sully_%%d%3$c, filename, i);%1$c%2$csprintf(exec, %3$c./Sully_%%d%3$c, i);%1$c%2$c%1$c%2$cFILE *f = fopen(filename, %3$cw%3$c);%1$c%2$cif(f) {%1$c%2$c%2$cchar *s = %3$c%4$s%3$c;%1$c%2$c%2$cfprintf(f, s, 10, 9, 34, s, i);%1$c%2$c%2$cfclose(f);%1$c%2$c}%1$c%2$csystem(compile);%1$c%2$csystem(exec);%1$c%2$creturn 0;%1$c}%1$c";
		fprintf(f, s, 10, 9, 34, s, i);
		fclose(f);
	}
	system(compile);
	system(exec);
	return 0;
}
```

## Paso 5: Implementar el decremento

El truco es simple: cuando escribo el archivo, paso `i-1` en lugar de `i`:

```c
#include <stdio.h>
#include <stdlib.h>

int main() {
	int i = 5;
	char filename[100];
	char compile[100];
	char exec[100];
	
	sprintf(filename, "Sully_%d.c", i);
	sprintf(compile, "gcc -Wall -Wextra -Werror %s -o Sully_%d", filename, i);
	sprintf(exec, "./Sully_%d", i);
	
	FILE *f = fopen(filename, "w");
	if(f) {
		// Aquí está la magia: paso (i-1) como segundo argumento
		char *s = "#include <stdio.h>%1$c#include <stdlib.h>%1$c%1$cint main() {%1$c%2$cint i = %5$d;%1$c%2$cchar filename[100];%1$c%2$cchar compile[100];%1$c%2$cchar exec[100];%1$c%2$c%1$c%2$csprintf(filename, %3$cSully_%%d.c%3$c, i);%1$c%2$csprintf(compile, %3$cgcc -Wall -Wextra -Werror %%s -o Sully_%%d%3$c, filename, i);%1$c%2$csprintf(exec, %3$c./Sully_%%d%3$c, i);%1$c%2$c%1$c%2$cFILE *f = fopen(filename, %3$cw%3$c);%1$c%2$cif(f) {%1$c%2$c%2$cchar *s = %3$c%4$s%3$c;%1$c%2$c%2$cfprintf(f, s, 10, 9, 34, s, i-1);%1$c%2$c%2$cfclose(f);%1$c%2$c}%1$c%2$csystem(compile);%1$c%2$csystem(exec);%1$c%2$creturn 0;%1$c}%1$c";
		fprintf(f, s, 10, 9, 34, s, i-1);  // ← Paso i-1 aquí
		fclose(f);
	}
	system(compile);
	system(exec);
	return 0;
}
```

Así:
- Sully.c (i=5) → crea Sully_5.c con i=4
- Sully_5 (i=4) → crea Sully_4.c con i=3
- Y así sucesivamente...

## Paso 6: Añadir la condición de parada

Solo debo crear archivos y ejecutar si `i >= 0`:

```c
#include <stdio.h>
#include <stdlib.h>

int main() {
	int i = 5;
	
	if (i < 0)
		return 0;
	
	char filename[100];
	char compile[100];
	char exec[100];
	
	sprintf(filename, "Sully_%d.c", i);
	sprintf(compile, "gcc -Wall -Wextra -Werror %s -o Sully_%d", filename, i);
	sprintf(exec, "./Sully_%d", i);
	
	FILE *f = fopen(filename, "w");
	if(f) {
		char *s = "#include <stdio.h>%1$c#include <stdlib.h>%1$c%1$cint main() {%1$c%2$cint i = %5$d;%1$c%2$c%1$c%2$cif (i < 0)%1$c%2$c%2$creturn 0;%1$c%2$c%1$c%2$cchar filename[100];%1$c%2$cchar compile[100];%1$c%2$cchar exec[100];%1$c%2$c%1$c%2$csprintf(filename, %3$cSully_%%d.c%3$c, i);%1$c%2$csprintf(compile, %3$cgcc -Wall -Wextra -Werror %%s -o Sully_%%d%3$c, filename, i);%1$c%2$csprintf(exec, %3$c./Sully_%%d%3$c, i);%1$c%2$c%1$c%2$cFILE *f = fopen(filename, %3$cw%3$c);%1$c%2$cif(f) {%1$c%2$c%2$cchar *s = %3$c%4$s%3$c;%1$c%2$c%2$cfprintf(f, s, 10, 9, 34, s, i-1);%1$c%2$c%2$cfclose(f);%1$c%2$c}%1$c%2$csystem(compile);%1$c%2$cif (i > 0)%1$c%2$c%2$csystem(exec);%1$c%2$creturn 0;%1$c}%1$c";
		fprintf(f, s, 10, 9, 34, s, i-1);
		fclose(f);
	}
	system(compile);
	if (i > 0)
		system(exec);
	return 0;
}
```

Nota: Solo ejecuto el siguiente programa si `i > 0`, así Sully_0 no intentará ejecutar Sully_-1.

## Paso 7: Versión final simplificada

Elimino los tabuladores para hacer el código más compacto:

```c
#include <stdio.h>
#include <stdlib.h>

int main() {
int i = 5;
if (i < 0) return 0;
char filename[100];
char compile[100];
char exec[100];
sprintf(filename, "Sully_%d.c", i);
sprintf(compile, "gcc -Wall -Wextra -Werror %s -o Sully_%d", filename, i);
sprintf(exec, "./Sully_%d", i);
FILE *f = fopen(filename, "w");
if(f) {
char *s = "#include <stdio.h>%1$c#include <stdlib.h>%1$c%1$cint main() {%1$cint i = %2$d;%1$cif (i < 0) return 0;%1$cchar filename[100];%1$cchar compile[100];%1$cchar exec[100];%1$csprintf(filename, %3$cSully_%%d.c%3$c, i);%1$csprintf(compile, %3$cgcc -Wall -Wextra -Werror %%s -o Sully_%%d%3$c, filename, i);%1$csprintf(exec, %3$c./Sully_%%d%3$c, i);%1$cFILE *f = fopen(filename, %3$cw%3$c);%1$cif(f) {%1$cchar *s = %3$c%4$s%3$c;%1$cfprintf(f, s, 10, i-1, 34, s);%1$cfclose(f);%1$c}%1$csystem(compile);%1$cif (i > 0) system(exec);%1$creturn 0;%1$c}%1$c";
fprintf(f, s, 10, i-1, 34, s);
fclose(f);
}
system(compile);
if (i > 0) system(exec);
return 0;
}
```

## Cómo verifico que funciona

```bash
# Compilo el original
gcc -Wall -Wextra -Werror Sully.c -o Sully

# Ejecuto
./Sully

# Verifico los archivos creados
ls -la | grep Sully
# Debería ver:
# Sully (original)
# Sully_5.c, Sully_5
# Sully_4.c, Sully_4
# ... hasta
# Sully_0.c, Sully_0

# Verifico que decrementan correctamente
diff Sully.c Sully_5.c
# Debería mostrar: int i = 5; vs int i = 4;

diff Sully_5.c Sully_0.c  
# Debería mostrar: int i = 4; vs int i = 0;
```

## Cómo funciona la cadena de ejecución

1. **Sully** (i=5) 
   - Crea Sully_5.c con i=4 (porque escribe i-1)
   - Compila → Sully_5
   - Ejecuta Sully_5

2. **Sully_5** (i=4)
   - Crea Sully_4.c con i=3
   - Compila → Sully_4
   - Ejecuta Sully_4

3. **...continúa hasta...**

4. **Sully_1** (i=1)
   - Crea Sully_0.c con i=0
   - Compila → Sully_0
   - Ejecuta Sully_0

5. **Sully_0** (i=0)
   - Crea Sully_-1.c con i=-1
   - Compila → Sully_-1
   - NO ejecuta (porque i=0, no > 0)

6. **Si alguien ejecutara Sully_-1** (i=-1)
   - Como i < 0, termina inmediatamente sin crear archivos

## Trucos importantes

1. **%%d en sprintf**: Para escribir un `%d` literal en el string
2. **Pasar i-1 en fprintf**: El truco clave para decrementar automáticamente
3. **Orden de argumentos**: `10, i-1, 34, s` (nota el i-1)
4. **Doble condición**: 
   - `i < 0` → no crear archivo
   - `i > 0` → no ejecutar (evita ejecutar Sully_0)

## Ventajas de esta solución

### Más simple:
- No necesito detectar si soy el original o una copia
- No necesito `#include <string.h>`
- No necesito `__FILE__` ni `argv`
- El código es más corto y directo

### El truco está en fprintf:
```c
// En lugar de escribir el mismo valor de i:
fprintf(f, s, 10, i, 34, s);

// Escribo i-1:
fprintf(f, s, 10, i-1, 34, s);
```

## Nota sobre el comportamiento

Con esta implementación:
- Sully crea Sully_5.c (no Sully_6.c)
- El último archivo ejecutado es Sully_0
- Se crea pero no se ejecuta Sully_-1.c

Esto cumple perfectamente con el subject que dice que el programa debe ejecutarse "solo si el entero X es mayor o igual a 0".

## Paso 8: Versión híbrida Grace-Sully con macros (opcional)

Puedo hacer el código más elegante usando macros como en Grace. Voy a transformar el código paso a paso:

### 8.1 Primero, extraigo el valor inicial a una macro

```c
#include <stdio.h>
#include <stdlib.h>
#define I 5  // ← Nueva macro para el valor inicial

int main() {
int i = I;  // ← Uso la macro
if (i < 0) return 0;
// ... resto del código
}
```

### 8.2 Creo la macro S para el string (como en Grace)

```c
#define I 5
#define S "#include <stdio.h>%1$c#include <stdlib.h>%1$c#define I %2$d%1$c#define S %3$c%4$s%3$c%1$c..."
```

Nota: En el string, uso `%2$d` para el valor de i-1 y `%4$s` para el string S.

### 8.3 Creo la macro M() para ocultar main (como en Grace)

```c
#define M() int main(){int i=I;if(i<0)return 0;char f[99],c[99],e[99];sprintf(f,"Sully_%d.c",i);sprintf(c,"gcc -Wall -Wextra -Werror %s -o Sully_%d",f,i);sprintf(e,"./Sully_%d",i);FILE*p=fopen(f,"w");if(p){fprintf(p,S,10,i-1,34,S);fclose(p);}system(c);if(i>0)system(e);}
```

### 8.4 Código final híbrido

```c
#include <stdio.h>
#include <stdlib.h>
#define I 5
#define S "#include <stdio.h>%1$c#include <stdlib.h>%1$c#define I %2$d%1$c#define S %3$c%4$s%3$c%1$c#define M() int main(){int i=I;if(i<0)return 0;char f[99],c[99],e[99];sprintf(f,%3$cSully_%%d.c%3$c,i);sprintf(c,%3$cgcc -Wall -Wextra -Werror %%s -o Sully_%%d%3$c,f,i);sprintf(e,%3$c./Sully_%%d%3$c,i);FILE*p=fopen(f,%3$cw%3$c);if(p){fprintf(p,S,10,i-1,34,S);fclose(p);}system(c);if(i>0)system(e);}%1$cM()"
#define M() int main(){int i=I;if(i<0)return 0;char f[99],c[99],e[99];sprintf(f,"Sully_%d.c",i);sprintf(c,"gcc -Wall -Wextra -Werror %s -o Sully_%d",f,i);sprintf(e,"./Sully_%d",i);FILE*p=fopen(f,"w");if(p){fprintf(p,S,10,i-1,34,S);fclose(p);}system(c);if(i>0)system(e);}
M()
```

### 8.5 Cambios respecto a la versión sin macros

1. **I en lugar de 5 hardcoded**: Más fácil cambiar el valor inicial
2. **M() como en Grace**: Oculta el main en una macro
3. **Variables más cortas**: `f`, `c`, `e` en lugar de `filename`, `compile`, `exec`
4. **Arrays más pequeños**: `[99]` en lugar de `[100]` para ahorrar espacio

### 8.6 Ventajas de esta versión

- **Consistencia**: Los tres ejercicios (Colleen, Grace, Sully) usan un estilo similar
- **Elegancia**: Las macros hacen el código más limpio
- **Flexibilidad**: Cambiar `#define I 5` a otro valor es trivial
- **Compacto**: El código es más corto

### 8.7 El string S desglosado

```
#include <stdio.h>%1$c           → #include <stdio.h>\n
#include <stdlib.h>%1$c          → #include <stdlib.h>\n
#define I %2$d%1$c               → #define I 4\n (o el valor i-1)
#define S %3$c%4$s%3$c%1$c      → #define S "todo este string"\n
#define M() int main(){...}%1$c  → #define M() int main(){...}\n
M()                              → M()
```

Esta versión híbrida combina lo mejor de Grace (estructura con macros) con la funcionalidad de Sully (auto-replicación con compilación).

## Conclusión

Sully combina todos los conceptos de los quines anteriores:
- Auto-referencia (como Colleen)
- Escritura a archivo (como Grace)
- Uso de macros para estructura (como Grace)
- Compilación y ejecución dinámica (nuevo en Sully)
