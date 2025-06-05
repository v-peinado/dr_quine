# Tutorial: Crear Grace - De Quine básico a macros

## Introducción

En este tutorial voy a explicar cómo crear Grace partiendo de un quine básico. El objetivo es cumplir los requisitos del subject: un comentario multilínea, exactamente 3 defines, y sin declarar main directamente.

## Paso 1: Entender los requisitos

Según el subject, el comentario debe verse así:
```
/*
	This program will print its own source when run.
*/
```

Y el programa sin main declarado:
```c
#include <stdio.h>
#define FT(x)int main(){ /* code */ }
[..]
FT(xxxxxxxx)
```

## Paso 2: Punto de partida - Quine básico

Empiezo con un quine simple que ya funciona escribiendo a archivo:

```c
/*
	This program will print its own source when run.
*/
#include <stdio.h>

int main() {
	FILE *f = fopen("Grace_kid.c", "w");
	if(f) {
		char *s = "/*%1$c%2$cThis program will print its own source when run.%1$c*/%1$c#include <stdio.h>%1$c%1$cint main() {%1$c%2$cFILE *f = fopen(%3$cGrace_kid.c%3$c, %3$cw%3$c);%1$c%2$cif(f) {%1$c%2$c%2$cchar *s = %3$c%4$s%3$c;%1$c%2$c%2$cfprintf(f, s, 10, 9, 34, s);%1$c%2$c%2$cfclose(f);%1$c%2$c}%1$c%2$creturn 0;%1$c}%1$c";
		fprintf(f, s, 10, 9, 34, s);
		fclose(f);
	}
	return 0;
}
```

Los argumentos posicionales que uso:
- `%1$c` → 10 = `\n` (salto de línea)
- `%2$c` → 9 = `\t` (tabulador)
- `%3$c` → 34 = `"` (comillas)
- `%4$s` → s = el string completo

## Paso 3: Simplificar sin tabuladores

Para hacer el código más simple, elimino los tabuladores:

```c
/*
	This program will print its own source when run.
*/
#include <stdio.h>

int main() {
	FILE *f = fopen("Grace_kid.c", "w");
	if(f) {
		char *s = "/*%1$c	This program will print its own source when run.%1$c*/%1$c#include <stdio.h>%1$c%1$cint main() {%1$cFILE *f = fopen(%2$cGrace_kid.c%2$c, %2$cw%2$c);%1$cif(f) {%1$cchar *s = %2$c%3$s%2$c;%1$cfprintf(f, s, 10, 34, s);%1$cfclose(f);%1$c}%1$creturn 0;%1$c}%1$c";
		fprintf(f, s, 10, 34, s);
		fclose(f);
	}
	return 0;
}
```

Ahora solo necesito 3 argumentos:
- `%1$c` → 10 = `\n`
- `%2$c` → 34 = `"`
- `%3$s` → s = el string

## Paso 4: Primer define - FILE_NAME

Voy a extraer "Grace_kid.c" a una macro.

### Identifico dónde aparece:
- En el código: `fopen("Grace_kid.c", "w")`
- En el string: `fopen(%2$cGrace_kid.c%2$c, %2$cw%2$c)`

### Creo la macro y actualizo:

```c
/*
	This program will print its own source when run.
*/
#include <stdio.h>
#define FILE_NAME "Grace_kid.c"

int main() {
	FILE *f = fopen(FILE_NAME, "w");
	if(f) {
		char *s = "/*%1$c	This program will print its own source when run.%1$c*/%1$c#include <stdio.h>%1$c#define FILE_NAME %2$cGrace_kid.c%2$c%1$c%1$cint main() {%1$cFILE *f = fopen(FILE_NAME, %2$cw%2$c);%1$cif(f) {%1$cchar *s = %2$c%3$s%2$c;%1$cfprintf(f, s, 10, 34, s);%1$cfclose(f);%1$c}%1$creturn 0;%1$c}%1$c";
		fprintf(f, s, 10, 34, s);
		fclose(f);
	}
	return 0;
}
```

## Paso 5: Segundo define - STR

Muevo el string largo a una macro para mejorar la legibilidad.

### El string debe incluir su propia definición:
En el string, donde antes decía `char *s = %2$c%3$s%2$c;`, ahora debe decir:
`#define STR %2$c%3$s%2$c`

### Código actualizado:

```c
/*
	This program will print its own source when run.
*/
#include <stdio.h>
#define FILE_NAME "Grace_kid.c"
#define STR "/*%1$c	This program will print its own source when run.%1$c*/%1$c#include <stdio.h>%1$c#define FILE_NAME %2$cGrace_kid.c%2$c%1$c#define STR %2$c%3$s%2$c%1$c%1$cint main() {%1$cFILE *f = fopen(FILE_NAME, %2$cw%2$c);%1$cif(f) {%1$cfprintf(f, STR, 10, 34, STR);%1$cfclose(f);%1$c}%1$creturn 0;%1$c}%1$c"

int main() {
	FILE *f = fopen(FILE_NAME, "w");
	if(f) {
		fprintf(f, STR, 10, 34, STR);
		fclose(f);
	}
	return 0;
}
```

## Paso 6: Tercer define - MAIN() - El truco final

Este es el paso crucial. Grace requiere que NO declaremos main directamente.

### Creo la macro MAIN():

```c
#define MAIN() int main(){FILE *f=fopen(FILE_NAME,"w");if(f){fprintf(f,STR,10,34,STR);fclose(f);}return 0;}
```

### Actualizo el string para incluir:
1. La definición de MAIN
2. La llamada `MAIN()` al final

## Código final de Grace

```c
/*
	This program will print its own source when run.
*/
#include <stdio.h>
#define FILE_NAME "Grace_kid.c"
#define STR "/*%1$c	This program will print its own source when run.%1$c*/%1$c#include <stdio.h>%1$c#define FILE_NAME %2$cGrace_kid.c%2$c%1$c#define STR %2$c%3$s%2$c%1$c#define MAIN() int main(){FILE *f=fopen(FILE_NAME,%2$cw%2$c);if(f){fprintf(f,STR,10,34,STR);fclose(f);}return 0;}%1$cMAIN()%1$c"
#define MAIN() int main(){FILE *f=fopen(FILE_NAME,"w");if(f){fprintf(f,STR,10,34,STR);fclose(f);}return 0;}
MAIN()
```

## Cómo verifico que funciona

```bash
# Compilo
gcc -Wall -Wextra -Werror -o Grace Grace.c

# Ejecuto (crea Grace_kid.c)
./Grace

# Verifico que son idénticos
diff Grace.c Grace_kid.c
```

Si diff no muestra nada, ¡perfecto!