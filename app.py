from tkinter import *
from tkinter.filedialog import askopenfile
from PIL import Image, ImageTk
from os import system
from subprocess import Popen
from time import sleep
import rle

color = "#20bebe"
LARGEFONT = ("Montserrat-Medium", 25, "bold")
BUTTONFONT = ("Montserrat-Medium", 12)
logoPath = "./graphics/logo-small.png"
faviconPath = "./graphics/favicon.ico"
btnbg = "#ffffff" #d0d0d0
default = "./Output/"

select = None

def MOVE_TO_FRONT_COMPRESS(file):
    name = file.name.split("/")[-1]
    string = file.read()
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
    
    with open(default+"compressed_move_to_front_"+name, "w") as fw:
        fw.write(str(encode))

    return default+"compressed_move_to_front_"+name

def LZW_COMPRESS(file):
    total_alph = int(file.readline())
    init_dict = dict()
    for i in range(total_alph):
        data = file.readline().split()
        init_dict[data[0]] = int(data[1])
    
    sequence = file.readline()
    print(sequence,init_dict)
    name = file.name.split("/")[-1]
    encode_table = []
    encode_list = []
    for i in init_dict.items():
        encode_table.append([i[0], i[1]])
    init_char = ''
    init_char = init_char + sequence[0]
    index_encode_table = len(encode_table)
    next_char = ''
    for i in range(len(sequence)):
        flag = 0
        if i != len(sequence) - 1:
            next_char = next_char + sequence[i + 1]
        for j  in range(len(encode_table)):
            if str(init_char + next_char) == str(encode_table[j][0]):
                flag = 1
        if flag == 1:
            init_char = str(init_char + next_char)
        else:
            for k in range(len(encode_table)):
                if init_char == encode_table[k][0]:
                    encode_list.append(encode_table[k][1])
            index_encode_table = index_encode_table + 1
            encode_table.append([str(init_char + next_char), index_encode_table])
            init_char = next_char
        next_char = ''
    for i in range(len(encode_table)):
        if sequence[-1] == encode_table[i][0]:
            encode_list.append(encode_table[i][1])
    for i in range(len(encode_table)):
        for j in range(2):
            print("  ", encode_table[i][j], end = "\t\t")
    encoded_sequence = ''
    for i in range(len(encode_list)):
        encoded_sequence = encoded_sequence + str(encode_list[i]) + ' '
    
    with open(default+"compressed_lzw"+name, "w") as fw:
        fw.write(str([init_dict, encode_list]))
    return default+"compressed_lzw"+name

def LZW_DECOMPRESS(file):
    name = file.name.split("/")[-1]
    
    master_directory = eval(file.read())
    
    init_dict = master_directory[0]
    encode_list = master_directory[1]
    decode_table = []
    for i in init_dict.items():
        decode_table.append([i[0], i[1]])
    decode_sequence = ''
    old = encode_list[0]
    seq = ''
    for i in range(len(decode_table)):
        if int(old) == int(decode_table[i][1]):
            seq = str(decode_table[i][0])
    cal = ''
    cal = cal + str(seq[0])
    decode_sequence = decode_sequence + seq
    index_decode_table = len(decode_table)
    for i in range(len(encode_list) - 1):
        new = encode_list[i + 1]
        flag = 1
        for j in range(len(decode_table)):
            if int(new) != int(decode_table[j][1]):
                flag = 0
        if flag == 1:
            for k in range(len(decode_table)):
                if int(old) == int(decode_table[k][1]):
                    seq = str(decode_table[k][0])
            seq = seq + cal
        else:
            for l in range(len(decode_table)):
                if int(new) == int(decode_table[l][1]):
                    seq = str(decode_table[l][0])
        decode_sequence = decode_sequence + seq
        cal = ''
        cal = cal + seq[0]
        for m in range(len(decode_table)):
            if int(old) == int(decode_table[m][1]):
                old_seq = decode_table[m][0]
        index_decode_table = index_decode_table + 1
        decode_table.append([str(old_seq + cal), index_decode_table])
        old = new
    print("Deocoded Sequence is: ", decode_sequence)
    
    with open(default+"decompressed_lzw_"+name, "w") as fw:
        fw.write(str(decode_sequence))

    return default+"decompressed_lzw_"+name

def LZ78_COMPRESS(file):
    name = file.name.split("/")[-1]
    total_alph = int(file.readline())
    dictionary = dict()
    for i in range(total_alph):
        data = file.readline().split()
        dictionary[data[0]] = data[1]
    sequence = file.readline()
    
    len_seq = len(sequence)
    index_dir = ['']
    encode_list = list()
    word = ''
    alphabet = list(dictionary.keys())
    codewords = list(dictionary.values())
    for i in sequence:
        word = word + i
        if not word in index_dir:
            index_dir.append(word)
            encode_list.append([index_dir.index(word[:-1]), word[-1]])
            word = ''
        elif i == len_seq:
            encode_list.append([index_dir.index(word), ''])
            word = ''
    for i in range(len(encode_list)):
        for j in range(len(alphabet)):
            if encode_list[i][1] == alphabet[j]:
                encode_list[i][1] = codewords[j]
    print("Index\tCodeword")
    print("------------------------------")
    for i in range(len(encode_list)):
        for j in range(2):
            print("  ", encode_list[i][j], end = "\t")
        print()
    
    with open(default+"compressed_lz78_"+name, "w") as fw:
        fw.write(str([encode_list, dictionary, index_dir]))

    return default+"compressed_lz78_"+name

