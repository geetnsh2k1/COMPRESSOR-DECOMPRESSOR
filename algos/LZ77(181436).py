sequence = input("Enter the sequence to be coded: ")
search_buf_length = int(input("Enter the size of search_buffer: "))
look_ahead_buf_length = int(input("Enter the size of the look ahead buffer: "))
buffer = ""
sequence_length = len(sequence)
search_buf_pos, look_ahead_buf_pos = 0, search_buf_length
encode_list = []

def Init():
    global buffer
    buffer = sequence[search_buf_pos:search_buf_pos+search_buf_length]
    for i in buffer:
        encode_list.append([0,0,i])
    buffer += sequence[look_ahead_buf_pos:look_ahead_buf_pos+look_ahead_buf_length]

def MoveForward(step):
    global search_buf_pos, look_ahead_buf_pos, buffer
    print("mf :", buffer)
    search_buf_pos += step; look_ahead_buf_pos += step
    buffer = sequence[search_buf_pos:search_buf_pos+search_buf_length+look_ahead_buf_length]

def Encode():
    print(buffer)
    sym_offset = search_buf_length
    max_length, max_offset, next_sym = 0, 0, buffer[sym_offset]
    buffer_length = len(buffer)
    if buffer_length - sym_offset == 1:
        encode_list.append([0,0,next_sym])
        return max_length
    for offset in range(1,search_buf_length+1):
        pos = sym_offset - offset
        n = 0
        while buffer[pos + n] == buffer[sym_offset + n]:
            n += 1
            if n == buffer_length - search_buf_length - 1: break
        if max_length < n:
            max_length = n
            max_offset = offset
            next_sym = buffer[sym_offset+n]
    encode_list.append([max_offset, max_length, next_sym])
    return max_length

def LZ77():
    while 1:
        step = Encode() + 1
        MoveForward(step)
        if look_ahead_buf_pos >= sequence_length: break
#Main Encode
Init()
LZ77()
for i in encode_list:
    print(i)

def Decode(encode_lise):
    ans = ''
    for i in encode_list:
        offset, length, sym = i
        for j in range(length):
            ans += ans[-offset]
        ans += sym
    return ans

# Main decode
print(Decode(encode_list))
