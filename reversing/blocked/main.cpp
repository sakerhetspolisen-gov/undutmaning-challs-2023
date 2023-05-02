#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "main.h"

constexpr int BLOCK_SIZE = 308;
constexpr int BSIZE = BLOCK_SIZE * sizeof(Value);

#define RAND_PTR() (rand() % ((BLOCK_SIZE / 2) + BLOCK_SIZE)) + BLOCK_SIZE

Value x(int k) // derive_values
{
    int x2 = rand() % (128 + (k + 1));
    int y2 = rand() % (x2 - k);

    int d = x2 - y2 - k;
    int x1 = rand() % d;
    int y1 = d - x1;
    return Value{x1, y1, x2, y2};
}

Value y(std::set<int>& used) // find_pointers
{
    Value p = Value{RAND_PTR(), 0, RAND_PTR(), 0}; // {RAND_PTR(), RAND_PTR(), RAND_PTR(), RAND_PTR()}

    while (used.count(p.x1))
        p.x1 = RAND_PTR();
    used.insert(p.x1);

    /* kommentarerna är till för att ha varje värde vara en pekare, istället för bara låta två vara det
     while (used.count(p.y1))
        p.y1 = RAND_PTR();
    used.insert(p.y1); */

    while (used.count(p.x2))
        p.x2 = RAND_PTR();
    used.insert(p.x2);

    /* while (used.count(p.y2))
        p.y2 = RAND_PTR();
    used.insert(p.y2); */

    return p;
}

int* encode(const char* encode)
{
    int* block = (int*)malloc(BSIZE);
    std::set<int> used;
    int encode_len = strlen(encode);
    int idx = 0;

    for (int i = 0; i < encode_len; i++)
    {
        Value v = x(encode[i]);
        Value p = y(used);

        block[idx] = p.x1;
        block[idx + 1] = v.y1; // p.y1;
        block[idx + 2] = p.x2;
        block[idx + 3] = v.y2; // v.y2;

        block[p.x1] = v.x1;
        //block[p.y1] = v.y1;
        block[p.x2] = v.x2;
        //block[p.y2] = v.y2;
        idx += 4;
    }
    return block;
}

#ifdef MAKE_FLAG
    void generate_flag(const char* f)
    {
        int* encoded = encode(f);
        int x = sizeof(Value) * strlen(f);
        printf("const int flag[] = { ");
        for (int i = 0; i < x; i++)
            if (i != x - 1)
                printf("%d, ", encoded[i]);
            else printf("%d };\n", encoded[i]);
        printf("Klistra in detta i main.h.\n");
    }
#endif

#ifdef SOLVE
    const char* solve()
    {
        char* s = (char*)malloc(BSIZE);
        int idx = 0;
        for (int i = 0; i < BSIZE; i++)
        {
            Value p = {flag[idx], flag[idx + 1], flag[idx + 2], flag[idx + 3]};
            Value v = {flag[p.x1], p.y1, flag[p.x2], p.y2}; // flag[p.x1], flag[p.y1], flag[p.x2], flag[p.y2]

            int z2 = v.x2 - v.y2;
            int z1 = v.x1 + v.y1;
            if ((s[i] = z2 - z1) == '}')
                break;
            idx += 4;
        }
        return s;
    }
#endif

int main()
{
    srand(1337);

    #ifdef SOLVE
        printf("%s\n", solve());
        return 0;
    #endif

    #ifdef MAKE_FLAG
        FILE* file = fopen("flag.txt", "rb");
        if (!file)
            return -1;

        fseek(file, 0, SEEK_END);
        size_t file_size = ftell(file);
        fseek(file, 0, SEEK_SET);

        char* f = (char*)malloc(file_size + 1);
        fread(f, file_size, 1, file);
        fclose(file);

        f[file_size] = 0;
        generate_flag(f);
        return 0;
    #endif

    char input[128];
    printf("Submit your flag.\n");
    scanf("%s", input);

    if (memcmp(encode(input), flag, sizeof(flag)) == 0)
        printf("Congratulations! You found the flag :D\n");
    else
        printf("Wrong flag :(\n");

    return 0;
}