def LZ78_DECOMPRESS(file):
    name = file.name.split("/")[-1]
    
    master_directory = eval(file.read()) 
    
    encode_list = master_directory[0]
    dictionary = master_directory[1]
    index_dir = master_directory[2]
    alphabet = list(dictionary.keys())
    codewords = list(dictionary.values())
    for i in range(len(encode_list)):
        for j in range(len(codewords)):
            if encode_list[i][1] == codewords[j]:
                encode_list[i][1] = alphabet[j]
    decoded_sequence = ''
    for i in range(len(encode_list)):
        if encode_list[i][0] == '0':
            decoded_sequence = decoded_sequence + encode_list[i][1]
        else:
            decoded_sequence = decoded_sequence + str(index_dir[encode_list[i][0]])
            decoded_sequence = decoded_sequence + encode_list[i][1]
    print("The decoded sequence is: " + decoded_sequence)

    with open(default+"decompressed_lz78_"+name, "w") as fw:
        fw.write(str(decoded_sequence))
    
    return default+"decompressed_lz78_"+name

def BURROWS_WHEELER_COMPRESS(file):
    name = file.name.split("/")[-1]
    
    string = file.read()
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
        
    with open(default+"compressed_bw_"+name, "w") as fw:
        fw.write(str(sort))
    
    return default+"compressed_bw_"+name

def LZ77_COMPRESS(file):
    name = file.name.split("/")[-1]
    
    total_alph = int(file.readline())
    dictionary = dict()
    len_code = None
    for i in range(total_alph):
        data = file.readline().split()
        dictionary[data[0]] = data[1]
        len_code = len(data[1])
    sequence = file.readline()
    
    search_buf_length = int(file.readline())
    look_ahead_buf_length = int(file.readline())
    
    str_length = len(sequence)
    search_buf_pos, look_ahead_buf_pos = 0, search_buf_length
    encode_list = []
    buffer = sequence[search_buf_pos:search_buf_pos+search_buf_length]
    for i in buffer:
        encode_list.append([0,0,dictionary[i]])
    buffer = buffer + sequence[look_ahead_buf_pos:look_ahead_buf_pos+look_ahead_buf_length]
    while 1:
        sym_offset = search_buf_length
        max_length, max_offset, next_sym = 0, 0, buffer[sym_offset]
        buffer_length = len(buffer)
        if buffer_length - sym_offset == 1:
            encode_list.append([0,0,dictionary[next_sym]])
            step = max_length + 1
            search_buf_pos =  search_buf_pos + step
            look_ahead_buf_pos = look_ahead_buf_pos + step
            buffer = sequence[search_buf_pos:search_buf_pos+search_buf_length+look_ahead_buf_length]
        else:    
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
            encode_list.append([max_offset, max_length, dictionary[next_sym]])
            step = max_length + 1
            search_buf_pos =  search_buf_pos + step
            look_ahead_buf_pos = look_ahead_buf_pos + step
            buffer = sequence[search_buf_pos:search_buf_pos+search_buf_length+look_ahead_buf_length]
            if look_ahead_buf_pos >= str_length: break
    print("Offset\tLength\tCodeword")
    print("-----------------------------------")
    for i in range(len(encode_list)):
        for j in range(3):
            print("   " + str(encode_list[i][j]), end = "\t")
        print()
    
    with open(default+"compressed_bw_"+name, "w") as fw:
        fw.write(str([encode_list, dictionary, len_code]))
    
    return default+"compressed_bw_"+name

def bin_fix(num, k):
    bin_cd = bin(num)
    return bin_cd[2:].zfill(k)

def BINRLE_COMPRESS(file):
    # first line must be k and then string 
    name = file.name.split("/")[-1]
    k = int(file.readline())
    string = file.read()
    
    print(k, string)
    
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
                for i in range(count_list[i][1] - 1):
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
    if(int_val[-1] > 0):
        print("The decoded sequence is: " + decode[:length - 1])
    else:
        print("The decoded sequence is: " + decode)

    with open(default+"decompressed_binrle_"+name, "w") as fw:
        fw.write(str(decode))
    
    return default+"decompressed_binrle_"+name

def RLE_COMPRESS(file):
    name = file.name.split("/")[-1]
    
    data = file.read().split(" ")
    with open(default+"compressed_rle_"+name, "w") as fw:
        fw.write(str(rle.encode(data)))
    
    return default+"compressed_binrle_"+name

