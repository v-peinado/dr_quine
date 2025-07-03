# Compiler and flags
CC			= gcc
CFLAGS		= -Wall -Wextra -Werror
RM			= rm -f

# Programs
COLLEEN		= Colleen
GRACE		= Grace
SULLY		= Sully

# Source files
COLLEEN_SRC	= Colleen.c
GRACE_SRC	= Grace.c
SULLY_SRC	= Sully.c

# Object files
COLLEEN_OBJ	= $(COLLEEN_SRC:.c=.o)
GRACE_OBJ	= $(GRACE_SRC:.c=.o)
SULLY_OBJ	= $(SULLY_SRC:.c=.o)

# All programs
PROGRAMS	= $(COLLEEN) $(GRACE) $(SULLY)

# Colors for pretty output
GREEN		= \033[0;32m
YELLOW		= \033[0;33m
RED			= \033[0;31m
RESET		= \033[0m

# Default target
all: $(PROGRAMS)

# Colleen compilation
$(COLLEEN): $(COLLEEN_OBJ)
	@$(CC) $(CFLAGS) -o $(COLLEEN) $(COLLEEN_OBJ)
	@echo "$(GREEN)✓ $(COLLEEN) compiled$(RESET)"

# Grace compilation
$(GRACE): $(GRACE_OBJ)
	@$(CC) $(CFLAGS) -o $(GRACE) $(GRACE_OBJ)
	@echo "$(GREEN)✓ $(GRACE) compiled$(RESET)"

# Sully compilation
$(SULLY): $(SULLY_OBJ)
	@$(CC) $(CFLAGS) -o $(SULLY) $(SULLY_OBJ)
	@echo "$(GREEN)✓ $(SULLY) compiled$(RESET)"

# Object files compilation
%.o: %.c
	@$(CC) $(CFLAGS) -c $< -o $@
	@echo "$(YELLOW)○ Compiling $<$(RESET)"

# Clean object files
clean:
	@$(RM) $(COLLEEN_OBJ) $(GRACE_OBJ) $(SULLY_OBJ)
	@$(RM) Grace_kid.c
	@$(RM) Sully_*.c
	@$(RM) Sully_*
	@# Remove only numbered Sully executables, not the original
	@for i in 0 1 2 3 4 5; do \
		$(RM) Sully_$$i 2>/dev/null || true; \
	done
	@echo "$(RED)✗ Object files cleaned$(RESET)"

# Clean everything
fclean: clean
	@$(RM) $(PROGRAMS)
	@echo "$(RED)✗ Executables removed$(RESET)"

# Recompile everything
re: fclean all

# Test targets (bonus for development)
test: all
	@echo "$(YELLOW)Testing Colleen...$(RESET)"
	@./$(COLLEEN) > tmp_colleen.c
	@if diff -q $(COLLEEN_SRC) tmp_colleen.c > /dev/null; then \
		echo "$(GREEN)✓ Colleen test passed$(RESET)"; \
	else \
		echo "$(RED)✗ Colleen test failed$(RESET)"; \
	fi
	@$(RM) tmp_colleen.c
	@echo "$(YELLOW)Testing Grace...$(RESET)"
	@./$(GRACE)
	@if diff -q $(GRACE_SRC) Grace_kid.c > /dev/null; then \
		echo "$(GREEN)✓ Grace test passed$(RESET)"; \
	else \
		echo "$(RED)✗ Grace test failed$(RESET)"; \
	fi
	@echo "$(YELLOW)Testing Sully...$(RESET)"
	@./$(SULLY)
	@if [ -f "Sully_5.c" ] && [ -f "Sully_0.c" ]; then \
		echo "$(GREEN)✓ Sully test passed (files created)$(RESET)"; \
	else \
		echo "$(RED)✗ Sully test failed$(RESET)"; \
	fi

# Individual test targets
test_colleen: $(COLLEEN)
	@./$(COLLEEN) > tmp.c && diff $(COLLEEN_SRC) tmp.c && echo "$(GREEN)✓ Colleen is a valid quine$(RESET)" || echo "$(RED)✗ Colleen failed$(RESET)"
	@$(RM) tmp.c

test_grace: $(GRACE)
	@./$(GRACE) && diff $(GRACE_SRC) Grace_kid.c && echo "$(GREEN)✓ Grace is a valid quine$(RESET)" || echo "$(RED)✗ Grace failed$(RESET)"

test_sully: $(SULLY)
	@./$(SULLY) && ls -la Sully_*.c | wc -l

# Phony targets
.PHONY: all clean fclean re test test_colleen test_grace test_sully