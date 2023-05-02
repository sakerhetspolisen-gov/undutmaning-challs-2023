#include <stdio.h>
#include <stddef.h>
#include <stdlib.h>
#include <unistd.h>
#include <termios.h> 
#include <fcntl.h>


#define UP 'w'
#define LEFT 'a'
#define DOWN 's'
#define RIGHT 'd'
#define MAP_Y_MAX 25
#define MAP_Y_MIN 0
#define MAP_X_MAX 100
#define MAP_X_MIN 0
#define STDIN 0

#define KRED  ""
#define KGRN  ""
#define KYEL  ""
#define KBLU  ""


struct snakestruct{
    struct snakestruct * next;
    int x;
    int y;
};



char getch();
int printmap();
int move_snake();
int set_direction(char input);
int check_if_input();
int red(char c);
int green(char c);
int blue(char c);
int yellow(char c);
int place_fruit();
int save_apple_core(int y, int x);
int place_apple_cores();

char map[MAP_Y_MAX][MAP_X_MAX] = {
    "****************************************************************************************************",
    "*                                                                                                  *",
    "*                                                                                                  *",
    "*                                                                                                  *",
    "*                                                                                                  *",
    "*                                                                                                  *",
    "*                                                                                                  *",
    "*                                                                                                  *",
    "*                                                                                                  *",
    "*                                                                                                  *",
    "*                                                                                                  *",
    "*                                                                                                  *",
    "*                                                                                                  *",
    "*                                                                                                  *",
    "*                                                                                                  *",
    "*                                                                                                  *",
    "*                                                                                                  *",
    "*                                                                                                  *",
    "*                                                                                                  *",
    "*                                                                                                  *",
    "*                                                                                                  *",
    "*                                                                                                  *",
    "*                                                                                                  *",
    "*                                                                                                  *",
    "****************************************************************************************************",
};

int gameover = 0;
int status;
char input = '\0';
char direction = RIGHT;
char symbol = '#';
char fruit = '@';
char wall = '*';
char apple_core = '+';

int save_apple_location = 1;

int apple_cores_index = 0;
int apple_cores[266][2];

