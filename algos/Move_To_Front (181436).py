def movetofront(string):
    alphabet = list()
    init = 97
    encode = list()
    str_lst = list(string)
    for i in range(26):
        alphabet.append(chr(init))
        init = init + 1
    for i in range(len(str_lst)):
        for j in range(len(alphabet)):
            if str_lst[i] == alphabet[j]:
                encode.append(j)
                alphabet.insert(0, alphabet[j])
                del alphabet[j + 1]
                # print(alphabet)
    print(encode)

string = input("Enter the string: ")
movetofront(string)
