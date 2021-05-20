from dahuffman import HuffmanCodec
from string import ascii_lowercase
import math
from tkinter import *
from tkinter.filedialog import askopenfile
from PIL import Image, ImageTk
from os import system
from subprocess import Popen
from time import sleep
import os

color = "#20bebe"
LARGEFONT = ("Montserrat-Medium", 25, "bold")
BUTTONFONT = ("Montserrat-Medium", 12)
logoPath = "./graphics/logo-small.png"
faviconPath = "./graphics/favicon.ico"
btnbg = "#ffffff" 
default = "./Output/"

select = None
###################################################################

def AC_COMPRESS(file):
    name = file.name.split("/")[-1]
    singal = file.readline().strip()
    singal_dict = {}
    for i in file:
        x = i
        char = i[0]
        temp = i[2:]
        temp = list(temp.split(","))
        singal_dict[char] = tuple([float(temp[0].strip()),float(temp[1].strip())])
    
        
    Low = 0
    High = 1
    for s in singal:
        CodeRange = High - Low
        High = Low + CodeRange * singal_dict[s][1]
        Low = Low + CodeRange * singal_dict[s][0]

    with open(default+"compressed_ac_"+name, "w") as fw:
        fw.write(str(Low)+"\n"+str(singal_dict)+"\n"+str(len(singal)))

    return default+"compressed_ac_"+name

def AC_DECOMPRESS(file):
    name = file.name.split("/")[-1]
    temp = file.read().split("\n")
    encoded_number, singal_dict, singal_length = eval(temp[0]),eval(temp[1]),eval(temp[2])
    singal = []
    while singal_length:
        for k, v in singal_dict.items():
            if v[0] <= encoded_number < v[1]:
                singal.append(k)
                range = v[1] - v[0]
                encoded_number -= v[0]
                encoded_number /= range
                break
        singal_length -= 1
    singal = "".join(singal)

    with open(default+"decompressed_ac_"+name, "w") as fw:
        fw.write(str(singal))

    return default+"decompressed_ac_"+name

 ###################################################################
"""
def MOVE_TO_FRONT_COMPRESS(file):
    name = file.name.split("/")[-1]
    strng = file.read()
    
    symboltable = list(ascii_lowercase)
    
    sequence, pad = [], symboltable[::]
    for char in strng:
        indx = pad.index(char)
        sequence.append(indx)
        pad = [pad.pop(indx)] + pad
    
    with open(default+"compressed_move_to_front_"+name, "w") as fw:
        fw.write(str(sequence))

    return default+"compressed_move_to_front_"+name

def MOVE_TO_FRONT_DECOMPRESS(file):
    name = file.name.split("/")[-1]
    sequence = eval(file.read())
    
    symboltable = list(ascii_lowercase)
    
    chars, pad = [], symboltable[::]
    for indx in sequence:
        char = pad[indx]
        chars.append(char)
        pad = [pad.pop(indx)] + pad
    data = ''.join(chars)

    with open(default+"decompressed_move_to_front_"+name, "w") as fw:
        fw.write(data)

    return default+"decompressed_move_to_front_"+name
"""

def LZW_COMPRESS(file):
    name = file.name.split("/")[-1]
    uncompressed = file.read().strip()
    dict_size = 256
    dictionary = dict((chr(i), i) for i in range(dict_size))
    w = ""
    result = []
    for c in uncompressed:
        wc = w + c
        if wc in dictionary:
            w = wc
        else:
            result.append(dictionary[w])
            dictionary[wc] = dict_size
            dict_size += 1
            w = c
    if w:
        result.append(dictionary[w])
    
    with open(default+"compressed_lzw"+name, "w") as fw:
        fw.write(str(result))
    return default+"compressed_lzw"+name

def LZW_DECOMPRESS(file):
    name = file.name.split("/")[-1]
    
    compressed = eval(file.read())
    from io import StringIO
    dict_size = 256
    dictionary = dict((i, chr(i)) for i in range(dict_size))
    result = StringIO()
    w = chr(compressed.pop(0))
    result.write(w)
    for k in compressed:
        if k in dictionary:
            entry = dictionary[k]
        elif k == dict_size:
            entry = w + w[0]
        else:
            raise ValueError('Bad compressed k: %s' % k)
        result.write(entry)
        dictionary[dict_size] = w + entry[0]
        dict_size += 1
        w = entry
    
    with open(default+"decompressed_lzw_"+name, "w") as fw:
        fw.write(str(result.getvalue()))
    return default+"decompressed_lzw_"+name

