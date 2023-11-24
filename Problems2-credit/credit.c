#include <cs50.h>
#include <stdio.h>

int main(void)
{
    long n = get_long("Number: ");
    long card_type_num = n;
    string card_type = "\n";
    long digit_length_check = n;
    int digit_length = 0;
    bool card_type_invalid = false;
    int last_num = 0;
    int seccond_to_last_num = 0;


    // Check card digits length
    while (digit_length_check > 0)
    {
        digit_length += 1;
        digit_length_check = digit_length_check / 10;
    }


    // Check credit card type
    // Get first 2 digits
    while (card_type_num > 99)
    {
        // Keeping update until only first 2 digits remain
        card_type_num = card_type_num / 10;
    }
    // Because VISA is 4, so need to check for single digit
    // Return Card type
    // VISA
    if ((card_type_num >= 40 && card_type_num < 50) && (digit_length == 13 || digit_length == 16))
    {
        card_type = "VISA\n";
        // printf("%s", card_type);
    }
    // Check  AMEX or MASTERCARD or INVALID
    // MASTERCARD
    else if ((card_type_num >= 51 && card_type_num < 56) && (digit_length == 16))
    {
        card_type = "MASTERCARD\n";
    }
    // AMEX
    else if ((card_type_num == 34 || card_type_num == 37) && (digit_length == 15))
    {
        card_type = "AMEX\n";
    }
    // INVALID
    else
    {
        card_type = "INVALID\n";
        card_type_invalid = true;
        printf("%s", card_type);
    }


    // When card type checked and pass, go to next step
    if (card_type_invalid == false)
    {
        // Check checksum when the card type is correct
        while (n > 0)
        {
            // get Last number
            int i = n % 10;
            // Calculations, add all numbers
            last_num += i;
            // update n and remove the last number (i)
            n = (n - i) / 10;

            // get Second-to-last number
            int j = n % 10;
            // Calculations, multiply by 2
            int k = j * 2;
            // If the number greater than 10, Add the two numbers together e.g(12 => 1 + 2 = 3)
            if (k > 9)
            {
                // Get the first digit
                int first = k / 10;
                // Get the second digit
                int second = k % 10;
                k = first + second;
            }
            // update seccond_to_last_num Sum
            seccond_to_last_num += k;
            // update n and remove the last number (j)
            n = (n - j) / 10;
        }
        // Check "checksum"
        int checksum_num = seccond_to_last_num + last_num;
        // Check if the last digit is 0
        int checksum = checksum_num % 10;


        // Return the result to user
        if (checksum == 0)
        {
            printf("%s", card_type);
        }
        else
        {
            printf("INVALID\n");
        }


    }
}


