/*
 * Comment outside the program
 */
#include <stdio.h>
void p() {
        char *s = "/*%c * Comment outside the program%c */%c#include <stdio.h>%cvoid p() {%c%cchar *s = %c%s%c;%c%cprintf(s, 10, 10, 10, 10, 10, 9, 34, s, 34, 10, 9, 10, 10, 10, 9, 10, 9, 10, 9, 10, 10);%c}%cint main() {%c%c/* Comment inside main function */%c%cp();%c%creturn 0;%c}";
        printf(s, 10, 10, 10, 10, 10, 9, 34, s, 34, 10, 9, 10, 10, 10, 9, 10, 9, 10, 9, 10, 10);
}
int main() {
        /* Comment inside main function */
        p();
        return 0;
}