def LZ78_COMPRESS(file):
    name = file.name.split("/")[-1]
    text_from_file = file.read().strip()
    dict_of_codes = {text_from_file[0]: '1'}
    string = '0' + text_from_file[0]
    text_from_file = text_from_file[1:]
    combination = ''
    code = 2
    for char in text_from_file:
        combination += char
        if combination not in dict_of_codes:
            dict_of_codes[combination] = str(code)
            if len(combination) == 1:
                string += '0' + str(combination)
            else:
                string += str(dict_of_codes[combination[0:-1]]) + str(combination[-1])
            code += 1
            combination = ''
    
    with open(default+"compressed_lz78_"+name, "w") as fw:
        fw.write(str(string))

    return default+"compressed_lz78_"+name

def LZ78_DECOMPRESS(file):
    name = file.name.split("/")[-1]
    
    text_from_file = file.read().strip()
    dict_of_codes = {'0': '', '1': text_from_file[1]}
    string = str(dict_of_codes['1'])
    text_from_file = text_from_file[2:]
    combination = ''
    code = 2
    for char in text_from_file:
        if char in '1234567890':
            combination += char
        else:
            dict_of_codes[str(code)] = dict_of_codes[combination] + char
            string += str(dict_of_codes[combination] + char)
            combination = ''
            code += 1

    with open(default+"decompressed_lz78_"+name, "w") as fw:
        fw.write(str(string))
    
    return default+"decompressed_lz78_"+name

"""
def BURROWS_WHEELER_COMPRESS(file):
    name = file.name.split("/")[-1]
    text = file.read().strip()
    L = ''
    F = ''
    last_str = text
    len_text = len(text)
    rotate_list = []
    rotate_list.append(last_str)
    for i in range(len_text - 1):
        last_str = last_str[-1] + last_str[-len_text:-1]
        rotate_list.append(last_str)
 
    sorted_list = sorted(rotate_list)
    for eachstr in sorted_list:
        L = L + eachstr[-1]
        F = F + eachstr[0]
        
    with open(default+"compressed_bw_"+name, "w") as fw:
        fw.write(str(L))
    
    return default+"compressed_bw_"+name

def C(c):
    global L
 
    num_Tc = 0
    for eachchr in L:
        if c > eachchr:
            num_Tc += 1
    return num_Tc - 1
 
def Occ(c,r):
    global L
    row = -1
    num_Lc = 0
    if r == 0:
        return 0
    for eachchr in L:
        row += 1
        if eachchr == c:
            num_Lc += 1
        if row == r - 1:
            break
    return num_Lc
L = ""    
def BURROWS_WHEELER_DECOMPRESS(file):
    name = file.name.split("/")[-1]
    L = eval(file.read())
    r = 0
    T = ''
 
    while L[r] != "#":
        T = L[r] + T
        c = L[r]
        r = C(c) + Occ(c, r) + 1
    print(T)
        
    with open(default+"decompressed_bw_"+name, "w") as fw:
        fw.write(str(L))
    
    return default+"decompressed_bw_"+name
"""

def Init(buffer, sequence, search_buf_length, look_ahead_buf_length, search_buf_pos, look_ahead_buf_pos, encode_list):
    buffer = sequence[search_buf_pos:search_buf_pos+search_buf_length]
    for i in buffer:
        encode_list.append([0,0,i])
    buffer += sequence[look_ahead_buf_pos:look_ahead_buf_pos+look_ahead_buf_length]
    return buffer, encode_list

def MoveForward(step, sequence, search_buf_length, look_ahead_buf_length, search_buf_pos, look_ahead_buf_pos, buffer):
    search_buf_pos += step 
    look_ahead_buf_pos += step
    buffer = sequence[search_buf_pos:search_buf_pos+search_buf_length+look_ahead_buf_length]
    return buffer, search_buf_pos, look_ahead_buf_pos

def LZ77_SHIT_Encode(buffer, search_buf_length, encode_list):
    sym_offset = search_buf_length
    max_length, max_offset, next_sym = 0, 0, buffer[sym_offset]
    buffer_length = len(buffer)
    if buffer_length - sym_offset == 1:
        encode_list.append([0,0,next_sym])
        return max_length, buffer, search_buf_length, encode_list
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
    return max_length, buffer, search_buf_length, encode_list