int apple_index = 0;
int apples[266][2] = {
{5, 64},
{14, 79},
{20, 20},
{11, 79},
{4, 55},
{9, 7},
{14, 95},
{14, 12},
{8, 64},
{15, 5},
{19, 68},
{16, 64},
{8, 56},
{17, 41},
{11, 5},
{6, 1},
{1, 38},
{15, 73},
{13, 86},
{3, 67},
{9, 86},
{19, 58},
{7, 86},
{14, 61},
{21, 76},
{11, 8},
{5, 31},
{18, 55},
{17, 31},
{11, 64},
{9, 56},
{10, 37},
{4, 27},
{12, 32},
{8, 10},
{19, 27},
{6, 56},
{17, 73},
{19, 75},
{21, 5},
{4, 12},
{5, 91},
{10, 79},
{11, 43},
{4, 49},
{19, 25},
{16, 11},
{23, 26},
{4, 45},
{19, 73},
{16, 13},
{6, 13},
{19, 43},
{13, 41},
{3, 34},
{18, 73},
{5, 87},
{7, 11},
{11, 55},
{15, 86},
{14, 40},
{18, 31},
{15, 49},
{4, 23},
{19, 93},
{11, 49},
{6, 41},
{15, 19},
{19, 5},
{10, 19},
{11, 41},
{11, 45},
{10, 56},
{10, 34},
{6, 97},
{10, 8},
{4, 79},
{4, 64},
{19, 78},
{8, 15},
{19, 77},
{13, 26},
{8, 19},
{7, 19},
{17, 12},
{5, 88},
{19, 95},
{11, 51},
{23, 46},
{6, 80},
{5, 27},
{19, 23},
{7, 5},
{19, 79},
{4, 97},
{9, 9},
{13, 4},
{11, 19},
{17, 5},
{19, 11},
{14, 51},
{5, 71},
{8, 71},
{9, 79},
{15, 10},
{19, 21},
{14, 74},
{6, 5},
{14, 5},
{4, 31},
{11, 7},
{11, 86},
{4, 14},
{16, 73},
{9, 64},
{13, 36},
{6, 43},
{19, 3},
{3, 3},
{18, 13},
{18, 41},
{15, 77},
{12, 86},
{5, 95},
{6, 86},
{19, 19},
{15, 41},
{14, 41},
{7, 1},
{19, 87},
{5, 97},
{5, 13},
{4, 3},
{12, 7},
{6, 12},
{9, 19},
{1, 93},
{19, 13},
{9, 62},
{8, 63},
{14, 9},
{17, 86},
{17, 7},
{18, 79},
{14, 86},
{19, 31},
{4, 62},
{7, 41},
{13, 32},
{16, 41},
{13, 30},
{5, 38},
{7, 79},
{11, 47},
{12, 64},
{19, 45},
{16, 19},
{14, 76},
{13, 28},
{18, 86},
{2, 96},
{12, 19},
{9, 5},
{11, 62},
{19, 34},
{5, 89},
{6, 79},
{19, 15},
{13, 8},
{15, 31},
{13, 16},
{3, 71},
{8, 41},
{4, 21},
{5, 56},
{4, 5},
{13, 5},
{16, 79},
{22, 94},
{19, 89},
{2, 50},
{12, 79},
{19, 39},
{7, 64},
{10, 86},
{19, 4},
{6, 78},
{20, 98},
{11, 53},
{14, 31},
{16, 51},
{6, 64},
{19, 41},
{4, 29},
{20, 84},
{5, 19},
{14, 58},
{5, 93},
{18, 19},
{5, 41},
{13, 45},
{20, 50},
{10, 64},
{12, 80},
{17, 19},
{8, 86},
{8, 5},
{12, 41},
{12, 5},
{16, 31},
{4, 7},
{4, 53},
{17, 64},
{7, 78},
{10, 41},
{13, 79},
{6, 19},
{4, 43},
{21, 58},
{15, 64},
{12, 1},
{19, 91},
{16, 86},
{19, 64},
{13, 19},
{4, 18},
{4, 47},
{10, 46},
{13, 70},
{12, 43},
{14, 54},
{19, 56},
{19, 29},
{18, 64},
{22, 29},
{15, 79},
{16, 5},
{4, 41},
{10, 5},
{19, 7},
{23, 88},
{9, 41},
{4, 51},
{13, 34},
{14, 47},
{7, 43},
{21, 2},
{14, 19},
{15, 75},
{20, 7},
{19, 66},
{17, 79},
{3, 31},
{8, 79},
{19, 54},
{14, 64},
{4, 19},
{7, 56},
{18, 5},
{4, 16},
{13, 64},
{4, 25},
{5, 79},
{5, 5},
{4, 4},
{17, 53},
};


struct snakestruct *temp_seg;
struct snakestruct *snake_head;
struct snakestruct *snake_tail;
struct snakestruct *snake_cursor;



int main(){

    snake_head = (struct snakestruct*) malloc(sizeof(struct snakestruct));
    snake_tail = (struct snakestruct*) malloc(sizeof(struct snakestruct));

    snake_head->x = 29;
    snake_head->y = 9;
    snake_head->next = NULL;

    snake_tail->x = 28;
    snake_tail->y = 9;
    snake_tail->next = snake_head;

    save_apple_location = 0;

    while(!gameover){

        if(check_if_input()){
            input = getch();
            if(input != '\0'){
                set_direction(input);
                input = '\0';
            }
        }

        status = move_snake();
        status = place_fruit();
        status = printmap();

        if(direction == LEFT || direction == RIGHT){
            status = usleep(50000);
        }else{
            status = usleep(100000);
        }
    }
}

int set_direction(char input){

    if(input == 'w' && direction != DOWN)
        direction = UP;
    
    else if(input == 'a' && direction != RIGHT)
        direction = LEFT;
    
    else if(input == 's' && direction != UP)
        direction = DOWN;

    else if(input == 'd' && direction != LEFT)
        direction = RIGHT;
    return 1;
}

char getch()
{
    char c;
    c= getchar();
    return(c);
}

