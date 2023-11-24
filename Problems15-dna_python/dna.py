import csv
import sys


def main():

    # TODO: Check for command-line usage
    if len(sys.argv) != 3:
        sys.exit("Usage: python dna.py data.csv sequence.txt")

    # Get the file from folders
    # In terminal: python dna.py databases/small.csv sequences/1.txt
    data_csv = sys.argv[1]
    sequence_txt = sys.argv[2]

    list_of_column = []
    list_of_dict = []
    subsequence_list = []
    match_person = None

    # TODO: Read database file into a variable
    # Using .reader() to make a list of column
    with open(f"{data_csv}", "r") as database:
        database_reader = csv.reader(database)
        # Get the first line in csv file
        for row in database_reader:
            list_of_column.append(row)
            # just add 1 line then break the loop
            break

    # Using .DictReader() to make a list of dictionary
    with open(f"{data_csv}", "r") as database:
        data_dict = csv.DictReader(database)
        for item in data_dict:
            # item would be like:
            # [{'name': 'Alice', 'AGATC': '2', 'AATG': '8', 'TATC': '3'}, {'name': 'Bob', 'AGATC': '4', 'AATG': '1', 'TATC': '5'}...]
            list_of_dict.append(item)

        # Get all the subsequence(depends on how many STR in .csv)
        # Subsequence is (e.g AGATC,AATG,TATC)
        # Using the column items to make a list
        how_many_subsequence = len(list_of_column[0]) - 1
        for i in range(how_many_subsequence):
            subsequence = list_of_column[0][i+1]
            subsequence_list.append(subsequence)
        # print(subsequence_list)

    # TODO: Read DNA sequence file into a variable
    # DNA sequence = (AAGGTAAGTTTAGAATATAAAAGGTGAGTTAAATAGAATAGGTTAAAATTAAAGGAGAT....)
    # As a strings
    with open(f"{sequence_txt}", "r") as sequence:
        sequence_reader = sequence.read()
        # print(sequence_reader)

    # TODO: Find longest match of each STR in DNA sequence
    # STR = Short Tandem Repeat
    # 1 for loop: Get the person data e.g{'name': 'Alice', 'AGATC': '2', 'AATG': '8', 'TATC': '3'}
    # 2 for loop: Check the STR(e.g 'AGATC') 1 by 1, if match, counter += 1, if not then pass

        # person_dict is a single dict by person{'name': 'Alice', 'AGATC': '2', 'AATG': '8', 'TATC': '3'}
        for person_dict in list_of_dict:

            # If the match_counter == Num of type of STR(csv column)
            # that person DNA matched
            match_counter = 0

    # TODO: Check database for matching profiles

            # We want to get a number of longest match of some kind like "AGATC" here
            # The i is a subsequence(e.g "AGATC")
            for i in subsequence_list:

                # Get the STR num from the person
                num_of_STR = int(person_dict[i])

                # Call the longest_match function
                # It will return the longest match of (something like "AGATC") = 4
                # It means Repeated 4 times in a row ("AGATCAGATCAGATCAGATC") in the DNA
                longest_match_check = longest_match(sequence_reader, i)

                # Compare the person num and the longest_match
                if num_of_STR == longest_match_check:
                    match_counter += 1

            # If all STR match, found the person
            if match_counter == len(subsequence_list):
                match_person = person_dict['name']

    # Return the result
    if match_person != None:
        print(match_person)
    else:
        print("No match")

    return


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()