def compress(data):
    dictionary, word = {0: ''}, 0
    dynamic_dictionary = lambda dictionary, key: dictionary.get(key) or dictionary.__setitem__(key,
                                                                                               len(dictionary)) or 0
    return [token for char in data for token in [(word, char)] for word in [dynamic_dictionary(dictionary, token)] if
            not word] + [(word, '')]


def decompress(data):
    dictionary, j = {0: ''}, ''.join
    dynamic_dictionary = lambda dictionary, value: dictionary.__setitem__(len(dictionary), value) or value
    return j([dynamic_dictionary(dictionary, dictionary[codeword] + char) for (codeword, char) in data])

data = input("Enter the sequence to be encoded: ")
compress_data = compress(data)
print(compress_data)
decompress_data = decompress(compress_data)
print('COMPRESSING:', compress_data)
print('DECOMPRESSING:', decompress_data)