int printmap(){
    int y = 0;
    int x = 0;

    if(save_apple_location){
            place_apple_cores();
        }

    system("clear");
    for(y; y < MAP_Y_MAX; y++){
        for(x = 0; x < MAP_X_MAX; x++){
            // printf("%c\033[1;31m",map[y][x]);
            if(map[y][x] == '*')
                yellow(map[y][x]);
            else if(map[y][x] == '@')
                red(map[y][x]);
            else if(map[y][x] == '#')
                green(map[y][x]);
            else if(map[y][x] == '+')
                blue(map[y][x]);
            else
                printf("%c",map[y][x]);
        }
        printf("\n");
    }
    return 1;
}
int red(char c){
    printf("\033[1;31m%c",c);
    return 0;
}
int green(char c){
    printf("\033[1;32m%c",c);
    return 0;
}
int blue(char c){
    printf("\033[1;34m%c",c);
    return 0;
}
int yellow(char c){
    printf("\033[1;33m%c",c);
    return 0;
}

int move_snake(){
    int temp_x = snake_head->x;
    int temp_y = snake_head->y;
    snake_cursor = snake_tail;

    if(direction == UP){
        temp_y = snake_head->y;
        temp_y--;
    }   
    else if (direction == LEFT){
        temp_x = snake_head->x;
        temp_x = temp_x -1;
    }
    else if (direction == DOWN){
        temp_y = snake_head->y;
        temp_y++;
    }
    else if (direction == RIGHT){
        temp_x = snake_head->x;
        temp_x = temp_x +1;
    }
    
        if(map[temp_y][temp_x] == fruit){
    
        temp_seg = (struct snakestruct*) malloc(sizeof(struct snakestruct));
        snake_head->next = temp_seg;
        snake_head = temp_seg;
        snake_head->x = temp_x;
        snake_head->y = temp_y;
        snake_head->next = NULL;
        apple_index++;

        map[temp_y][temp_x] = ' ';


        if(save_apple_location)
                save_apple_core(temp_y,temp_x);

    }else if(map[temp_y][temp_x] == wall){
        
        if(map[snake_tail->y][snake_tail->x] != '*'){
            map[snake_tail->y][snake_tail->x] = ' ';
        }
        
        while(snake_cursor->next != NULL){
            snake_cursor->x = snake_cursor->next->x;
            snake_cursor->y = snake_cursor->next->y;
            snake_cursor = snake_cursor->next;
        }
        if(direction == LEFT)
            temp_x = MAP_X_MAX -2;
        if(direction == RIGHT)
            temp_x = MAP_X_MIN +1;
        if(direction == UP)
            temp_y = MAP_Y_MAX -2;
        if(direction == DOWN)
            temp_y = MAP_Y_MIN +1;

        snake_head->x = temp_x;
        snake_head->y = temp_y;
        snake_cursor = snake_tail;
        
    }else{
        map[snake_tail->y][snake_tail->x] = ' ';
        while(snake_cursor->next != NULL){
            snake_cursor->x = snake_cursor->next->x;
            snake_cursor->y = snake_cursor->next->y;
            snake_cursor = snake_cursor->next;
        }
        snake_head->x = temp_x;
        snake_head->y = temp_y;
        snake_cursor = snake_tail;
    }

    while(snake_cursor->next != NULL){
        map[snake_cursor->y][snake_cursor->x] = symbol;
        snake_cursor = snake_cursor->next;
    }
    map[snake_cursor->y][snake_cursor->x] = symbol;
    snake_cursor = snake_tail;


    return 1;
}

int place_fruit(){

    map[apples[apple_index][0]][apples[apple_index][1]] = fruit;

    return 1;
}

int save_apple_core(int y, int x){

    apple_cores[apple_index - 1][0] = y;
    apple_cores[apple_index - 1][1] = x;

    return 1;
}

int place_apple_cores(){

    for(int i = 0; i < apple_index; i++){            
        map[apple_cores[i][0]][apple_cores[i][1]] = '+';
    }
        
    return 1;
}

int check_if_input(){
    struct termios oldt, newt;
    int ch;
    int oldf;

    tcgetattr(STDIN_FILENO, &oldt);
    newt = oldt;
    newt.c_lflag &= ~(ICANON | ECHO);
    tcsetattr(STDIN_FILENO, TCSANOW, &newt);
    oldf = fcntl(STDIN_FILENO, F_GETFL, 0);
    fcntl(STDIN_FILENO, F_SETFL, oldf | O_NONBLOCK);

    ch = getchar();

    tcsetattr(STDIN_FILENO, TCSANOW, &oldt);
    fcntl(STDIN_FILENO, F_SETFL, oldf);

    if(ch != EOF)
    {
    ungetc(ch, stdin);
    return 1;
    }

    return 0;    
}
