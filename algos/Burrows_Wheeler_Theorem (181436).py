def burrows_wheeler_theorem(string):
    words = list(string)
    encode = []
    for i in range(len(words)):
        word = string[-1] + string[:-1]
        new = ''.join(word)
        string = new
        encode.append(new)
    sort = sorted(encode)
    print(sort)
    for i in range(len(words)):
        element = sort[i]
        last = element[- 1]
        print(last)

string = input("Enter the string: ")
burrows_wheeler_theorem(string)