def LZ77_COMPRESS(file):
    name = file.name.split("/")[-1]
    
    sequence = file.readline().strip()
    search_buf_length = int(file.readline())
    look_ahead_buf_length = int(file.readline())
    sequence_length = len(sequence)
    search_buf_pos, look_ahead_buf_pos = 0, search_buf_length
    encode_list = []
    buffer = ""
    buffer, encode_list = Init(buffer, sequence, search_buf_length, look_ahead_buf_length, search_buf_pos, look_ahead_buf_pos, encode_list)
    while 1:
        step, buffer, search_buf_length, encode_list = LZ77_SHIT_Encode(buffer, search_buf_length, encode_list)
        step += 1
        buffer, search_buf_pos, look_ahead_buf_pos = MoveForward(step, sequence, search_buf_length, look_ahead_buf_length, search_buf_pos, look_ahead_buf_pos, buffer)
        if look_ahead_buf_pos >= sequence_length: break
    
    with open(default+"compressed_lz77_"+name, "w") as fw:
        fw.write(str(encode_list))
    
    return default+"compressed_lz77_"+name

def LZ77_DECOMPRESS(file):
    name = file.name.split("/")[-1]
    
    encode_list = eval(file.read())
    ans = ''
    for i in encode_list:
        offset, length, sym = i
        for j in range(length):
            ans += ans[-offset]
        ans += sym
    with open(default+"decompressed_lz77_"+name, "w") as fw:
        fw.write(str(ans))
    
    return default+"decompressed_lz77_"+name

def bin_fix(num, k):
    bin_cd = bin(num)
    return bin_cd[2:].zfill(k)

def BINRLE_COMPRESS(file):
    name = file.name.split("/")[-1]
    string = file.readline().strip()
    k = int(file.readline())
    
    count_list = []
    listc = [i for i in string]
    count = 0
    i = 0
    previous_character = listc[0]
    while (i <= len(listc) - 1):
        while (listc[i] == previous_character):
            i = i + 1
            count = count + 1
            if i > len(listc) - 1:
                break
        x = [previous_character, count]
        count_list.append(x)
        if i > len(listc) - 1:
            break
        previous_character = listc[i]
        count = 0
    max_bits = ((2**k) - 1)
    encode = ""
    for i in range(len(count_list)):
        if count_list[i][0] == '0':
            if count_list[i][1] < max_bits:
                code = bin_fix(count_list[i][1], k)
                encode = encode + code
            else:
                this = count_list[i][1]
                while(this != 0):
                    if this > max_bits:
                        code = bin_fix(max_bits, k)
                        encode = encode + code
                        this = this - max_bits
                    elif this == max_bits:
                        if count_list[i + 1][0] == '0':
                            code = bin_fix(max_bits, k)
                            encode = encode + code
                            this = 0
                        else:
                            code = bin_fix(max_bits, k)
                            encode = encode + code
                            encode = encode + bin_fix(0, k)
                            this = 0
                            
                    else:
                        code = bin_fix(this, k)
                        encode = encode + code
                        this = 0
        else:
            if(int(count_list[i][1]) > 1):
                for i in range(count_list[i][1]-1):
                    encode = encode + bin_fix(0, k)
    with open(default+"compressed_binrle_"+name, "w") as fw:
        fw.write(str([encode, k]))
    
    return default+"compressed_binrle_"+name

def BINRLE_DECOMPRESS(file):
    name = file.name.split("/")[-1]
    master_file = eval(file.read())
    
    encoded = master_file[0]
    k = master_file[1]
    seq_mas = []
    while encoded:
        seq_mas.append(encoded[:k])
        encoded = encoded[k:]
    decode = ""
    int_val = []
    max_bits = ((2 ** k) - 1)
    for i in range(len(seq_mas)):
        integer = int(seq_mas[i],2)
        int_val.append(integer)
    for i in range(len(int_val)):
        if int_val[i] == max_bits:
            decode = decode  + '0' * max_bits
            if int_val[i + 1] == '0':
                decode = decode + '1'
            else:
                pass
        elif int_val[i] == '0':
            decode = decode + '1'
        else:
            decode = decode + ('0' * int_val[i])
            decode = decode + '1'
    length = len(decode)
    if(int_val[-1] < 0):
        decode = decode[:length]
    elif(int_val[-1] >= 0):
        decode = decode[:length - 1]
    
        
    with open(default+"decompressed_binrle_"+name, "w") as fw:
        fw.write(str(decode))
    return default+"decompressed_binrle_"+name

