#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <math.h>


int main(void)
{
    string text = get_string("Text: ");


// letters counter
    int letters = 0;
    for (int i = 0; text[i] != '\0'; i++)
    {
        // If the character is lowercase or upper, counter +1
        if (islower(text[i]) || isupper(text[i]))
        {
            letters++;
        }
    }


// words counter
// The concept is counting the whitespace then +1
    int words = 1;
    for (int j = 0; text[j] != '\0'; j++)
    {
        // (prevent count 2 space) and (prevent count the space at the end)
        if ((isspace(text[j]) && isspace(text[j + 1]) != true) && (isspace(text[j]) && text[j + 1] != '\0'))
        {
            words++;
        }
    }


// sentences counter
// any sequence of characters that ends with a . or a ! or a ? to be a sentence
    int sentences = 0;
    for (int k = 0; text[k] != '\0'; k++)
    {
        if (text[k] == '.' || text[k] == '!' || text[k] == '?')
        {
            sentences++;
        }
    }


// Coleman-Liau Formula
    // L = letters / words * 100
    float l = (float) letters / (float) words * 100;

    // S = sentences / words * 100
    float s = (float) sentences / (float) words * 100;

    // index = 0.0588 * L - 0.296 * S - 15.8
    float index = 0.0588 * l - 0.296 * s - 15.8;

    if (index <= 16 && index >= 1)
    {
        printf("Grade %i\n", (int) round(index));
    }
    else if (index < 1)
    {
        index = 1;
        printf("Before Grade %i\n", (int) round(index));
    }
    else if (index > 16)
    {
        index = 16;
        printf("Grade %i+\n", (int) round(index));
    }
}





