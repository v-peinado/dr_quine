#include <stdio.h>
#include <stdlib.h>

int main() {
int i = 5;
if (i < 0) return 0;
char filename[20];
char compile[200];
char exec[20];
sprintf(filename, "Sully_%d.c", i);
sprintf(compile, "gcc -Wall -Wextra -Werror %s -o Sully_%d", filename, i);
sprintf(exec, "./Sully_%d", i);
FILE *f = fopen(filename, "w");
if(f) {
char *s = "#include <stdio.h>%1$c#include <stdlib.h>%1$c%1$cint main() {%1$cint i = %2$d;%1$cif (i < 0) return 0;%1$cchar filename[20];%1$cchar compile[200];%1$cchar exec[20];%1$csprintf(filename, %3$cSully_%%d.c%3$c, i);%1$csprintf(compile, %3$cgcc -Wall -Wextra -Werror %%s -o Sully_%%d%3$c, filename, i);%1$csprintf(exec, %3$c./Sully_%%d%3$c, i);%1$cFILE *f = fopen(filename, %3$cw%3$c);%1$cif(f) {%1$cchar *s = %3$c%4$s%3$c;%1$cfprintf(f, s, 10, i-1, 34, s);%1$cfclose(f);%1$c}%1$csystem(compile);%1$cif (i > 0) system(exec);%1$creturn 0;%1$c}%1$c";
fprintf(f, s, 10, i-1, 34, s);
fclose(f);
}
system(compile);
if (i > 0) system(exec);
return 0;
}