def RLE_COMPRESS(file):
    name = file.name.split("/")[-1]
    
    str1 = file.read().strip()

    count = 0
    length = len(str1)
    i = 0
    final_rle = []
    rle = []
    previous_character = str1[0]
    while (i <= length - 1):
        while (str1[i] == previous_character):
            i = i + 1
            count = count + 1
            if i > length - 1:
                break
        x = [previous_character, count]
        rle.append(x)
        if i > length - 1:
            break
        previous_character = str1[i]
        count = 0
    alphabets = []
    alpha_codes = []
    rle_max = max(rle, key=lambda x: x[1])
    places_code = math.ceil(math.log(rle_max[1], 2))
    for i in range(len(rle)):
        rle[i][1] = bin_fix(rle[i][1], places_code)
    for i in range(0,len(rle)):
        a = rle[i][0]
        if a not in alphabets:
            alphabets.append(a)
    places_alpha = math.ceil(math.log(len(alphabets),2)) 
    for i in range(len(alphabets)):
        numb = bin_fix(i, places_alpha)
        alpha_codes.append([alphabets[i],numb])
    for i in range(len(rle)):
        for j in range(len(alpha_codes)):
            if alpha_codes[j][0] == rle[i][0]:
                final_rle.append((alpha_codes[j][1],rle[i][1]))
    final_rle = tuple(final_rle)
    data = [final_rle,alpha_codes]

    with open(default+"compressed_rle_"+name, "w") as fw:
        fw.write(str(data))
    
    return default+"compressed_rle_"+name

def RLE_DECOMPRESS(file):
    name = file.name.split("/")[-1]
    
    master_directory = eval(file.read())

    final_str = []
    final_strg = ''
    str1 = []
    final_rle1 = master_directory[0]
    final_rle = list(map(list,final_rle1))
    alpha_codes = master_directory[1]
    for i in range(len(final_rle)):
        for j in range(len(alpha_codes)):
            if alpha_codes[j][1] == final_rle[i][0]:
                str1.append([alpha_codes[j][0],final_rle[i][1]])
    for i in range(len(str1)):
        final_str.append([str1[i][0],int(str1[i][1],2)])
    for i in range(len(final_str)):
        for j in range(final_str[i][1]):
            final_strg = final_strg + str(final_str[i][0])
    data = final_strg

    with open(default+"decompressed_rle_"+name, "w") as fw:
        fw.write(str(data))
    
    return default+"decompressed_rle_"+name

def HFM_COMPRESS(file):
    name = file.name.split("/")[-1]
    sequence = file.readline().strip()
    dictionary = {}
    for data in file:
        data = data.split()
        dictionary[data[0]] = eval(data[1])
    codec = HuffmanCodec.from_frequencies(dictionary)
    encoded = codec.encode(sequence)
    print(type(encoded))
    with open(default+"compressed_hfm_"+name, "w") as fw:
        fw.write(str(encoded) + str("\n") + str(dictionary))
    return default+"compressed_hfm_"+name

def HFM_DECOMPRESS(file):
    name = file.name.split("/")[-1]
    encoded = eval(file.readline().strip())
    dictionary = eval(file.readline())
    codec = HuffmanCodec.from_frequencies(dictionary)
    ans = codec.decode(encoded)
    with open(default+"decompressed_hfm_"+name, "w") as fw:
        fw.write(str(ans))
    return default+"decompressed_hfm_"+name

def binary_fix(i, n):
    binary = bin(i)
    return binary[2:].zfill(n)

def TUNSTALL_COMPRESS(file):
    name = file.name.split("/")[-1]
    
    string = file.readline().strip()
    n = int(file.readline().strip())
    len_str = len(string)
    dictionary = dict()
    for i in string:
        if i in dictionary:
            dictionary[i] = dictionary[i] + 1
        else:
            dictionary[i] = 1
    alphabet = []
    probability = []
    for i in dictionary.items():
        alphabet.append(i[0])
        probability.append(i[1])
    for i in range(len(probability)):
        probability[i] = probability[i] / len_str
    N = len(alphabet)
    k = math.floor(((2 ** n) - N)/ (N - 1))
    
    alpha, prob, k, N, n, string = alphabet, probability, k, N, n, string
    
    final = []
    for i in range(N):
        final.append([alpha[i], prob[i]])
    for i in range(k):
        last = max(final, key = lambda x:x[1])
        for i in range(N):
            final.append([last[0] + alpha[i], last[1] * prob[i]])
        final.pop(final.index(last))
    for i in range(len(final)):
        final[i][1] = binary_fix(i, n)
    print("The set of alphabets and codes are: ")
    print("Alphabet\tCode")
    print("-------------------------")
    for i in range(len(final)):
        print(final[i][0], end = "\t")
        print(final[i][1])
    stri = list(string)
    encode = ""
    count = 0
    flag = 0
    for i in range(len(stri)):
        for j in range(len(final)):
            if stri[i] == final[j][0]:
                encode = encode + str(final[j][1])
                flag = 1
        if flag == 1:
            flag = 0
        else:
            count = count + 1
            if count == len(stri):
                break
            else:
                stri.insert(i + 1,str(stri[i]+stri[i + 1]))
                stri.pop(i + 2)
    
    with open(default+"compressed_tunstall_"+name, "w") as fw:
        fw.write(str([encode, final, n]))
    return default+"compressed_tunstall_"+name

