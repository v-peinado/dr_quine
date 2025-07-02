/*
 * Comment outside the program
 */
#include <stdio.h>
void p() {
	char *s = "/*%1$c * Comment outside the program%1$c */%1$c#include <stdio.h>%1$cvoid p() {%1$c%2$cchar *s = %3$c%4$s%3$c;%1$c%2$cprintf(s, 10, 9, 34, s);%1$c}%1$cint main() {%1$c%2$c/* Comment inside main function */%1$c%2$cp();%1$c%2$creturn 0;%1$c}";
	printf(s, 10, 9, 34, s);
}
int main() {
	/* Comment inside main function */
	p();
	return 0;
}