#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <strings.h>
#include <string.h>
#include <stdlib.h>


int main(int argc, string argv[])
{
// Get key
    string key = argv[1];


// Nothing Input
    if (argc != 2)
    {
        printf("Usage: ./substitution KEY\n");
        return 1;
    }


// Validate Key
    // Check key length
    int key_length = 0;
    for (int i = 0; key[i] != '\0'; i++)
    {
        // Input correct
        if (islower(key[i]) || isupper(key[i]))
        {
            key_length++;
        }

        // Not alphabetic
        else if (islower(key[i]) != true || isupper(key[i]) != true)
        {
            printf("Key must only contain alphabetic characters.\n");
            return 1;
        }
    }


// Key length not correct
    if (key_length != 26)
    {
        printf("Key must contain 26 characters.\n");
        return 1;
    }


// Key charaecter Repeat
    for (int j = 0; j < strlen(key); j++)
    {
        for (int k = j + 1; k < strlen(key); k++)
        {
            if (key[j] == key[k])
            {
                return 1; // to stop the program
            }
        }
    }


// Get plaintext
    string plaintext = get_string("paintext: ");
    printf("ciphertext: "); // Put this here then Cipher result will be printed after it


// For normal position number
    string alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";


// KEY array
// Convert all characters to uppercase
// Create an array to store KEY character mapping (ASCII num)
    int key_array[strlen(key)];
    for (int k = 0; k < strlen(key); k++)
    {
        if (islower(key[k])) // if char is lowercase, switch it to uppercase
        {
            int char_num = (int) key[k];
            key_array[k] = char_num - 32; // Use ASCII to convert it to uppercase(-32), The data type is int(ASCII num)
            // printf("%c", key_array[k]);
        }
        else // If char is uppercase, just put it in KEY array
        {
            int char_num = (int) key[k];
            key_array[k] = char_num; // The data type is int(ASCII num)
            // printf("%c", key_array[k]);
        }
    }


// CIPHER array
// CIPHER array is for final result
// Create an array to store Cipher character mapping
    int ptxt_len = strlen(plaintext);
    int alp_len = strlen(alphabet);
    int cipher_array[ptxt_len];

    for (int p = 0; p < ptxt_len; p++)
    {
        if (islower(plaintext[p])) // If char is lowercase, switch to uppercase for checking with aplhabet
        {
            int ptxt_char_num = (int) plaintext[p]; // Convent plaintext char to ASCII number
            char ptxt_char = ptxt_char_num - 32; // convent plaintext char to Uppercase(-32), switch back the type to char
            for (int m = 0 ; m < alp_len; m++) // Loop though all alphabet to find the position number
            {
                if (ptxt_char == alphabet[m]) // Compare 2 char, char to char, when match,
                {
                    int plaintext_char_num = m; // Get the position number
                    // Use the position number from KEY array get the character, use ASCII number switching back it to lowercaes(+32), then convert it to char type
                    char cipher_char = key_array[m] + 32;
                    // Save the cipher char to Cipher array. e.g H will turn to J, H from plaintext[7], J from Key array[7]
                    cipher_array[p] = cipher_char;
                    printf("%c", cipher_array[p]);
                    // printf("ciphertext: %c", key[m]);
                    // printf("Character %i \n", plaintext_char_num);
                }
            }
        }
        else if (isupper(plaintext[p])) // If char is uppercase, no need to convert, because aplhabet is uppercase
        {
            for (int m = 0 ; m < alp_len; m++) // Loop though all alphabet to find the position number
            {
                if (plaintext[p] == alphabet[m]) // Compare 2 char, char to char, when match,
                {
                    int plaintext_char_num = m; // Get the position number
                    // Save the cipher char to Cipher array. e.g H will turn to J, H from plaintext[7], J from Key array[7]
                    cipher_array[p] = key_array[m];
                    printf("%c", cipher_array[p]);
                    // printf("ciphertext: %c", key[m]);
                    // printf("Character %i \n", plaintext_char_num);
                }
            }
        }
        else // If not uppercase or lowercase, just put it into cipher_array
        {
            cipher_array[p] = plaintext[p];
            printf("%c", cipher_array[p]);
        }
    }
    printf("\n");

}