def TUNSTALL_DECOMPRESS(file):
    name = file.name.split("/")[-1]
    
    makefile = eval(file.read())
    
    encode = makefile[0]
    final = makefile[1]
    n = makefile[2]    
    decode = []
    while encode:
        decode.append(encode[:n])
        encode = encode[n:]
    string = ""
    for i in range(len(decode)):
        for j in range(len(final)):
            if decode[i] == str(final[j][1]):
                string = string + final[j][0]
                
    with open(default+"decompressed_tunstall_"+name, "w") as fw:
        fw.write(str(string))
    return default+"decompressed_tunstall_"+name

def bin_code(t):
    x=[];
    if(t==0):
        return [0];
    while(t>0):
        x.append(t%2);
        t=int(t/2)
    return x

def unary(t):
    y=[];
    for i in range(t-1):
        y.append(0)
    y.append(1)
    return y

def GOLOMB_COMPRESS(file):
    name = file.name.split("/")[-1]
    
    x=int(file.readline())  
    b=int(file.readline())
    
    q=int(x/b)
    y=unary(q+1)
    r=x-(q*b)
    i=math.floor(math.log(b,2))
    d=math.pow(2,i+1)-b
    if(r>=d):
        r+=int(d)
    r2=bin_code(r)
    if(len(r2)<=i and r>=d):
        r2.append(0);
    if(len(r2)<i and r<d):
        r2.append(0) 
    r2=r2[::-1]
    y=y+r2
    
    with open(default+"compressed_golomb_"+name, "w") as fw:
        fw.write(str([y, b]))
    return default+"compressed_golomb_"+name

def g_decode(x):
    num=0;
    for i in range(len(x)):
        num+=(int(x[len(x)-1-i])*(math.pow(2,i)));
    return num;

def GOLOMB_DECOMPRESS(file):
    name = file.name.split("/")[-1]
    
    data = eval(file.read())
    
    x=str(data[0])
    x=list(x)
    b=int(data[1])
    i=math.floor(math.log(b,2))
    d=math.pow(2,i+1)-b

    rnum = 0
    p2=0;
    l=1;
    while(p2<len(x)):
        t=0;
        flag=0;
        r=[];
        k=i;
        q=0;
        for p in range(p2,len(x)):
            if(x[p]=='0' and flag==0):
                t+=1;
                continue;
            if(x[p]=='1' and flag==0):
                q=t;
                flag=1;
                continue;
            r.append(x[p]);
            k-=1;
            if(k==0):
                rnum=g_decode(r);
                if(rnum<d):
                    p2=p+1;
                    break;
            if(k==-1):
                rnum=g_decode(r);
                rnum=rnum-d;
                p2=p+1;
                break;
        ans=q*b+rnum;
        print(int(ans));
        break
        l=0;
        
    with open(default+"decompressed_golomb_"+name, "w") as fw:
        fw.write(str(ans))
    return default+"decompressed_golomb_"+name

