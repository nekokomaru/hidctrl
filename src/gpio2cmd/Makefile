CC = gcc
CFLAGS = -O2 -std=gnu99 -Wall -Wno-declaration-after-statement

PROGRAM = gpio2cmd
CONF = gpio2cmd.conf
OBJS = gpio2cmd.o

.SUFFIXES: .c .o

.PHONY: all
all: $(PROGRAM)

$(PROGRAM): $(OBJS)
	$(CC) -o $@ $^

.c.o:
	$(CC) $(CFLAGS) -c $<

.PHONY: clean
clean:
	$(RM) $(PROGRAM) $(OBJS)

.PHONY: install
install: $(PROGRAM)
	install $(PROGRAM) /usr/local/bin
	install -m 644 $(CONF) /usr/local/etc

.PHONY: uninstall
uninstall:
	$(RM) /usr/local/bin/$(PROGRAM)
	$(RM) /usr/local/etc/$(CONF)