def RLE_DECOMPRESS(file):
    name = file.name.split("/")[-1]
    
    data = file.read()
    with open(default+"decompressed_rle_"+name, "w") as fw:
        fw.write(str(rle.decode(data)))
    
    return default+"decompressed_binrle_"+name

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

        mtf_button = Button(self, text ="MOVE TO FRONT", command = lambda : self.open_nxt("mtf"), bg=color, fg="white", height=2, width=20, font=BUTTONFONT)
        mtf_button.grid(row = 4, column = 0, padx = (50, 0), pady = 10)
        
        lzw_button = Button(self, text ="LZW", command = lambda : self.open_nxt("lzw"), bg=color, fg="white", height=2, width=20, font=BUTTONFONT)
        lzw_button.grid(row = 4, column = 2, padx = (0, 50), pady = 10)
        
        binrle_button = Button(self, text ="BINARY RLE", command = lambda : self.open_nxt("binrle"), bg=color ,fg="white", height=2, width=20, font=BUTTONFONT)
        binrle_button.grid(row = 5, column = 0, padx = (50, 0), pady = 10)
        
        lz77_button = Button(self, text ="LZ77", command = lambda : self.open_nxt("lz77"), bg=color, fg="white", height=2, width=20, font=BUTTONFONT)
        lz77_button.grid(row = 5, column = 2, padx = (0, 50), pady = 10)
        
        burrows_button = Button(self, text ="BURROWS WHEELER", command = lambda : self.open_nxt("bw"), bg=color, fg="white", height=2, width=20, font=BUTTONFONT)
        burrows_button.grid(row = 6, column = 0, padx = (50, 0), pady = 10)
        
        lz78_button = Button(self, text ="LZ78", command = lambda : self.open_nxt("lz78"), bg=color, fg="white", height=2, width=20, font=BUTTONFONT)
        lz78_button.grid(row = 6, column = 2, padx = (0, 50), pady = 10)
        
        arith_button = Button(self, text ="ARITHMATIC CODING", command = lambda : self.open_nxt("ac"), bg=color, fg="white", height=2, width=20, font=BUTTONFONT)
        arith_button.grid(row = 7, column = 0, padx = (50, 0), pady = 10)

        rle_button = Button(self, text ="RLE", command = lambda : self.open_nxt("rle"), bg=color, fg="white", height=2, width=20, font=BUTTONFONT)
        rle_button.grid(row = 7, column = 2, padx = (0, 50), pady = 10)
        # hoffmann 

    def open_nxt(self, algo):
        self.slt_algo = algo
        global select
        select = select.split("_")[0]
        select += "_"+algo
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
        upload_file_button.grid(row = 2, column = 1, padx = 6, pady = 6)

        button2 = Button(self, text ="Home Page", command = lambda : controller.show_frame(StartPage, slt=None), bg=btnbg, fg=color, height=1, width=10,font=BUTTONFONT)
        button2.grid(row = 8, column = 1, padx = 6, pady = 6)

    def open_file(self):
        file = askopenfile(parent=self, mode='r', title="Choose a file")
        if not file:
            self.textbox_text = ""
            text_box = Text(self, height=1, width=70, padx=6, pady=6)
            text_box.insert(1.0, self.textbox_text)
            text_box.tag_add("center", 1.0, "end")
            text_box.grid(column=2, row=2)
            return
        # text box
        self.textbox_text = file.name
        scrollbar = Scrollbar(self, orient=HORIZONTAL)
        text_box = Text(self, height=1, width=70, padx=6, pady=6, xscrollcommand=scrollbar.set)
        text_box.insert(1.0, self.textbox_text)
        # text_box.tag_configure("center", justify="center")
        text_box.tag_add("center", 1.0, "end")
        text_box.grid(column=2, row=2)
        scrollbar.config(command=text_box.xview)
        
        self.browse_text.set("File Uploaded")
        Page2.label_text.set("OUTPUT")
        
        path = None
        global select
        if select == "c_mtf":
            path = MOVE_TO_FRONT_COMPRESS(file)
        elif select == "c_lzw":
            path = LZW_COMPRESS(file)
        elif select == "c_binrle":
            path = BINRLE_COMPRESS(file)
        elif select == "c_lz77":
            pass
        elif select == "c_lz78":
            path = LZ78_COMPRESS(file)
        elif select == "c_ac":
            pass
        elif select == "c_bw":
            path = BURROWS_WHEELER_COMPRESS(file)
        elif select == "c_rle":
            path = RLE_COMPRESS(file)
        elif select == "d_mtf":
            pass
        elif select == "d_lzw":
            path = LZW_DECOMPRESS(file)
        elif select == "d_binrle":
            path = BINRLE_DECOMPRESS(file)
        elif select == "d_lz77":
            pass
        elif select == "d_lz78":
            path = LZ78_DECOMPRESS(file)
        elif select == "d_ac":
            pass
        elif select == "d_bw":
            pass
        elif select == "d_rle":
            path = RLE_DECOMPRESS(file)
        else:
            self.ctrl.show_frame(StartPage, slt=None)
        
        if path!=None:
            cmd = "notepad.exe "+path
            Popen(cmd)
            path = None
            
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