class tkinterApp(Tk):
    
    def __init__(self, *args, **kwargs): 
        Tk.__init__(self, *args, **kwargs)
        self.title("FCDC")
        self.geometry("720x480")
        self.minsize(720, 480)
        self.maxsize(720, 350)
        
        self.iconbitmap(faviconPath)
        
        container = Frame(self) 
        container.pack(side = "top", fill = "both", expand = True) 

        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)

        self.frames = {} 

        for F in (StartPage, Page1, Page2):
            frame = F(container, self)

            self.frames[F] = frame 

            frame.grid(row = 0, column = 0, sticky ="nsew")

        self.show_frame(StartPage, slt=NONE)

    def show_frame(self, cont, slt):
        global select
        if slt != "unchange":
            select = slt
            if slt == "c_":
                cont.label_text.set("COMPRESS")
            elif slt == "d_":
                cont.label_text.set("DECOMPRESS")
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(Frame):
    name = "Start"
    def __init__(self, parent, controller): 
        Frame.__init__(self, parent)
        
        logo = Image.open(logoPath)
        logo = ImageTk.PhotoImage(logo)
        logo_label = Label(self, image=logo)
        logo_label.image = logo
        logo_label.grid(column=1, row=0, pady=50)
        
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=0)        

        button1 = Button(self, text ="COMPRESS", command = lambda : controller.show_frame(Page1,slt="c_"), bg=color, fg="white", height=2, width=20, font=BUTTONFONT)
        button1.grid(row = 1, column = 1, padx = 265, pady = 20)

        button2 = Button(self, text ="DECOMPRESS", command = lambda : controller.show_frame(Page1,slt="d_"), bg=color, fg="white", height=2, width=20,font=BUTTONFONT)
        button2.grid(row = 2, column = 1, padx = 265, pady = 20)

