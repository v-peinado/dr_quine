# De Quine básico a Grace: Guía detallada

## Paso 3: Punto de partida - Quine con argumentos posicionales (simplificado)

Partimos de este quine funcional que escribe a archivo:

```c
/*
 * Comment
 */
#include <stdio.h>

int main() {
    FILE *f = fopen("Grace_kid.c", "w");
    if(f) {
        char *s = "/*%1$c * Comment%1$c */%1$c#include <stdio.h>%1$c%1$cint main() {%1$cFILE *f = fopen(%2$cGrace_kid.c%2$c, %2$cw%2$c);%1$cif(f) {%1$cchar *s = %2$c%3$s%2$c;%1$cfprintf(f, s, 10, 34, s);%1$cfclose(f);%1$c}%1$creturn 0;%1$c}%1$c";
        fprintf(f, s, 10, 34, s);
        fclose(f);
    }
    return 0;
}
```

### Argumentos posicionales explicados (versión simplificada):
- `%1$c` → Primer argumento (10) = `\n` (salto de línea)
- `%2$c` → Segundo argumento (34) = `"` (comillas)
- `%3$s` → Tercer argumento (STR) = el string completo

## Paso 4: Crear el primer define - FILE_NAME

### 4.1 Identificar qué extraer
Buscamos en el código las apariciones de `"Grace_kid.c"`:
- En el main: `fopen("Grace_kid.c", "w")`
- En el string: `fopen(%2$cGrace_kid.c%2$c, %2$cw%2$c)`

### 4.2 Crear la macro
```c
#define FILE_NAME "Grace_kid.c"
```

### 4.3 Reemplazar en el código principal
```c
FILE *f = fopen(FILE_NAME, "w");  // Antes: fopen("Grace_kid.c", "w")
```

### 4.4 Actualizar el string
El string debe incluir la definición de la macro:
```c
char *s = "/*%1$c * Comment%1$c */%1$c#include <stdio.h>%1$c#define FILE_NAME %3$cGrace_kid.c%3$c%1$c%1$cint main() {%1$c%2$cFILE *f = fopen(FILE_NAME, %3$cw%3$c);%1$c...";
```

### 4.5 Código resultante
```c
/*
 * Comment
 */
#include <stdio.h>
#define FILE_NAME "Grace_kid.c"

int main() {
    FILE *f = fopen(FILE_NAME, "w");
    if(f) {
        char *s = "/*%1$c * Comment%1$c */%1$c#include <stdio.h>%1$c#define FILE_NAME %2$cGrace_kid.c%2$c%1$c%1$cint main() {%1$cFILE *f = fopen(FILE_NAME, %2$cw%2$c);%1$cif(f) {%1$cchar *s = %2$c%3$s%2$c;%1$cfprintf(f, s, 10, 34, s);%1$cfclose(f);%1$c}%1$creturn 0;%1$c}%1$c";
        fprintf(f, s, 10, 34, s);
        fclose(f);
    }
    return 0;
}
```

## Paso 5: Crear el segundo define - STR

### 5.1 Por qué necesitamos STR
- El string es muy largo y dificulta la lectura
- Grace requiere exactamente 3 defines
- Necesitamos que el string se referencie a sí mismo

### 5.2 Crear la macro STR
```c
#define STR "contenido_del_string"
```

### 5.3 Actualizar el string para incluir su propia definición
El string debe contener:
```
#define STR %2$c%3$s%2$c
```
Donde `%3$s` será reemplazado por el contenido de STR

### 5.4 Cambiar las referencias
- En el código: eliminar la declaración `char *s = "...";`
- En fprintf: `fprintf(f, STR, 10, 34, STR);`

### 5.5 Código resultante
```c
/*
 * Comment
 */
#include <stdio.h>
#define FILE_NAME "Grace_kid.c"
#define STR "/*%1$c * Comment%1$c */%1$c#include <stdio.h>%1$c#define FILE_NAME %2$cGrace_kid.c%2$c%1$c#define STR %2$c%3$s%2$c%1$c%1$cint main() {%1$cFILE *f = fopen(FILE_NAME, %2$cw%2$c);%1$cif(f) {%1$cfprintf(f, STR, 10, 34, STR);%1$cfclose(f);%1$c}%1$creturn 0;%1$c}%1$c"

int main() {
    FILE *f = fopen(FILE_NAME, "w");
    if(f) {
        fprintf(f, STR, 10, 34, STR);
        fclose(f);
    }
    return 0;
}
```

## Paso 6: Crear el tercer define - MAIN()

### 6.1 Requisito crítico de Grace
- **NO debe haber `int main()` declarado directamente**
- El main debe estar "oculto" en una macro

### 6.2 Crear la macro MAIN()
```c
#define MAIN() int main() { FILE *f = fopen(FILE_NAME, "w"); if(f) { fprintf(f, STR, 10, 34, STR); fclose(f); } return 0; }
```

### 6.3 Actualizar el string
El string debe incluir:
1. La definición de MAIN: `#define MAIN() int main() {...}`
2. La llamada a MAIN: `MAIN()`

### 6.4 Estructura del string actualizada
```
"/* Comment */
#include <stdio.h>
#define FILE_NAME "Grace_kid.c"
#define STR "..."
#define MAIN() int main() {...}
MAIN()"
```

