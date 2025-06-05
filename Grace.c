/*
 * Comment
 */
#include <stdio.h>
#define FILE_NAME "Grace_kid.c"
#define STR "/*%1$c * Comment%1$c */%1$c#include <stdio.h>%1$c#define FILE_NAME %2$cGrace_kid.c%2$c%1$c#define STR %2$c%3$s%2$c%1$c#define MAIN() int main(){FILE *f=fopen(FILE_NAME,%2$cw%2$c);if(f){fprintf(f,STR,10,34,STR);fclose(f);}return 0;}%1$cMAIN()%1$c"
#define MAIN() int main(){FILE *f=fopen(FILE_NAME,"w");if(f){fprintf(f,STR,10,34,STR);fclose(f);}return 0;}
MAIN()