class Page1(Frame):
    
    def __init__(self, parent, controller):
        self.slt_algo = None
        self.ctrl = controller
        Frame.__init__(self, parent)
        Page1.label_text = StringVar()
        Page1.label_text.set("FCDC")
        
        label = Label(self, textvariable =Page1.label_text, font = LARGEFONT, fg=color)
        label.config(anchor=CENTER)
        label.grid(row = 0, column = 1, pady=25)        
        
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=0)
        
        button1 = Button(self, text ="HOME PAGE", command = lambda : controller.show_frame(StartPage, slt=None), bg=btnbg, fg=color, height=1, width=10,font=BUTTONFONT)
        button1.grid(row = 8, column = 1, padx = 6, pady = 20)

        # mtf_button = Button(self, text ="MOVE TO FRONT", command = lambda : self.open_nxt("mtf"), bg=color, fg="white", height=2, width=20, font=BUTTONFONT)
        # mtf_button.grid(row = 4, column = 0, padx = (50, 0), pady = 10)
        
        lzw_button = Button(self, text ="LZW", command = lambda : self.open_nxt("lzw"), bg=color, fg="white", height=2, width=20, font=BUTTONFONT)
        lzw_button.grid(row = 4, column = 0, padx = (50, 0), pady = 10)
        
        hfman_button = Button(self, text ="HUFFMAN", command = lambda : self.open_nxt("hfm"), bg=color, fg="white", height=2, width=20, font=BUTTONFONT)
        hfman_button.grid(row = 4, column = 1, padx = (25, 25), pady = 10)
        
        binrle_button = Button(self, text ="BINARY RLE", command = lambda : self.open_nxt("binrle"), bg=color ,fg="white", height=2, width=20, font=BUTTONFONT)
        binrle_button.grid(row = 4, column = 2, padx = (0, 50), pady = 10)
        
        lz77_button = Button(self, text ="LZ77", command = lambda : self.open_nxt("lz77"), bg=color, fg="white", height=2, width=20, font=BUTTONFONT)
        lz77_button.grid(row = 5, column = 0, padx = (50, 0), pady = 10)
        
        golomb_button = Button(self, text ="GOLOMB", command = lambda : self.open_nxt("golomb"), bg=color, fg="white", height=2, width=20, font=BUTTONFONT)
        golomb_button.grid(row = 5, column = 1, padx = (25, 25), pady = 10)
        
        # burrows_button = Button(self, text ="BURROWS WHEELER", command = lambda : self.open_nxt("bw"), bg=color, fg="white", height=2, width=20, font=BUTTONFONT)
        # burrows_button.grid(row = 6, column = 0, padx = (50, 0), pady = 10)
        
        lz78_button = Button(self, text ="LZ78", command = lambda : self.open_nxt("lz78"), bg=color, fg="white", height=2, width=20, font=BUTTONFONT)
        lz78_button.grid(row = 6, column = 0, padx = (50, 0), pady = 10)
        
        tunstall_button = Button(self, text ="TUNSTALL", command = lambda : self.open_nxt("tunstall"), bg=color, fg="white", height=2, width=20, font=BUTTONFONT)
        tunstall_button.grid(row = 6, column = 1, padx = (25, 25), pady = 10)
        
        arith_button = Button(self, text ="ARITHMATIC CODING", command = lambda : self.open_nxt("ac"), bg=color, fg="white", height=2, width=20, font=BUTTONFONT)
        arith_button.grid(row = 7, column = 0, padx = (50, 0), pady = 10)

        rle_button = Button(self, text ="RLE", command = lambda : self.open_nxt("rle"), bg=color, fg="white", height=2, width=20, font=BUTTONFONT)
        rle_button.grid(row = 7, column = 1, padx = (25, 25), pady = 10)

    def open_nxt(self, algo):
        self.slt_algo = algo
        global select
        select = select.split("_")[0]
        select += "_"+algo
        
        if select == "c_mtf":
            Page2.textbox_text1 = """1. First line in the file contains the sequence to be encoded.
For Example:
********
finisher
********"""
        elif select == "c_lzw":
            Page2.textbox_text1 = """1. First line in the file contains the sequence to be encoded.
For example
********
cabarararrarabacbabrara
********"""
        elif select == "c_binrle":
            Page2.textbox_text1 = """1. First line in the file contains the sequence to be encoded.
2. Second line in the file contains the number of bits in which the sequence is to be coded.
For example:
********
00000000000000000000111000010000101000001100000000000000000010100000
4 
********"""
        elif select == "c_lz77":
            Page2.textbox_text1 = """1. First line in the file contains the sequence to be encoded.
2. Second line in the file contains the search buffer length.
3. Third line in the filse contains the look ahead buffer length.
For example
********
cabarararrarabacbabrara
7
6
********"""
        elif select == "c_lz78":
            Page2.textbox_text1 = """1. First line in the file contains the sequence to be encoded.
For example
********
abracadabra
********"""
        elif select == "c_ac":
            Page2.textbox_text1 = """1. First line in file contains the sequence to be encoded.
2. Next n lines contain the symbols separated by space along with specific range separated by comma.
For example:
********
CABCDAC
A 0.0,0.1
B 0.1,0.5
C 0.5,0.7
D 0.7,1.0
********"""
            
        elif select == "c_bw":
            Page2.textbox_text1 = """1. First line in the file contains the sequence to be encoded.
For Example:
********
selvestyerstallone
********"""
        elif select == "c_rle":
            Page2.textbox_text1 = """II.Run Length Encoding
1. First line in the files contains the sequence to be encoded.
For example: 
********
AAAAAAAAAAAAAAAABBBBBBBBBBBBBBBBBBBBCCCCCCCCCCCCCAAAAAAAAAAACCCCCBB
********"""
        elif select == "c_hfm":
            Page2.textbox_text1 = """1. First line in the file contains the sequence to be encoded.
2. Next n lines representing n differenct characters used in the sequence with a space separated number assigned to it.
For example
********
exeneeeexniqneieini
e 100
n 20
x 1
i 40
q 3
********"""
        elif select == "c_golomb":
            Page2.textbox_text1 = """1. First line in the file contains the divident.
2. Second line in the file contains the divisor.
For Example: 
********
117
17
********"""
        elif select == "c_tunstall":
            Page2.textbox_text1 = """1. First line in the file contains the sequence to be encoded.
2. Second line in the file contains the number of bits in which the sequence is to be coded.
For example:
********
ababaaaabacacbaaa
4
********
Please Note: The bits needed for the encoding of the sequence must be greater than or equal to upper bound of number of letters in sequence ^ 0.5"""
            
        if select[0] == "d":
            Page2.textbox_text1 = "The decoding of the file is possible only if it is compressed by this appication."
        Page2.text_box1.configure(state='normal')
        Page2.text_box1.delete("1.0","end")
        Page2.text_box1.insert(1.0, Page2.textbox_text1)
        Page2.text_box1.configure(state='disabled')

        self.ctrl.show_frame(Page2, "unchange")
            
