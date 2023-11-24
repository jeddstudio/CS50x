#include <stdio.h>
#include <stdlib.h>

// each block is 512 in memory card
const int BLOCK_SIZE = 512;

// counting total number of JPEG found
int pic_counter = 0;

// A place for the program to temporarily store data
// use "unsigned" to read hexadecimal values below
unsigned char buffer[512];

// filenames will be ###.jpg
// finally, it is clear that the required value is 8
// 8 => "###.jpg\0", total 8 character
char filename[8];


int main(int argc, char *argv[])
{
    // Set the pointer for storing input and output file
    // Pointers are just addresses
    FILE *input = fopen(argv[1], "r");
    FILE *output = NULL;

    // Check if the user input is vaild
    // if less or more than 2 argument, program not running
    if (argc != 2)
    {
        printf("Usage: ./recover IMAGE\n");
        return 1;
    }
    // Check "input file" is valid
    if (input == NULL)
    {
        printf("Could not open file");
        return 2;
    }

    // Read the input file
    // While the file is still available for reading, it is TRUE
    // While the file is NOT available for reading, it is FALSE, While loop will stop
    while (fread(buffer, sizeof(char), BLOCK_SIZE, input))
    {
        // Condition of checking JPEG
        // (buffer[3] & 0xf0) == 0xe0 is CS50 provided to check the fourth byt
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            // CS50 provided to automatically name a JPEG in order
            sprintf(filename, "%03i.jpg", pic_counter);

            // Open output file to ready to write data into it
            // it is empty at this moment
            output = fopen(filename, "w");

            // Add a counter when a JPEG found
            pic_counter++;
        }

        // if output been assign something, it is not NULL anymore at this step
        // so if still is NULL, just go back while loop and running nxt
        if (output == NULL)
        {
            continue;
        }
        // if NOT NULL, write the data that store in buffer into output file
        else
        {
            fwrite(buffer, sizeof(char), BLOCK_SIZE, output);
        }
    }
    printf("Total recovered: %i\n", pic_counter);
    fclose(input);
    fclose(output);
    return 0;
}
