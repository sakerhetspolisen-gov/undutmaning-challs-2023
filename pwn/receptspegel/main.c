#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#define RECEPT_SIZE 128

int main()
{
    int i, length;
    char *recept = malloc(RECEPT_SIZE);
    char *flag = malloc(64);
    
    /* Se till att allt kommer in och ut som det ska */
    setbuf(stdout, NULL);
    setbuf(stdin, NULL);
    
    if (read(open("./flag.txt", 0), flag, 64) == 0) {
        printf("Fel: ingen flag.txt\n");
        exit(1);
    }

    printf("Välkommen till RS (ReceptSpegel) - skriv ett recept och få det tillbaka!\n");

    printf("Receptets längd: ");
    scanf("%d", &length);

    if (length > RECEPT_SIZE) {
        printf("Ojdå, så långa recept får inte plats!\n");
        exit(1);
    }
    getc(stdin); // Svälj new line från tidigare

    printf("Skriv ditt recept: ");

    for (i = 0; i != length; i++) {
        if ((recept[i] = getc(stdin)) == '\n')
            break;
    }

    printf("Recept: %s\n", recept);
    return 0;
}