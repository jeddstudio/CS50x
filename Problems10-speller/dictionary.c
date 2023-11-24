// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>

#include "dictionary.h"

// new import
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
// for strcasecmp()
#include <cs50.h>
#include <strings.h>


// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// TODO: Choose number of buckets in hash table
// Why 676? because "aa, ab, ac..." is 0-25. "ba, bb, bc..." is 26-51, 26*26=676
// Finally, it can't set to 676, I think it might be a some memory issue,
// 676 is faster but it has make many empty array, and maybe that's the reason of "free memory errors"
// So, use the "N = 26" and "% N"(hash function) method
const unsigned int N = 26;

// for the Size function
unsigned int lib_counter;

// Hash table
node *table[N];




// Check Function
////////////////////////////////////////////////////////////////////////////////////////////////
// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // TODO
    int check_arr_num = hash(word);
    node *cursor = table[check_arr_num];

    // Using loop to go through linked list
    while (cursor != NULL)
    {
        // if found the word, return true
        if (strcasecmp(word, cursor->word) == 0)
        {
            return true;
        }
        else
        {
            // move the cursor to the next node
            cursor = cursor->next;
        }
    }
    return false;
}
////////////////////////////////////////////////////////////////////////////////////////////////




// Hash Function
////////////////////////////////////////////////////////////////////////////////////////////////
// Hashes word to a number
unsigned int hash(const char *word)
{
    int word_length = strlen(word);
    int hash_n = 0;
    if (word_length > 1)
    {
        // TODO: Improve this hash function
        // return toupper(word[0]) - 'A';
        int first_letter = toupper(word[0]) - 'A';
        int second_letter = toupper(word[1]) - 'A';
        // third_letter = toupper(word[2]) - 'A';

        // "aa, ab, ac..." is 0-25. "ba, bb, bc..." is 26-51
        // so first letter a = 0-25, b = 26-51, c = 52-77
        // use the basic array 0=a, 1=b, 2=c, then + second letter, it will be find the 2 letter array
        // if the word is "boy", b = 1*26 =26, o = 14, then 26 + 14 = 40
        hash_n = (first_letter * 26) + second_letter;
    }
    else
    {
        // When the word has only 1 char, just return a number
        hash_n = toupper(word[0]) - 'A';
    }
    return hash_n % N;
}
////////////////////////////////////////////////////////////////////////////////////////////////




// Load Function
///////////////////////////////////////////////////////////////////////////////////
// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // TODO
    // 1. Open dictionary file
    // Standard code for open file from manual.cs50.io
    FILE *file = fopen(dictionary, "r");
    if (file != NULL)
    {
        // char *dic_word = malloc(sizeof(dic_word));
        char dic_word[LENGTH + 1];

        // 2. Read strings from file one at a time
        while (fscanf(file, "%s", dic_word) != EOF)
        {
            // 3. Create a new node for each word
            node *n = malloc(sizeof(node));

            // standard code for return when error
            if (n == NULL)
            {
                return 1;
            }
            // put the word from dictionary to node
            strcpy(n->word, dic_word);
            // new node pointer is NULL
            // set the next pointer, because don't know where should it points to, so set it to NULL
            n->next = NULL;

            // 4. Hash word to obtain a hash value
            // it will return one int 0-25(A-Z) for sort in table
            unsigned hash_code = hash(dic_word);

            // 5. Insert node into hash table at that location
            // The importance of order
            // this code from Class on Youtube [01:10:09]- Linked List Demonstration
            // in my notes CS50 - 048
            n->next = table[hash_code];
            table[hash_code] = n;
            lib_counter++;
        }
    }
    // if file == NULL
    else
    {
        return false;
    }
    // close the file when the job is done
    fclose(file);
    return true;
}
////////////////////////////////////////////////////////////////////////////////////////////////




// Size Function
////////////////////////////////////////////////////////////////////////////////////////////////
// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    if (lib_counter != 0)
    {
        return lib_counter;
    }
    return 0;
}
////////////////////////////////////////////////////////////////////////////////////////////////




// Unloads Function
////////////////////////////////////////////////////////////////////////////////////////////////
// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // TODO
    // This method come from Linked Lists Short Youtube
    // in my note Linked Lists
    for (int i = 0; i < N; i++)
    {
        node *del_cursor = table[i];
        while (del_cursor != NULL)
        {
            node *tmp = del_cursor;
            del_cursor = del_cursor->next;
            free(tmp);
        }
        if (del_cursor == NULL)
        {
            return true;
        }
    }
    return false;
}
////////////////////////////////////////////////////////////////////////////////////////////////