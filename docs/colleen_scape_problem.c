/*
	Comment out
*/

#include <stdio.h>

void print_source(const char *s)
{
	printf("%s", s);
}

int main(void)
{
/*
	Comment.
*/
	const char *s = "/*\n\tComment out\n*/\n\n#include <stdio.h>\n\nvoid print_source(const char *s)\n{\n\tprintf(\"%s\", s);\n}\n\nint main(void)\n{\n/*\n\tComment.\n*/\n\tconst char *s = \"/*\\n\\tComment out\\n*/\\n\\n#include <stdio.h>\\n\\nvoid print_source(const char *s)\\n{\\n\\tprintf(\\\"%s\\\", s);\\n}\\n\\nint main(void)\\n{\\n/*\\n\\tComment.\\n*/\\n\\tconst char *s = \\\"\\\";\n\tprint_source(s);\n\treturn (0);\n}\n\";\n\tprint_source(s);\n\treturn (0);\n}\n";
	print_source(s);
	return (0);
}