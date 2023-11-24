# TODO

def main():

    # Using try and except to check user input data type
    # it mush be a number, if not go back to main() and ask another input
    try:
        # Get a number from user and convert it to int
        height = int(input("Height: "))
    except ValueError:
        print("Please Enter number 1-8")
        # go back to top and run the program at the beginning
        main()

    # At least 1 layer, No more than 8
    # if less than 1 or more than 8
    # go back to top and run the program at the beginning
    if (height < 1 or height > 8):
        main()

    # If user input is correct, make the Pyramids
    else:
        brick_loops(height)


def brick_loops(height):
    # Here are modifiable parameters to maintain flexibility
    space = 1
    mid_space = 2
    hash_1 = 1
    hash_2 = 1

    while height > 0:
        space = height-1

        print((space * " ") + (hash_1 * "#") + (mid_space * " ") + (hash_1 * "#"))

        height -= 1
        hash_1 += 1
        hash_2 += 1


if __name__ == "__main__":
    main()