### 6.5 Versión compacta del string
Para hacer el quine más compacto, eliminamos saltos de línea innecesarios en MAIN:
```c
#define MAIN() int main(){FILE *f=fopen(FILE_NAME,"w");if(f){fprintf(f,STR,10,34,STR);fclose(f);}return 0;}
```

## Paso 7: Código final de Grace (simplificado sin tabuladores)

```c
/*
 * Comment
 */
#include <stdio.h>
#define FILE_NAME "Grace_kid.c"
#define STR "/*%1$c * Comment%1$c */%1$c#include <stdio.h>%1$c#define FILE_NAME %2$cGrace_kid.c%2$c%1$c#define STR %2$c%3$s%2$c%1$c#define MAIN() int main(){FILE *f=fopen(FILE_NAME,%2$cw%2$c);if(f){fprintf(f,STR,10,34,STR);fclose(f);}return 0;}%1$cMAIN()%1$c"
#define MAIN() int main(){FILE *f=fopen(FILE_NAME,"w");if(f){fprintf(f,STR,10,34,STR);fclose(f);}return 0;}
MAIN()
```

## Explicación del string STR

El string contiene exactamente lo que se escribirá en Grace_kid.c:

### Visualización con formato (para mayor claridad):
```c
/*
 * Comment
 */
#include <stdio.h>
#define FILE_NAME "Grace_kid.c"
#define STR "todo este string..."
#define MAIN() int main(){
	FILE *f=fopen(FILE_NAME,"w");
	if(f){
		fprintf(f,STR,10,34,STR);
		fclose(f);
	}
	return 0;
}
MAIN()
```

### Mapeo real del string:
```
/*%1$c * Comment%1$c */%1$c                                    → /* Comment */
#include <stdio.h>%1$c                                         → #include <stdio.h>
#define FILE_NAME %2$cGrace_kid.c%2$c%1$c                     → #define FILE_NAME "Grace_kid.c"
#define STR %2$c%3$s%2$c%1$c                                  → #define STR "todo este string"
#define MAIN() int main(){...}%1$c                            → #define MAIN() int main(){...}
MAIN()%1$c                                                     → MAIN()
```

**Nota**: Aunque el código real no usa tabuladores (para simplificar), el archivo resultante será idéntico funcionalmente.

## Verificación final

### Checklist de requisitos:
- ✅ **Un comentario**: `/* Comment */`
- ✅ **Tres defines exactos**: `FILE_NAME`, `STR`, `MAIN()`
- ✅ **Sin main declarado**: El main está dentro de `MAIN()`
- ✅ **Ejecutado por macro**: `MAIN()` al final
- ✅ **Escribe a archivo**: Crea `Grace_kid.c`

### Cómo funciona (versión simplificada):
1. El preprocesador expande `MAIN()` creando la función `main`
2. `main` abre el archivo `Grace_kid.c`
3. `fprintf` escribe el string `STR` en el archivo
4. Solo 3 argumentos necesarios:
   - `%1$c` → Saltos de línea (10)
   - `%2$c` → Comillas (34)
   - `%3$s` → El string STR completo (auto-referencia)
5. El resultado es un archivo idéntico al código fuente original

## Prueba del quine

Para verificar que funciona:

```bash
# Compilar Grace
gcc -o Grace Grace.c

# Ejecutar (crea Grace_kid.c)
./Grace

# Verificar que son idénticos
diff Grace.c Grace_kid.c

# Si no hay salida, ¡el quine funciona perfectamente!
```

## Posibles errores comunes

### 1. Olvidar escapar comillas en el string
```c
// MAL
#define STR "...#define FILE_NAME "Grace_kid.c"..."

// BIEN  
#define STR "...#define FILE_NAME %2$cGrace_kid.c%2$c..."
```

### 2. No incluir la llamada a MAIN() en el string
```c
// El string debe terminar con:
"...MAIN()%1$c"
```

### 3. Declarar main directamente
```c
// MAL
int main() { ... }

// BIEN
#define MAIN() int main() { ... }
MAIN()
```

### 4. Tener más o menos de 3 defines
Debe ser exactamente 3, ni más ni menos.

## Optimizaciones opcionales

### Nombres más cortos
```c
#define F "Grace_kid.c"
#define S "..."
#define M() int main(){...}
M()
```

### Eliminar el chequeo de error
```c
#define M() int main(){FILE *f=fopen(F,"w");fprintf(f,S,10,34,S);fclose(f);return 0;}
```

**Nota**: Algunos compiladores permiten omitir `return 0;` en main, lo que haría el código aún más corto.

### Versión ultra-compacta
Combinando todas las optimizaciones:
```c
/**/
#include <stdio.h>
#define F "Grace_kid.c"
#define S "/**/%1$c#include <stdio.h>%1$c#define F %2$cGrace_kid.c%2$c%1$c#define S %2$c%3$s%2$c%1$c#define M()int main(){FILE*f=fopen(F,%2$cw%2$c);fprintf(f,S,10,34,S);fclose(f);}%1$cM()"
#define M()int main(){FILE*f=fopen(F,"w");fprintf(f,S,10,34,S);fclose(f);}
M()
```