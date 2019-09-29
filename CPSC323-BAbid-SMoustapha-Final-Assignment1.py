"""
CPSC 232 Compilers Project 1
Members:
Abid Bakhtiyar
Moustapha Said
"""
keywords = ["int", "float", "bool", "if", "else", "then", "do", "while", "whileend", "do", "doend", "for", "and", "or",
            "function"]  # lists of key values that will be used
# to identify the token
separator = ['\'', '(', ')', '{', '}', '[', ']', ',', '.', ':', ';', '!']
operators = ['*', '+', '-', '=', '/', '>', '<', '%']

#             char      num      "!"     sep     "."     op     "\n"
# new            1        2        4       0       0      0       0
# string         1        1        4       0       0      0       0
# int            5        2        4       0       3      0       0
# float          5        3        4       0       5      0       0
# comment        4        4        0       4       4      4       4
# invalid         0        0        0       0       0      0       0

statetable = [
    # state table that traverses through current states[rows] and passed char states [column]
    [1, 2, 4, 0, 0, 0, 0],
    [1, 1, 4, 0, 0, 0, 0],
    [5, 2, 4, 0, 3, 0, 0],
    [5, 3, 4, 0, 5, 0, 0],
    [4, 4, 0, 4, 4, 4, 4],
    [0, 0, 0, 0, 0, 0, 0]

]


def testChar(char, state):
    # tests what the current state is and what the passed character state is to find what what should be retrieved
    # from the state table
    currState = state
    if char.isalpha():  # checks for alphabetic characters
        currState = statetable[currState][0]
        return currState

    elif char.isdigit() or (char == "$"):  # checks for a digit or a $
        currState = statetable[currState][1]
        return currState
    elif char == "!":  # checks check for "!"
        currState = statetable[currState][2]
        return currState
    elif char == ".":  # checks for "."
        currState = statetable[currState][4]
        return currState
    elif char.isspace():  # checks if the character is a " "
        currState = statetable[currState][6]
        return currState
    else:
        if (char in operators) or (
                char.isspace()):  # searches if character is an operator or its a space
            currState = statetable[currState][5]
            return currState
        elif (char in separator) or (
                char.isspace()):  # checks if character is a separator or its a space
            currState = statetable[currState][3]
            return currState


def showTemp(temp, output):  # Decides if token is an integer or float
    if temp != "":  # If our temp is blank, consider it a space
        is_float = False  # checks if it's a float or integer
        if temp in keywords:  # if our temp word is inside the list of keywords, then write into the output file
            output.write(temp + "    =     keyword\n")
            return
        is_keyword = True

        if (temp[0].isalpha()) and (
                is_keyword):  # if the first letter of our temp word is a alphabetical character and we had
            # already determine if its a keyword, then now we check if it is an identifier
            output.write(temp + "    =     identifier\n")
            return

        for a in temp:  # checks if temp word has a "." meaning it has to be a float
            if a == ".":
                is_float = True

        if not is_float:  # if not a float it has to be an integer
            output.write(temp + "    =     Integer\n")
            return

        elif is_float:  # if it has decimal it is a float
            output.write(temp + "    =     Float\n")
            return

        output.write(temp + "    =     Invalid\n")  # base case
        return


def showChar(char, output):  # decides with char is operator or separator
    temp = char
    if char in operators:  # checks if our character is in the list of operators
        output.write(temp + "    =     Operator\n")
    if char in separator:  # checks if our character is in the list of separators
        output.write(temp + "    =     Seperator\n")


def main():
    with open('SampleInputFile.txt', 'r') as file:
        # opens a text file and saves its data as file. MUST CHANGE TEXT FILE IF TESTING WITH
        # DIFFERENT FILE TYPE

        temp = " "
        currState = 0

        output = open("output.txt", "w+")  # creates an output file
        data = file.read()
        sentences = data.splitlines()  # parses data into a list of sentences
        for sen in sentences:  # puts list of sentences into a single sentence
            for a in range(len(sen)):  # Parses the sentence into individual chars
                char = sen[a]
                if currState != 4:  # make sure the current state is not a comment
                    currState = testChar(char, currState)
                    if currState == 0:
                        showTemp(temp, output)
                        showChar(char, output)
                        temp = ""

                    elif currState == 1 or currState == 2 or currState == 3:
                        # our current states allows us to add a character to our word
                        temp += char

                    elif currState == 4:  # our current state checks what temp is
                        showTemp(temp, output)
                        temp = ""

                    elif currState == 5:  # checks if we get an invalid word
                        showTemp(temp, output)
                        showChar(char, output)
                        temp = ""

                elif (char == "!") and (currState == 4):
                    currState = statetable[currState][2]

    showTemp(temp, output)
    output.close()  # closes output file
    print("lexeme               token")
    print("---------------------------")

    with open("output.txt", "r") as export:  # opens output file to be displayed
        read_data = export.read()
        print(read_data)


if __name__ == "__main__":
    main()