class Page2(Frame): 
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.ctrl = controller
        
        Page2.label_text = StringVar()
        Page2.label_text.set("UPLOAD FILE")
        label = Label(self, textvariable = Page2.label_text, font = LARGEFONT, fg=color)
        label.grid(row = 0, column = 2, padx = 90, pady = 10)
    
        self.browse_text = StringVar() 
        self.browse_text.set("Upload File")
        self.textbox_text = ""
        upload_file_button = Button(self, textvariable=self.browse_text, command =self.open_file, bg=color, fg="white", height=1, width=10, font=BUTTONFONT)
        upload_file_button.grid(row = 8, column = 2, padx = 6, pady = 10)

        button2 = Button(self, text ="Home Page", command = lambda : controller.show_frame(StartPage, slt=None), bg=btnbg, fg=color, height=1, width=10,font=BUTTONFONT)
        button2.grid(row = 10, column = 2, padx = 6, pady = 10)

        # text box
        global select
        Page2.textbox_text1 = "Description here"
        scrollbar = Scrollbar(self, orient=HORIZONTAL)
        Page2.text_box1 = Text(self, height=10, width=70, padx=0, pady=6, xscrollcommand=scrollbar.set)
        Page2.text_box1.insert(1.0, Page2.textbox_text1)
        Page2.text_box1.tag_add("center", 1.0, "end")
        Page2.text_box1.configure(state='disabled')
        Page2.text_box1.grid(column=2, row=4, padx=80, pady = 25)
        scrollbar.config(command=Page2.text_box1.xview)

        
    def open_file(self):
        
        file = askopenfile(parent=self, mode='r', title="Choose a file")
        if not file:
            self.textbox_text = ""
            text_box = Text(self, height=1, width=70, padx=6, pady=6)
            text_box.insert(1.0, self.textbox_text)
            text_box.tag_add("center", 1.0, "end")
            text_box.grid(column=2, row=7)
            return
        # text box
        self.textbox_text = file.name
        scrollbar = Scrollbar(self, orient=HORIZONTAL)
        text_box = Text(self, height=1, width=70, padx=6, pady=6, xscrollcommand=scrollbar.set)
        text_box.insert(1.0, self.textbox_text)
        # text_box.tag_configure("center", justify="center")
        text_box.tag_add("center", 1.0, "end")
        text_box.grid(column=2, row=7)
        scrollbar.config(command=text_box.xview)
        
        self.browse_text.set("File Uploaded")
        Page2.label_text.set("OUTPUT")
        
        path = None
        global select
        show = True
        if select[0] == "d":
            show=False
            
        if select == "c_lzw":
            path = LZW_COMPRESS(file)
        elif select == "c_binrle":
            path = BINRLE_COMPRESS(file)
        elif select == "c_lz77":
            path = LZ77_COMPRESS(file)
        elif select == "c_lz78":
            path = LZ78_COMPRESS(file)
        elif select == "c_ac":
            path = AC_COMPRESS(file)
        elif select == "c_rle":
            path = RLE_COMPRESS(file)
        elif select == "c_hfm":
            path = HFM_COMPRESS(file)
        elif select == "c_golomb":
            path = GOLOMB_COMPRESS(file)
        elif select == "c_tunstall":
            path = TUNSTALL_COMPRESS(file)
        elif select == "d_lzw":
            path = LZW_DECOMPRESS(file)
        elif select == "d_binrle":
            path = BINRLE_DECOMPRESS(file)
        elif select == "d_lz77":
            path = LZ77_DECOMPRESS(file)
        elif select == "d_lz78":
            path = LZ78_DECOMPRESS(file)
        elif select == "d_ac":
            path = AC_DECOMPRESS(file)
        elif select == "d_rle":
            path = RLE_DECOMPRESS(file)
        elif select == "d_hfm":
            path = HFM_DECOMPRESS(file)
        elif select == "d_golomb":
            path = GOLOMB_DECOMPRESS(file)
        elif select == "d_tunstall":
            path = TUNSTALL_DECOMPRESS(file) 
        else:
            self.ctrl.show_frame(StartPage, slt=None)
                
        if path!=None:
            if show: 
                c_size = os.stat(path).st_size
            
                o_size = os.stat(file.name).st_size

                compression_ratio = o_size/c_size
                efficiency = (1 - (c_size/o_size)) * 100
                
                ef_path = "./" + str(select) + "_efficiency.txt"
                with open(ef_path, "w") as fw:
                    fw.write("Compression Ratio : " + str(compression_ratio))
                    fw.write("\n")
                    fw.write("Efficiency : " + str(efficiency)) 
            
            cmd = "notepad.exe "+path
            Popen(cmd)
            path = None
            
            if show:
                cmd = "notepad.exe "+ef_path
                Popen(cmd)
            # label = Label(self, text = "Output Generated!", font = ("Montserrat-Medium", 45, "bold"), fg=color)
            # label.grid(row = 4, column = 2, padx = 90, pady = 10)
            # sleep(10) 
            # label.after(1, label.master.destroy)
            self.browse_text.set("Upload File")
        
        self.textbox_text = ""
        file.close()    
        Page2.label_text.set("UPLOAD FILE")
        self.ctrl.show_frame(StartPage, slt=None)

app = tkinterApp()

app.mainloop()
