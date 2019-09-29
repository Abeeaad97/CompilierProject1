keywords = ["int", "float", "bool", "if", "else", "then", "do", "while", "whileend", "do", "doend", "for", "and", "or",
            "function"]  # lists of key values that will be used
# to identify the token
separator = ['\'', '(', ')', '{', '}', '[', ']', ',', '.', ':', ';', '!', ' ']
operators = ['*', '+', '-', '=', '/', '>', '<', '%', ]

#             char      num      "!"     sep     "."     op     "\n"
# new            1        2        4       0       0      0       0
# string         1        1        4       0       0      0       0
# int            5        2        4       0       3      0       0
# float          5        3        4       0       5      0       0
# comment        4        4        0       4       4      4       4
# invalid         0        0        0       0       0      0       0

statetable = [  # state table that uses coordinates of current states[rows] and passed character state[columns]
    [1, 2, 4, 0, 0, 0, 0],
    [1, 1, 4, 0, 0, 0, 0],
    [5, 2, 4, 0, 3, 0, 0],
    [5, 3, 4, 0, 5, 0, 0],
    [4, 4, 0, 4, 4, 4, 4],
    [0, 0, 0, 0, 0, 0, 0]

]


def testChar(char, state):
    # A series of tests that checks what the current state is and what the passed character state
    # is to determine what coordinates should be retrieved from the state table
    currentState = state
    # print("currentState is: ", currentState)
    if char.isalpha():  # checks if the character is a alphabetical character
        currentState = statetable[currentState][0]
        return currentState

    elif char.isdigit() or (char == "$"):  # checks if the character is a digit or a $
        currentState = statetable[currentState][1]
        return currentState
    elif char == "!":  # checks if the character is a "!"
        currentState = statetable[currentState][2]
        return currentState
    elif char == ".":  # checks if the character is a "."
        currentState = statetable[currentState][4]
        return currentState
    elif char.isspace():  # checks if the character is a " "
        currentState = statetable[currentState][6]
        return currentState
    else:
        if (char in operators) or (
                char.isspace()):  # checks if the character is in the operator list or a space
            currentState = statetable[currentState][5]
            return currentState
        elif (char in separator) or (
                char.isspace()):  # checks if the character is in the separator list or a space
            currentState = statetable[currentState][3]
            return currentState


def showTemp(temp, output):  # This is where we will check what type of token is our temporary parsed word
    if temp != "":  # If our temp is blank, then ignore everything and consider as a space and do nothing
        # is_keyword = False  # bool phrase that will keep track if the word is a keyword or an identifier
        is_float = False  # bool phrase that will keep track if the word is an integer or a float
        # print("temp here is: ", temp)
        if temp in keywords:  # if our temp word is inside the list of keywords, then write into the output file that
            # it is a keyword
            #   print("Keyword")
            output.write(temp + "    =     keyword\n")
            return
        is_keyword = True

        if (temp[0].isalpha()) and (
                is_keyword):  # if the first letter of our temp word is a alphabetical character and we had
            # already determine if its a keyword, then now we check if it is an identifier
            output.write(temp + "    =     identifier\n")
            return

        for a in temp:  # checking to see of the temp word has a period which would indicate that it is no longer a
            # digit
            if a == ".":
                is_float = True

        if not is_float:  # if our temp word has no decimal, that it cannot be a float but a digit
            output.write(temp + "    =     Integer\n")
            return

        elif is_float:  # if our temp word has a decimal, than it cannot be digit but a float
            output.write(temp + "    =     Float\n")
            return

        output.write(temp + "    =     Invalid\n")  # if all tests above failed, then the word is an invalid word
        return


def showChar(char, output):  # Checks if our single character is a operator or a separator
    temp = char
    if char in operators:  # checks if our character is in the list of operators
        output.write(temp + "    =     Operator\n")
    if char in separator:  # checks if our character is in the list of separators
        output.write(temp + "    =     Seperator\n")


def main():
    with open('SampleInputFile2.txt',
              'r') as file:  # opens a text file and saves its data as file. MUST CHANGE TEXT FILE IF TESTING WITH
        # DIFFERENT FILE TYPE

        temp = " "
        # char = " "
        currentstate = 0

        output = open("output.txt", "w+")  # creates an output file that will store the token and lexeme
        data = file.read()
        sentencesbank = data.splitlines()  # parses data into a list of sentences
        for sentences in sentencesbank:  # parses list of sentences into single sentences
            #   print(sentences)
            for a in range(len(sentences)):  # parses single sentence into characters
                #      print("a is: ", a)
                char = sentences[a]
                #     print("char is now: ", char)
                #    print("currentstate is: ", currentstate)
                if currentstate != 4:  # checks if our current state isn't a comment block
                    currentstate = testChar(char, currentstate)
                    #       print("new current state is: ", currentstate)
                    if currentstate == 0:
                        showTemp(temp, output)
                        showChar(char, output)
                        temp = ""

                    elif currentstate == 1 or currentstate == 2 or currentstate == 3:  # our current states allows us
                        # to add the character into our temporary word
                        temp += char
                    #          print("in state 1 2 3 and temp is: ", temp)

                    elif currentstate == 4:  # our current state checks what temp is
                        showTemp(temp, output)
                        #         print("tmep is: ", temp)
                        #        print("here in state 4")
                        temp = ""

                    elif currentstate == 5:  # checks if we get an invalid word
                        showTemp(temp, output)
                        showChar(char, output)
                        temp = ""

                elif (char == "!") and (currentstate == 4):
                    currentstate = statetable[currentstate][2]
                #       print("current state is now :", currentstate)

    showTemp(temp, output)
    # temp = " "
    output.close()  # closes output file
    print("lexeme               token")
    print("---------------------------")

    with open("output.txt", "r") as export:  # opens output file to be displayed
        read_data = export.read()
        print(read_data)


if __name__ == "__main__":
    main()
