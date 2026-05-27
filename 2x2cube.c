#include <stdint.h>
#include <stdio.h>

typedef enum {WHITE, YELLOW, RED, ORANGE, BLUE, GREEN} Color;

int totalStickers = 21;

typedef struct {
    uint64_t state;
} Cube;

//         +---+---+
//         | 0 | 1 |  <- Top / Up
//         | 2 | 3 |
// +---+---+---+---+---+---+---+---+
// | 4 | 5 | 8 | 9 |12 |13 |16 |17 |  <- Left, Front, Right, Back
// | 6 | 7 |10 |11 |14 |15 |18 |19 |
// +---+---+---+---+---+---+---+---+
//         |20 |21 |
//         |22 |23 |  <- Bottom / Down
//         +---+---+


//         +---+---+
//         | 0 | 1 |  <- Top / Up
//         | 2 | L |
// +---+---+---+---+---+---+---+---+
// | 3 | 4 | 7 | L | L |10 |13 |14 |  <- Left, Front, Right, Back
// | 5 | 6 | 8 | 9 |11 |12 |15 |16 |
// +---+---+---+---+---+---+---+---+
//         |17 |18 |
//         |19 |20 |  <- Bottom / Down
//         +---+---+

Cube solved_cube() {
    Cube c;
    c.state = 0;
    Color colors[] = {
        WHITE, WHITE, WHITE,
        RED, RED, RED, RED,
        BLUE, BLUE, BLUE,
        ORANGE, ORANGE, ORANGE,
        GREEN, GREEN, GREEN, GREEN,
        YELLOW, YELLOW, YELLOW, YELLOW
    };

    for(int i = 0; i < totalStickers; i++){
        c.state |= ( (uint64_t) colors[i] << (i * 3));
    }
    
    return c;
}
