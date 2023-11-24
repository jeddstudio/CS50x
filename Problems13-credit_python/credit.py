# TODO

user_input = input("Number: ")

card_num = int(user_input)
card_type = None
card_type_invalid = False
card_start_num = int(user_input[0]+user_input[1])


# Check card digits length
digit_length = len(user_input)


# Check Card Type
# Visa uses 13- and 16-digit numbers, Visa numbers start with 4
# MasterCard uses 16-digit numbers, MasterCard numbers start with 51, 52, 53, 54, or 55
# American Express uses 16-digit numbers, All American Express numbers start with 34 or 37

# VISA
if (user_input[0] == "4") and (digit_length == 13 or digit_length == 16):
    card_type = "VISA"

# MASTERCARD
elif (card_start_num >= 51 or card_start_num < 56) and (digit_length == 16):
    card_type = "MASTERCARD"

# AMEX
elif (card_start_num == 34 or card_start_num == 37) and (digit_length == 15):
    card_type = "AMEX"

else:
    card_type = "INVALID"
    card_type_invalid = True
    print(card_type)


# Checksum
# Using Luhn’s Algorithm
if card_type_invalid == False:

    luhn_num = 0
    # counter for the loop
    length_counter = digit_length

    # grab the last number
    last_digit_position = digit_length - 1
    # grab the number that starting with the number’s second-to-last digit
    second_to_last_digit_position = last_digit_position - 1

    while length_counter > 0:
        # Step of Luhn’s Algorithm
        # sum of start from end
        sum_num_1 = int(user_input[last_digit_position])
        luhn_num = sum_num_1 + luhn_num

        # Bug prevention
        # if length_counter = 1, then the loop will keeping run, and it wfill get -1,
        # it will go back to the last number and make a bug
        if length_counter > 1:

            # Step of Luhn’s Algorithm
            # get the second-to-last digit and convert it to int
            # then multiply digit by 2
            sum_num_2 = int(user_input[second_to_last_digit_position])
            i = sum_num_2 * 2

            # if the number is double digits (e.g 6 * 2 = 12)
            # split it to 1 and 2, then add those
            if i > 9:
                first = int(i / 10)
                second = i % 10
                i = first + second

            # Step of Luhn’s Algorithm
            luhn_num = i + luhn_num

            # counter for stop the while loop
            last_digit_position -= 2
            second_to_last_digit_position -= 2
            length_counter -= 2

        # if length_counter <= 1, no need to get number anymore
        else:
            break

    # check the last number of checksum digits
    # if it is 0, card no. is Valid
    # using the.% function,
    # if the luhn_num = 80, it will be 0
    # if the luhn_num = 87, it will be 7
    checksum_last_num = luhn_num % 10

    if checksum_last_num == 0:
        print(card_type)
    else:
        print("INVALID")