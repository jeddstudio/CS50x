#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int n;
    int hash = 1;
    do
    {
        n = get_int("Height(1-8): ");
    }
    while (n < 1 || n > 8);

    // Start making a pyramid
    // for each row
    while (n > 0)
    {
        // Print a space
        int j = n - 1;
        while (j > 0)
        {
            printf(" ");
            j--;
        }
        // Print a brick
        for (int k = hash; k > 0; k--)
        {
            printf("#");
        }

        printf("\n");
        n--;
        hash++;
    }


}