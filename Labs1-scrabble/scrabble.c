#include <ctype.h>
#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Points assigned to each letter of the alphabet
int POINTS[] = {1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};
char ALPHABET[] = {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'};

int compute_score(string word);

int main(void)
{
    // Get input words from both players
    string word1 = get_string("Player 1: ");
    string word2 = get_string("Player 2: ");

    // Score both words
    int score1 = compute_score(word1);
    int score2 = compute_score(word2);


    // TODO: Print the winner
    if (score1 > score2)
    {
        printf("Player 1 wins!\n");
    }
    else if (score1 < score2)
    {
        printf("Player 2 wins!\n");
    }
    else
    {
        printf("Tie!\n");
    }
}


// Use two arrays for comparison
int compute_score(string word)
{
    int score = 0;
    int len = strlen(word);
    for (int i = 0 ; i < len; i++)
    {
        // pack a char from word[i]
        if (islower(word[i]))
        {
            int word_char_num = (int) word[i];
            char word_char = word_char_num - 32; // Convert char to uppercase for comparison
            for (int m = 0; m < 26; m++) // m is used to compare through all alphabet
            {
                if (word_char == ALPHABET[m]) // compare 1 by 1
                {
                    score += POINTS[m]; // get the point at the same location as the two arrays

                }
            }
        }
        else if (isupper(word[i]))
        {
            int word_char_num = (int) word[i];
            char word_char = word_char_num;
            for (int m = 0; m < 26; m++)
            {
                if (word_char == ALPHABET[m])
                {
                    score += POINTS[m];
                }
            }
        }
    }
    return score;
}